"""Mutation-playbook helpers for the shipped finance fixture."""

from __future__ import annotations

import re
from typing import cast

from cleanloop.dataset_contract import MUTATION_RULES
from cleanloop.date_normalizer import normalize_date
from cleanloop.input_loader import normalize_text


NUMBER_PATTERN = re.compile(r"^-?\d+(?:\.\d+)?$")
TOKEN_WORD_PATTERN = re.compile(r"[^A-Z0-9]+")
BLANK_CANCELLED_TOKEN = "BLANK_CANCELLED_OR_VOID"
RESOLUTION_AMOUNT_TOKEN = "RESOLUTION_AMOUNT"
TOKEN_ALIASES = {
    "TRIAL FREE": "FREE TRIAL",
    "FREE TRIAL": "FREE TRIAL",
    "OFFSET ZERO": "OFFSET",
    "ZERO OFFSET": "OFFSET",
    "HOLD FX": "FX HOLD",
}


def strip_currency_tokens(amount_text: str, currency_text: str) -> str:
    """Remove known currency markers and formatting characters from an amount string."""
    cleaned = amount_text.upper()
    for token in {currency_text, "USD", "EUR", "GBP", "AUD", "CHF", "$", "€", "£"}:
        if token:
            cleaned = cleaned.replace(token, "")
    cleaned = cleaned.replace(",", "")
    cleaned = cleaned.replace("CR", "")
    cleaned = cleaned.replace(" ", "")
    return cleaned.strip()


def canonicalize_amount_token(amount_text: str) -> str:
    """Collapse noisy textual amount labels into stable mutation-playbook tokens."""
    token = TOKEN_WORD_PATTERN.sub(" ", amount_text.upper())
    token = " ".join(token.split())
    return TOKEN_ALIASES.get(token, token)


def normalize_adjusted_amount(record: dict[str, str]) -> str | None:
    """Read the approved adjusted amount when the mutation playbook needs it."""
    if record.get("approval_flag", "") != "approved":
        return None

    adjusted_amount = normalize_text(record.get("adjusted_amount", ""))
    if not adjusted_amount:
        return None

    cleaned = strip_currency_tokens(adjusted_amount, record.get("currency", ""))
    if not NUMBER_PATTERN.match(cleaned):
        return None
    return str(float(cleaned))


def normalize_resolution_amount(record: dict[str, str]) -> str | None:
    """Read the approved resolution amount for investigated anomaly rows."""
    if record.get("resolution_flag", "") != "approved":
        return None

    resolution_amount = normalize_text(record.get("resolution_amount", ""))
    if not resolution_amount:
        return None

    cleaned = strip_currency_tokens(resolution_amount, record.get("currency", ""))
    if not NUMBER_PATTERN.match(cleaned):
        return None
    return str(float(cleaned))


def resolve_mutation_rule(record: dict[str, str]) -> dict[str, str] | None:
    """Resolve token-based or contextual mutation rules for one finance row."""
    raw_amount = normalize_text(record["raw_amount"])
    token = canonicalize_amount_token(raw_amount)
    if token:
        direct_rule = MUTATION_RULES.get(token)
        if direct_rule is not None:
            return cast(dict[str, str], direct_rule)

        if normalize_resolution_amount(record) is not None:
            return cast(
                dict[str, str] | None, MUTATION_RULES.get(RESOLUTION_AMOUNT_TOKEN)
            )
        return None

    blank_rule = MUTATION_RULES.get(BLANK_CANCELLED_TOKEN)
    if blank_rule is None:
        if normalize_resolution_amount(record) is not None:
            return cast(
                dict[str, str] | None, MUTATION_RULES.get(RESOLUTION_AMOUNT_TOKEN)
            )
        return None

    statuses = cast(tuple[str, ...], blank_rule.get("statuses", ()))
    if record.get("status", "") in statuses:
        return cast(dict[str, str], blank_rule)
    if normalize_resolution_amount(record) is not None:
        return cast(dict[str, str] | None, MUTATION_RULES.get(RESOLUTION_AMOUNT_TOKEN))
    return None


def normalize_numeric_amount(record: dict[str, str]) -> tuple[str | None, str | None]:
    """Normalize one amount when the token is already numeric-like."""
    amount_text = normalize_text(record["raw_amount"])
    if not amount_text:
        if resolve_mutation_rule(record) is not None:
            return None, "requires_mutation_playbook"
        return None, "missing_amount"

    if MUTATION_RULES.get(canonicalize_amount_token(amount_text)) is not None:
        return None, "requires_mutation_playbook"

    cleaned = strip_currency_tokens(amount_text, record["currency"])
    if NUMBER_PATTERN.match(cleaned):
        return str(float(cleaned)), None

    if resolve_mutation_rule(record) is not None:
        return None, "requires_mutation_playbook"

    return None, "unmapped_amount_token"


def build_normalized_row(record: dict[str, str], value: str) -> dict[str, str] | None:
    """Build one canonical finance row when core fields are available."""
    date_value = normalize_date(record["raw_date"])
    entity = normalize_text(record["customer"])
    currency = normalize_text(record["currency"]).upper()
    category = normalize_text(record["status"]).lower()
    if not date_value or not entity or not category:
        return None
    return {
        "date": date_value,
        "entity": entity,
        "currency": currency,
        "value": value,
        "category": category,
    }


def apply_mutation_playbook(
    record: dict[str, str],
) -> tuple[dict[str, str] | None, str, str]:
    """Apply the anomaly playbook for textual finance amounts."""
    rule = resolve_mutation_rule(record)
    if rule is None:
        return (
            None,
            "unmapped_amount_token",
            "No shipped mutation rule matches this token.",
        )

    strategy = rule.get("strategy", "zero_value")
    if strategy == "adjusted_amount":
        repaired_value = normalize_adjusted_amount(record)
        if repaired_value is None:
            return None, "missing_adjusted_amount", rule["mutation_hint"]
    elif strategy == "resolution_amount":
        repaired_value = normalize_resolution_amount(record)
        if repaired_value is None:
            return None, "missing_resolution_amount", rule["mutation_hint"]
    else:
        repaired_value = "0.0"

    row = build_normalized_row(record, repaired_value)
    if row is None:
        return (
            None,
            "unparseable_date",
            "Normalize the date before applying the mutation rule.",
        )
    return row, "mutation_fixed", rule["mutation_hint"]


def build_failure_row(
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
