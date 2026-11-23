import json
from pathlib import Path

import pytest

from src.data import (
    DataValidationError,
    add_display_archetype,
    load_label_overrides,
    load_tournament_file,
    save_label_overrides,
    validate_records,
)


def record(**changes):
    row = {
        "tournament_id": "event-1",
        "tournament_date": "2026-11-20",
        "tournament_type": "Standard Challenge",
        "deck_id": "deck-1",
    }
    row.update(changes)
    return row


def test_accepts_multiple_tournaments_and_optional_missing_values():
    frame = validate_records(
        [record(), record(tournament_id="event-2", deck_id="deck-1", tournament_date="2026-11-21")]
    )
    assert frame.tournament_id.nunique() == 2
    assert frame.loc[0, "player"] == ""


@pytest.mark.parametrize(
    "changes", [{"deck_id": ""}, {"tournament_id": ""}, {"tournament_type": ""}, {"tournament_date": "yesterday"}]
)
def test_rejects_missing_required_values_and_invalid_dates(changes):
    with pytest.raises(DataValidationError):
        validate_records([record(**changes)])


def test_rejects_duplicate_deck_within_tournament():
    with pytest.raises(DataValidationError, match="repetidos"):
        validate_records([record(), record()])


def test_rejects_empty_import():
    with pytest.raises(DataValidationError, match="no contiene listas"):
        validate_records([])


def test_reads_csv_and_json(tmp_path):
    csv_path = tmp_path / "input.csv"
    csv_path.write_text(
        "tournament_id,tournament_date,tournament_type,deck_id\ne1,2026-11-20,Challenge,d1\n",
        encoding="utf-8",
    )
    json_path = tmp_path / "input.json"
    json_path.write_text(json.dumps([record()]), encoding="utf-8")
    assert len(load_tournament_file(csv_path.open(encoding="utf-8"), "input.csv")) == 1
    assert len(load_tournament_file(json_path.open(encoding="utf-8"), "input.json")) == 1


def test_saves_and_loads_manual_labels(tmp_path):
    path = tmp_path / "labels.json"
    labels = {"event-1::deck-1": "Control"}
    save_label_overrides(path, labels)
    assert load_label_overrides(path) == labels
    shown = add_display_archetype(validate_records([record()]), labels)
    assert shown.loc[0, "archetype_display"] == "Control"


def test_supplied_tournament_sample_imports():
    sample = Path(__file__).parents[1] / "data" / "standard_challenge_32_2026-11-20.csv"
    with sample.open(encoding="utf-8") as file:
        frame = load_tournament_file(file, sample.name)
    assert len(frame) == 32
    assert frame["tournament_id"].nunique() == 1
    assert frame["player"].nunique() == 32
    assert (frame["decklist"] == "").all()
