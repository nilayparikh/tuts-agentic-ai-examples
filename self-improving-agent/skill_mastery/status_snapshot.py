"""Project status snapshot for the Skill Mastery example.

Mirrors `cleanloop/status_snapshot.py` and `prompt_evolution/status_snapshot.py`.
Collects catalog, environment, and output state into one structured payload so
the CLI can render a learner-friendly status view without reaching into private
helpers across the codebase.
"""

from __future__ import annotations

import json
import os
import platform
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import util

from skill_mastery.config import SkillMasteryCatalog, load_catalog

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EXAMPLE_ROOT = PROJECT_ROOT / "skill_mastery"
DATA_DIR = EXAMPLE_ROOT / ".data"
OUTPUT_DIR = EXAMPLE_ROOT / ".output"
GOLD_DIR = EXAMPLE_ROOT / ".gold"
SESSION_PATH = OUTPUT_DIR / "latest_session.json"
TRACES_DIR = OUTPUT_DIR / "traces"


@dataclass(frozen=True)
class CatalogStatus:
    """Catalog health summary for status reporting."""

    contexts: int
    habit_definitions: int
    demonstrations: int
    usecases: int
    gold_references: int


@dataclass(frozen=True)
class EnvironmentStatus:
    """Environment health summary for status reporting."""

    python_version: str
    platform: str
    env_file_exists: bool
    model: str | None
    endpoint: str | None
    api_key_configured: bool


@dataclass(frozen=True)
class OutputStatus:
    """Output artifact summary for status reporting."""

    has_session: bool
    best_round: int | None
    rounds_recorded: int
    has_traces: bool
    trace_runs: int


@dataclass(frozen=True)
class ProjectStatus:
    """Top-level Skill Mastery status snapshot."""

    catalog: CatalogStatus
    environment: EnvironmentStatus
    output: OutputStatus


def _load_catalog_status(catalog: SkillMasteryCatalog) -> CatalogStatus:
    """Summarize the live catalog and gold reference coverage."""
    gold_count = 0
    if GOLD_DIR.exists():
        gold_count = sum(1 for _ in GOLD_DIR.glob("*.md"))
    return CatalogStatus(
        contexts=len(catalog.contexts),
        habit_definitions=len(catalog.habit_definitions),
        demonstrations=len(catalog.demonstrations),
        usecases=len(catalog.usecases),
        gold_references=gold_count,
    )


def _load_environment_status() -> EnvironmentStatus:
    """Summarize Python and provider environment readiness."""
    util.load_env()
    config = util.resolve_llm_env()
    return EnvironmentStatus(
        python_version=platform.python_version(),
        platform=platform.system(),
        env_file_exists=(PROJECT_ROOT / ".env").exists(),
        model=config.get("model"),
        endpoint=config.get("endpoint"),
        api_key_configured=bool(os.getenv("OPENAI_API_KEY") or config.get("api_key")),
    )


def _load_output_status() -> OutputStatus:
    """Summarize the artifacts produced by previous loop runs."""
    has_session = SESSION_PATH.exists()
    best_round: int | None = None
    rounds_recorded = 0
    if has_session:
        try:
            payload = json.loads(SESSION_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            payload = {}
        rounds = payload.get("rounds", [])
        if isinstance(rounds, list):
            rounds_recorded = len(rounds)
        candidate_round = payload.get("best_round")
        if isinstance(candidate_round, int):
            best_round = candidate_round
    has_traces = TRACES_DIR.exists()
    trace_runs = 0
    runs_dir = TRACES_DIR / "runs"
    if runs_dir.exists():
        trace_runs = sum(1 for entry in runs_dir.iterdir() if entry.is_dir())
    return OutputStatus(
        has_session=has_session,
        best_round=best_round,
        rounds_recorded=rounds_recorded,
        has_traces=has_traces,
        trace_runs=trace_runs,
    )


def collect_status(data_dir: Path = DATA_DIR) -> ProjectStatus:
    """Build the full Skill Mastery status snapshot."""
    catalog = load_catalog(data_dir)
    return ProjectStatus(
        catalog=_load_catalog_status(catalog),
        environment=_load_environment_status(),
        output=_load_output_status(),
    )


def render_status(status: ProjectStatus) -> str:
    """Render the status snapshot as plain-text learner output."""
    lines: list[str] = []
    lines.append("Catalog:")
    lines.append(f"  Contexts:         {status.catalog.contexts}")
    lines.append(f"  Habit seeds:      {status.catalog.habit_definitions}")
    lines.append(f"  Demonstrations:   {status.catalog.demonstrations}")
    lines.append(f"  Use cases:        {status.catalog.usecases}")
    lines.append(f"  Gold references:  {status.catalog.gold_references}")
    lines.append("")
    lines.append("Environment:")
    lines.append(f"  Python:    {status.environment.python_version}")
    lines.append(f"  Platform:  {status.environment.platform}")
    lines.append(
        "  .env:      "
        + ("exists" if status.environment.env_file_exists else "missing")
    )
    lines.append(f"  Model:     {status.environment.model or 'unset'}")
    lines.append(f"  Endpoint:  {status.environment.endpoint or 'unset'}")
    lines.append(
        "  API key:   "
        + ("configured" if status.environment.api_key_configured else "missing")
    )
    lines.append("")
    lines.append("Output:")
    lines.append(
        "  Session:        " + ("present" if status.output.has_session else "none")
    )
    lines.append(f"  Rounds saved:   {status.output.rounds_recorded}")
    best_round = status.output.best_round if status.output.best_round else "-"
    lines.append(f"  Best round:     {best_round}")
    lines.append(
        "  Traces:         " + ("present" if status.output.has_traces else "none")
    )
    lines.append(f"  Named runs:     {status.output.trace_runs}")
    return "\n".join(lines)


def status_payload(status: ProjectStatus) -> dict[str, Any]:
    """Return a JSON-safe dictionary view of the status snapshot."""
    return {
        "catalog": {
            "contexts": status.catalog.contexts,
            "habit_definitions": status.catalog.habit_definitions,
            "demonstrations": status.catalog.demonstrations,
            "usecases": status.catalog.usecases,
            "gold_references": status.catalog.gold_references,
        },
        "environment": {
            "python_version": status.environment.python_version,
            "platform": status.environment.platform,
            "env_file_exists": status.environment.env_file_exists,
            "model": status.environment.model,
            "endpoint": status.environment.endpoint,
            "api_key_configured": status.environment.api_key_configured,
        },
        "output": {
            "has_session": status.output.has_session,
            "best_round": status.output.best_round,
            "rounds_recorded": status.output.rounds_recorded,
            "has_traces": status.output.has_traces,
            "trace_runs": status.output.trace_runs,
        },
    }
