"""Shared finance cleaning runtime for the CleanLoop starter and mutable genome."""

from __future__ import annotations

import csv
import re
from pathlib import Path

import pandas as pd

from cleanloop import datasets as cleanloop_datasets


FINANCE_COLUMNS = ("date", "entity", "value", "category")
FAILURE_COLUMNS = (
    "source_file",
    "invoice_id",
    "customer",
    "raw_date",
    "raw_amount",
    "currency",
    "status",
    "anomaly_reason",
    "mutation_hint",
)
MUTATION_ZERO_TOKENS = {
    "FREE TRIAL": "Map the promotional invoice to 0.0 and preserve the status.",
    "COMPLIMENTARY": "Map the complimentary invoice to 0.0 and preserve the status.",
    "OFFSET": "Map the offset entry to 0.0 and preserve the status.",
}
NUMBER_PATTERN = re.compile(r"^-?\d+(?:\.\d+)?$")
ISO_DATE_PATTERN = re.compile(r"^(\d{4})[-/](\d{2})[-/](\d{2})$")


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


def _normalize_text(value: object) -> str:
    """Convert raw scalars to trimmed strings without crashing on NaN."""
    if pd.isna(value):
        return ""
    return str(value).strip()


def _read_finance_records(csv_file: Path) -> list[dict[str, str]]:
    """Read one finance CSV file into raw records with source metadata."""
    rows = _read_csv_rows(csv_file)
    if not rows:
        return []

    header = rows[0]
    body = rows[1:]
    records: list[dict[str, str]] = []
    for row in body:
        rebuilt = _reshape_finance_row(row, len(header))
        raw = dict(zip(header, rebuilt))
        records.append(
            {
                "source_file": csv_file.name,
                "invoice_id": _normalize_text(raw.get("invoice_id", "")),
                "customer": _normalize_text(raw.get("customer", "")),
                "raw_date": _normalize_text(raw.get("issued", "")),
                "raw_amount": _normalize_text(raw.get("amount", "")),
                "currency": _normalize_text(raw.get("currency", "")).upper(),
                "status": _normalize_text(raw.get("status", csv_file.stem)).lower(),
            }
        )
    return records


def _normalize_date(raw_date: str) -> str | None:
    """Normalize mixed finance dates into YYYY-MM-DD using the arena's day-first rules."""
    date_text = _normalize_text(raw_date)
    if not date_text:
        return None

    match = ISO_DATE_PATTERN.match(date_text)
    if match:
        year, month, day = match.groups()
        if int(day) <= 12:
            return f"{year}-{day}-{month}"
        return f"{year}-{month}-{day}"

    parsed = pd.to_datetime(date_text, errors="coerce", dayfirst=True)
    if pd.isna(parsed):
        return None
    return parsed.strftime("%Y-%m-%d")


def _strip_currency_tokens(amount_text: str, currency_text: str) -> str:
    """Remove known currency markers and formatting characters from an amount string."""
    cleaned = amount_text.upper()
    for token in {currency_text, "USD", "EUR", "GBP", "AUD", "CHF", "$", "€", "£"}:
        if token:
            cleaned = cleaned.replace(token, "")
    cleaned = cleaned.replace(",", "")
    cleaned = cleaned.replace("CR", "")
    cleaned = cleaned.replace(" ", "")
    return cleaned.strip()


def _normalize_numeric_amount(
    raw_amount: str,
    currency_text: str,
) -> tuple[str | None, str | None]:
    """Normalize one amount when the token is already numeric-like."""
    amount_text = _normalize_text(raw_amount)
    if not amount_text:
        return None, "missing_amount"

    if amount_text.upper() in MUTATION_ZERO_TOKENS:
        return None, "requires_mutation_playbook"

    cleaned = _strip_currency_tokens(amount_text, currency_text)
    if not NUMBER_PATTERN.match(cleaned):
        return None, "unmapped_amount_token"

    return str(float(cleaned)), None


def _build_normalized_row(record: dict[str, str], value: str) -> dict[str, str] | None:
    """Build one canonical finance row when core fields are available."""
    date_value = _normalize_date(record["raw_date"])
    entity = _normalize_text(record["customer"])
    category = _normalize_text(record["status"]).lower()
    if not date_value:
        return None
    if not entity:
        return None
    if not category:
        return None
    return {
        "date": date_value,
        "entity": entity,
        "value": value,
        "category": category,
    }


def _apply_mutation_playbook(
    record: dict[str, str],
) -> tuple[dict[str, str] | None, str, str]:
    """Apply the anomaly playbook for textual finance amounts."""
    raw_amount = _normalize_text(record["raw_amount"])
    token = raw_amount.upper()
    if token not in MUTATION_ZERO_TOKENS:
        return (
            None,
            "unmapped_amount_token",
            "No shipped mutation rule matches this token.",
        )

    row = _build_normalized_row(record, "0.0")
    if row is None:
        return (
            None,
            "unparseable_date",
            "Normalize the date before applying the mutation rule.",
        )
    return row, "mutation_fixed", MUTATION_ZERO_TOKENS[token]


def _build_failure_row(
    record: dict[str, str],
    anomaly_reason: str,
    mutation_hint: str,
) -> dict[str, str]:
    """Capture one unshipped anomaly for mutation-failure review."""
    return {
        "source_file": record["source_file"],
        "invoice_id": record["invoice_id"],
        "customer": record["customer"],
        "raw_date": record["raw_date"],
        "raw_amount": record["raw_amount"],
        "currency": record["currency"],
        "status": record["status"],
        "anomaly_reason": anomaly_reason,
        "mutation_hint": mutation_hint,
    }


def _write_rows(
    output_path: Path,
    rows: list[dict[str, str]],
    columns: tuple[str, ...],
) -> None:
    """Write rows to CSV using a stable column order."""
    frame = pd.DataFrame(rows, columns=list(columns))
    if not frame.empty and tuple(columns) == FINANCE_COLUMNS:
        frame = frame.sort_values(by=["date", "entity"], kind="stable")
    elif not frame.empty:
        frame = frame.sort_values(by=["source_file", "invoice_id"], kind="stable")
    frame.to_csv(output_path, index=False)


def clean(input_dir: Path, output_path: Path) -> None:
    """Run the deterministic stage first, then the mutation fallback exports."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    config = cleanloop_datasets.get_dataset_config()
    success_path = cleanloop_datasets.get_mutation_success_path(output_path.parent)
    failure_path = cleanloop_datasets.get_mutation_failures_path(output_path.parent)

    deterministic_rows: list[dict[str, str]] = []
    mutation_rows: list[dict[str, str]] = []
    failure_rows: list[dict[str, str]] = []

    for csv_file in cleanloop_datasets.get_input_paths(input_dir):
        for record in _read_finance_records(csv_file):
            value, anomaly_reason = _normalize_numeric_amount(
                record["raw_amount"],
                record["currency"],
            )
            if value is not None:
                row = _build_normalized_row(record, value)
                if row is not None:
                    deterministic_rows.append(row)
                    continue
                failure_rows.append(
                    _build_failure_row(
                        record,
                        "unparseable_date",
                        "Normalize the issued date before exporting the canonical row.",
                    )
                )
                continue

            mutated_row, mutation_reason, mutation_hint = _apply_mutation_playbook(
                record
            )
            if mutated_row is not None:
                mutation_rows.append(mutated_row)
                continue

            failure_rows.append(
                _build_failure_row(
                    record,
                    anomaly_reason or mutation_reason,
                    mutation_hint,
                )
            )

    master_rows = deterministic_rows + mutation_rows
    _write_rows(output_path, master_rows, config.required_columns)
    _write_rows(success_path, mutation_rows, config.required_columns)
    _write_rows(failure_path, failure_rows, FAILURE_COLUMNS)
