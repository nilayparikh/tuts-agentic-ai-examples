"""dashboard.py — Streamlit monitoring dashboard.

Tabbed dashboard that visualizes the self-improving loop in
real time. Reads the dataset-specific history log to show
iteration-by-iteration progress.

Course alignment:
    - Lesson 04: loop observability and operator feedback

Usage:
    streamlit run cleanloop/dashboard.py

Reads from:
    cleanloop/.output/<dataset>_eval_history.json   — loop iteration results
    cleanloop/clean_data.py                         — current genome source
    git log                                         — commit history
"""

# pyright: reportMissingImports=false, reportMissingModuleSource=false
# pylint: disable=too-many-lines
import html
import sys
from pathlib import Path

import pandas as pd  # type: ignore[import-not-found, import-untyped]
import streamlit as st  # type: ignore[import-not-found]

# ─── PATHS ────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from cleanloop import datasets as cleanloop_datasets  # noqa: E402
from cleanloop import dashboard_artifacts  # noqa: E402
from cleanloop import dashboard_metrics  # noqa: E402
from cleanloop.history_store import load_history as load_history_file  # noqa: E402

OUTPUT_DIR = PROJECT_ROOT / "cleanloop" / ".output"
DATASET_CONFIG = cleanloop_datasets.get_dataset_config()


def _layout_css() -> str:
    """Return dashboard CSS that follows Streamlit's active theme."""
    return """
    <style>
    .block-container {
        max-width: 1460px;
        padding-top: 1.4rem;
    }
    [data-testid="stMetric"] {
        background: var(--secondary-background-color);
        border: 1px solid rgba(120, 130, 150, 0.28);
        border-radius: 8px;
        padding: 0.8rem 0.95rem;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.05);
    }
    [data-testid="stMetricLabel"] p {
        font-size: 0.78rem;
        letter-spacing: 0;
    }
    [data-testid="stMetricValue"] {
        white-space: normal;
        overflow-wrap: anywhere;
    }
    [data-testid="stMetricValue"] div {
        font-size: 1.55rem;
        line-height: 1.2;
    }
    section[data-testid="stSidebar"] [data-testid="stMetricValue"] div {
        font-size: 1.45rem;
    }
    div[data-testid="stDataFrame"] {
        border: 1px solid rgba(120, 130, 150, 0.24);
        border-radius: 8px;
        overflow: hidden;
    }
    .cleanloop-panel {
        background: var(--secondary-background-color);
        border: 1px solid rgba(120, 130, 150, 0.24);
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .cleanloop-signal {
        color: var(--primary-color);
        font-weight: 650;
    }
    .trace-shell {
        border: 1px solid rgba(120, 130, 150, 0.28);
        border-radius: 8px;
        background: var(--secondary-background-color);
        padding: 0.9rem 1rem 1rem;
        margin: 0.4rem 0 1rem;
    }
    .trace-header {
        display: flex;
        justify-content: space-between;
        gap: 1rem;
        font-weight: 650;
        margin-bottom: 0.75rem;
    }
    .trace-row {
        display: grid;
        grid-template-columns: minmax(220px, 30%) 1fr 70px;
        gap: 0.8rem;
        align-items: center;
        min-height: 34px;
        border-top: 1px solid rgba(120, 130, 150, 0.16);
    }
    .trace-row:first-of-type {
        border-top: 0;
    }
    .trace-label {
        overflow-wrap: anywhere;
        font-size: 0.84rem;
        line-height: 1.2;
    }
    .trace-meta {
        opacity: 0.72;
        font-size: 0.72rem;
    }
    .trace-lane {
        position: relative;
        height: 14px;
        border-left: 1px solid rgba(120, 130, 150, 0.3);
        border-right: 1px solid rgba(120, 130, 150, 0.3);
        background: linear-gradient(
            90deg,
            rgba(120, 130, 150, 0.16) 0,
            rgba(120, 130, 150, 0.16) 1px,
            transparent 1px,
            transparent 20%
        );
        background-size: 20% 100%;
    }
    .trace-bar {
        position: absolute;
        top: 2px;
        height: 10px;
        border-radius: 3px;
        min-width: 7px;
    }
    .trace-span { background: #3b82f6; }
    .trace-event { background: #10b981; }
    .trace-log { background: #f59e0b; }
    .trace-duration {
        text-align: right;
        font-variant-numeric: tabular-nums;
        font-size: 0.78rem;
        opacity: 0.85;
    }
    </style>
    """


# =====================================================================
# SECTION: Streamlit Page Configuration
# Lesson 04 — Use a wide layout so the operator can compare history,
# failures, artifacts, and the current genome without losing context.
# set_page_config must be the first Streamlit command.
# =====================================================================

st.set_page_config(
    page_title="CleanLoop Dashboard",
    page_icon="",
    layout="wide",
)
RUN_SUMMARIES = dashboard_artifacts.list_run_summaries(OUTPUT_DIR)
RUN_OPTIONS = [
    "Current artifacts",
    *[str(row["Run Instance"]) for row in RUN_SUMMARIES],
]
DEFAULT_RUN_INDEX = 1 if RUN_SUMMARIES else 0
SELECTED_RUN_LABEL = st.sidebar.selectbox(
    "Run Instance",
    RUN_OPTIONS,
    index=DEFAULT_RUN_INDEX,
)
SELECTED_RUN_INSTANCE = (
    None if SELECTED_RUN_LABEL == "Current artifacts" else SELECTED_RUN_LABEL
)
ACTIVE_PATHS = dashboard_artifacts.get_dashboard_artifact_paths(
    OUTPUT_DIR,
    DATASET_CONFIG.name,
    SELECTED_RUN_INSTANCE,
)
HISTORY_PATH = ACTIVE_PATHS["history"]
OUTPUT_CSV = ACTIVE_PATHS["output_csv"]
EXPORTED_LOGS_PATH = ACTIVE_PATHS["exported_logs"]
MUTATION_SUCCESS_PATH = ACTIVE_PATHS["mutation_success"]
MUTATION_FAILURES_PATH = ACTIVE_PATHS["mutation_failures"]

st.markdown(_layout_css(), unsafe_allow_html=True)
st.title(f"CleanLoop - {DATASET_CONFIG.label} Dashboard")
st.caption(f"Selected dataset: {DATASET_CONFIG.name} | Run: {SELECTED_RUN_LABEL}")

INPUT_DIR = PROJECT_ROOT / "cleanloop" / ".input"
ATTEMPT_TOKEN_BUDGET = 2200


def load_history() -> list[dict]:
    """Load eval history from the JSON log file."""
    return load_history_file(HISTORY_PATH)


def _llm_info(history_row: dict) -> dict:
    """Return normalized LLM diagnostics for one history entry."""
    llm_details = history_row.get("llm")
    if isinstance(llm_details, dict):
        return llm_details
    return {
        "selected_attempt": "none",
        "attempts": [],
        "prompt_tokens": None,
        "completion_tokens": None,
        "total_tokens": None,
    }


def _blueprint_rows(history_rows: list[dict]) -> list[dict[str, object]]:
    """Build a compact per-round blueprint table."""
    rows: list[dict[str, object]] = []
    judge_rows = dashboard_metrics.build_judge_metric_rows(history_rows)
    signal_rows = dashboard_metrics.build_round_signal_rows(
        history_rows,
        token_budget=ATTEMPT_TOKEN_BUDGET,
    )
    for history_row, judge_row, signal_row in zip(
        history_rows,
        judge_rows,
        signal_rows,
    ):
        llm_details = _llm_info(history_row)
        before_score = history_row.get(
            "before_score",
            history_row.get("score", "?"),
        )
        score = history_row.get("score", "?")
        total = history_row.get("total", "?")
        rows.append(
            {
                "Round": history_row.get("round"),
                "Action": history_row.get("action", ""),
                "Before": f"{before_score}/{total}",
                "After": f"{score}/{total}",
                "Delta": history_row.get("score_delta", 0),
                "Focus Area": signal_row.get("Focus Area"),
                "Signal": signal_row.get("Operator Signal"),
                "LLM Path": llm_details.get("selected_attempt", "none"),
                "Tokens": signal_row.get("Tokens"),
                "Token Efficiency": signal_row.get("Tokens per Recall Point"),
                "Recall %": judge_row.get("After Recall %"),
                "Precision %": judge_row.get("After Precision %"),
                "Missing": judge_row.get("Missing Rows"),
                "Unexpected": judge_row.get("Unexpected Rows"),
                "Hypothesis": history_row.get("hypothesis", ""),
                "Started": history_row.get("started_at", ""),
                "Finished": history_row.get("finished_at", ""),
            }
        )
    return rows


def _attempt_rows(history_rows: list[dict]) -> list[dict[str, object]]:
    """Flatten all LLM attempts across rounds for diagnostics tables."""
    rows: list[dict[str, object]] = []
    for history_row in history_rows:
        llm_details = _llm_info(history_row)
        for attempt_row in llm_details.get("attempts", []):
            usage = (
                attempt_row.get("usage", {}) if isinstance(attempt_row, dict) else {}
            )
            rows.append(
                {
                    "Round": history_row.get("round"),
                    "Label": attempt_row.get("label"),
                    "Model": attempt_row.get("model"),
                    "Code Found": attempt_row.get("code_found"),
                    "Prompt Tokens": usage.get("prompt_tokens"),
                    "Completion Tokens": usage.get("completion_tokens"),
                    "Total Tokens": usage.get("total_tokens"),
                    "Prompt Chars": attempt_row.get("prompt_chars"),
                    "Response Chars": attempt_row.get("response_chars"),
                    "Hypothesis": attempt_row.get("hypothesis"),
                }
            )
    return rows


def _total_tokens(history_rows: list[dict]) -> int:
    """Sum total LLM tokens across all rounds when available."""
    total = 0
    for history_row in history_rows:
        total += dashboard_metrics.llm_token_total(history_row)
    return total


def _artifact_status_counts(rows: list[dict[str, object]]) -> tuple[int, int]:
    """Return present and missing artifact counts."""
    present = sum(1 for row in rows if row.get("Status") == "present")
    missing = sum(1 for row in rows if row.get("Status") == "missing")
    return present, missing


def _readable_label(value: object) -> str:
    """Return a compact label for dashboard display."""
    text = str(value or "unknown").strip()
    return text.replace("_", " ") if text else "unknown"


def _display_project_path(value: object) -> str:
    """Render artifact paths relative to the example root when possible."""
    try:
        path = Path(str(value))
        return path.relative_to(PROJECT_ROOT).as_posix()
    except (OSError, ValueError):
        return str(value).replace("\\", "/")


def _latest_strategy(history_rows: list[dict], strategy: dict[str, object]) -> dict:
    """Return latest metacognition, preferring history over strategy file."""
    if history_rows:
        metacognition = history_rows[-1].get("metacognition")
        if isinstance(metacognition, dict):
            return metacognition
    return strategy


def _read_invoice_rows(path: Path, invoice_id: str) -> list[dict[str, object]]:
    """Read rows matching an invoice id from one CSV file."""
    if not path.exists() or not invoice_id.strip():
        return []
    try:
        frame = pd.read_csv(path, dtype=str)
    except (
        OSError,
        ValueError,
        pd.errors.ParserError,
        pd.errors.EmptyDataError,
    ):
        return []
    if "invoice_id" not in frame.columns:
        return []
    matches = frame[
        frame["invoice_id"].fillna("").str.casefold() == invoice_id.strip().casefold()
    ]
    rows = matches.to_dict(orient="records")
    for row in rows:
        row["_artifact"] = path.name
    return rows


def _load_invoice_artifact_rows(invoice_id: str) -> list[dict[str, object]]:
    """Load matching invoice rows from input and mutation sidecar artifacts."""
    rows: list[dict[str, object]] = []
    for input_path in cleanloop_datasets.get_input_paths(
        INPUT_DIR, DATASET_CONFIG.name
    ):
        rows.extend(_read_invoice_rows(input_path, invoice_id))
    rows.extend(_read_invoice_rows(MUTATION_SUCCESS_PATH, invoice_id))
    rows.extend(_read_invoice_rows(MUTATION_FAILURES_PATH, invoice_id))
    return rows


def _default_invoice_id(row_decisions: list[dict[str, object]]) -> str:
    """Pick a useful default invoice id for drill-down."""
    for row in row_decisions:
        if row.get("decision") != "deterministic_row" and row.get("invoice_id"):
            return str(row["invoice_id"])
    for row in row_decisions:
        if row.get("invoice_id"):
            return str(row["invoice_id"])
    return ""


def _unique_values(table_rows: list[dict[str, object]], key: str) -> list[str]:
    """Return sorted non-empty values for a table filter."""
    values = {str(row.get(key, "")).strip() for row in table_rows if row.get(key)}
    return sorted(value for value in values if value)


def _select_columns(
    table_rows: list[dict[str, object]],
    preferred_columns: list[str],
) -> pd.DataFrame:
    """Return a dataframe with preferred columns first and all other columns after."""
    frame = pd.DataFrame(table_rows)
    if frame.empty:
        return frame
    ordered = [column for column in preferred_columns if column in frame.columns]
    remainder = [column for column in frame.columns if column not in ordered]
    return frame[ordered + remainder]


def _trace_option_label(trace_id: str, trace_records: list[dict[str, object]]) -> str:
    """Return a readable label for a trace sample selector."""
    invoices = sorted(
        {
            str(record.get("invoice_id"))
            for record in trace_records
            if record.get("trace_id") == trace_id and record.get("invoice_id")
        }
    )
    scopes = sorted(
        {
            str(record.get("scope_name"))
            for record in trace_records
            if record.get("trace_id") == trace_id and record.get("scope_name")
        }
    )
    invoice_label = invoices[0] if invoices else "no invoice"
    scope_label = scopes[0].replace("cleanloop.", "") if scopes else "unknown scope"
    return f"{trace_id[:12]} | {invoice_label} | {scope_label}"


def _bar_class(kind: object) -> str:
    """Return the CSS class for one trace timeline bar."""
    normalized = str(kind or "").strip().casefold()
    if normalized == "event":
        return "trace-event"
    if normalized == "log":
        return "trace-log"
    return "trace-span"


def _safe_float(value: object, default: float = 0.0) -> float:
    """Convert a dashboard cell value to float for timeline layout."""
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return default
    return default


def _render_trace_timeline(rows: list[dict[str, object]], heading: str) -> None:
    """Render a compact waterfall timeline for trace rows."""
    if not rows:
        st.info("No trace records matched the selected trace sample.")
        return

    max_offset = max(_safe_float(row.get("Offset ms", 0.0)) for row in rows)
    max_duration = max(_safe_float(row.get("Duration ms", 0.0)) for row in rows)
    total_ms = round(max_offset + max_duration, 2)
    row_html: list[str] = []
    for row in rows:
        row_label = html.escape(str(row.get("Name", "trace record")))
        scope = html.escape(str(row.get("Scope", "unknown")))
        stage = html.escape(str(row.get("Stage", "")))
        decision = html.escape(str(row.get("Decision", "")))
        kind = html.escape(str(row.get("Kind", "span")))
        left_percent = _safe_float(row.get("Left %", 0.0))
        width = _safe_float(row.get("Width %", 4.0), 4.0)
        duration = _safe_float(row.get("Duration ms", 0.0))
        row_html.append(
            "<div class='trace-row'>"
            f"<div class='trace-label'><strong>{row_label}</strong>"
            f"<div class='trace-meta'>{kind} | {scope} | {stage} {decision}</div>"
            "</div>"
            "<div class='trace-lane'>"
            f"<div class='trace-bar {_bar_class(kind)}' "
            f"style='left:{left_percent:.2f}%;width:{width:.2f}%;'></div>"
            "</div>"
            f"<div class='trace-duration'>{duration:.2f} ms</div>"
            "</div>"
        )

    markup = (
        "<div class='trace-shell'>"
        f"<div class='trace-header'><span>{html.escape(heading)}</span>"
        f"<span>{len(rows)} records | {total_ms:.2f} ms</span></div>"
        f"{''.join(row_html)}"
        "</div>"
    )
    st.markdown(markup, unsafe_allow_html=True)


def _show_failure_list(title: str, failures: list[str]) -> None:
    """Render a small failure list block."""
    st.markdown(f"**{title}**")
    if failures:
        for item in failures:
            st.markdown(f"- `{item}`")
        return
    st.caption("None.")


# Load data
history = load_history()
artifact_bundle = dashboard_artifacts.load_dashboard_artifacts(
    OUTPUT_DIR,
    DATASET_CONFIG.name,
    SELECTED_RUN_INSTANCE,
)
artifact_health_rows = dashboard_artifacts.build_artifact_health_rows(
    OUTPUT_DIR,
    DATASET_CONFIG.name,
    SELECTED_RUN_INSTANCE,
)
strategy_snapshot = dashboard_artifacts.load_strategy_snapshot(
    OUTPUT_DIR,
    DATASET_CONFIG.name,
    SELECTED_RUN_INSTANCE,
)
run_diagnostics = dashboard_artifacts.load_run_diagnostics(
    OUTPUT_DIR,
    SELECTED_RUN_INSTANCE,
)
round_signal_rows = dashboard_metrics.build_round_signal_rows(
    history,
    token_budget=ATTEMPT_TOKEN_BUDGET,
)
row_decision_summary_rows = dashboard_metrics.build_row_decision_summary_rows(
    artifact_bundle["row_decisions"]
)
artifact_present_count, artifact_missing_count = _artifact_status_counts(
    artifact_health_rows
)
latest_strategy = _latest_strategy(history, strategy_snapshot)

if not history:
    st.warning(f"No {HISTORY_PATH.name} found. " "Run `python util.py loop` first.")


# =====================================================================
# SECTION: Sidebar Metrics
# =====================================================================

st.sidebar.metric("Total Rounds", len(history))
st.sidebar.metric("Artifacts Present", artifact_present_count)
st.sidebar.metric("Artifacts Missing", artifact_missing_count)

if history:
    last = history[-1]
    latest_judge = dashboard_metrics.latest_judge_metrics(history)
    st.sidebar.metric("Latest Score", f"{last['score']}/{last['total']}")
    st.sidebar.metric(
        "Best Score",
        f"{max(e['score'] for e in history)}/{history[0]['total']}",
    )

    commits_count = sum(1 for e in history if e.get("action") == "commit")
    reverts_count = sum(1 for e in history if e.get("action") == "revert")
    skipped_count = sum(1 for e in history if e.get("action") == "skip")
    st.sidebar.metric("Commits", commits_count)
    st.sidebar.metric("Reverts", reverts_count)
    st.sidebar.metric("Skipped", skipped_count)
    st.sidebar.metric("Total Tokens", _total_tokens(history))
    if latest_judge:
        st.sidebar.metric(
            "Latest Recall", f"{latest_judge['cleanliness_score'] * 100:.1f}%"
        )
        st.sidebar.metric(
            "Latest Precision", f"{latest_judge['output_precision'] * 100:.1f}%"
        )
        st.sidebar.metric("Missing Rows", int(latest_judge["missing_rows"]))
        st.sidebar.metric("Unexpected Rows", int(latest_judge["unexpected_rows"]))
    st.sidebar.caption(f"History: {_display_project_path(HISTORY_PATH)}")
    st.sidebar.caption(f"Output: {_display_project_path(OUTPUT_CSV)}")
    st.sidebar.caption(
        f"Traces: {_display_project_path(ACTIVE_PATHS['otel_spans'].parent)}"
    )
    st.sidebar.caption(f"Logs: {_display_project_path(EXPORTED_LOGS_PATH)}")
else:
    st.sidebar.caption(f"History: {_display_project_path(HISTORY_PATH)}")
    st.sidebar.caption(f"Output: {_display_project_path(OUTPUT_CSV)}")
    st.sidebar.caption(
        f"Traces: {_display_project_path(ACTIVE_PATHS['otel_spans'].parent)}"
    )


# =====================================================================
# SECTION: Operator Snapshot
# =====================================================================

st.markdown("### Operator Snapshot")
if history:
    last = history[-1]
    latest_judge = dashboard_metrics.latest_judge_metrics(history)
    latest_signal = round_signal_rows[-1] if round_signal_rows else {}
    score_columns = st.columns([1, 1, 1, 1.45, 1, 1, 1])
    score_columns[0].metric("Latest Score", f"{last['score']}/{last['total']}")
    score_columns[1].metric(
        "Best Score", f"{max(e['score'] for e in history)}/{last['total']}"
    )
    score_columns[2].metric("Action", str(last.get("action", "unknown")))
    score_columns[3].metric(
        "Focus",
        _readable_label(latest_signal.get("Focus Area", "unknown")),
    )
    score_columns[4].metric("Missing Rows", int(latest_judge.get("missing_rows", 0)))
    score_columns[5].metric(
        "Unexpected Rows",
        int(latest_judge.get("unexpected_rows", 0)),
    )
    score_columns[6].metric("Tokens", _total_tokens(history))
    st.markdown(
        f"<div class='cleanloop-panel'><span class='cleanloop-signal'>Signal:</span> "
        f"{latest_signal.get('Operator Signal', 'watch')}<br>"
        f"<span class='cleanloop-signal'>Focus:</span> "
        f"{_readable_label(latest_signal.get('Focus Area', 'unknown'))}<br>"
        f"<span class='cleanloop-signal'>Guidance:</span> "
        f"{latest_strategy.get('guidance', 'No strategy guidance recorded.')}</div>",
        unsafe_allow_html=True,
    )
else:
    st.info(
        "No run history yet. Artifact health and traces can still be inspected below."
    )

if artifact_missing_count:
    st.warning(f"{artifact_missing_count} expected dashboard artifacts are missing.")
else:
    st.success("All expected dashboard artifacts are present.")


# =====================================================================
# SECTION: Tabbed Layout
# =====================================================================

(
    tab_overview,
    tab_score,
    tab_blueprint,
    tab_data,
    tab_observability,
    tab_logs,
    tab_diag,
) = st.tabs(
    [
        "Operator Overview",
        "Score Timeline",
        "Round Blueprint",
        "Data Quality",
        "Observability",
        "Execution Logs",
        "Diagnostics",
    ],
)

# --- Tab 0: Operator Overview ---
with tab_overview:
    st.subheader("Round Signals")
    signal_df = pd.DataFrame(round_signal_rows)
    if signal_df.empty:
        st.info("No round signals yet.")
    else:
        st.dataframe(signal_df, width="stretch", hide_index=True)

    st.subheader("Artifact Health")
    health_df = pd.DataFrame(artifact_health_rows)
    if not health_df.empty:
        health_df["Path"] = health_df["Path"].map(_display_project_path)
    st.dataframe(health_df, width="stretch", hide_index=True)

    st.subheader("Strategy Snapshot")
    if latest_strategy:
        st.json(latest_strategy)
    else:
        st.info("No strategy snapshot has been recorded yet.")

    st.subheader("Run Archive")
    if RUN_SUMMARIES:
        run_summary_df = pd.DataFrame(RUN_SUMMARIES)
        run_summary_df["Path"] = run_summary_df["Path"].map(_display_project_path)
        st.dataframe(run_summary_df, width="stretch", hide_index=True)
    else:
        st.info("No saved run instances yet.")

    if run_diagnostics:
        st.subheader("Run Diagnostics")
        st.json(run_diagnostics)

# --- Tab 1: Score Over Time ---
with tab_score:
    if not history:
        st.info("No score history yet.")
    else:
        score_df = pd.DataFrame(
            [
                {
                    "Round": history_entry["round"],
                    "Passed": history_entry["score"],
                    "Failed": history_entry["total"] - history_entry["score"],
                }
                for history_entry in history
            ]
        )
        st.line_chart(
            score_df.set_index("Round")[["Passed", "Failed"]],
            color=["#0f9f8e", "#c2410c"],
        )

        signal_df = pd.DataFrame(round_signal_rows)
        if not signal_df.empty and signal_df["Tokens"].gt(0).any():
            token_chart = signal_df.set_index("Round")[["Tokens"]]
            st.subheader("Token Usage by Round")
            st.bar_chart(token_chart)

        if not signal_df.empty:
            st.subheader("Token Efficiency")
            st.dataframe(
                signal_df[
                    [
                        "Round",
                        "Action",
                        "Focus Area",
                        "Recall Delta %",
                        "Tokens",
                        "Tokens per Recall Point",
                        "Operator Signal",
                    ]
                ],
                width="stretch",
                hide_index=True,
            )

        judge_df = pd.DataFrame(dashboard_metrics.build_judge_metric_rows(history))
        if not judge_df.empty:
            st.subheader("Judge Metric Trends")
            trend_df = judge_df.set_index("Round")[
                ["After Recall %", "After Precision %"]
            ]
            st.line_chart(trend_df)

# --- Tab 2: Round Blueprint ---
with tab_blueprint:
    blueprint_df = pd.DataFrame(_blueprint_rows(history))
    if blueprint_df.empty:
        st.info("No round blueprint yet.")
    else:
        st.dataframe(blueprint_df, width="stretch", hide_index=True)

    judge_df = pd.DataFrame(dashboard_metrics.build_judge_metric_rows(history))
    if not judge_df.empty:
        st.subheader("Judge Metric Deltas")
        st.dataframe(judge_df, width="stretch", hide_index=True)

    if history:
        st.subheader("Round-by-Round Blueprint")
    for history_entry in history:
        llm_info = _llm_info(history_entry)
        before_metrics = history_entry.get("before_metrics", {})
        after_metrics = history_entry.get("metrics", {})
        label = (
            f"Round {history_entry.get('round', '?')} | {history_entry.get('action', '?')} | "
            f"{history_entry.get('before_score', history_entry.get('score', '?'))}/"
            f"{history_entry.get('total', '?')} -> {history_entry.get('score', '?')}/"
            f"{history_entry.get('total', '?')}"
        )
        with st.expander(label):
            left, right = st.columns(2)
            with left:
                st.markdown("**Execution**")
                st.write(
                    {
                        "dataset": history_entry.get("dataset"),
                        "model": history_entry.get("model"),
                        "started_at": history_entry.get("started_at"),
                        "finished_at": history_entry.get("finished_at"),
                        "hypothesis": history_entry.get("hypothesis"),
                        "llm_path": llm_info.get("selected_attempt"),
                    }
                )
                _show_failure_list(
                    "Failures Before", history_entry.get("before_failed", [])
                )
            with right:
                st.markdown("**Judge Metrics**")
                st.write(
                    {
                        "before": before_metrics,
                        "after": after_metrics,
                    }
                )
                st.markdown("**Artifacts**")
                st.json(history_entry.get("artifacts", {}))
                _show_failure_list("Failures After", history_entry.get("failed", []))
                logs_df = pd.DataFrame(
                    dashboard_metrics.build_log_rows([history_entry])
                )
                if not logs_df.empty:
                    st.markdown("**Execution Logs**")
                    st.dataframe(logs_df, width="stretch", hide_index=True)
            st.markdown("**Mutable Genome Diff**")
            st.code(
                dashboard_metrics.build_mutation_diff(
                    history_entry.get("genome_before"),
                    history_entry.get("genome_after"),
                ),
                language="diff",
            )

# --- Tab 3: Data Quality ---
with tab_data:
    st.subheader("Output Data Quality")
    st.caption("The generated master CSV for the selected dataset family.")
    row_decision_df = pd.DataFrame(row_decision_summary_rows)
    if not row_decision_df.empty:
        st.markdown("**Row Decision Summary**")
        st.dataframe(row_decision_df, width="stretch", hide_index=True)
    else:
        st.info("No row-decision traces have been exported yet.")

    st.markdown("**Searchable Raw Decisions**")
    raw_decision_query = st.text_input(
        "Raw Decision Search",
        value="",
        placeholder="Search invoice, decision, source file, anomaly reason, run id",
        key="raw_decision_search",
    )
    decision_filter_columns = st.columns(2)
    with decision_filter_columns[0]:
        selected_decisions = st.multiselect(
            "Decision",
            _unique_values(artifact_bundle["row_decisions"], "decision"),
            key="raw_decision_filter",
        )
    with decision_filter_columns[1]:
        selected_sources = st.multiselect(
            "Source File",
            _unique_values(artifact_bundle["row_decisions"], "source_file"),
            key="raw_source_filter",
        )
    filtered_decisions = dashboard_metrics.filter_row_decision_rows(
        artifact_bundle["row_decisions"],
        query=raw_decision_query,
        decisions=selected_decisions,
        source_files=selected_sources,
    )
    if filtered_decisions:
        st.dataframe(
            _select_columns(
                filtered_decisions,
                [
                    "timestamp",
                    "run_instance",
                    "invoice_id",
                    "decision",
                    "stage",
                    "source_file",
                    "anomaly_reason",
                    "trace_id",
                ],
            ),
            width="stretch",
            hide_index=True,
        )
    else:
        st.info("No raw row decisions matched the current filters.")

    selected_invoice_id = st.text_input(
        "Invoice Drill-Down",
        value=_default_invoice_id(artifact_bundle["row_decisions"]),
    )
    if selected_invoice_id.strip():
        invoice_trace_rows = dashboard_metrics.filter_rows_by_invoice(
            artifact_bundle["row_decisions"],
            selected_invoice_id,
        )
        invoice_artifact_rows = _load_invoice_artifact_rows(selected_invoice_id)
        drill_left, drill_right = st.columns(2)
        with drill_left:
            st.markdown("**Trace Decisions**")
            if invoice_trace_rows:
                st.dataframe(
                    pd.DataFrame(invoice_trace_rows),
                    width="stretch",
                    hide_index=True,
                )
            else:
                st.info("No trace decisions matched that invoice.")
        with drill_right:
            st.markdown("**Input and Sidecar Rows**")
            if invoice_artifact_rows:
                st.dataframe(
                    pd.DataFrame(invoice_artifact_rows),
                    width="stretch",
                    hide_index=True,
                )
            else:
                st.info("No input or sidecar rows matched that invoice.")

        correlated_records = {
            "Spans": dashboard_metrics.filter_observability_rows(
                artifact_bundle["otel_spans"],
                query=selected_invoice_id,
            ),
            "Events": dashboard_metrics.filter_observability_rows(
                artifact_bundle["otel_events"],
                query=selected_invoice_id,
            ),
            "Logs": dashboard_metrics.filter_observability_rows(
                artifact_bundle["otel_logs"],
                query=selected_invoice_id,
            ),
        }
        correlated_flat_records = [
            record
            for records in correlated_records.values()
            for record in records
            if record.get("trace_id")
        ]
        invoice_trace_ids = sorted(
            {str(record.get("trace_id")) for record in correlated_flat_records}
        )
        if invoice_trace_ids:
            selected_invoice_trace_id = st.selectbox(
                "Trace Timeline",
                invoice_trace_ids,
                format_func=lambda trace_id: _trace_option_label(
                    trace_id,
                    correlated_flat_records,
                ),
                key="invoice_trace_timeline",
            )
            _render_trace_timeline(
                dashboard_metrics.build_trace_timeline_rows(
                    artifact_bundle["otel_spans"],
                    artifact_bundle["otel_events"],
                    artifact_bundle["otel_logs"],
                    trace_id=selected_invoice_trace_id,
                    invoice_id=selected_invoice_id,
                ),
                "Correlated trace waterfall",
            )
        else:
            st.info("No OTEL trace id is linked to this invoice yet.")
        with st.expander("Correlated OTEL Records"):
            for label, records in correlated_records.items():
                st.markdown(f"**{label}**")
                if records:
                    st.dataframe(
                        _select_columns(
                            records,
                            [
                                "timestamp",
                                "scope_name",
                                "stage",
                                "decision",
                                "invoice_id",
                                "source_file",
                                "trace_id",
                                "span_id",
                            ],
                        ),
                        width="stretch",
                        hide_index=True,
                    )
                else:
                    st.caption("No matching records.")

    judge_df = pd.DataFrame(dashboard_metrics.build_judge_metric_rows(history))
    if not judge_df.empty:
        st.markdown("**Per-Round Judge Metrics**")
        st.dataframe(judge_df, width="stretch", hide_index=True)

    if OUTPUT_CSV.exists():
        try:
            df = pd.read_csv(OUTPUT_CSV)
            col1, col2, col3 = st.columns(3)
            col1.metric("Rows", len(df))
            col2.metric("Columns", len(df.columns))
            col3.metric("Nulls", int(df.isnull().sum().sum()))

            st.markdown("**Column Summary**")
            summary = pd.DataFrame(
                {
                    "Column": df.columns,
                    "Dtype": [str(d) for d in df.dtypes],
                    "Non-Null": [int(df[c].notna().sum()) for c in df.columns],
                    "Unique": [int(df[c].nunique()) for c in df.columns],
                }
            )
            st.dataframe(summary, width="stretch", hide_index=True)

            st.markdown("**Sample Rows**")
            st.dataframe(df.head(20), width="stretch", hide_index=True)

            st.markdown("**Input Files**")
            st.write(list(DATASET_CONFIG.input_filenames))
        except (
            OSError,
            ValueError,
            pd.errors.ParserError,
            pd.errors.EmptyDataError,
        ) as exc:
            st.error(f"Could not read CSV: {exc}")
    else:
        st.info(f"No {OUTPUT_CSV.name} yet — run the loop first.")

# --- Tab 4: Observability ---
with tab_observability:
    st.subheader("OTEL Trace, Event, Log, and Scope Views")
    otel_spans = artifact_bundle["otel_spans"]
    otel_events = artifact_bundle["otel_events"]
    otel_logs = artifact_bundle["otel_logs"]
    observable_counts = st.columns(4)
    observable_counts[0].metric("Spans", len(otel_spans))
    observable_counts[1].metric("Events", len(otel_events))
    observable_counts[2].metric("Logs", len(otel_logs))
    observable_counts[3].metric(
        "Scopes",
        len(_unique_values([*otel_spans, *otel_events, *otel_logs], "scope_name")),
    )

    scope_summary = dashboard_metrics.build_scope_summary_rows(
        otel_spans,
        otel_events,
        otel_logs,
    )
    if scope_summary:
        st.markdown("**Instrumentation Scopes**")
        st.dataframe(pd.DataFrame(scope_summary), width="stretch", hide_index=True)

    observability_query = st.text_input(
        "Trace/Event/Log Search",
        value="",
        placeholder="Search invoice id, round, component, stage, trace id, message",
        key="observability_search",
    )
    selected_scopes = st.multiselect(
        "Scope Filter",
        _unique_values([*otel_spans, *otel_events, *otel_logs], "scope_name"),
        key="observability_scope_filter",
    )
    filtered_spans = dashboard_metrics.filter_observability_rows(
        otel_spans,
        query=observability_query,
        scopes=selected_scopes,
    )
    filtered_events = dashboard_metrics.filter_observability_rows(
        otel_events,
        query=observability_query,
        scopes=selected_scopes,
    )
    filtered_logs = dashboard_metrics.filter_observability_rows(
        otel_logs,
        query=observability_query,
        scopes=selected_scopes,
    )

    filtered_trace_records = [
        record
        for record in [*filtered_spans, *filtered_events, *filtered_logs]
        if record.get("trace_id")
    ]
    observability_trace_ids = sorted(
        {str(record.get("trace_id")) for record in filtered_trace_records}
    )
    if observability_trace_ids:
        selected_trace_id = st.selectbox(
            "Trace Waterfall",
            observability_trace_ids,
            format_func=lambda trace_id: _trace_option_label(
                trace_id,
                filtered_trace_records,
            ),
            key="observability_trace_waterfall",
        )
        _render_trace_timeline(
            dashboard_metrics.build_trace_timeline_rows(
                otel_spans,
                otel_events,
                otel_logs,
                trace_id=selected_trace_id,
            ),
            "Selected trace waterfall",
        )
    else:
        st.info("No trace id is available for the current observability filter.")

    st.markdown("**Trace Spans**")
    if filtered_spans:
        st.dataframe(
            _select_columns(
                filtered_spans,
                [
                    "timestamp",
                    "scope_name",
                    "name",
                    "stage",
                    "decision",
                    "round",
                    "invoice_id",
                    "source_file",
                    "status_code",
                    "trace_id",
                    "span_id",
                    "parent_span_id",
                ],
            ),
            width="stretch",
            hide_index=True,
        )
    else:
        st.info("No OTEL spans matched the current filters.")

    st.markdown("**Events**")
    if filtered_events:
        st.dataframe(
            _select_columns(
                filtered_events,
                [
                    "timestamp",
                    "scope_name",
                    "event_type",
                    "name",
                    "stage",
                    "decision",
                    "round",
                    "invoice_id",
                    "source_file",
                    "trace_id",
                    "span_id",
                ],
            ),
            width="stretch",
            hide_index=True,
        )
    else:
        st.info("No OTEL events matched the current filters.")

    st.markdown("**Logs**")
    if filtered_logs:
        st.dataframe(
            _select_columns(
                filtered_logs,
                [
                    "timestamp",
                    "severity_text",
                    "scope_name",
                    "body",
                    "stage",
                    "decision",
                    "round",
                    "trace_id",
                    "span_id",
                ],
            ),
            width="stretch",
            hide_index=True,
        )
    else:
        st.info("No OTEL logs matched the current filters.")


# --- Tab 5: Execution Logs ---
with tab_logs:
    st.subheader("Execution Logs")
    st.caption(
        "Every structured teaching log emitted during the loop, including token usage."
    )
    exported_logs_df = pd.DataFrame(artifact_bundle["exported_logs"])
    if exported_logs_df.empty:
        st.info("No exported loop-log JSONL file has been written yet.")
    else:
        st.markdown("**Exported Log Stream**")
        st.dataframe(exported_logs_df, width="stretch", hide_index=True)

    logs_df = pd.DataFrame(dashboard_metrics.build_log_rows(history))
    if logs_df.empty:
        st.info("No execution logs have been recorded yet.")
    else:
        st.markdown("**History-Backed Round Logs**")
        st.dataframe(logs_df, width="stretch", hide_index=True)

        st.subheader("Round Log Streams")
        for history_entry in reversed(history):
            round_logs = history_entry.get("logs", [])
            if not isinstance(round_logs, list) or not round_logs:
                continue
            label = (
                f"Round {history_entry.get('round', '?')} | {history_entry.get('action', '?')} | "
                f"{history_entry.get('score', '?')}/{history_entry.get('total', '?')}"
            )
            with st.expander(label):
                for log in round_logs:
                    if not isinstance(log, dict):
                        continue
                    line = f"[{log.get('tag', 'UNKNOWN')}] {log.get('message', '')}"
                    prompt_tokens = log.get("prompt_tokens")
                    completion_tokens = log.get("completion_tokens")
                    total_tokens = log.get("total_tokens")
                    if any(
                        isinstance(value, int)
                        for value in [prompt_tokens, completion_tokens, total_tokens]
                    ):
                        line += (
                            f" | prompt={prompt_tokens}"
                            f" | completion={completion_tokens}"
                            f" | total={total_tokens}"
                        )
                    st.code(line)

# --- Tab 6: Diagnostics ---
with tab_diag:
    st.subheader("LLM Call Diagnostics")
    st.caption(
        "Every recorded LLM attempt, including token counts and response previews."
    )

    attempt_df = pd.DataFrame(_attempt_rows(history))
    attempt_outcome_df = pd.DataFrame(
        dashboard_metrics.build_attempt_outcome_rows(
            history,
            token_budget=ATTEMPT_TOKEN_BUDGET,
        )
    )
    if not attempt_outcome_df.empty:
        st.markdown("**Attempt Outcome Summary**")
        st.dataframe(attempt_outcome_df, width="stretch", hide_index=True)

    if attempt_df.empty:
        st.info("No LLM attempt diagnostics have been recorded yet.")
    else:
        st.dataframe(attempt_df, width="stretch", hide_index=True)

    st.subheader("Trace Exports")
    trace_counts = st.columns(6)
    trace_counts[0].metric("Run Events", len(artifact_bundle["run_events"]))
    trace_counts[1].metric("Proposal Events", len(artifact_bundle["proposal_events"]))
    trace_counts[2].metric("Row Decisions", len(artifact_bundle["row_decisions"]))
    trace_counts[3].metric("OTEL Spans", len(artifact_bundle["otel_spans"]))
    trace_counts[4].metric("OTEL Events", len(artifact_bundle["otel_events"]))
    trace_counts[5].metric("OTEL Logs", len(artifact_bundle["otel_logs"]))

    run_events_df = pd.DataFrame(artifact_bundle["run_events"])
    if run_events_df.empty:
        st.info("No run-event traces have been exported yet.")
    else:
        st.markdown("**Run Events**")
        st.dataframe(run_events_df, width="stretch", hide_index=True)

    proposal_events_df = pd.DataFrame(artifact_bundle["proposal_events"])
    if proposal_events_df.empty:
        st.info("No proposal-event traces have been exported yet.")
    else:
        st.markdown("**Proposal Events**")
        st.dataframe(proposal_events_df, width="stretch", hide_index=True)

    row_decisions_df = pd.DataFrame(artifact_bundle["row_decisions"])
    if row_decisions_df.empty:
        st.info("No row-decision traces have been exported yet.")
    else:
        st.markdown("**Row Decisions**")
        st.dataframe(row_decisions_df, width="stretch", hide_index=True)

    st.subheader("Full Round Logs")
    for history_entry in reversed(history):
        label = (
            f"Round {history_entry.get('round', '?')} | {history_entry.get('action', '?')} | "
            f"{history_entry.get('score', '?')}/{history_entry.get('total', '?')}"
        )
        with st.expander(label):
            llm_info = _llm_info(history_entry)
            st.markdown("**Round Record**")
            st.json(history_entry)
            llm_error = llm_info.get("error") if isinstance(llm_info, dict) else None
            if llm_error:
                st.error(llm_error)
            attempts = llm_info.get("attempts", [])
            if attempts:
                st.markdown("**Attempt Breakdown**")
                for attempt_record in attempts:
                    st.write(
                        {
                            "label": attempt_record.get("label"),
                            "model": attempt_record.get("model"),
                            "code_found": attempt_record.get("code_found"),
                            "usage": attempt_record.get("usage"),
                            "prompt_chars": attempt_record.get("prompt_chars"),
                            "response_chars": attempt_record.get("response_chars"),
                            "hypothesis": attempt_record.get("hypothesis"),
                        }
                    )
                    st.markdown("**Messages**")
                    st.json(attempt_record.get("messages", []))
                    st.markdown("**Response Preview**")
                    st.code(attempt_record.get("response_preview", ""))


if __name__ == "__main__":
    pass
