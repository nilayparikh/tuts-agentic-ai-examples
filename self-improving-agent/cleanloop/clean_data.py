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

from pathlib import Path

import pandas as pd


# =====================================================================
# SECTION: The Genome — Clean Function
# Lesson 03 — This naive starter genome reads only the selected dataset
# family and concatenates or lightly normalizes those files.
#
# Why it fails:
#   - sales data still includes symbols, blanks, and mixed date formats
#   - finance data still includes sentinels and text values in numeric fields
#   - sensor data still includes NULL, ERROR, and impossible readings
#
# The agent must rewrite this function to handle all dataset-specific edge cases.
# After the loop runs, this file will contain the "evolved" version.
# =====================================================================

from cleanloop import datasets as cleanloop_datasets


def _read_sales_frame(csv_file: Path) -> pd.DataFrame:
    """Read one sales CSV file with tolerant row parsing."""
    try:
        return pd.read_csv(csv_file, engine="python", on_bad_lines="skip")
    except Exception:
        return pd.DataFrame()


def _read_finance_frame(csv_file: Path) -> pd.DataFrame:
    """Read one finance CSV file and map it into a shared finance schema."""
    try:
        raw = pd.read_csv(csv_file, engine="python", on_bad_lines="skip")
    except Exception:
        return pd.DataFrame()

    if raw.empty:
        return raw

    if "invoice_id" in raw.columns:
        return raw.rename(
            columns={"issued": "date", "customer": "entity", "amount": "value"}
        )[["date", "entity", "value"]].assign(category="invoice")

    return raw.rename(
        columns={"trade_date": "date", "ticker": "entity", "close": "value"}
    )[["date", "entity", "value"]].assign(category="stock")


def _read_sensor_frame(csv_file: Path) -> pd.DataFrame:
    """Read one sensor CSV file with tolerant row parsing."""
    try:
        return pd.read_csv(csv_file, engine="python", on_bad_lines="skip")
    except Exception:
        return pd.DataFrame()


def _read_dataset_frame(csv_file: Path, dataset_name: str) -> pd.DataFrame:
    """Read one dataset-family CSV into the starter output schema."""
    if dataset_name == "sales":
        return _read_sales_frame(csv_file)
    if dataset_name == "finance":
        return _read_finance_frame(csv_file)
    return _read_sensor_frame(csv_file)


def clean(input_dir: Path, output_path: Path) -> None:
    """Read the selected dataset family from input_dir and write a master CSV.

    This is the naive starting implementation. The self-improving loop
    will rewrite this function to handle messy values, missing fields,
    sentinels, and inconsistent date or timestamp formats.
    """
    output_path.parent.mkdir(exist_ok=True)
    config = cleanloop_datasets.detect_dataset_from_output_path(output_path)

    frames: list[pd.DataFrame] = []
    for csv_file in cleanloop_datasets.get_input_paths(input_dir, config.name):
        try:
            df = _read_dataset_frame(csv_file, config.name)
            if not df.empty:
                frames.append(df)
        except Exception:
            continue

    if not frames:
        pd.DataFrame(columns=list(config.required_columns)).to_csv(output_path, index=False)
        return

    master = pd.concat(frames, ignore_index=True)
    
    # Dataset-specific cleaning
    if config.name == "sales":
        # Clean price: remove currency symbols, commas, whitespace, and handle text sentinels
        if "price" in master.columns:
            master["price"] = master["price"].astype(str).str.replace(r'[$,\s]', '', regex=True)
            master["price"] = master["price"].replace(
                ['ERROR', 'NULL', 'N/A', 'NA', 'null', 'error', 'None', ''], pd.NA
            )
            master["price"] = pd.to_numeric(master["price"], errors='coerce')
        
        # Clean date: parse various formats, coerce errors to NaT
        if "date" in master.columns:
            master["date"] = pd.to_datetime(master["date"], errors='coerce')
        
        # Clean product: strip whitespace and standardize missing values
        if "product" in master.columns:
            master["product"] = master["product"].astype(str).str.strip()
            master["product"] = master["product"].replace(
                ['', 'nan', 'None', 'null', 'NULL', 'N/A', 'NA'], pd.NA
            )
        
        # Drop rows with missing critical values
        critical_cols = [c for c in ["date", "product", "price"] if c in master.columns]
        if critical_cols:
            master = master.dropna(subset=critical_cols)
    
    elif config.name == "finance":
        if "value" in master.columns:
            master["value"] = pd.to_numeric(master["value"], errors='coerce')
        if "date" in master.columns:
            master["date"] = pd.to_datetime(master["date"], errors='coerce')
        critical_cols = [c for c in ["date", "entity", "value"] if c in master.columns]
        if critical_cols:
            master = master.dropna(subset=critical_cols)
    
    elif config.name == "sensor":
        if "reading" in master.columns:
            master["reading"] = pd.to_numeric(master["reading"], errors='coerce')
        if "timestamp" in master.columns:
            master["timestamp"] = pd.to_datetime(master["timestamp"], errors='coerce')
        critical_cols = [c for c in ["timestamp", "sensor_id", "reading"] if c in master.columns]
        if critical_cols:
            master = master.dropna(subset=critical_cols)

    master.to_csv(output_path, index=False)