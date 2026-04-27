"""Reset helpers for restoring the starter genome while keeping sample outputs."""

from __future__ import annotations

from pathlib import Path
from typing import Callable


def reset_to_starter(
    *,
    output_dir: Path,
    genome_path: Path,
    starter_genome_path: Path,
    emit: Callable[[str], None] = print,
) -> int:
    """Restore the starter genome without deleting the shipped output artifacts."""
    if output_dir.exists():
        emit("Preserved cleanloop/.output sample artifacts")
    else:
        emit("No cleanloop/.output directory present")

    genome_path.write_text(
        starter_genome_path.read_text(encoding="utf-8"), encoding="utf-8"
    )
    emit("Restored clean_data.py from clean_data_starter.py")
    emit("\nReady to re-run: python util.py loop\n")
    return 0
