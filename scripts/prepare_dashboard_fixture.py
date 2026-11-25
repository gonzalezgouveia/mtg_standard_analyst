"""Create an isolated Streamlit copy with a minimal synthetic tournament database."""

import json
import shutil
from datetime import date, timedelta
from pathlib import Path
from uuid import uuid4

from src.database import DEFAULT_DATABASE_NAME, sync_local_data


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    scratch = root / "data" / ".dashboard-tests"
    scratch.mkdir(exist_ok=True)
    # Inherit the project data directory permissions for the user's Streamlit process.
    fixture = scratch / f"dashboard-{uuid4().hex[:12]}"
    fixture.mkdir()
    shutil.copy2(root / "app.py", fixture / "app.py")
    shutil.copytree(root / "src", fixture / "src", ignore=shutil.ignore_patterns("__pycache__"))
    data_dir = fixture / "data"
    data_dir.mkdir()

    today = date.today()
    records = [
        {
            "tournament_id": "fixture-recent",
            "tournament_date": (today - timedelta(days=6)).isoformat(),
            "tournament_type": "Standard Challenge 32",
            "deck_id": "1",
            "archetype": "Arquetipo de prueba",
            "participants_total": 4,
        },
        {
            "tournament_id": "fixture-older",
            "tournament_date": (today - timedelta(days=7)).isoformat(),
            "tournament_type": "Standard Challenge 16",
            "deck_id": "1",
        },
    ]
    (data_dir / "synthetic_tournaments.json").write_text(
        json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    _, errors = sync_local_data(data_dir, data_dir / DEFAULT_DATABASE_NAME)
    if errors:
        raise SystemExit("\n".join(errors))

    print(fixture.relative_to(root).as_posix())


if __name__ == "__main__":
    main()
