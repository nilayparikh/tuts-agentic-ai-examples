"""Date normalization helpers for the shipped finance fixture."""

# pyright: reportMissingImports=false, reportMissingModuleSource=false
# pylint: disable=import-error

from __future__ import annotations

import re

import pandas as pd  # type: ignore[import-not-found, import-untyped]

from cleanloop.input_loader import normalize_text


ISO_DATE_PATTERN = re.compile(r"^(\d{4})[-/](\d{2})[-/](\d{2})$")


def normalize_date(raw_date: str) -> str | None:
    """Normalize mixed finance dates into YYYY-MM-DD using day-first fallback."""
    date_text = normalize_text(raw_date)
    if not date_text:
        return None

    match = ISO_DATE_PATTERN.match(date_text)
    if match:
        year, month, day = match.groups()
        return f"{year}-{month}-{day}"

    parsed = pd.to_datetime(date_text, errors="coerce", dayfirst=True)
    if pd.isna(parsed):
        return None
    return parsed.strftime("%Y-%m-%d")
