"""clean_data.py — Enhanced genome for CleanLoop demos.

This file captures an improved baseline that addresses issues with malformed values,
ensures numeric prices, and aligns with the reference output.
"""

import csv
from pathlib import Path

import pandas as pd

from cleanloop import datasets as cleanloop_datasets


SALES_COLUMNS = ("date", "product", "price", "quantity")


def _read_csv_rows(csv_file: Path) -> list[list[str]]:
    """Read CSV rows without trying to clean malformed values."""
    with csv_file.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        return [row for row in reader if any(cell.strip() for cell in row)]


def _has_exact_header(row: list[str], expected_columns: tuple[str, ...]) -> bool:
    """Detect a header row that already matches the target schema."""
    normalized = tuple(cell.strip().lower() for cell in row)
    return normalized == expected_columns


def _reshape_sales_row(row: list[str]) -> list[str]:
    """Keep sales rows aligned even when price contains an unquoted comma."""
    if len(row) < 4:
        return row + [""] * (4 - len(row))
    if len(row) == 4:
        return row
    return [row[0], row[1], ",".join(row[2:-1]), row[-1]]


def _parse_date(date_str: str) -> pd.Timestamp:
    """Parse date from various formats into a standard datetime."""
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m-%d-%Y", "%Y/%m/%d"):
        try:
            return pd.to_datetime(date_str, format=fmt)
        except (ValueError, TypeError):
            continue
    return pd.NaT


def _clean_price(price_str: str) -> float:
    """Convert price to a numeric float, handling commas."""
    try:
        return float(price_str.replace(",", ""))
    except (ValueError, TypeError):
        return pd.NA


def _strip_frame(frame: pd.DataFrame, columns: tuple[str, ...]) -> pd.DataFrame:
    """Trim whitespace but keep raw values otherwise untouched."""
    stripped = frame.reindex(columns=list(columns)).copy()
    for column in columns:
        stripped[column] = stripped[column].fillna("").astype(str).str.strip()
    return stripped


def _read_sales_frame(csv_file: Path) -> pd.DataFrame:
    """Read one sales CSV file into the shared sales schema."""
    rows = _read_csv_rows(csv_file)
    if not rows:
        return pd.DataFrame(columns=list(SALES_COLUMNS))

    body = rows[1:] if _has_exact_header(rows[0], SALES_COLUMNS) else rows
    records = [_reshape_sales_row(row) for row in body]
    return pd.DataFrame(records, columns=list(SALES_COLUMNS))


def _normalize_sales_frame(master: pd.DataFrame) -> pd.DataFrame:
    """Ensure dates are parseable and prices are numeric."""
    master['date'] = master['date'].apply(_parse_date)
    master['price'] = master['price'].apply(_clean_price)
    return master


def _read_dataset_frame(csv_file: Path, dataset_name: str) -> pd.DataFrame:
    """Read one dataset-family CSV into a shared intermediate schema."""
    if dataset_name == "sales":
        return _read_sales_frame(csv_file)
    return pd.DataFrame(columns=list(SALES_COLUMNS))  # Placeholder for other datasets


def _normalize_dataset_frame(master: pd.DataFrame, dataset_name: str) -> pd.DataFrame:
    """Do only minimal shaping for the starter genome."""
    if dataset_name == "sales":
        return _normalize_sales_frame(master)
    return _strip_frame(master, SALES_COLUMNS)


def clean(input_dir: Path, output_path: Path) -> None:
    """Read one dataset family and write a cleaned master CSV."""
    output_path.parent.mkdir(exist_ok=True)
    config = cleanloop_datasets.detect_dataset_from_output_path(output_path)

    frames: list[pd.DataFrame] = []
    for csv_file in cleanloop_datasets.get_input_paths(input_dir, config.name):
        frame = _read_dataset_frame(csv_file, config.name)
        if not frame.empty:
            frames.append(frame)

    if not frames:
        pd.DataFrame(columns=list(config.required_columns)).to_csv(output_path, index=False)
        return

    master = pd.concat(frames, ignore_index=True)
    master = _normalize_dataset_frame(master, config.name)
    master = master.dropna(subset=config.required_columns)
    master = master.sort_values(by=list(config.required_columns[:1]), kind="stable")
    master.to_csv(output_path, index=False)