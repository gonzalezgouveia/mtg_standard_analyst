"""SQLite persistence and idempotent import for local tournament files."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sqlite3
from typing import Any

import pandas as pd

from src.data import (
    CARD_FIELDS,
    FIELDS,
    DataValidationError,
    load_card_file,
    load_tournament_file,
)

DEFAULT_DATABASE_NAME = "mtg_standard_analyst.sqlite3"
CARD_DIRECTORIES = ("examples", "cards")

SCHEMA = """
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS tournaments (
    tournament_id TEXT PRIMARY KEY,
    tournament_date TEXT NOT NULL,
    tournament_type TEXT NOT NULL,
    tournament_category TEXT NOT NULL DEFAULT '',
    participants_total INTEGER CHECK (participants_total IS NULL OR participants_total > 0),
    source_url TEXT NOT NULL DEFAULT '',
    snapshot_hash TEXT NOT NULL,
    imported_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS decks (
    tournament_id TEXT NOT NULL,
    deck_id TEXT NOT NULL,
    player TEXT NOT NULL DEFAULT '',
    placement TEXT NOT NULL DEFAULT '',
    archetype TEXT NOT NULL DEFAULT '',
    decklist TEXT NOT NULL DEFAULT '',
    source_url TEXT NOT NULL DEFAULT '',
    PRIMARY KEY (tournament_id, deck_id),
    FOREIGN KEY (tournament_id) REFERENCES tournaments(tournament_id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS deck_cards (
    tournament_id TEXT NOT NULL,
    deck_id TEXT NOT NULL,
    zone TEXT NOT NULL CHECK (zone IN ('mainboard', 'sideboard')),
    card_name TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    source_url TEXT NOT NULL DEFAULT '',
    PRIMARY KEY (tournament_id, deck_id, zone, card_name),
    FOREIGN KEY (tournament_id, deck_id)
        REFERENCES decks(tournament_id, deck_id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS tournament_sources (
    tournament_id TEXT NOT NULL,
    source_path TEXT NOT NULL,
    snapshot_hash TEXT NOT NULL,
    PRIMARY KEY (tournament_id, source_path),
    FOREIGN KEY (tournament_id) REFERENCES tournaments(tournament_id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS card_sources (
    tournament_id TEXT PRIMARY KEY,
    source_path TEXT NOT NULL,
    snapshot_hash TEXT NOT NULL,
    imported_at TEXT NOT NULL,
    FOREIGN KEY (tournament_id) REFERENCES tournaments(tournament_id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_decks_player ON decks(player);
CREATE INDEX IF NOT EXISTS idx_decks_archetype ON decks(archetype);
CREATE INDEX IF NOT EXISTS idx_deck_cards_name ON deck_cards(card_name);
"""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _normalize_tournament_category(tournament_type: str) -> str:
    base = re.sub(r"\s+\d+\s*$", "", tournament_type).strip().casefold()
    if base == "standard showcase challenge":
        return "Standard Showcase Challenge"
    if base == "standard challenge":
        return "Standard Challenge"
    return ""


def connect_database(path: str | Path) -> sqlite3.Connection:
    """Open the local database and enable foreign-key enforcement."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path, timeout=10)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA busy_timeout = 10000")
    return connection


def initialize_database(path: str | Path) -> None:
    connection = connect_database(path)
    try:
        connection.executescript(SCHEMA)
        columns = {row["name"] for row in connection.execute("PRAGMA table_info(tournaments)")}
        if "tournament_category" not in columns:
            connection.execute(
                "ALTER TABLE tournaments ADD COLUMN tournament_category TEXT NOT NULL DEFAULT ''"
            )
        for row in connection.execute(
            "SELECT tournament_id, tournament_type FROM tournaments WHERE tournament_category = ''"
        ).fetchall():
            connection.execute(
                "UPDATE tournaments SET tournament_category = ? WHERE tournament_id = ?",
                (_normalize_tournament_category(row["tournament_type"]), row["tournament_id"]),
            )
        connection.commit()
    finally:
        connection.close()


def _records(frame: pd.DataFrame, fields: tuple[str, ...]) -> list[dict[str, str]]:
    return [
        {field: "" if pd.isna(value) else str(value).strip() for field, value in row.items()}
        for row in frame.loc[:, list(fields)].to_dict("records")
    ]


def _digest(records: list[dict[str, Any]], sort_keys: tuple[str, ...]) -> str:
    ordered = sorted(
        records,
        key=lambda row: tuple(str(row.get(field, "")) for field in sort_keys),
    )
    payload = json.dumps(ordered, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _event_hash(frame: pd.DataFrame) -> str:
    return _digest(_records(frame, FIELDS), ("deck_id",))


def _card_hash(frame: pd.DataFrame) -> str:
    return _digest(_records(frame, CARD_FIELDS), ("deck_id", "zone", "card_name"))


def _validate_event_consistency(frame: pd.DataFrame, tournament_id: str) -> None:
    for field in ("tournament_date", "tournament_type", "participants_total"):
        values = set(frame[field].fillna("").astype(str))
        if len(values) > 1:
            raise DataValidationError(
                f"El campo {field} no es consistente en el torneo {tournament_id}."
            )


def _ingest_event(
    connection: sqlite3.Connection,
    tournament_id: str,
    frame: pd.DataFrame,
    source_paths: list[str],
) -> str:
    _validate_event_consistency(frame, tournament_id)
    records = _records(frame, FIELDS)
    snapshot_hash = _event_hash(frame)
    tournament_date = records[0]["tournament_date"]
    tournament_type = records[0]["tournament_type"]
    raw_total = records[0]["participants_total"]
    participants_total = int(raw_total) if raw_total else None
    source_url = next((row["source_url"] for row in records if row["source_url"]), "")
    current = connection.execute(
        "SELECT snapshot_hash FROM tournaments WHERE tournament_id = ?", (tournament_id,)
    ).fetchone()

    with connection:
        if current is None or current["snapshot_hash"] != snapshot_hash:
            connection.execute(
                """INSERT INTO tournaments
                   (tournament_id, tournament_date, tournament_type, tournament_category,
                    participants_total, source_url, snapshot_hash, imported_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(tournament_id) DO UPDATE SET
                     tournament_date=excluded.tournament_date,
                     tournament_type=excluded.tournament_type,
                     tournament_category=excluded.tournament_category,
                     participants_total=excluded.participants_total,
                     source_url=excluded.source_url,
                     snapshot_hash=excluded.snapshot_hash,
                     imported_at=excluded.imported_at""",
                (tournament_id, tournament_date, tournament_type,
                 _normalize_tournament_category(tournament_type), participants_total,
                 source_url, snapshot_hash, _now()),
            )
            valid_ids = [row["deck_id"] for row in records]
            placeholders = ",".join("?" for _ in valid_ids)
            connection.execute(
                f"DELETE FROM decks WHERE tournament_id = ? AND deck_id NOT IN ({placeholders})",
                [tournament_id, *valid_ids],
            )
            for row in records:
                connection.execute(
                    """INSERT INTO decks
                       (tournament_id, deck_id, player, placement, archetype, decklist, source_url)
                       VALUES (?, ?, ?, ?, ?, ?, ?)
                       ON CONFLICT(tournament_id, deck_id) DO UPDATE SET
                         player=excluded.player, placement=excluded.placement,
                         archetype=excluded.archetype, decklist=excluded.decklist,
                         source_url=excluded.source_url""",
                    (tournament_id, row["deck_id"], row["player"], row["placement"],
                     row["archetype"], row["decklist"], row["source_url"]),
                )
        for source_path in source_paths:
            connection.execute(
                """INSERT INTO tournament_sources(tournament_id, source_path, snapshot_hash)
                   VALUES (?, ?, ?) ON CONFLICT(tournament_id, source_path)
                   DO UPDATE SET snapshot_hash=excluded.snapshot_hash""",
                (tournament_id, source_path, snapshot_hash),
            )
    return "sin cambios" if current is not None and current["snapshot_hash"] == snapshot_hash else "actualizado"


def _validate_card_relationships(
    connection: sqlite3.Connection, tournament_id: str, frame: pd.DataFrame
) -> None:
    decks = {
        row["deck_id"]: row
        for row in connection.execute(
            "SELECT deck_id, player, placement, archetype FROM decks WHERE tournament_id = ?",
            (tournament_id,),
        )
    }
    if not decks:
        raise DataValidationError(
            f"No se encuentran listas del torneo {tournament_id}; importa primero sus metadatos."
        )
    for deck_id, group in frame.groupby("deck_id", sort=False):
        if deck_id not in decks:
            raise DataValidationError(
                f"La lista {deck_id} del torneo {tournament_id} no existe en los metadatos."
            )
        stored = decks[deck_id]
        first = group.iloc[0]
        for field in ("player", "placement", "archetype"):
            value = str(first[field]).strip()
            if value and value != stored[field]:
                raise DataValidationError(
                    f"El campo {field} de la lista {deck_id} no coincide con los metadatos."
                )


def _ingest_card_snapshot(
    connection: sqlite3.Connection,
    tournament_id: str,
    frame: pd.DataFrame,
    source_path: str,
) -> str:
    snapshot_hash = _card_hash(frame)
    _validate_card_relationships(connection, tournament_id, frame)
    current = connection.execute(
        "SELECT snapshot_hash FROM card_sources WHERE tournament_id = ?", (tournament_id,)
    ).fetchone()
    if current is not None and current["snapshot_hash"] == snapshot_hash:
        with connection:
            connection.execute(
                "UPDATE card_sources SET source_path=? WHERE tournament_id=?",
                (source_path, tournament_id),
            )
        return "sin cambios"

    rows = _records(frame, CARD_FIELDS)
    with connection:
        connection.execute("DELETE FROM deck_cards WHERE tournament_id = ?", (tournament_id,))
        for row in rows:
            connection.execute(
                """INSERT INTO deck_cards
                   (tournament_id, deck_id, zone, card_name, quantity, source_url)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (tournament_id, row["deck_id"], row["zone"], row["card_name"],
                 int(row["quantity"]), row["source_url"]),
            )
        connection.execute(
            """INSERT INTO card_sources(tournament_id, source_path, snapshot_hash, imported_at)
               VALUES (?, ?, ?, ?) ON CONFLICT(tournament_id) DO UPDATE SET
                 source_path=excluded.source_path, snapshot_hash=excluded.snapshot_hash,
                 imported_at=excluded.imported_at""",
            (tournament_id, source_path, snapshot_hash, _now()),
        )
    return "actualizado"


def _relative(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.name


def _sync_metadata_files(
    connection: sqlite3.Connection, data_dir: Path
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    snapshots: dict[str, list[tuple[Path, pd.DataFrame, str]]] = {}
    for path in sorted(data_dir.iterdir(), key=lambda item: item.name.lower()):
        if (
            not path.is_file()
            or path.name.lower() == "archetype_labels.json"
            or path.suffix.lower() not in {".csv", ".json"}
        ):
            continue
        try:
            with path.open("rb") as file:
                frame = load_tournament_file(file, path.name)
            for tournament_id, event in frame.groupby("tournament_id", sort=False):
                event = event.reset_index(drop=True)
                _validate_event_consistency(event, tournament_id)
                snapshots.setdefault(tournament_id, []).append(
                    (path, event, _event_hash(event))
                )
        except (DataValidationError, OSError) as exc:
            errors.append(f"{path.name}: {exc}")

    summaries: list[str] = []
    for tournament_id, versions in snapshots.items():
        hashes = {item[2] for item in versions}
        if len(hashes) > 1:
            names = ", ".join(item[0].name for item in versions)
            errors.append(
                f"Conflicto: los archivos {names} contienen versiones distintas "
                f"del torneo {tournament_id}; no se importó ninguna."
            )
            continue
        path, event, _ = versions[0]
        paths = [_relative(item[0], data_dir) for item in versions]
        try:
            outcome = _ingest_event(connection, tournament_id, event, paths)
            summaries.append(f"{tournament_id}: {outcome} ({len(event)} listas)")
        except (DataValidationError, sqlite3.Error) as exc:
            errors.append(f"{path.name}: no se pudo guardar {tournament_id}: {exc}")
    return summaries, errors


def _sync_card_files(
    connection: sqlite3.Connection, data_dir: Path
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    snapshots: dict[str, list[tuple[Path, pd.DataFrame, str]]] = {}
    paths: list[Path] = []
    for directory_name in CARD_DIRECTORIES:
        directory = data_dir / directory_name
        if directory.is_dir():
            paths.extend(
                path for path in directory.iterdir()
                if path.is_file() and path.name.lower().endswith("_cards.csv")
            )
    for path in sorted(paths, key=lambda item: item.as_posix().lower()):
        try:
            with path.open("rb") as file:
                frame = load_card_file(file, path.name)
            for tournament_id, event_cards in frame.groupby("tournament_id", sort=False):
                event_cards = event_cards.reset_index(drop=True)
                snapshots.setdefault(tournament_id, []).append(
                    (path, event_cards, _card_hash(event_cards))
                )
        except (DataValidationError, OSError) as exc:
            errors.append(f"{path.relative_to(data_dir).as_posix()}: {exc}")

    summaries: list[str] = []
    for tournament_id, versions in snapshots.items():
        hashes = {item[2] for item in versions}
        if len(hashes) > 1:
            names = ", ".join(item[0].name for item in versions)
            errors.append(
                f"Conflicto: los archivos de cartas {names} contienen versiones distintas "
                f"del torneo {tournament_id}; no se importó ninguna."
            )
            continue
        path, cards, _ = versions[0]
        source_path = _relative(path, data_dir)
        try:
            outcome = _ingest_card_snapshot(connection, tournament_id, cards, source_path)
            summaries.append(f"{tournament_id}: cartas {outcome} ({len(cards)} filas)")
        except (DataValidationError, sqlite3.Error) as exc:
            errors.append(f"{source_path}: no se pudieron guardar las cartas: {exc}")
    return summaries, errors


def sync_local_data(
    data_directory: str | Path, database_path: str | Path
) -> tuple[list[str], list[str]]:
    """Import root-level tournament files plus explicit card snapshots into SQLite."""
    data_dir = Path(data_directory)
    data_dir.mkdir(parents=True, exist_ok=True)
    initialize_database(database_path)
    connection = connect_database(database_path)
    try:
        summaries, errors = _sync_metadata_files(connection, data_dir)
        card_summaries, card_errors = _sync_card_files(connection, data_dir)
        return summaries + card_summaries, errors + card_errors
    finally:
        connection.close()


def query_decks(database_path: str | Path) -> pd.DataFrame:
    connection = connect_database(database_path)
    try:
        rows = connection.execute(
            """SELECT d.tournament_id, t.tournament_date, t.tournament_type,
                      t.tournament_category, t.participants_total, t.imported_at,
                      d.deck_id, d.player, d.placement, d.archetype, d.decklist, d.source_url
               FROM decks AS d JOIN tournaments AS t USING (tournament_id)
               ORDER BY t.tournament_date DESC, t.tournament_id, d.placement, d.deck_id"""
        ).fetchall()
        columns = [
            "tournament_id", "tournament_date", "tournament_type", "tournament_category",
            "participants_total", "imported_at",
            "deck_id", "player", "placement", "archetype", "decklist", "source_url",
        ]
        frame = pd.DataFrame([dict(row) for row in rows], columns=columns)
        for column in (
            "tournament_id", "tournament_date", "tournament_type", "tournament_category",
            "imported_at", "deck_id", "player", "placement", "archetype", "decklist", "source_url",
        ):
            frame[column] = frame[column].fillna("").astype(str)
        return frame
    finally:
        connection.close()


def query_card_counts(
    database_path: str | Path, tournament_ids: list[str] | None = None
) -> dict[str, int]:
    connection = connect_database(database_path)
    try:
        if tournament_ids is not None and not tournament_ids:
            return {"rows": 0, "decks": 0}
        where = ""
        params: tuple[str, ...] = ()
        if tournament_ids is not None:
            where = f" WHERE tournament_id IN ({','.join('?' for _ in tournament_ids)})"
            params = tuple(tournament_ids)
        return {
            "rows": connection.execute(
                f"SELECT COUNT(*) FROM deck_cards{where}", params
            ).fetchone()[0],
            "decks": connection.execute(
                "SELECT COUNT(DISTINCT tournament_id || '::' || deck_id) FROM deck_cards" + where,
                params,
            ).fetchone()[0],
        }
    finally:
        connection.close()
