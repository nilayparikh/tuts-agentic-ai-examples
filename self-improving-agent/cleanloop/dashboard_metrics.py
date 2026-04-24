"""Helpers for richer CleanLoop dashboard judge metrics."""

from __future__ import annotations

from difflib import unified_diff


def _attempt_usage_value(attempt: dict[str, object], key: str) -> int:
    """Return one numeric usage field for an LLM attempt."""
    usage = attempt.get("usage") if isinstance(attempt, dict) else None
    if not isinstance(usage, dict):
        return 0
    value = usage.get(key, 0)
    if isinstance(value, int):
        return value
    return 0


def _metric_value(metrics: dict[str, object] | None, key: str) -> float:
    """Return one numeric metric value with a zero default."""
    if not isinstance(metrics, dict):
        return 0.0
    value = metrics.get(key, 0)
    if isinstance(value, (int, float)):
        return float(value)
    return 0.0


def latest_judge_metrics(history_rows: list[dict]) -> dict[str, float]:
    """Return the most recent after-metrics snapshot for sidebar summaries."""
    if not history_rows:
        return {}
    latest = history_rows[-1].get("metrics")
    if not isinstance(latest, dict):
        return {}
    return {
        "cleanliness_score": _metric_value(latest, "cleanliness_score"),
        "output_precision": _metric_value(latest, "output_precision"),
        "matched_rows": _metric_value(latest, "matched_rows"),
        "missing_rows": _metric_value(latest, "missing_rows"),
        "unexpected_rows": _metric_value(latest, "unexpected_rows"),
        "reference_rows": _metric_value(latest, "reference_rows"),
        "output_rows": _metric_value(latest, "output_rows"),
    }


def build_judge_metric_rows(history_rows: list[dict]) -> list[dict[str, object]]:
    """Build per-round dashboard rows for recall, precision, and row-gap deltas."""
    rows: list[dict[str, object]] = []
    for entry in history_rows:
        before = entry.get("before_metrics") if isinstance(entry, dict) else {}
        after = entry.get("metrics") if isinstance(entry, dict) else {}

        before_recall = _metric_value(before, "cleanliness_score") * 100
        after_recall = _metric_value(after, "cleanliness_score") * 100
        before_precision = _metric_value(before, "output_precision") * 100
        after_precision = _metric_value(after, "output_precision") * 100
        before_missing = int(_metric_value(before, "missing_rows"))
        after_missing = int(_metric_value(after, "missing_rows"))
        before_unexpected = int(_metric_value(before, "unexpected_rows"))
        after_unexpected = int(_metric_value(after, "unexpected_rows"))

        rows.append(
            {
                "Round": entry.get("round"),
                "Action": entry.get("action", ""),
                "Before Recall %": round(before_recall, 2),
                "After Recall %": round(after_recall, 2),
                "Recall Delta %": round(after_recall - before_recall, 2),
                "Before Precision %": round(before_precision, 2),
                "After Precision %": round(after_precision, 2),
                "Precision Delta %": round(after_precision - before_precision, 2),
                "Matched Rows": int(_metric_value(after, "matched_rows")),
                "Reference Rows": int(_metric_value(after, "reference_rows")),
                "Output Rows": int(_metric_value(after, "output_rows")),
                "Missing Rows": after_missing,
                "Missing Rows Delta": after_missing - before_missing,
                "Unexpected Rows": after_unexpected,
                "Unexpected Rows Delta": after_unexpected - before_unexpected,
            }
        )
    return rows


def diagnose_attempt_outcome(attempt: dict[str, object], token_budget: int) -> str:
    """Explain the most likely outcome for one recorded LLM attempt."""
    if attempt.get("code_found"):
        return "returned code"

    response_chars = attempt.get("response_chars", 0)
    if not isinstance(response_chars, int):
        response_chars = 0

    completion_tokens = _attempt_usage_value(attempt, "completion_tokens")
    configured_budget = attempt.get("max_tokens", token_budget)
    if not isinstance(configured_budget, int):
        configured_budget = token_budget
    if response_chars == 0 and completion_tokens >= configured_budget:
        return "token budget exhausted before code output"
    if response_chars == 0:
        return "empty response without code"
    return "response contained no extractable code"


def build_attempt_outcome_rows(
    history_rows: list[dict],
    *,
    token_budget: int,
) -> list[dict[str, object]]:
    """Flatten LLM attempts into dashboard rows with operator-facing diagnoses."""
    rows: list[dict[str, object]] = []
    for entry in history_rows:
        llm = entry.get("llm") if isinstance(entry, dict) else None
        if not isinstance(llm, dict):
            continue
        for attempt in llm.get("attempts", []):
            if not isinstance(attempt, dict):
                continue
            rows.append(
                {
                    "Round": entry.get("round"),
                    "Label": attempt.get("label", ""),
                    "Code Found": attempt.get("code_found", False),
                    "Completion Tokens": _attempt_usage_value(attempt, "completion_tokens"),
                    "Total Tokens": _attempt_usage_value(attempt, "total_tokens"),
                    "Diagnosis": diagnose_attempt_outcome(attempt, token_budget),
                }
            )
    return rows


def build_log_rows(history_rows: list[dict]) -> list[dict[str, object]]:
    """Flatten structured round logs into dashboard table rows."""
    rows: list[dict[str, object]] = []
    for entry in history_rows:
        logs = entry.get("logs") if isinstance(entry, dict) else None
        if not isinstance(logs, list):
            continue
        for log in logs:
            if not isinstance(log, dict):
                continue
            rows.append(
                {
                    "Round": entry.get("round"),
                    "Tag": log.get("tag"),
                    "Message": log.get("message"),
                    "Prompt Tokens": log.get("prompt_tokens"),
                    "Completion Tokens": log.get("completion_tokens"),
                    "Total Tokens": log.get("total_tokens"),
                }
            )
    return rows


def build_mutation_diff(before_code: object, after_code: object) -> str:
    """Render one unified diff between the previous and candidate genome source."""
    if not isinstance(before_code, str) or not isinstance(after_code, str):
        return "No code change recorded."
    if before_code == after_code:
        return "No code change recorded."

    diff_lines = unified_diff(
        before_code.splitlines(),
        after_code.splitlines(),
        fromfile="before/clean_data.py",
        tofile="after/clean_data.py",
        lineterm="",
    )
    rendered = "\n".join(diff_lines)
    return rendered or "No code change recorded."


def build_mutation_diff_rows(history_rows: list[dict]) -> list[dict[str, object]]:
    """Build one dashboard row per round with the mutable-genome diff."""
    rows: list[dict[str, object]] = []
    for entry in history_rows:
        rows.append(
            {
                "Round": entry.get("round"),
                "Action": entry.get("action", ""),
                "Hypothesis": entry.get("hypothesis", ""),
                "Diff": build_mutation_diff(
                    entry.get("genome_before"),
                    entry.get("genome_after"),
                ),
            }
        )
    return rows