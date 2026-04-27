"""Persistence helpers for CleanLoop history artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_history(history_path: Path) -> list[dict[str, Any]]:
    """Load the round history file if it exists, else return an empty list."""
    if not history_path.exists():
        return []
    return json.loads(history_path.read_text(encoding="utf-8"))


def save_history(history_path: Path, history: list[dict[str, Any]]) -> None:
    """Persist round history using a stable JSON format for the dashboard."""
    history_path.write_text(json.dumps(history, indent=2), encoding="utf-8")
