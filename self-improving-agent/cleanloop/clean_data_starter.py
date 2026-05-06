"""clean_data_starter.py — Starter genome for the CleanLoop finance cleaner."""

from __future__ import annotations

from pathlib import Path

from cleanloop.clean_data_runtime import clean_starter as _runtime_clean


def clean(input_dir: Path, output_path: Path) -> None:
    """Run only the deterministic stage before the loop mutates the genome."""
    # Mutation surface: keep the module shape intact and upgrade this function,
    # not the top-level imports or helper layout.
    _runtime_clean(input_dir, output_path)
