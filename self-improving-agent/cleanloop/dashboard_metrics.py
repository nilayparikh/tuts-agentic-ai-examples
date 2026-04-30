"""Helpers for richer CleanLoop dashboard judge metrics."""

from __future__ import annotations

from datetime import datetime
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


def _int_value(value: object, default: int = 0) -> int:
    """Return one integer value with a safe default."""
    if isinstance(value, bool):
        return default
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    return default


def _llm_details(history_row: dict[str, object]) -> dict[str, object]:
    """Return normalized LLM details for one history row."""
    llm = history_row.get("llm")
    if isinstance(llm, dict):
        return llm
    return {}


def llm_token_total(history_row: dict[str, object]) -> int:
    """Return total LLM tokens, falling back to prompt plus completion tokens."""
    llm = _llm_details(history_row)
    total_tokens = _int_value(llm.get("total_tokens"))
    if total_tokens > 0:
        return total_tokens

    prompt_tokens = _int_value(llm.get("prompt_tokens"))
    completion_tokens = _int_value(llm.get("completion_tokens"))
    if prompt_tokens or completion_tokens:
        return prompt_tokens + completion_tokens

    attempts = llm.get("attempts")
    if not isinstance(attempts, list):
        return 0

    attempt_total = 0
    for attempt in attempts:
        if not isinstance(attempt, dict):
            continue
        usage_total = _attempt_usage_value(attempt, "total_tokens")
        if usage_total > 0:
            attempt_total += usage_total
            continue
        attempt_total += _attempt_usage_value(attempt, "prompt_tokens")
        attempt_total += _attempt_usage_value(attempt, "completion_tokens")
    return attempt_total


def _metacognition(history_row: dict[str, object]) -> dict[str, object]:
    """Return normalized metacognition for one history row."""
    details = history_row.get("metacognition")
    if isinstance(details, dict):
        return details
    return {}


def _score_delta(history_row: dict[str, object]) -> int:
    """Return a numeric score delta for one history row."""
    if "score_delta" in history_row:
        return _int_value(history_row.get("score_delta"))
    return _int_value(history_row.get("score")) - _int_value(
        history_row.get("before_score")
    )


def _recall_delta_percent(history_row: dict[str, object]) -> float:
    """Return after-minus-before recall delta as percentage points."""
    before_value = history_row.get("before_metrics")
    after_value = history_row.get("metrics")
    before = before_value if isinstance(before_value, dict) else None
    after = after_value if isinstance(after_value, dict) else None
    before_recall = _metric_value(before, "cleanliness_score") * 100
    after_recall = _metric_value(after, "cleanliness_score") * 100
    return round(after_recall - before_recall, 2)


def _token_efficiency_label(tokens: int, recall_delta: float) -> str | float:
    """Return a readable token efficiency label for one round."""
    if tokens <= 0:
        return "no LLM calls"
    if recall_delta <= 0:
        return "no recall gain"
    return round(tokens / recall_delta, 1)


def _operator_signal(
    action: str,
    score_delta: int,
    recall_delta: float,
    tokens: int,
    stalled_focus: bool,
) -> str:
    """Classify the round into an operator-facing signal."""
    signal = "watch"
    if stalled_focus:
        signal = "stalled focus"
    elif action == "skip":
        signal = "proposal unavailable"
    elif tokens and recall_delta <= 0:
        signal = "spend without recall gain"
    elif score_delta > 0 or recall_delta > 0:
        signal = "improving"
    elif action == "revert":
        signal = "reverted"
    elif action == "commit":
        signal = "committed"
    return signal


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
                    "Completion Tokens": _attempt_usage_value(
                        attempt, "completion_tokens"
                    ),
                    "Total Tokens": _attempt_usage_value(attempt, "total_tokens"),
                    "Diagnosis": diagnose_attempt_outcome(attempt, token_budget),
                }
            )
    return rows


def build_round_signal_rows(
    history_rows: list[dict],
    *,
    token_budget: int,
) -> list[dict[str, object]]:
    """Build per-round operator signals for focus, score, and token efficiency."""
    rows: list[dict[str, object]] = []
    for entry in history_rows:
        if not isinstance(entry, dict):
            continue
        metacognition = _metacognition(entry)
        llm = _llm_details(entry)
        action = str(entry.get("action", ""))
        score_delta = _score_delta(entry)
        recall_delta = _recall_delta_percent(entry)
        repeated_failure_count = _int_value(
            metacognition.get("repeated_failure_count"),
            default=0,
        )
        tokens = llm_token_total(entry)
        stalled_focus = repeated_failure_count > 1 and score_delta <= 0
        rows.append(
            {
                "Round": entry.get("round"),
                "Action": action,
                "Focus Area": metacognition.get("focus_area", "unknown"),
                "Repeated Failures": repeated_failure_count,
                "Stalled Focus": stalled_focus,
                "Score Delta": score_delta,
                "Recall Delta %": recall_delta,
                "Tokens": tokens,
                "Budget Used %": (
                    round((tokens / token_budget) * 100, 1) if token_budget > 0 else 0.0
                ),
                "Tokens per Recall Point": _token_efficiency_label(
                    tokens,
                    recall_delta,
                ),
                "LLM Path": llm.get("selected_attempt", "none"),
                "Operator Signal": _operator_signal(
                    action,
                    score_delta,
                    recall_delta,
                    tokens,
                    stalled_focus,
                ),
                "Guidance": metacognition.get("guidance", ""),
            }
        )
    return rows


def build_row_decision_summary_rows(
    row_decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    """Group row-decision trace records by decision outcome."""
    counts: dict[str, int] = {}
    source_files: dict[str, set[str]] = {}
    anomaly_reasons: dict[str, set[str]] = {}
    example_invoices: dict[str, list[str]] = {}
    for record in row_decisions:
        if not isinstance(record, dict):
            continue
        decision = str(record.get("decision") or "unknown")
        counts[decision] = counts.get(decision, 0) + 1
        source_file = record.get("source_file")
        if source_file:
            source_files.setdefault(decision, set()).add(str(source_file))
        anomaly_reason = record.get("anomaly_reason")
        if anomaly_reason:
            anomaly_reasons.setdefault(decision, set()).add(str(anomaly_reason))
        invoice_id = record.get("invoice_id")
        invoices = example_invoices.setdefault(decision, [])
        if invoice_id and len(invoices) < 5:
            invoices.append(str(invoice_id))

    rows: list[dict[str, object]] = []
    for decision, count in counts.items():
        rows.append(
            {
                "Decision": decision,
                "Rows": count,
                "Source Files": ", ".join(sorted(source_files.get(decision, set()))),
                "Anomaly Reasons": ", ".join(
                    sorted(anomaly_reasons.get(decision, set()))
                ),
                "Example Invoices": ", ".join(example_invoices.get(decision, [])),
            }
        )
    return sorted(rows, key=lambda row: (-_int_value(row["Rows"]), row["Decision"]))


def filter_rows_by_invoice(
    rows: list[dict[str, object]],
    invoice_id: str,
) -> list[dict[str, object]]:
    """Return trace rows matching one invoice id case-insensitively."""
    normalized_invoice = invoice_id.strip().casefold()
    if not normalized_invoice:
        return []
    matches: list[dict[str, object]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        candidate = str(row.get("invoice_id", "")).strip().casefold()
        if candidate == normalized_invoice:
            matches.append(row)
    return matches


def _as_filter_set(values: list[str] | tuple[str, ...] | None) -> set[str]:
    """Return non-empty casefolded filter values."""
    if not values:
        return set()
    return {value.strip().casefold() for value in values if value.strip()}


def _row_matches_query(row: dict[str, object], query: str) -> bool:
    """Return whether a row contains all case-insensitive query terms."""
    terms = [item for item in query.strip().casefold().split() if item]
    if not terms:
        return True
    haystack = " ".join(str(value).casefold() for value in row.values())
    return all(term in haystack for term in terms)


def filter_row_decision_rows(
    rows: list[dict[str, object]],
    *,
    query: str = "",
    decisions: list[str] | tuple[str, ...] | None = None,
    source_files: list[str] | tuple[str, ...] | None = None,
    run_instances: list[str] | tuple[str, ...] | None = None,
) -> list[dict[str, object]]:
    """Filter raw row-decision records for dashboard search controls."""
    decision_filter = _as_filter_set(decisions)
    source_filter = _as_filter_set(source_files)
    run_filter = _as_filter_set(run_instances)
    matches: list[dict[str, object]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        if (
            decision_filter
            and str(row.get("decision", "")).casefold() not in decision_filter
        ):
            continue
        if (
            source_filter
            and str(row.get("source_file", "")).casefold() not in source_filter
        ):
            continue
        if run_filter and str(row.get("run_instance", "")).casefold() not in run_filter:
            continue
        if not _row_matches_query(row, query):
            continue
        matches.append(row)
    return matches


def filter_observability_rows(
    rows: list[dict[str, object]],
    *,
    query: str = "",
    scopes: list[str] | tuple[str, ...] | None = None,
) -> list[dict[str, object]]:
    """Filter OTEL-shaped span, event, or log rows by search and scope."""
    scope_filter = _as_filter_set(scopes)
    matches: list[dict[str, object]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        if (
            scope_filter
            and str(row.get("scope_name", "")).casefold() not in scope_filter
        ):
            continue
        if not _row_matches_query(row, query):
            continue
        matches.append(row)
    return matches


def build_scope_summary_rows(
    spans: list[dict[str, object]],
    events: list[dict[str, object]],
    logs: list[dict[str, object]],
) -> list[dict[str, object]]:
    """Summarize OTEL-shaped records by instrumentation scope."""
    summary: dict[str, dict[str, object]] = {}
    for label, records in (
        ("Spans", spans),
        ("Events", events),
        ("Logs", logs),
    ):
        for record in records:
            if not isinstance(record, dict):
                continue
            scope = str(
                record.get("scope_name") or record.get("component") or "unknown"
            )
            row = summary.setdefault(
                scope,
                {
                    "Scope": scope,
                    "Spans": 0,
                    "Events": 0,
                    "Logs": 0,
                    "Components": set(),
                    "Run Instances": set(),
                },
            )
            row[label] = _int_value(row.get(label)) + 1
            component = record.get("component")
            if component:
                cast_set = row["Components"]
                if isinstance(cast_set, set):
                    cast_set.add(str(component))
            run_instance = record.get("run_instance")
            if run_instance:
                cast_set = row["Run Instances"]
                if isinstance(cast_set, set):
                    cast_set.add(str(run_instance))

    rows: list[dict[str, object]] = []
    for row in summary.values():
        components = row.get("Components")
        run_instances = row.get("Run Instances")
        rows.append(
            {
                "Scope": row["Scope"],
                "Spans": row["Spans"],
                "Events": row["Events"],
                "Logs": row["Logs"],
                "Components": (
                    ", ".join(sorted(components)) if isinstance(components, set) else ""
                ),
                "Run Instances": (
                    ", ".join(sorted(run_instances))
                    if isinstance(run_instances, set)
                    else ""
                ),
            }
        )
    return sorted(rows, key=lambda row: str(row["Scope"]))


def _parse_iso_timestamp(value: object) -> datetime | None:
    """Parse one ISO timestamp from an OTEL-shaped record."""
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _record_name(record: dict[str, object], kind: str) -> str:
    """Return a compact trace timeline label for one record."""
    for key in ("name", "body", "stage", "decision"):
        value = record.get(key)
        if value:
            return str(value)
    return kind


def _record_matches_value(record: dict[str, object], key: str, value: str) -> bool:
    """Return whether a record key matches a non-empty string value."""
    if not value.strip():
        return True
    return str(record.get(key, "")).strip().casefold() == value.strip().casefold()


def _record_duration_ms(record: dict[str, object]) -> float:
    """Return span duration in milliseconds, or a visible default."""
    started_at = _parse_iso_timestamp(record.get("start_time"))
    finished_at = _parse_iso_timestamp(record.get("end_time"))
    if started_at is not None and finished_at is not None:
        duration = (finished_at - started_at).total_seconds() * 1000
        if duration > 0:
            return round(duration, 2)
    return 1.25


def build_trace_timeline_rows(
    spans: list[dict[str, object]],
    events: list[dict[str, object]],
    logs: list[dict[str, object]],
    *,
    trace_id: str = "",
    invoice_id: str = "",
    limit: int = 80,
) -> list[dict[str, object]]:
    """Build waterfall rows for one trace id or invoice id."""
    records: list[tuple[str, dict[str, object]]] = []
    for kind, source_rows in (
        ("span", spans),
        ("event", events),
        ("log", logs),
    ):
        for record in source_rows:
            if not isinstance(record, dict):
                continue
            if not _record_matches_value(record, "trace_id", trace_id):
                continue
            if not _record_matches_value(record, "invoice_id", invoice_id):
                continue
            records.append((kind, record))

    records.sort(
        key=lambda item: (
            str(item[1].get("timestamp", "")),
            {"span": 0, "event": 1, "log": 2}.get(item[0], 9),
            str(item[1].get("span_id", "")),
        )
    )
    records = records[: max(limit, 1)]

    rows: list[dict[str, object]] = []
    total_steps = max(len(records), 1)
    total_ms = max(total_steps * 2.5, 2.5)
    for index, (kind, record) in enumerate(records):
        offset_ms = round(index * 2.5, 2)
        duration_ms = _record_duration_ms(record) if kind == "span" else 0.75
        left_percent = round((offset_ms / total_ms) * 100, 2)
        width_percent = max(round((duration_ms / total_ms) * 100, 2), 3.5)
        rows.append(
            {
                "Step": index + 1,
                "Kind": kind,
                "Scope": record.get("scope_name", "unknown"),
                "Name": _record_name(record, kind),
                "Stage": record.get("stage", ""),
                "Decision": record.get("decision", ""),
                "Trace ID": record.get("trace_id", ""),
                "Span ID": record.get("span_id", ""),
                "Parent Span ID": record.get("parent_span_id", ""),
                "Invoice": record.get("invoice_id", ""),
                "Source File": record.get("source_file", ""),
                "Timestamp": record.get("timestamp", ""),
                "Offset ms": offset_ms,
                "Duration ms": duration_ms,
                "Left %": min(left_percent, 96.5),
                "Width %": min(width_percent, 100 - min(left_percent, 96.5)),
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
