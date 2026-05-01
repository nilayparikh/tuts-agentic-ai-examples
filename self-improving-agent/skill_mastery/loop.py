"""Skill Mastery loop that learns and composes reusable habits."""

from __future__ import annotations

from difflib import unified_diff
import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

import util

from prompt_evolution.hermes_client import HermesAgentRunner
from skill_mastery.config import SkillMasteryCatalog, SkillMasteryProfile
from skill_mastery.evaluator import SkillEvaluationResult, evaluate_response
from skill_mastery.history_store import HistoryStore
from skill_mastery.learner import LearnedHabit, learn_reusable_habits
from skill_mastery.mutation_playbook import render_brief, select_strategies
from skill_mastery.selector import select_habits
from skill_mastery.tracing import TraceRecorder  # type: ignore[import-not-found]

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EXAMPLE_ROOT = PROJECT_ROOT / "skill_mastery"
OUTPUT_DIR = EXAMPLE_ROOT / ".output"

util.load_env()

LogSink = Callable[[str], None]


def _iso_now() -> str:
    """Return the current UTC timestamp in ISO-8601 form."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _habit_markdown(habits: list[LearnedHabit]) -> str:
    """Render learned or selected habits as Markdown bullets."""
    lines = []
    for habit in habits:
        lines.append(f"- {habit.label}: {habit.instruction}")
        lines.append(f"  Stop: {habit.stop_condition}")
    return "\n".join(lines)


def build_round_diff(before_text: str, after_text: str) -> str:
    """Render a unified diff for the mutable reply artifact."""
    if before_text == after_text:
        return "No changes."
    return "\n".join(
        unified_diff(
            before_text.splitlines(),
            after_text.splitlines(),
            fromfile="before",
            tofile="after",
            lineterm="",
        )
    )


def _emit_log(
    round_logs: list[str],
    log_sink: LogSink | None,
    tag: str,
    message: str,
) -> None:
    """Record one verbose execution log entry and optionally print it."""
    line = f"[{tag}] {message}"
    round_logs.append(line)
    if log_sink is not None:
        log_sink(line)


def _build_llm_request_record(  # pylint: disable=too-many-arguments
    runner: HermesAgentRunner,
    *,
    request_kind: str,
    task_id: str,
    system_prompt: str,
    user_prompt: str,
    response: Any,
) -> dict[str, Any]:
    """Capture the important metadata for one LLM request."""
    messages = getattr(response, "messages", [])
    return {
        "kind": request_kind,
        "task_id": task_id,
        "model": getattr(runner, "model", None),
        "provider": getattr(runner, "provider", None),
        "base_url": getattr(runner, "base_url", None),
        "system_prompt_chars": len(system_prompt),
        "user_prompt_chars": len(user_prompt),
        "response_chars": len(getattr(response, "text", "")),
        "message_count": len(messages) if isinstance(messages, list) else 0,
        "captured_output_chars": len(getattr(response, "raw_output", "")),
    }


def _build_llm_summary(
    runner: HermesAgentRunner,
    requests: list[dict[str, Any]],
) -> dict[str, Any]:
    """Summarize the LLM usage for one round."""
    return {
        "model": getattr(runner, "model", None),
        "provider": getattr(runner, "provider", None),
        "base_url": getattr(runner, "base_url", None),
        "request_count": len(requests),
        "requests": requests,
    }


def _latest_mutation_diff(history: list[dict[str, Any]]) -> str | None:
    """Return the newest available mutation diff from the saved history."""
    for entry in reversed(history):
        diff_text = entry.get("mutation_diff")
        if isinstance(diff_text, str) and diff_text.strip():
            return diff_text
    return None


def _existing_trace_metadata() -> dict[str, Any] | None:
    """Load previous trace metadata when interactive review rewrites outputs."""
    session_path = OUTPUT_DIR / "latest_session.json"
    if not session_path.exists():
        return None
    try:
        payload = json.loads(session_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    trace_payload = payload.get("trace")
    return trace_payload if isinstance(trace_payload, dict) else None


def _usecase_slug(profile: SkillMasteryProfile) -> str | None:
    """Return the active use case slug when the run came from a use case."""
    if profile.usecase is None:
        return None
    return profile.usecase.slug


def _usecase_brief(profile: SkillMasteryProfile) -> str:
    """Render use case facts for the generation prompt when available."""
    if profile.usecase is None:
        return ""
    usecase = profile.usecase
    facts = "\n".join(f"- {item}" for item in usecase.customer_facts)
    risk_flags = "\n".join(f"- {item}" for item in usecase.risk_flags)
    criteria = "\n".join(f"- {item}" for item in usecase.success_criteria)
    expected_habits = ", ".join(usecase.expected_habit_slugs)
    return (
        f"Use Case: {usecase.label}\n"
        f"Expected Habit Slugs: {expected_habits}\n"
        f"Customer Facts\n{facts}\n\n"
        f"Risk Flags\n{risk_flags}\n\n"
        f"Success Criteria\n{criteria}\n\n"
    )


def build_generation_system_prompt(
    profile: SkillMasteryProfile,
    selected_habits: list[LearnedHabit],
) -> str:
    """Build the system prompt that Hermes uses to compose the reply."""
    policies = "\n".join(
        f"- {policy.description}" for policy in profile.context.required_policy_points
    )
    forbidden = "\n".join(f"- {claim}" for claim in profile.context.forbidden_claims)
    habits = "\n".join(
        f"- {habit.label}: {habit.instruction} Stop when: {habit.stop_condition}"
        for habit in selected_habits
    )
    return (
        "You are composing one customer-ready support reply with a small set of "
        "reusable habit cards. Apply each selected habit once, keep the response "
        "natural, and do not expose the habit framework.\n\n"
        f"{_usecase_brief(profile)}"
        f"Context: {profile.context.label}\n"
        f"Service Summary: {profile.context.service_summary}\n"
        f"Escalation Path: {profile.context.escalation_path}\n\n"
        f"Required Policy Points\n{policies}\n\n"
        f"Forbidden Claims\n{forbidden}\n\n"
        f"Selected Habit Cards\n{habits}\n"
    )


def build_generation_user_prompt(profile: SkillMasteryProfile) -> str:
    """Build the user prompt for the current service issue."""
    return (
        "Draft one customer-ready reply for this issue. Return only the final message.\n\n"
        f"Customer problem:\n{profile.problem}\n"
    )


def build_user_feedback_guide(
    profile: SkillMasteryProfile,
    selected_habits: list[LearnedHabit],
) -> str:
    """Explain what follow-up feedback the user can give after the first draft."""
    habit_names = ", ".join(habit.label for habit in selected_habits)
    first_policy = profile.context.required_policy_points[0].description
    return (
        "What you can ask to improve next:\n"
        f"- Habit emphasis: ask it to lean harder on habits such as {habit_names}.\n"
        '  If you ask "lead with the problem", expect the mirror habit to show up earlier.\n'
        f"- Policy grounding: ask it to name rules such as {first_policy.lower()}.\n"
        '  If you ask "mention certification earlier", expect the gate or '
        "review rule sooner.\n"
        "- Closing move: ask for one confirmation question, one checkpoint, or one named owner.\n"
        '  If you ask "end with one clear question", expect a tighter next step.\n'
        "- Tone and brevity: ask it to be calmer, more direct, shorter, or more reassuring.\n"
        '  If you ask "make it shorter and more direct", expect less preamble '
        "and a faster action line.\n"
        "You can also provide feedback like: sound more human, cite the policy "
        "first, ask one clarifying question, or avoid sounding too formal."
    )


REVISION_SYSTEM_PROMPT = (
    "You revise one customer-support reply using fixed habit cards and evaluator feedback. "
    "Return only the improved final message."
)


def build_revision_user_prompt(
    profile: SkillMasteryProfile,
    selected_habits: list[LearnedHabit],
    response_text: str,
    evaluation: SkillEvaluationResult,
    user_feedback: str | None = None,
) -> str:
    """Build the revision brief for a follow-up reply attempt."""
    issues = "\n".join(f"- {issue}" for issue in evaluation.issues) or "- None"
    habits = "\n".join(
        f"- {habit.label}: {habit.instruction}" for habit in selected_habits
    )
    feedback_block = ""
    if user_feedback:
        feedback_block = f"User feedback:\n- {user_feedback}\n\n"
    return (
        f"Context: {profile.context.label}\n"
        f"Customer problem:\n{profile.problem}\n\n"
        f"Selected habits:\n{habits}\n\n"
        f"Current reply:\n{response_text}\n\n"
        f"{feedback_block}"
        f"Issues to fix:\n{issues}\n\n"
        "Revise the reply so it covers the missing habits and policy points "
        "without overpromising."
    )


def _serialize_round(
    round_number: int,
    response_text: str,
    evaluation: SkillEvaluationResult,
    user_feedback: str | None = None,
) -> dict[str, Any]:
    """Convert one round into a JSON-safe history record."""
    payload = {
        "round": round_number,
        "response": response_text,
        "score": evaluation.total_score,
        "total": evaluation.max_score,
        "issues": evaluation.issues,
        "strengths": evaluation.strengths,
    }
    if user_feedback:
        payload["user_feedback"] = user_feedback
    return payload


def _best_round(history: list[dict[str, Any]]) -> dict[str, Any]:
    """Return the highest-scoring round from the current history."""
    for round_data in reversed(history):
        if round_data.get("selected"):
            return round_data
    return max(history, key=lambda item: (item["score"], item["round"]))


def _write_outputs(
    profile: SkillMasteryProfile,
    learned_habits: list[LearnedHabit],
    selected_habits: list[LearnedHabit],
    history: list[dict[str, Any]],
    trace_metadata: dict[str, Any] | None = None,
) -> None:
    """Persist the latest session, learned habits, selected habits, and best reply."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    best = _best_round(history)
    active_trace_metadata = trace_metadata or _existing_trace_metadata()
    session_payload = {
        "generated_at": _iso_now(),
        "problem": profile.problem,
        "usecase": asdict(profile.usecase) if profile.usecase else None,
        "context": asdict(profile.context),
        "selected_habits": [habit.slug for habit in selected_habits],
        "rounds": history,
        "best_round": best["round"],
    }
    if active_trace_metadata is not None:
        session_payload["trace"] = active_trace_metadata
    (OUTPUT_DIR / "latest_session.json").write_text(
        json.dumps(session_payload, indent=2),
        encoding="utf-8",
    )
    (OUTPUT_DIR / "learned_habits.json").write_text(
        json.dumps([asdict(habit) for habit in learned_habits], indent=2),
        encoding="utf-8",
    )
    (OUTPUT_DIR / "selected_habits.md").write_text(
        _habit_markdown(selected_habits),
        encoding="utf-8",
    )
    (OUTPUT_DIR / "best_response.md").write_text(
        str(best["response"]),
        encoding="utf-8",
    )
    latest_mutation_diff = _latest_mutation_diff(history)
    if latest_mutation_diff is not None:
        (OUTPUT_DIR / "latest_mutation.diff").write_text(
            latest_mutation_diff,
            encoding="utf-8",
        )


def save_outputs(
    profile: SkillMasteryProfile,
    learned_habits: list[LearnedHabit],
    selected_habits: list[LearnedHabit],
    history: list[dict[str, Any]],
) -> None:
    """Persist Skill Mastery outputs after extra feedback-driven revisions."""
    _write_outputs(profile, learned_habits, selected_habits, history)


def reset_outputs() -> None:
    """Delete the Skill Mastery output directory if it exists."""
    if not OUTPUT_DIR.exists():
        return
    import shutil

    shutil.rmtree(OUTPUT_DIR)


def _draft_with_reranker(  # pylint: disable=too-many-arguments
    *,
    profile: SkillMasteryProfile,
    selected_habits: list[LearnedHabit],
    system_prompt: str,
    user_prompt: str,
    candidate_count: int,
    runner: HermesAgentRunner,
    task_id: str,
) -> tuple[Any, list[dict[str, Any]]]:
    """Run a best-of-N rerank pass and return the winning response + per-call records."""
    from skill_mastery.reranker import rerank_drafts  # local import for cycle safety

    captured_responses: list[Any] = []

    def _draft(system_text: str, user_text: str, draft_task_id: str) -> Any:
        response = runner.run_text(
            system_prompt=system_text,
            user_prompt=user_text,
            task_id=draft_task_id,
        )
        captured_responses.append(response)
        return response

    rerank_result = rerank_drafts(
        profile=profile,
        selected_habits=selected_habits,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        candidate_count=candidate_count,
        runner=runner,
        draft_function=_draft,
        base_task_id=task_id,
    )
    request_records: list[dict[str, Any]] = []
    for index, candidate in enumerate(rerank_result.candidates):
        # Pair each captured response with its candidate.
        if index < len(captured_responses):
            response = captured_responses[index]
        else:
            response = type(
                "R", (), {"text": candidate.response_text, "messages": []}
            )()
        request_records.append(
            _build_llm_request_record(
                runner,
                request_kind="draft_rerank_candidate",
                task_id=candidate.task_id,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                response=response,
            )
        )
    if rerank_result.best_index < len(captured_responses):
        winning_response = captured_responses[rerank_result.best_index]
    else:
        winning_response = type(
            "R", (), {"text": rerank_result.best.response_text, "messages": []}
        )()
    return winning_response, request_records


def run_skill_mastery(  # pylint: disable=too-many-locals,too-many-arguments
    catalog: SkillMasteryCatalog,
    profile: SkillMasteryProfile,
    *,
    max_iterations: int = 2,
    runner: HermesAgentRunner | None = None,
    log_sink: LogSink | None = None,
    run_instance: str | None = None,
    use_reranker: bool = False,
    candidate_count: int = 3,
    history_store: HistoryStore | None = None,
    session_id: str | None = None,
) -> list[dict[str, Any]]:
    """Learn reusable habits, select a small set, and compose a reply.

    When `use_reranker` is True the first round samples ``candidate_count``
    drafts from Hermes against the same habit selection and keeps the
    highest-scoring candidate. Revisions still use a single Hermes call.
    Each round record is also appended to ``history_store`` when supplied
    so external dashboards can read the durable JSONL trail.
    """
    active_runner = runner or HermesAgentRunner.from_env()
    trace_recorder = TraceRecorder(output_dir=OUTPUT_DIR, run_instance=run_instance)
    usecase_slug = _usecase_slug(profile)
    learned_habits = learn_reusable_habits(catalog)
    selected_habits = select_habits(profile, learned_habits)
    history: list[dict[str, Any]] = []
    durable_store = history_store
    active_session_id = session_id or _iso_now()

    trace_recorder.record_event(
        "loop",
        "started",
        usecase_slug=usecase_slug,
        context_slug=profile.context.slug,
        max_iterations=max_iterations,
    )
    trace_recorder.record_habits(
        stage="habit_learning",
        decision="promoted",
        habit_slugs=[habit.slug for habit in learned_habits],
        usecase_slug=usecase_slug,
    )
    trace_recorder.record_habits(
        stage="habit_selection",
        decision="selected",
        habit_slugs=[habit.slug for habit in selected_habits],
        usecase_slug=usecase_slug,
        expected_habits=(
            list(profile.usecase.expected_habit_slugs) if profile.usecase else []
        ),
    )

    response_text = ""
    evaluation: SkillEvaluationResult | None = None
    previous_response: str | None = None
    for round_number in range(1, max_iterations + 1):
        round_logs: list[str] = []
        llm_requests: list[dict[str, Any]] = []
        if round_number == 1:
            task_id = f"skill-mastery-draft-{round_number}"
            system_prompt = build_generation_system_prompt(profile, selected_habits)
            user_prompt = build_generation_user_prompt(profile)
            _emit_log(
                round_logs,
                log_sink,
                "ROUND_START",
                f"Skill Mastery round {round_number}/{max_iterations}.",
            )
            trace_recorder.record_event(
                "round",
                "started",
                round=round_number,
                usecase_slug=usecase_slug,
            )
            if use_reranker and candidate_count > 1:
                _emit_log(
                    round_logs,
                    log_sink,
                    "REQUESTING_LLM_DRAFT_RERANK",
                    "provider="
                    f"{getattr(active_runner, 'provider', None)} "
                    "model="
                    f"{getattr(active_runner, 'model', None)} "
                    f"task={task_id} candidates={candidate_count}",
                )
                result, rerank_records = _draft_with_reranker(
                    profile=profile,
                    selected_habits=selected_habits,
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    candidate_count=candidate_count,
                    runner=active_runner,
                    task_id=task_id,
                )
                llm_requests.extend(rerank_records)
                for record in rerank_records:
                    trace_recorder.record_llm_request(
                        round_number=round_number,
                        request=record,
                        usecase_slug=usecase_slug,
                    )
            else:
                _emit_log(
                    round_logs,
                    log_sink,
                    "REQUESTING_LLM_DRAFT",
                    "provider="
                    f"{getattr(active_runner, 'provider', None)} "
                    "model="
                    f"{getattr(active_runner, 'model', None)} "
                    f"task={task_id}",
                )
                result = active_runner.run_text(
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    task_id=task_id,
                )
                request_record = _build_llm_request_record(
                    active_runner,
                    request_kind="draft",
                    task_id=task_id,
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    response=result,
                )
                llm_requests.append(request_record)
                trace_recorder.record_llm_request(
                    round_number=round_number,
                    request=request_record,
                    usecase_slug=usecase_slug,
                )
        else:
            assert evaluation is not None
            task_id = f"skill-mastery-revision-{round_number}"
            system_prompt = REVISION_SYSTEM_PROMPT
            mutation_strategies = select_strategies(evaluation)
            mutation_brief = render_brief(mutation_strategies, profile, selected_habits)
            user_prompt = build_revision_user_prompt(
                profile,
                selected_habits,
                response_text,
                evaluation,
                user_feedback=mutation_brief,
            )
            _emit_log(
                round_logs,
                log_sink,
                "ROUND_START",
                f"Skill Mastery round {round_number}/{max_iterations}.",
            )
            trace_recorder.record_event(
                "round",
                "started",
                round=round_number,
                usecase_slug=usecase_slug,
            )
            _emit_log(
                round_logs,
                log_sink,
                "REQUESTING_LLM_REVISION",
                "provider="
                f"{getattr(active_runner, 'provider', None)} "
                "model="
                f"{getattr(active_runner, 'model', None)} "
                f"task={task_id}",
            )
            result = active_runner.run_text(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                task_id=task_id,
            )
            request_record = _build_llm_request_record(
                active_runner,
                request_kind="revision",
                task_id=task_id,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                response=result,
            )
            llm_requests.append(request_record)
            trace_recorder.record_llm_request(
                round_number=round_number,
                request=request_record,
                usecase_slug=usecase_slug,
            )

        response_text = result.text
        evaluation = evaluate_response(profile, selected_habits, response_text)
        _emit_log(
            round_logs,
            log_sink,
            "ROUND_SCORE",
            f"Score {evaluation.total_score}/{evaluation.max_score}.",
        )
        trace_recorder.record_evaluation(
            round_number=round_number,
            score=evaluation.total_score,
            total=evaluation.max_score,
            issues=evaluation.issues,
            strengths=evaluation.strengths,
            usecase_slug=usecase_slug,
        )
        entry = _serialize_round(round_number, response_text, evaluation)
        if previous_response is not None:
            mutation_diff = build_round_diff(previous_response, response_text)
            entry["mutation_diff"] = mutation_diff
            _emit_log(round_logs, log_sink, "RESPONSE_DIFF", mutation_diff)
        entry["logs"] = round_logs
        entry["llm"] = _build_llm_summary(active_runner, llm_requests)
        history.append(entry)
        if durable_store is not None:
            persisted = dict(entry)
            persisted["session_id"] = active_session_id
            persisted["usecase_slug"] = usecase_slug
            durable_store.append(persisted)
        previous_response = response_text
        if evaluation.total_score >= evaluation.max_score:
            break

    best = _best_round(history)
    trace_recorder.record_event(
        "loop",
        "completed",
        usecase_slug=usecase_slug,
        rounds=len(history),
        best_round=best["round"],
        best_score=best["score"],
        best_total=best["total"],
    )
    _write_outputs(
        profile,
        learned_habits,
        selected_habits,
        history,
        trace_metadata=trace_recorder.metadata(),
    )
    return history


def run_feedback_refinement(  # pylint: disable=too-many-arguments,too-many-locals
    profile: SkillMasteryProfile,
    selected_habits: list[LearnedHabit],
    *,
    current_response: str,
    round_number: int,
    user_feedback: str,
    runner: HermesAgentRunner | None = None,
    log_sink: LogSink | None = None,
) -> dict[str, Any]:
    """Run one extra Skill Mastery revision using explicit user feedback."""
    active_runner = runner or HermesAgentRunner.from_env()
    evaluation = evaluate_response(profile, selected_habits, current_response)
    round_logs: list[str] = []
    llm_requests: list[dict[str, Any]] = []
    task_id = f"skill-mastery-feedback-revision-{round_number}"
    user_prompt = build_revision_user_prompt(
        profile,
        selected_habits,
        current_response,
        evaluation,
        user_feedback=user_feedback,
    )
    _emit_log(
        round_logs,
        log_sink,
        "REQUESTING_LLM_REVISION",
        "provider="
        f"{getattr(active_runner, 'provider', None)} "
        "model="
        f"{getattr(active_runner, 'model', None)} "
        f"task={task_id}",
    )
    result = active_runner.run_text(
        system_prompt=REVISION_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        task_id=task_id,
    )
    llm_requests.append(
        _build_llm_request_record(
            active_runner,
            request_kind="revision",
            task_id=task_id,
            system_prompt=REVISION_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            response=result,
        )
    )
    updated_evaluation = evaluate_response(profile, selected_habits, result.text)
    mutation_diff = build_round_diff(current_response, result.text)
    _emit_log(round_logs, log_sink, "RESPONSE_DIFF", mutation_diff)
    entry = _serialize_round(
        round_number,
        result.text,
        updated_evaluation,
        user_feedback=user_feedback,
    )
    entry["logs"] = round_logs
    entry["llm"] = _build_llm_summary(active_runner, llm_requests)
    entry["mutation_diff"] = mutation_diff
    return entry
