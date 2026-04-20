"""clean_data.py — The Genome (mutable).

This is the ONLY file the agent is allowed to modify.
It starts as a naive dataset-family cleaner that fails many assertions.
The self-improving loop rewrites this file iteratively until all
assertions pass for the selected dataset family.

Lesson references:
  - Lesson 03: Lines 20-45  (naive implementation — the starting genome)
  - Lesson 06: Lines 20-45  (this is what the loop rewrites)
  - Lesson 09: Lines 20-45  (challenger generates data that breaks this)

Usage:
    Not run directly — imported by prepare.py, loop.py, and reranker.py.
"""

import csv
import re
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
TEXT_SENTINELS = {"", "na", "n/a", "nan", "none", "null"}
NUMERIC_SENTINELS = TEXT_SENTINELS | {
    "error",
    "offline",
    "free",
    "free trial",
    "complimentary",
    "tbd",
    "pending",
    "offset",
}
FINANCE_ZERO_SENTINELS = {"free trial", "complimentary", "offset"}


def _read_csv_rows(csv_file: Path) -> list[list[str]]:
    """Read raw CSV rows without dropping malformed records."""
    with csv_file.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        return [row for row in reader if any(cell.strip() for cell in row)]


def _has_exact_header(row: list[str], expected_columns: tuple[str, ...]) -> bool:
    """Detect whether a row exactly matches the expected header."""
    normalized = tuple(cell.strip().lower() for cell in row)
    return normalized == expected_columns


def _reshape_sales_row(row: list[str]) -> list[str]:
    """Rebuild one sales row when the price field contains an unquoted comma."""
    if len(row) < 4:
        return row + [""] * (4 - len(row))
    if len(row) == 4:
        return row
    return [row[0], row[1], ",".join(row[2:-1]), row[-1]]


def _reshape_finance_row(row: list[str], header_length: int) -> list[str]:
    """Rebuild one finance row when the amount field contains an unquoted comma."""
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


def _clean_text_value(value: object) -> str | None:
    """Normalize text fields and treat blank sentinels as missing."""
    if pd.isna(value):
        return None
    text = str(value).strip()
    if text.lower() in TEXT_SENTINELS:
        return None
    return text or None


def _clean_numeric_value(value: object) -> float | None:
    """Normalize currency-like and sentinel-like values into floats."""
    if pd.isna(value):
        return None

    text = str(value).strip()
    if text.lower() in NUMERIC_SENTINELS:
        return None

    cleaned = re.sub(r"[^0-9,.-]", "", text)
    if not cleaned or cleaned in {"-", ".", ",", "-.", "-,"}:
        return None

    if "," in cleaned and "." in cleaned:
        cleaned = cleaned.replace(",", "")
    elif cleaned.count(",") == 1 and "." not in cleaned:
        whole, fraction = cleaned.split(",")
        if len(fraction) in {1, 2}:
            cleaned = f"{whole}.{fraction}"
        else:
            cleaned = whole + fraction
    else:
        cleaned = cleaned.replace(",", "")

    try:
        return float(cleaned)
    except ValueError:
        return None


def _clean_finance_value(value: object) -> float | None:
    """Normalize finance-specific non-cash states into meaningful numeric values."""
    if pd.isna(value):
        return None

    text = str(value).strip().lower()
    if text in FINANCE_ZERO_SENTINELS:
        return 0.0
    return _clean_numeric_value(value)


def _normalize_sales_frame(frame: pd.DataFrame) -> pd.DataFrame:
    """Normalize the concatenated sales frame into the target sales schema."""
    normalized = frame.copy()
    normalized["date"] = pd.to_datetime(
        normalized["date"],
        errors="coerce",
        format="mixed",
        dayfirst=True,
    ).dt.strftime("%Y-%m-%d")
    normalized["product"] = normalized["product"].apply(_clean_text_value)
    normalized["price"] = normalized["price"].apply(_clean_numeric_value)
    normalized["quantity"] = normalized["quantity"].apply(_clean_numeric_value)
    normalized = normalized.dropna(subset=list(SALES_COLUMNS))
    return normalized.loc[:, list(SALES_COLUMNS)]


def _normalize_finance_frame(frame: pd.DataFrame) -> pd.DataFrame:
    """Normalize the concatenated finance frame into the target finance schema."""
    normalized = frame.copy()
    normalized["date"] = pd.to_datetime(
        normalized["date"],
        errors="coerce",
        format="mixed",
        dayfirst=True,
    ).dt.strftime("%Y-%m-%d")
    normalized["entity"] = normalized["entity"].apply(_clean_text_value)
    normalized["value"] = normalized["value"].apply(_clean_finance_value)
    normalized["category"] = normalized["category"].apply(_clean_text_value)
    normalized["category"] = normalized["category"].fillna("unknown")
    normalized = normalized.dropna(subset=["date", "entity", "value"])
    return normalized.loc[:, list(FINANCE_COLUMNS)]


def _normalize_sensor_frame(frame: pd.DataFrame) -> pd.DataFrame:
    """Normalize the concatenated sensor frame into the target sensor schema."""
    normalized = frame.copy()
    timestamps = pd.to_datetime(
        normalized["timestamp"],
        errors="coerce",
        format="mixed",
        utc=True,
    )
    normalized["timestamp"] = timestamps.dt.strftime("%Y-%m-%d %H:%M:%S")
    normalized["sensor_id"] = normalized["sensor_id"].apply(_clean_text_value)
    normalized["temperature_c"] = normalized["temperature_c"].apply(_clean_numeric_value)
    normalized["humidity_pct"] = normalized["humidity_pct"].apply(_clean_numeric_value)
    normalized["pressure_hpa"] = normalized["pressure_hpa"].apply(_clean_numeric_value)
    normalized = normalized.dropna(subset=list(SENSOR_COLUMNS))
    return normalized.loc[:, list(SENSOR_COLUMNS)]


def _read_sales_frame(csv_file: Path) -> pd.DataFrame:
    """Read one sales CSV file while preserving headerless records."""
    rows = _read_csv_rows(csv_file)
    if not rows:
        return pd.DataFrame(columns=list(SALES_COLUMNS))

    body = rows[1:] if _has_exact_header(rows[0], SALES_COLUMNS) else rows
    records = [_reshape_sales_row(row) for row in body]
    return pd.DataFrame(records, columns=list(SALES_COLUMNS))


def _read_finance_frame(csv_file: Path) -> pd.DataFrame:
    """Read one finance CSV file and map it into the shared finance schema."""
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
    """Read one sensor CSV file and keep only the core telemetry columns."""
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
    """Normalize the concatenated frame for the selected dataset family."""
    if dataset_name == "sales":
        return _normalize_sales_frame(master)
    if dataset_name == "finance":
        return _normalize_finance_frame(master)
    return _normalize_sensor_frame(master)


def clean(input_dir: Path, output_path: Path) -> None:
    """Read the selected dataset family from input_dir and write a master CSV."""
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
