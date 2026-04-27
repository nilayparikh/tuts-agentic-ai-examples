"""Helpers for loading exported CleanLoop traces and raw loop logs."""

from __future__ import annotations

import json
from pathlib import Path

from cleanloop import datasets as cleanloop_datasets


def _read_jsonl_records(path: Path) -> list[dict[str, object]]:
    """Load one JSONL file into dashboard-safe record dicts."""
    if not path.exists():
        return []

    records: list[dict[str, object]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if not stripped:
                continue
            payload = json.loads(stripped)
            if isinstance(payload, dict):
                records.append(payload)
    return records


def load_dashboard_artifacts(
    output_dir: Path,
    dataset_name: str | None = None,
) -> dict[str, list[dict[str, object]]]:
    """Load the exported trace and raw-log artifacts for dashboard rendering."""
    return {
        "run_events": _read_jsonl_records(
            cleanloop_datasets.get_run_events_path(output_dir)
        ),
        "row_decisions": _read_jsonl_records(
            cleanloop_datasets.get_row_decisions_path(output_dir)
        ),
        "proposal_events": _read_jsonl_records(
            cleanloop_datasets.get_proposal_events_path(output_dir)
        ),
        "exported_logs": _read_jsonl_records(
            cleanloop_datasets.get_exported_logs_path(output_dir, dataset_name)
        ),
    }
