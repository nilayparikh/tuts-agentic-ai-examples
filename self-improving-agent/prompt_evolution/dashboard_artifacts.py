"""Dashboard artifact loaders for Prompt Evolution.

Mirrors `cleanloop/dashboard_artifacts.py`. The dashboard reads several
JSONL trace files plus the consolidated `latest_session.json`. This module
centralizes the loading logic so the Streamlit dashboard, tests, and
custom analysis scripts share one reader implementation.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EXAMPLE_ROOT = PROJECT_ROOT / "prompt_evolution"
OUTPUT_DIR = EXAMPLE_ROOT / ".output"
SESSION_PATH = OUTPUT_DIR / "latest_session.json"
TRACE_DIR = OUTPUT_DIR / "traces"


@dataclass(frozen=True)
class DashboardArtifacts:
    """All artifacts the dashboard needs in one bundle."""

    session: dict[str, Any] | None
    run_events: list[dict[str, Any]]
    llm_requests: list[dict[str, Any]]
    evaluator_events: list[dict[str, Any]]
    latest_diff: str | None


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    """Load a JSONL file, skipping malformed or blank lines."""
    if not path.exists():
        return []
    records: list[dict[str, Any]] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            records.append(payload)
    return records


def _load_session(path: Path) -> dict[str, Any] | None:
    """Load the consolidated session payload when present."""
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    return payload if isinstance(payload, dict) else None


def _load_diff(path: Path) -> str | None:
    """Load the latest mutation diff text when present."""
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def load_artifacts(
    *,
    session_path: Path = SESSION_PATH,
    trace_dir: Path = TRACE_DIR,
) -> DashboardArtifacts:
    """Load every artifact the dashboard renders."""
    return DashboardArtifacts(
        session=_load_session(session_path),
        run_events=_load_jsonl(trace_dir / "run_events.jsonl"),
        llm_requests=_load_jsonl(trace_dir / "llm_requests.jsonl"),
        evaluator_events=_load_jsonl(trace_dir / "evaluator_events.jsonl"),
        latest_diff=_load_diff(session_path.parent / "latest_mutation.diff"),
    )


def list_named_runs(trace_dir: Path = TRACE_DIR) -> list[str]:
    """Return sorted run-instance directories under traces/runs/."""
    runs_dir = trace_dir / "runs"
    if not runs_dir.exists():
        return []
    return sorted(item.name for item in runs_dir.iterdir() if item.is_dir())
