"""clean_data_starter.py — Immutable starter genome for CleanLoop demos.

This file captures the intentionally weak baseline that every teaching run
should begin from. `loop.py` copies this file over `clean_data.py` at the start
of each run so learners always see the same improvement process.
"""

import csv
from pathlib import Path

import pandas as pd

from cleanloop import datasets as cleanloop_datasets


SALES_COLUMNS = ("date", "product", "price", "quantity")
FINANCE_COLUMNS = ("date", "entity", "value", "category")
SENSOR_COLUMNS = (
    "timestamp",
    "sensor_id",
    "temperature_c",
    "humidity_pct",
    "pressure_hpa",
)
SENSOR_NUMERIC_COLUMNS = ("temperature_c", "humidity_pct", "pressure_hpa")
SENSOR_TEXT_SENTINELS = frozenset({"", "null", "none", "nan", "error", "offline"})


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


def _reshape_finance_row(row: list[str], header_length: int) -> list[str]:
    """Keep finance rows aligned even when amount contains an unquoted comma."""
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


def _strip_frame(frame: pd.DataFrame, columns: tuple[str, ...]) -> pd.DataFrame:
    """Trim whitespace but keep raw values otherwise untouched."""
    stripped = frame.reindex(columns=list(columns)).copy()
    for column in columns:
        stripped[column] = stripped[column].fillna("").astype(str).str.strip()
    return stripped


def _normalize_sensor_scalar(value: object) -> str:
    """Coerce one sensor cell to text without assuming pandas kept it as a string."""
    if pd.isna(value):
        return ""
    return str(value).strip()


def _normalize_sensor_timestamp(series: pd.Series) -> pd.Series:
    """Convert mixed sensor timestamps into one parseable UTC-normalized format."""
    text_values = series.map(_normalize_sensor_scalar)
    parsed = pd.to_datetime(text_values, errors="coerce", format="mixed", utc=True)
    normalized = parsed.dt.tz_convert(None).dt.strftime("%Y-%m-%d %H:%M:%S")
    return normalized.fillna("")


def _normalize_sensor_numeric(series: pd.Series) -> pd.Series:
    """Convert sensor readings to numeric values while handling text sentinels safely."""
    text_values = series.map(_normalize_sensor_scalar)
    cleaned = text_values.where(
        ~text_values.str.lower().isin(SENSOR_TEXT_SENTINELS),
        "",
    )
    return pd.to_numeric(cleaned, errors="coerce")


def _normalize_sensor_frame(master: pd.DataFrame) -> pd.DataFrame:
    """Apply starter-grade cleanup so sensor output clears obvious parse failures."""
    normalized = master.reindex(columns=list(SENSOR_COLUMNS)).copy()
    normalized["timestamp"] = _normalize_sensor_timestamp(normalized["timestamp"])
    normalized["sensor_id"] = normalized["sensor_id"].map(_normalize_sensor_scalar)

    for column in SENSOR_NUMERIC_COLUMNS:
        normalized[column] = _normalize_sensor_numeric(normalized[column])

    normalized = normalized.replace({"timestamp": {"": pd.NA}, "sensor_id": {"": pd.NA}})
    normalized = normalized.dropna(
        subset=["timestamp", "sensor_id", *SENSOR_NUMERIC_COLUMNS],
    )
    normalized["sensor_id"] = normalized["sensor_id"].astype(str)
    return normalized.reset_index(drop=True)


def _read_sales_frame(csv_file: Path) -> pd.DataFrame:
    """Read one sales CSV file into the shared sales schema."""
    rows = _read_csv_rows(csv_file)
    if not rows:
        return pd.DataFrame(columns=list(SALES_COLUMNS))

    body = rows[1:] if _has_exact_header(rows[0], SALES_COLUMNS) else rows
    records = [_reshape_sales_row(row) for row in body]
    return pd.DataFrame(records, columns=list(SALES_COLUMNS))


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
                "date": raw.get("issued", ""),
                "entity": raw.get("customer", ""),
                "value": raw.get("amount", ""),
                "category": raw.get("status", csv_file.stem),
            }
        )
    return pd.DataFrame(records, columns=list(FINANCE_COLUMNS))


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
    return _normalize_sensor_frame(master)


def clean(input_dir: Path, output_path: Path) -> None:
    """Read one dataset family and write a weak starter master CSV."""
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