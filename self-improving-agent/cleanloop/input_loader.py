"""Input loading helpers for the finance fixture used by CleanLoop."""

# pyright: reportMissingImports=false, reportMissingModuleSource=false
# pylint: disable=import-error

from __future__ import annotations

import csv
from pathlib import Path

import pandas as pd  # type: ignore[import-not-found, import-untyped]


def normalize_text(value: object) -> str:
    """Convert raw scalars to trimmed strings without crashing on NaN."""
    if pd.isna(value):
        return ""
    return str(value).strip()


def read_csv_rows(csv_file: Path) -> list[list[str]]:
    """Read raw CSV rows while preserving malformed amount fields."""
    with csv_file.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        return [row for row in reader if any(str(cell).strip() for cell in row)]


def reshape_finance_row(row: list[str], header_length: int) -> list[str]:
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


def read_finance_records(csv_file: Path) -> list[dict[str, str]]:
    """Read one finance CSV file into normalized raw records with source metadata."""
    rows = read_csv_rows(csv_file)
    if not rows:
        return []

    header = rows[0]
    body = rows[1:]
    records: list[dict[str, str]] = []
    for row in body:
        rebuilt = reshape_finance_row(row, len(header))
        raw = dict(zip(header, rebuilt))
        records.append(
            {
                "source_file": csv_file.name,
                "invoice_id": normalize_text(raw.get("invoice_id", "")),
                "customer": normalize_text(raw.get("customer", "")),
                "raw_date": normalize_text(raw.get("issued", "")),
                "raw_amount": normalize_text(raw.get("amount", "")),
                "currency": normalize_text(raw.get("currency", "")).upper(),
                "status": normalize_text(raw.get("status", csv_file.stem)).lower(),
                "adjusted_amount": normalize_text(raw.get("adjusted_amount", "")),
                "approval_flag": normalize_text(raw.get("approval_flag", "")).lower(),
                "resolution_amount": normalize_text(raw.get("resolution_amount", "")),
                "resolution_flag": normalize_text(
                    raw.get("resolution_flag", "")
                ).lower(),
            }
        )
    return records
