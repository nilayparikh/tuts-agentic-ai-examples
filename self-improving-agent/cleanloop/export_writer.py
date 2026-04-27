"""Stable CSV writing helpers for CleanLoop exports and anomaly reports."""

# pyright: reportMissingImports=false, reportMissingModuleSource=false
# pylint: disable=import-error

from __future__ import annotations

from pathlib import Path

import pandas as pd  # type: ignore[import-not-found, import-untyped]

from cleanloop.dataset_contract import FINANCE_COLUMNS


def write_rows(
    output_path: Path,
    rows: list[dict[str, str]],
    columns: tuple[str, ...],
    *,
    prioritize_non_zero: bool = False,
) -> None:
    """Write rows to CSV using a stable column order and deterministic sorting."""
    frame = pd.DataFrame(rows, columns=list(columns))
    if not frame.empty and tuple(columns) == FINANCE_COLUMNS:
        if prioritize_non_zero:
            frame["__abs_value"] = pd.to_numeric(frame["value"], errors="coerce").abs()
            frame = frame.sort_values(
                by=["__abs_value", "date", "entity"],
                ascending=[False, True, True],
                kind="stable",
            ).drop(columns=["__abs_value"])
        else:
            frame = frame.sort_values(by=["date", "entity"], kind="stable")
    elif not frame.empty:
        frame = frame.sort_values(by=["source_file", "invoice_id"], kind="stable")
    frame.to_csv(output_path, index=False)
