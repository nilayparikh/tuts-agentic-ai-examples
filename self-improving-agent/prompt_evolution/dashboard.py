"""Streamlit dashboard for Prompt Evolution execution traces."""

from __future__ import annotations

import json
import sys
from pathlib import Path

# pylint: disable=wrong-import-position

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
import streamlit as st

from prompt_evolution.loop import (  # noqa: E402
    build_round_diff as loop_build_round_diff,
)

OUTPUT_DIR = PROJECT_ROOT / "prompt_evolution" / ".output"
SESSION_PATH = OUTPUT_DIR / "latest_session.json"
MUTATION_DIFF_PATH = OUTPUT_DIR / "latest_mutation.diff"
TRACE_DIR = OUTPUT_DIR / "traces"
RUN_EVENTS_PATH = TRACE_DIR / "run_events.jsonl"
EVALUATOR_EVENTS_PATH = TRACE_DIR / "evaluator_events.jsonl"


def build_round_diff(before_text: str, after_text: str) -> str:
    """Re-export the round diff helper for dashboard tests and fallback rendering."""
    return loop_build_round_diff(before_text, after_text)


def load_session_payload(path: Path = SESSION_PATH) -> dict | None:
    """Load the latest prompt evolution session payload from disk."""
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, object]]:
    """Load JSONL trace records from disk, skipping malformed blank lines."""
    if not path.exists():
        return []
    records: list[dict[str, object]] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(item, dict):
            records.append(item)
    return records


def build_round_rows(payload: dict) -> list[dict[str, object]]:
    """Flatten the round history into a compact overview table."""
    rows: list[dict[str, object]] = []
    for entry in payload.get("rounds", []):
        llm = entry.get("llm", {}) if isinstance(entry, dict) else {}
        rows.append(
            {
                "Round": entry.get("round"),
                "Score": f"{entry.get('score', '?')}/{entry.get('total', '?')}",
                "LLM Requests": llm.get("request_count", 0),
                "User Feedback": entry.get("user_feedback", ""),
            }
        )
    return rows


def build_llm_rows(payload: dict) -> list[dict[str, object]]:
    """Flatten the LLM request rows across all rounds."""
    rows: list[dict[str, object]] = []
    for entry in payload.get("rounds", []):
        llm = entry.get("llm", {}) if isinstance(entry, dict) else {}
        for request in llm.get("requests", []):
            rows.append(
                {
                    "Round": entry.get("round"),
                    "Kind": request.get("kind"),
                    "Task": request.get("task_id"),
                    "Model": request.get("model"),
                    "Provider": request.get("provider"),
                    "System Chars": request.get("system_prompt_chars"),
                    "User Chars": request.get("user_prompt_chars"),
                    "Response Chars": request.get("response_chars"),
                }
            )
    return rows


def build_trace_rows(records: list[dict[str, object]]) -> list[dict[str, object]]:
    """Flatten trace records into a dashboard-friendly event table."""
    rows: list[dict[str, object]] = []
    for record in records:
        rows.append(
            {
                "Time": record.get("timestamp"),
                "Run": record.get("run_instance"),
                "Stage": record.get("stage"),
                "Decision": record.get("decision"),
                "Round": record.get("round", ""),
                "Scenario": record.get("scenario_slug", ""),
                "Score": record.get("score", ""),
                "Total": record.get("total", ""),
            }
        )
    return rows


def build_evaluator_rows(records: list[dict[str, object]]) -> list[dict[str, object]]:
    """Flatten evaluator records into score and issue-count rows."""
    rows: list[dict[str, object]] = []
    for record in records:
        rows.append(
            {
                "Round": record.get("round"),
                "Score": record.get("score"),
                "Total": record.get("total"),
                "Issues": record.get("issue_count"),
                "Strengths": record.get("strength_count"),
                "Scenario": record.get("scenario_slug", ""),
            }
        )
    return rows


def render_dashboard() -> None:
    """Render the Prompt Evolution trace dashboard."""
    st.set_page_config(page_title="Prompt Evolution Dashboard", layout="wide")
    st.title("Prompt Evolution Dashboard")
    payload = load_session_payload()
    if payload is None:
        st.warning("No latest_session.json found. Run the Prompt Evolution loop first.")
        st.stop()
    assert payload is not None

    rounds = payload.get("rounds", [])
    best_round = payload.get("best_round")
    st.metric("Rounds", len(rounds))
    st.metric("Best Round", best_round)
    st.caption(f"Problem: {payload.get('problem', '')}")

    tab_overview, tab_scenario, tab_trace, tab_diff, tab_llm = st.tabs(
        ["Overview", "Scenario", "Trace", "Diff", "LLM Requests"]
    )

    with tab_overview:
        overview_df = pd.DataFrame(build_round_rows(payload))
        if not overview_df.empty:
            st.dataframe(overview_df, width="stretch", hide_index=True)
        for entry in rounds:
            with st.expander(f"Round {entry.get('round')}"):
                st.markdown("**Response**")
                st.code(str(entry.get("response", "")), language="markdown")
                st.markdown("**Instructions**")
                st.code(str(entry.get("instructions", "")), language="text")
                st.markdown("**Logs**")
                st.code("\n".join(entry.get("logs", [])), language="text")

    with tab_scenario:
        scenario = payload.get("scenario")
        if isinstance(scenario, dict):
            st.subheader(str(scenario.get("label", "Scenario")))
            st.caption(str(scenario.get("customer_problem", "")))
            st.markdown("**Customer facts**")
            st.write(list(scenario.get("customer_facts", [])))
            st.markdown("**Risk flags**")
            st.write(list(scenario.get("risk_flags", [])))
            st.markdown("**Success criteria**")
            st.write(list(scenario.get("success_criteria", [])))
        else:
            st.info("This run did not use a named scenario.")

    with tab_trace:
        run_records = load_jsonl(RUN_EVENTS_PATH)
        evaluator_records = load_jsonl(EVALUATOR_EVENTS_PATH)
        trace_df = pd.DataFrame(build_trace_rows(run_records))
        evaluator_df = pd.DataFrame(build_evaluator_rows(evaluator_records))
        if trace_df.empty:
            st.info("No run_events.jsonl trace records found yet.")
        else:
            st.dataframe(trace_df, width="stretch", hide_index=True)
        if not evaluator_df.empty:
            st.markdown("**Evaluator events**")
            st.dataframe(evaluator_df, width="stretch", hide_index=True)

    with tab_diff:
        if MUTATION_DIFF_PATH.exists():
            st.code(MUTATION_DIFF_PATH.read_text(encoding="utf-8"), language="diff")
        elif len(rounds) >= 2:
            previous_entry = rounds[-2]
            current_entry = rounds[-1]
            st.code(
                build_round_diff(
                    str(previous_entry.get("instructions", "")),
                    str(current_entry.get("instructions", "")),
                ),
                language="diff",
            )
        else:
            st.info("No mutation diff recorded yet.")

    with tab_llm:
        llm_df = pd.DataFrame(build_llm_rows(payload))
        if llm_df.empty:
            st.info("No LLM requests recorded yet.")
        else:
            st.dataframe(llm_df, width="stretch", hide_index=True)


if __name__ == "__main__":
    render_dashboard()
