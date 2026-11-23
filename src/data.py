"""Import and validate manually exported tournament deck records."""

from __future__ import annotations

import csv
from datetime import date
import json
from pathlib import Path
from typing import Any

import pandas as pd

REQUIRED_FIELDS = ("tournament_id", "tournament_date", "tournament_type", "deck_id")
OPTIONAL_FIELDS = (
    "player",
    "placement",
    "archetype",
    "decklist",
    "source_url",
    "participants_total",
)
FIELDS = REQUIRED_FIELDS + OPTIONAL_FIELDS
CARD_REQUIRED_FIELDS = ("tournament_id", "deck_id", "zone", "card_name", "quantity")
CARD_OPTIONAL_FIELDS = (
    "tournament_date",
    "tournament_type",
    "player",
    "placement",
    "archetype",
    "source_url",
)
CARD_FIELDS = CARD_REQUIRED_FIELDS + CARD_OPTIONAL_FIELDS


class DataValidationError(ValueError):
    """Raised when an import file is malformed or missing required values."""


def _clean(value: Any) -> str:
    return "" if value is None else str(value).strip()


def validate_records(records: list[dict[str, Any]]) -> pd.DataFrame:
    if not isinstance(records, list):
        raise DataValidationError("El JSON debe contener una lista de registros.")
    if not records:
        raise DataValidationError("El archivo no contiene listas para importar.")

    normalized: list[dict[str, str]] = []
    for index, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            raise DataValidationError(f"El registro {index} debe ser un objeto.")
        row = {field: _clean(record.get(field)) for field in FIELDS}
        missing = [field for field in REQUIRED_FIELDS if not row[field]]
        if missing:
            raise DataValidationError(
                f"El registro {index} no tiene valores para: {', '.join(missing)}."
            )
        try:
            date.fromisoformat(row["tournament_date"])
            if len(row["tournament_date"]) != 10:
                raise ValueError
        except (ValueError, TypeError):
            raise DataValidationError(
                f"La fecha del registro {index} no es válida; usa YYYY-MM-DD."
            ) from None
        if row["participants_total"]:
            try:
                participants_total = int(row["participants_total"])
                if participants_total <= 0:
                    raise ValueError
            except ValueError:
                raise DataValidationError(
                    f"El total de participantes del registro {index} debe ser un entero mayor que cero."
                ) from None
            row["participants_total"] = str(participants_total)
        normalized.append(row)

    frame = pd.DataFrame(normalized, columns=FIELDS)
    for tournament_id, event in frame.groupby("tournament_id", sort=False):
        totals = set(event["participants_total"]) - {""}
        has_missing_total = (event["participants_total"] == "").any()
        if len(totals) > 1 or (len(totals) == 1 and has_missing_total):
            raise DataValidationError(
                "participants_total debe tener el mismo valor en todas las filas del torneo "
                f"{tournament_id}, o estar vacío en todas."
            )
    duplicates = frame.duplicated(["tournament_id", "deck_id"], keep=False)
    if duplicates.any():
        raise DataValidationError("Hay deck_id repetidos dentro del mismo torneo.")
    return frame


def load_tournament_file(file: Any, filename: str | None = None) -> pd.DataFrame:
    """Read uploaded CSV or JSON (a list of record objects) and validate it."""
    name = filename or getattr(file, "name", "")
    suffix = Path(name).suffix.lower()
    try:
        raw = file.getvalue() if hasattr(file, "getvalue") else file.read()
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8-sig")
        if suffix == ".csv":
            records = list(csv.DictReader(raw.splitlines()))
        elif suffix == ".json":
            records = json.loads(raw)
        else:
            raise DataValidationError("Formato no compatible: selecciona un archivo .csv o .json.")
    except DataValidationError:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError, csv.Error) as exc:
        raise DataValidationError(f"No se pudo leer el archivo: {exc}") from exc
    return validate_records(records)


def load_tournament_directory(directory: str | Path) -> tuple[list[pd.DataFrame], list[str]]:
    """Load valid tournament CSV/JSON files from a directory, reporting bad files individually."""
    directory = Path(directory)
    if not directory.exists():
        return [], []

    frames: list[pd.DataFrame] = []
    errors: list[str] = []
    for path in sorted(directory.iterdir(), key=lambda item: item.name.lower()):
        if not path.is_file() or path.suffix.lower() not in {".csv", ".json"}:
            continue
        try:
            with path.open("rb") as file:
                incoming = load_tournament_file(file, path.name)
            if frames:
                # Validate across files as well, so duplicate decks cannot be counted twice.
                combined = pd.concat([*frames, incoming], ignore_index=True)
                validate_records(combined.to_dict("records"))
            frames.append(incoming)
        except (DataValidationError, OSError) as exc:
            errors.append(f"{path.name}: {exc}")
    return frames, errors


def load_card_file(file: Any, filename: str | None = None) -> pd.DataFrame:
    """Read and validate a card-per-row CSV, keeping mainboard and sideboard separate."""
    name = filename or getattr(file, "name", "")
    if Path(name).suffix.lower() != ".csv":
        raise DataValidationError("El archivo de cartas debe tener formato CSV.")
    try:
        raw = file.getvalue() if hasattr(file, "getvalue") else file.read()
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8-sig")
        reader = csv.DictReader(raw.splitlines())
        if reader.fieldnames is None or not set(CARD_REQUIRED_FIELDS).issubset(reader.fieldnames):
            raise DataValidationError(
                "Faltan columnas obligatorias para cartas: "
                + ", ".join(CARD_REQUIRED_FIELDS)
                + "."
            )
        records = list(reader)
    except DataValidationError:
        raise
    except (UnicodeDecodeError, csv.Error) as exc:
        raise DataValidationError(f"No se pudo leer el archivo de cartas: {exc}") from exc
    if not records:
        raise DataValidationError("El archivo de cartas no contiene registros.")

    normalized: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str, str]] = set()
    per_deck_metadata: dict[tuple[str, str], tuple[str, ...]] = {}
    for index, record in enumerate(records, start=2):
        row = {field: _clean(record.get(field)) for field in CARD_FIELDS}
        missing = [field for field in CARD_REQUIRED_FIELDS if not row[field]]
        if missing:
            raise DataValidationError(
                f"La fila {index} no tiene valores para: {', '.join(missing)}."
            )
        row["zone"] = row["zone"].lower()
        if row["zone"] not in {"mainboard", "sideboard"}:
            raise DataValidationError(
                f"La zona de la fila {index} debe ser mainboard o sideboard."
            )
        try:
            quantity = int(row["quantity"])
            if quantity <= 0:
                raise ValueError
        except ValueError:
            raise DataValidationError(
                f"La cantidad de la fila {index} debe ser un entero mayor que cero."
            ) from None
        row["quantity"] = quantity

        key = (row["tournament_id"], row["deck_id"], row["zone"], row["card_name"])
        if key in seen:
            raise DataValidationError(
                f"La carta {row['card_name']} está repetida en la fila {index} "
                "para la misma lista y zona."
            )
        seen.add(key)

        deck_key = (row["tournament_id"], row["deck_id"])
        metadata = tuple(row[field] for field in ("player", "placement", "archetype"))
        if deck_key in per_deck_metadata and per_deck_metadata[deck_key] != metadata:
            raise DataValidationError(
                f"Los metadatos de la lista {row['deck_id']} no son consistentes "
                f"en la fila {index}."
            )
        per_deck_metadata[deck_key] = metadata
        normalized.append(row)
    return pd.DataFrame(normalized, columns=CARD_FIELDS)


def load_label_overrides(path: str | Path) -> dict[str, str]:
    """Load manual labels keyed by (tournament_id, deck_id)."""
    path = Path(path)
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict) or not all(
            isinstance(key, str) and isinstance(value, str)
            for key, value in payload.items()
        ):
            raise ValueError("El archivo debe ser un objeto JSON de etiquetas.")
        return payload
    except (json.JSONDecodeError, OSError) as exc:
        raise DataValidationError(f"No se pudieron leer las etiquetas guardadas: {exc}") from exc


def save_label_overrides(path: str | Path, labels: dict[str, str]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(labels, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def deck_key(row: pd.Series | dict[str, Any]) -> str:
    return f"{_clean(row['tournament_id'])}::{_clean(row['deck_id'])}"


def add_display_archetype(
    frame: pd.DataFrame, overrides: dict[str, str]
) -> pd.DataFrame:
    result = frame.copy()
    result["archetype_display"] = result.apply(
        lambda row: overrides.get(deck_key(row), "") or row["archetype"], axis=1
    )
    result["archetype_display"] = result["archetype_display"].replace("", "Sin etiquetar")
    return result
