import csv
from pathlib import Path

from src.database import connect_database, query_card_counts, query_decks, sync_local_data


def write_tournament(path: Path, rows: list[dict[str, str]]) -> None:
    fields = [
        "tournament_id", "tournament_date", "tournament_type", "deck_id", "player",
        "placement", "archetype", "decklist", "source_url", "participants_total",
    ]
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def record(deck_id: str, player: str, placement: str, archetype: str = "Control"):
    return {
        "tournament_id": "event-1",
        "tournament_date": "2026-11-20",
        "tournament_type": "Standard Challenge 32",
        "deck_id": deck_id,
        "player": player,
        "placement": placement,
        "archetype": archetype,
        "decklist": "",
        "source_url": "https://example.test/event-1",
        "participants_total": "2",
    }


def write_cards(path: Path, rows: list[dict[str, str]]) -> None:
    fields = [
        "tournament_id", "tournament_date", "tournament_type", "deck_id", "player",
        "placement", "archetype", "zone", "card_name", "quantity", "source_url",
    ]
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def card(deck_id: str, player: str, placement: str, name: str, quantity: int, zone="mainboard"):
    return {
        "tournament_id": "event-1",
        "tournament_date": "2026-11-20",
        "tournament_type": "Standard Challenge 32",
        "deck_id": deck_id,
        "player": player,
        "placement": placement,
        "archetype": "Control",
        "zone": zone,
        "card_name": name,
        "quantity": str(quantity),
        "source_url": f"https://example.test/deck/{deck_id}",
    }


def test_sync_stores_metadata_and_card_rows_idempotently(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / "examples").mkdir()
    write_tournament(data_dir / "event.csv", [record("d1", "alice", "1"), record("d2", "bob", "2")])
    write_cards(
        data_dir / "examples" / "event_cards.csv",
        [card("d1", "alice", "1", "Card A", 2), card("d1", "alice", "1", "Card B", 1, "sideboard")],
    )
    database = tmp_path / "local.sqlite3"

    summaries, errors = sync_local_data(data_dir, database)
    assert not errors
    assert len(query_decks(database)) == 2
    assert query_decks(database).loc[0, "participants_total"] == 2
    assert set(query_decks(database)["tournament_category"]) == {"Standard Challenge"}
    assert query_card_counts(database) == {"rows": 2, "decks": 1}
    assert any("cartas actualizado" in summary for summary in summaries)

    summaries, errors = sync_local_data(data_dir, database)
    assert not errors
    assert query_card_counts(database) == {"rows": 2, "decks": 1}
    assert any("sin cambios" in summary for summary in summaries)


def test_changed_snapshot_replaces_event_atomically_and_invalid_file_preserves_it(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    source = data_dir / "event.csv"
    write_tournament(source, [record("d1", "alice", "1"), record("d2", "bob", "2")])
    database = tmp_path / "local.sqlite3"
    sync_local_data(data_dir, database)

    write_tournament(source, [record("d1", "alice", "1", "Midrange")])
    _, errors = sync_local_data(data_dir, database)
    assert not errors
    result = query_decks(database)
    assert len(result) == 1
    assert result.loc[0, "archetype"] == "Midrange"

    source.write_text("tournament_id,deck_id\nevent-1,d3\n", encoding="utf-8")
    _, errors = sync_local_data(data_dir, database)
    assert errors
    result = query_decks(database)
    assert len(result) == 1
    assert result.loc[0, "deck_id"] == "d1"
    assert result.loc[0, "archetype"] == "Midrange"


def test_conflicting_complete_files_do_not_choose_a_version(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    write_tournament(data_dir / "a.csv", [record("d1", "alice", "1")])
    write_tournament(data_dir / "b.csv", [record("d1", "alice", "1", "Aggro")])
    database = tmp_path / "local.sqlite3"

    _, errors = sync_local_data(data_dir, database)

    assert any("Conflicto" in error for error in errors)
    assert query_decks(database).empty


def test_inconsistent_event_rejects_whole_file_and_loads_independent_file(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    source = data_dir / "multiple.csv"
    database = tmp_path / "local.sqlite3"
    first = record("d1", "alice", "1")
    second = {**record("d1", "bob", "1"), "tournament_id": "event-2"}
    independent = {**record("d1", "clara", "1"), "tournament_id": "event-3"}
    write_tournament(source, [first, second])
    assert not sync_local_data(data_dir, database)[1]
    stored = query_decks(database).set_index("tournament_id")

    inconsistent = {**second, "deck_id": "d2", "tournament_date": "2026-11-21"}
    write_tournament(source, [{**first, "archetype": "Aggro"}, second, inconsistent])
    write_tournament(data_dir / "independent.csv", [independent])
    summaries, errors = sync_local_data(data_dir, database)

    assert len(errors) == 1 and "multiple.csv" in errors[0] and "event-2" in errors[0]
    assert len(summaries) == 1 and summaries[0].startswith("event-3:")
    updated = query_decks(database).set_index("tournament_id")
    assert updated.loc[stored.index].equals(stored)
    assert updated.loc["event-3", "player"] == "clara"


def test_write_failure_rolls_back_all_events_in_file(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    source = data_dir / "multiple.csv"
    database = tmp_path / "local.sqlite3"
    first = record("d1", "alice", "1")
    second = {**record("d1", "bob", "1"), "tournament_id": "event-2"}
    removed = record("d2", "clara", "2")
    write_tournament(source, [first, removed, second])
    assert not sync_local_data(data_dir, database)[1]
    stored = query_decks(database)

    connection = connect_database(database)
    try:
        connection.execute(
            """CREATE TRIGGER reject_second_event BEFORE UPDATE ON decks
               WHEN NEW.tournament_id = 'event-2'
               BEGIN SELECT RAISE(ABORT, 'test write failure'); END"""
        )
    finally:
        connection.close()

    write_tournament(source, [{**first, "archetype": "Aggro"}, {**second, "archetype": "Tempo"}])
    summaries, errors = sync_local_data(data_dir, database)

    assert not summaries
    assert len(errors) == 1 and "multiple.csv" in errors[0] and "test write failure" in errors[0]
    assert query_decks(database).equals(stored)


def test_conflicted_files_leave_other_events_to_independent_sources(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    database = tmp_path / "local.sqlite3"
    contested = record("d1", "alice", "1")
    independent = {**record("d1", "bob", "1"), "tournament_id": "event-2"}
    write_tournament(data_dir / "a.csv", [contested, independent])
    write_tournament(data_dir / "b.csv", [{**contested, "archetype": "Aggro"}])

    _, errors = sync_local_data(data_dir, database)
    assert any("Conflicto" in error for error in errors)
    assert query_decks(database).empty

    write_tournament(data_dir / "independent.csv", [independent])
    _, errors = sync_local_data(data_dir, database)
    assert any("Conflicto" in error for error in errors)
    assert query_decks(database)["tournament_id"].tolist() == ["event-2"]


def test_invalid_card_snapshot_preserves_existing_cards(tmp_path):
    data_dir = tmp_path / "data"
    examples = data_dir / "examples"
    examples.mkdir(parents=True)
    write_tournament(data_dir / "event.csv", [record("d1", "alice", "1")])
    card_path = examples / "event_cards.csv"
    write_cards(card_path, [card("d1", "alice", "1", "Card A", 2)])
    database = tmp_path / "local.sqlite3"
    sync_local_data(data_dir, database)

    write_cards(card_path, [card("missing", "alice", "1", "Card B", 1)])
    _, errors = sync_local_data(data_dir, database)

    assert errors
    connection = connect_database(database)
    try:
        rows = connection.execute("SELECT card_name, quantity FROM deck_cards").fetchall()
    finally:
        connection.close()
    assert [(row["card_name"], row["quantity"]) for row in rows] == [("Card A", 2)]


def test_valid_changed_card_snapshot_replaces_old_cards(tmp_path):
    data_dir = tmp_path / "data"
    examples = data_dir / "examples"
    examples.mkdir(parents=True)
    write_tournament(data_dir / "event.csv", [record("d1", "alice", "1")])
    card_path = examples / "event_cards.csv"
    write_cards(card_path, [card("d1", "alice", "1", "Card A", 2)])
    database = tmp_path / "local.sqlite3"
    sync_local_data(data_dir, database)

    write_cards(card_path, [card("d1", "alice", "1", "Card B", 3)])
    summaries, errors = sync_local_data(data_dir, database)

    assert not errors
    assert any("cartas actualizado" in summary for summary in summaries)
    connection = connect_database(database)
    try:
        rows = connection.execute("SELECT card_name, quantity FROM deck_cards").fetchall()
    finally:
        connection.close()
    assert [(row["card_name"], row["quantity"]) for row in rows] == [("Card B", 3)]
