"""dashboard.py — Streamlit monitoring dashboard.

Tabbed dashboard that visualizes the self-improving loop in
real time. Reads the dataset-specific history log to show
iteration-by-iteration progress.

Course alignment:
    - Lesson 06: loop observability and operator feedback

Usage:
    streamlit run cleanloop/dashboard.py

Reads from:
    cleanloop/.output/<dataset>_eval_history.json   — loop iteration results
    cleanloop/clean_data.py                         — current genome source
    git log                                         — commit history
"""

import json
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

# ─── PATHS ────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from cleanloop import datasets as cleanloop_datasets
from cleanloop import dashboard_metrics

OUTPUT_DIR = PROJECT_ROOT / "cleanloop" / ".output"
DATASET_CONFIG = cleanloop_datasets.get_dataset_config()
HISTORY_PATH = cleanloop_datasets.get_history_path(OUTPUT_DIR, DATASET_CONFIG.name)


# =====================================================================
# SECTION: Streamlit Page Configuration
# Lesson 06 — Use a wide layout so the operator can compare history,
# failures, artifacts, and the current genome without losing context.
# set_page_config must be the first Streamlit command.
# =====================================================================

st.set_page_config(
    page_title="CleanLoop Dashboard",
    page_icon="",
    layout="wide",
)
st.title(f"CleanLoop — {DATASET_CONFIG.label} Dashboard")
st.caption(f"Selected dataset: {DATASET_CONFIG.name}")

OUTPUT_CSV = cleanloop_datasets.get_output_path(OUTPUT_DIR, DATASET_CONFIG.name)
ATTEMPT_TOKEN_BUDGET = 2200


def load_history() -> list[dict]:
    """Load eval history from the JSON log file."""
    if not HISTORY_PATH.exists():
        return []
    return json.loads(HISTORY_PATH.read_text(encoding="utf-8"))


def _llm_info(entry: dict) -> dict:
    """Return normalized LLM diagnostics for one history entry."""
    llm = entry.get("llm")
    if isinstance(llm, dict):
        return llm
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
    for entry, judge_row in zip(history_rows, judge_rows):
        llm = _llm_info(entry)
        rows.append(
            {
                "Round": entry.get("round"),
                "Action": entry.get("action", ""),
                "Before": f"{entry.get('before_score', entry.get('score', '?'))}/{entry.get('total', '?')}",
                "After": f"{entry.get('score', '?')}/{entry.get('total', '?')}",
                "Delta": entry.get("score_delta", 0),
                "LLM Path": llm.get("selected_attempt", "none"),
                "Tokens": llm.get("total_tokens"),
                "Recall %": judge_row.get("After Recall %"),
                "Precision %": judge_row.get("After Precision %"),
                "Missing": judge_row.get("Missing Rows"),
                "Unexpected": judge_row.get("Unexpected Rows"),
                "Hypothesis": entry.get("hypothesis", ""),
                "Started": entry.get("started_at", ""),
                "Finished": entry.get("finished_at", ""),
            }
        )
    return rows


def _attempt_rows(history_rows: list[dict]) -> list[dict[str, object]]:
    """Flatten all LLM attempts across rounds for diagnostics tables."""
    rows: list[dict[str, object]] = []
    for entry in history_rows:
        llm = _llm_info(entry)
        for attempt in llm.get("attempts", []):
            usage = attempt.get("usage", {}) if isinstance(attempt, dict) else {}
            rows.append(
                {
                    "Round": entry.get("round"),
                    "Label": attempt.get("label"),
                    "Model": attempt.get("model"),
                    "Code Found": attempt.get("code_found"),
                    "Prompt Tokens": usage.get("prompt_tokens"),
                    "Completion Tokens": usage.get("completion_tokens"),
                    "Total Tokens": usage.get("total_tokens"),
                    "Prompt Chars": attempt.get("prompt_chars"),
                    "Response Chars": attempt.get("response_chars"),
                    "Hypothesis": attempt.get("hypothesis"),
                }
            )
    return rows


def _total_tokens(history_rows: list[dict]) -> int:
    """Sum total LLM tokens across all rounds when available."""
    total = 0
    for entry in history_rows:
        value = _llm_info(entry).get("total_tokens")
        if isinstance(value, int):
            total += value
    return total


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

if not history:
    st.warning(f"No {HISTORY_PATH.name} found. " "Run `python util.py loop` first.")
    st.stop()


# =====================================================================
# SECTION: Sidebar Metrics
# =====================================================================

st.sidebar.metric("Total Rounds", len(history))

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
    st.sidebar.caption(f"History: {HISTORY_PATH.relative_to(PROJECT_ROOT)}")
    st.sidebar.caption(f"Output: {OUTPUT_CSV.relative_to(PROJECT_ROOT)}")


# =====================================================================
# SECTION: Tabbed Layout
# =====================================================================

tab_score, tab_blueprint, tab_data, tab_logs, tab_diag = st.tabs(
    [
        "Score Timeline",
        "Round Blueprint",
        "Data Quality",
        "Execution Logs",
        "Diagnostics",
    ],
)

# --- Tab 1: Score Over Time ---
with tab_score:
    score_df = pd.DataFrame(
        [
            {
                "Round": entry["round"],
                "Passed": entry["score"],
                "Failed": entry["total"] - entry["score"],
            }
            for entry in history
        ]
    )
    st.line_chart(
        score_df.set_index("Round")[["Passed", "Failed"]],
        color=["#4ecdc4", "#ff6b6b"],
    )

    attempt_df = pd.DataFrame(_attempt_rows(history))
    if not attempt_df.empty and attempt_df["Total Tokens"].notna().any():
        token_chart = attempt_df.groupby("Round", dropna=False)["Total Tokens"].sum(
            min_count=1
        )
        st.subheader("Token Usage by Round")
        st.bar_chart(token_chart)

    judge_df = pd.DataFrame(dashboard_metrics.build_judge_metric_rows(history))
    if not judge_df.empty:
        st.subheader("Judge Metric Trends")
        trend_df = judge_df.set_index("Round")[["After Recall %", "After Precision %"]]
        st.line_chart(trend_df)

# --- Tab 2: Round Blueprint ---
with tab_blueprint:
    blueprint_df = pd.DataFrame(_blueprint_rows(history))
    st.dataframe(blueprint_df, width="stretch", hide_index=True)

    judge_df = pd.DataFrame(dashboard_metrics.build_judge_metric_rows(history))
    if not judge_df.empty:
        st.subheader("Judge Metric Deltas")
        st.dataframe(judge_df, width="stretch", hide_index=True)

    st.subheader("Round-by-Round Blueprint")
    for entry in history:
        llm = _llm_info(entry)
        before_metrics = entry.get("before_metrics", {})
        after_metrics = entry.get("metrics", {})
        label = (
            f"Round {entry.get('round', '?')} | {entry.get('action', '?')} | "
            f"{entry.get('before_score', entry.get('score', '?'))}/"
            f"{entry.get('total', '?')} -> {entry.get('score', '?')}/"
            f"{entry.get('total', '?')}"
        )
        with st.expander(label):
            left, right = st.columns(2)
            with left:
                st.markdown("**Execution**")
                st.write(
                    {
                        "dataset": entry.get("dataset"),
                        "model": entry.get("model"),
                        "started_at": entry.get("started_at"),
                        "finished_at": entry.get("finished_at"),
                        "hypothesis": entry.get("hypothesis"),
                        "llm_path": llm.get("selected_attempt"),
                    }
                )
                _show_failure_list("Failures Before", entry.get("before_failed", []))
            with right:
                st.markdown("**Judge Metrics**")
                st.write(
                    {
                        "before": before_metrics,
                        "after": after_metrics,
                    }
                )
                st.markdown("**Artifacts**")
                st.json(entry.get("artifacts", {}))
                _show_failure_list("Failures After", entry.get("failed", []))
                logs_df = pd.DataFrame(dashboard_metrics.build_log_rows([entry]))
                if not logs_df.empty:
                    st.markdown("**Execution Logs**")
                    st.dataframe(logs_df, width="stretch", hide_index=True)
            st.markdown("**Mutable Genome Diff**")
            st.code(
                dashboard_metrics.build_mutation_diff(
                    entry.get("genome_before"),
                    entry.get("genome_after"),
                ),
                language="diff",
            )

# --- Tab 3: Data Quality ---
with tab_data:
    st.subheader("Output Data Quality")
    st.caption("The generated master CSV for the selected dataset family.")
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
        except Exception as exc:
            st.error(f"Could not read CSV: {exc}")
    else:
        st.info(f"No {OUTPUT_CSV.name} yet — run the loop first.")

# --- Tab 4: Execution Logs ---
with tab_logs:
    st.subheader("Execution Logs")
    st.caption(
        "Every structured teaching log emitted during the loop, including token usage."
    )
    logs_df = pd.DataFrame(dashboard_metrics.build_log_rows(history))
    if logs_df.empty:
        st.info("No execution logs have been recorded yet.")
    else:
        st.dataframe(logs_df, width="stretch", hide_index=True)

        st.subheader("Round Log Streams")
        for entry in reversed(history):
            round_logs = entry.get("logs", [])
            if not isinstance(round_logs, list) or not round_logs:
                continue
            label = (
                f"Round {entry.get('round', '?')} | {entry.get('action', '?')} | "
                f"{entry.get('score', '?')}/{entry.get('total', '?')}"
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

# --- Tab 5: Diagnostics ---
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

    st.subheader("Full Round Logs")
    for entry in reversed(history):
        label = (
            f"Round {entry.get('round', '?')} | {entry.get('action', '?')} | "
            f"{entry.get('score', '?')}/{entry.get('total', '?')}"
        )
        with st.expander(label):
            llm = _llm_info(entry)
            st.markdown("**Round Record**")
            st.json(entry)
            llm_error = llm.get("error") if isinstance(llm, dict) else None
            if llm_error:
                st.error(llm_error)
            attempts = llm.get("attempts", [])
            if attempts:
                st.markdown("**Attempt Breakdown**")
                for attempt in attempts:
                    st.write(
                        {
                            "label": attempt.get("label"),
                            "model": attempt.get("model"),
                            "code_found": attempt.get("code_found"),
                            "usage": attempt.get("usage"),
                            "prompt_chars": attempt.get("prompt_chars"),
                            "response_chars": attempt.get("response_chars"),
                            "hypothesis": attempt.get("hypothesis"),
                        }
                    )
                    st.markdown("**Messages**")
                    st.json(attempt.get("messages", []))
                    st.markdown("**Response Preview**")
                    st.code(attempt.get("response_preview", ""))


if __name__ == "__main__":
    pass
