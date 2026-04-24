"""clean_data.py — Clean and normalize finance data for CleanLoop.

This file is modified to improve the normalization process for the finance dataset.
"""

from __future__ import annotations

import csv
from pathlib import Path

import pandas as pd
import numpy as np

from cleanloop import datasets as cleanloop_datasets


FINANCE_COLUMNS = ("date", "entity", "value", "category")


def _read_csv_rows(csv_file: Path) -> list[list[str]]:
    """Read raw CSV rows while preserving malformed amount fields."""
    with csv_file.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        return [row for row in reader if any(str(cell).strip() for cell in row)]


def _reshape_finance_row(row: list[str], header_length: int) -> list[str]:
    """Keep finance rows aligned even when amount contains unquoted commas."""
    if len(row) < header_length:
        return row + [""] * (header_length - len(row))
    if len(row) == header_length:
        return row

    trailing_count = header_length - 3
    amount_end = len(row) - trailing_count
    amount = ",".join(row[2:amount_end])
    rebuilt = row[:2] + [amount] + row[amount_end:]
    if len(rebuilt) < header_length:
        rebuilt.extend([""] * (header_length - len(rebuilt)))
    return rebuilt[:header_length]


def _read_finance_frame(csv_file: Path) -> pd.DataFrame:
    """Read one finance CSV file into the shared finance schema."""
    rows = _read_csv_rows(csv_file)
    if not rows:
        return pd.DataFrame(columns=list(FINANCE_COLUMNS))

    header = rows[0]
    body = rows[1:]
    records: list[dict[str, str]] = []
    for row in body:
        rebuilt = _reshape_finance_row(row, len(header))
        raw = dict(zip(header, rebuilt))
        records.append(
            {
                "date": str(raw.get("issued", "")).strip(),
                "entity": str(raw.get("customer", "")).strip(),
                "value": str(raw.get("amount", "")).strip(),
                "category": str(raw.get("status", csv_file.stem)).strip(),
            }
        )
    return pd.DataFrame(records, columns=list(FINANCE_COLUMNS))


def _normalize_finance_frame(master: pd.DataFrame) -> pd.DataFrame:
    """Apply the intentionally limited baseline normalization."""
    normalized = master.reindex(columns=list(FINANCE_COLUMNS)).copy()

    # Normalize the 'value' column to handle currency symbols and accounting markers
    normalized['value'] = normalized['value'].replace(
        to_replace=r'[^\d\.\-\,]', value='', regex=True
    ).replace(',', '', regex=False)

    # Convert 'value' to numeric, coercing errors to NaN
    normalized['value'] = pd.to_numeric(normalized['value'], errors='coerce')

    # Fill NaN values in 'value' with 0
    normalized['value'] = normalized['value'].fillna(0)

    for column in FINANCE_COLUMNS:
        normalized[column] = normalized[column].fillna("").astype(str).str.strip()
    normalized = normalized[normalized["entity"] != ""]
    return normalized.reset_index(drop=True)


def clean(input_dir: Path, output_path: Path) -> None:
    """Merge the finance arena into one weak-but-runnable master CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    config = cleanloop_datasets.get_dataset_config()

    frames: list[pd.DataFrame] = []
    for csv_file in cleanloop_datasets.get_input_paths(input_dir):
        frame = _read_finance_frame(csv_file)
        if not frame.empty:
            frames.append(frame)

    if not frames:
        pd.DataFrame(columns=list(config.required_columns)).to_csv(output_path, index=False)
        return

    master = pd.concat(frames, ignore_index=True)
    master = _normalize_finance_frame(master)
    master = master.sort_values(by=["date", "entity"], kind="stable")
    master.to_csv(output_path, index=False)