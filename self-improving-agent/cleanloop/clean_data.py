"""clean_data.py — Shipped genome for the CleanLoop finance cleaner."""

from __future__ import annotations

from pathlib import Path

from cleanloop.clean_data_runtime import clean as _runtime_clean


def clean(input_dir: Path, output_path: Path) -> None:
    """Run the shipped deterministic-plus-mutation runtime."""
    _runtime_clean(input_dir, output_path)
