"""clean_data.py — Improved genome for cleaning sensor time series data.

This file contains enhanced logic to clean malformed sensor data, ensuring
all numeric fields are properly parsed and handling sentinel values.
"""

import csv
from pathlib import Path
import pandas as pd

from cleanloop import datasets as cleanloop_datasets

SENSOR_COLUMNS = (
    "timestamp",
    "sensor_id",
    "temperature_c",
    "humidity_pct",
    "pressure_hpa",
)

SENTINEL_VALUES = {
    "temperature_c": ["ERROR", "NULL", "999.9", "-999", "OFFLINE"],
    "humidity_pct": ["ERROR", "NULL", "999.9", "-999", "OFFLINE"],
    "pressure_hpa": ["ERROR", "NULL", "999.9", "-999", "OFFLINE"],
}

def _read_csv_rows(csv_file: Path) -> list[list[str]]:
    """Read CSV rows without trying to clean malformed values."""
    with csv_file.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        return [row for row in reader if any(cell.strip() for cell in row)]

def _has_exact_header(row: list[str], expected_columns: tuple[str, ...]) -> bool:
    """Detect a header row that already matches the target schema."""
    normalized = tuple(cell.strip().lower() for cell in row)
    return normalized == expected_columns

def _clean_numeric_column(series: pd.Series, column_name: str) -> pd.Series:
    """Convert a column to numeric, replacing sentinel values with NaN."""
    series = series.replace(SENTINEL_VALUES.get(column_name, []), pd.NA)
    return pd.to_numeric(series, errors='coerce')

def _clean_sensor_frame(frame: pd.DataFrame) -> pd.DataFrame:
    """Clean sensor data frame by handling sentinel values and parsing timestamps."""
    # Clean numeric columns
    for column in ["temperature_c", "humidity_pct", "pressure_hpa"]:
        frame[column] = _clean_numeric_column(frame[column], column)

    # Parse timestamps and handle mixed timezones
    frame['timestamp'] = pd.to_datetime(frame['timestamp'], errors='coerce', utc=True)

    # Fill NaN sensor_id with a placeholder or drop rows if necessary
    frame['sensor_id'] = frame['sensor_id'].fillna('UNKNOWN')

    return frame

def _read_sensor_frame(csv_file: Path) -> pd.DataFrame:
    """Read one sensor CSV file into the shared sensor schema."""
    raw = pd.read_csv(csv_file, engine="python", on_bad_lines="skip")
    return raw.reindex(columns=list(SENSOR_COLUMNS))

def _read_dataset_frame(csv_file: Path, dataset_name: str) -> pd.DataFrame:
    """Read one dataset-family CSV into a shared intermediate schema."""
    if dataset_name == "sales":
        return _read_sales_frame(csv_file)
    if dataset_name == "finance":
        return _read_finance_frame(csv_file)
    return _read_sensor_frame(csv_file)

def _normalize_dataset_frame(master: pd.DataFrame, dataset_name: str) -> pd.DataFrame:
    """Do only minimal shaping for the starter genome."""
    if dataset_name == "sales":
        return _strip_frame(master, SALES_COLUMNS)
    if dataset_name == "finance":
        return _strip_frame(master, FINANCE_COLUMNS)
    return _clean_sensor_frame(master)

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
    master = master.sort_values(by=list(config.required_columns[:1]), kind="stable")
    master.to_csv(output_path, index=False)