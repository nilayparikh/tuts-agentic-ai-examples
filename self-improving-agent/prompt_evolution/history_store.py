"""Durable round history store for Prompt Evolution sessions.

Mirrors `cleanloop/history_store.py`. Records each round's persistence as an
append-only JSONL file beside `latest_session.json`, so a learner can inspect
trajectory across runs without parsing the consolidated session payload.

The store is intentionally separate from `tracing.py`. Tracing emits OTEL-shaped
event records; the history store keeps the raw structured-round records that
back the dashboard and best-of selection.
"""

# pylint: disable=duplicate-code

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EXAMPLE_ROOT = PROJECT_ROOT / "prompt_evolution"
DEFAULT_OUTPUT_DIR = EXAMPLE_ROOT / ".output"
HISTORY_FILE_NAME = "round_history.jsonl"


@dataclass
class HistoryStore:
    """Append-only JSONL store of round records."""

    output_dir: Path = DEFAULT_OUTPUT_DIR
    file_name: str = HISTORY_FILE_NAME

    @property
    def path(self) -> Path:
        """Return the JSONL history path."""
        return self.output_dir / self.file_name

    def append(self, record: dict[str, Any]) -> None:
        """Append one round record as one JSON line."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, sort_keys=True) + "\n")

    def append_many(self, records: Iterable[dict[str, Any]]) -> None:
        """Append a sequence of round records preserving order."""
        for record in records:
            self.append(record)

    def load(self) -> list[dict[str, Any]]:
        """Return all stored records as a list of dictionaries."""
        if not self.path.exists():
            return []
        records: list[dict[str, Any]] = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            try:
                payload = json.loads(stripped)
            except json.JSONDecodeError:
                continue
            if isinstance(payload, dict):
                records.append(payload)
        return records

    def reset(self) -> None:
        """Delete the JSONL history file but leave the output directory intact."""
        if self.path.exists():
            self.path.unlink()


def select_best(records: list[dict[str, Any]]) -> dict[str, Any] | None:
    """Pick the record with the highest score; tie-break by latest round."""
    if not records:
        return None
    return max(
        records,
        key=lambda item: (
            int(item.get("score", 0)),
            int(item.get("round", 0)),
        ),
    )


def filter_by_session(
    records: list[dict[str, Any]],
    session_id: str,
) -> list[dict[str, Any]]:
    """Return records that belong to a specific session id."""
    return [record for record in records if record.get("session_id") == session_id]
