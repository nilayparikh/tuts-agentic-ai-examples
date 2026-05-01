"""Reset and recovery helpers for Prompt Evolution outputs.

Mirrors `cleanloop/reset_workflow.py`. Resetting Prompt Evolution must:

- clear runtime artifacts (`latest_session.json`, `best_*.md`,
  `latest_mutation.diff`, `traces/`, `round_history.jsonl`)
- preserve `.gold/` reference responses so demos remain reproducible
- preserve the mutable instruction block embedded in `README.md`

The starter instruction block is the README itself, not a separate file; the
loop never edits the README in place. That keeps the reset story narrow.
"""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EXAMPLE_ROOT = PROJECT_ROOT / "prompt_evolution"
OUTPUT_DIR = EXAMPLE_ROOT / ".output"
GOLD_DIR = EXAMPLE_ROOT / ".gold"

PROTECTED_OUTPUT_NAMES = frozenset({".gitignore", "README.md"})


@dataclass(frozen=True)
class ResetReport:
    """Summary of a Prompt Evolution reset."""

    deleted_paths: tuple[str, ...]
    preserved_paths: tuple[str, ...]


def _list_output_entries() -> list[Path]:
    """Return the entries under the output directory if it exists."""
    if not OUTPUT_DIR.exists():
        return []
    return sorted(OUTPUT_DIR.iterdir())


def reset(*, output_dir: Path = OUTPUT_DIR) -> ResetReport:
    """Delete runtime artifacts while preserving reference data.

    Returns a :class:`ResetReport` so a CLI can show learners exactly what was
    removed and what was kept.
    """
    deleted: list[str] = []
    preserved: list[str] = []
    if not output_dir.exists():
        return ResetReport(
            deleted_paths=tuple(deleted), preserved_paths=tuple(preserved)
        )

    for entry in sorted(output_dir.iterdir()):
        if entry.name in PROTECTED_OUTPUT_NAMES:
            preserved.append(entry.name)
            continue
        if entry.is_dir():
            shutil.rmtree(entry)
        else:
            entry.unlink()
        deleted.append(entry.name)

    if not any(output_dir.iterdir()):
        # Keep the directory so subsequent runs reuse the same path.
        pass

    return ResetReport(
        deleted_paths=tuple(deleted),
        preserved_paths=tuple(preserved),
    )


def render_report(report: ResetReport) -> str:
    """Render a reset summary as plain-text learner output."""
    lines: list[str] = []
    if report.deleted_paths:
        lines.append("Deleted:")
        lines.extend(f"  - {name}" for name in report.deleted_paths)
    else:
        lines.append("Deleted: nothing (output directory was already clean)")
    if report.preserved_paths:
        lines.append("Preserved:")
        lines.extend(f"  - {name}" for name in report.preserved_paths)
    if GOLD_DIR.exists():
        gold_count = sum(1 for _ in GOLD_DIR.glob("*.md"))
        lines.append(f"Gold references kept: {gold_count} files in .gold/")
    lines.append("Mutable instructions in README.md remain unchanged.")
    return "\n".join(lines)
