"""Import and validate manually exported tournament deck records."""

from __future__ import annotations

import csv
from datetime import date
import json
from pathlib import Path
from typing import Any

import pandas as pd

REQUIRED_FIELDS = ("tournament_id", "tournament_date", "tournament_type", "deck_id")
OPTIONAL_FIELDS = ("player", "placement", "archetype", "decklist", "source_url")
FIELDS = REQUIRED_FIELDS + OPTIONAL_FIELDS


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
        normalized.append(row)

    frame = pd.DataFrame(normalized, columns=FIELDS)
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
