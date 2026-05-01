"""Prompt evolution loop that mutates instructions with Hermes."""

from __future__ import annotations

from dataclasses import asdict, replace
from difflib import unified_diff
import json
from datetime import datetime, timezone
from pathlib import Path
import re
from typing import Any, Callable

import util

from prompt_evolution.config import (
    PolicyPoint,
    PromptEvolutionCatalog,
    SelectionProfile,
)
from prompt_evolution.evaluator import EvaluationResult, evaluate_response
from prompt_evolution.hermes_client import HermesAgentRunner, HermesResponse
from prompt_evolution.mutation_playbook import render_brief, select_strategies
from prompt_evolution.reranker import rerank_drafts
from prompt_evolution.tracing import TraceRecorder

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EXAMPLE_ROOT = PROJECT_ROOT / "prompt_evolution"
DATA_DIR = EXAMPLE_ROOT / ".data"
OUTPUT_DIR = EXAMPLE_ROOT / ".output"
README_PATH = EXAMPLE_ROOT / "README.md"

util.load_env()

LogSink = Callable[[str], None]

POLICY_OVERRIDE_HEADERS = frozenset(
    {
        "additional policy details:",
        "policy coverage points:",
        "required policy points:",
    }
)
POLICY_STOPWORDS = frozenset(
    {
        "the",
        "and",
        "for",
        "after",
        "before",
        "with",
        "can",
        "are",
        "is",
        "that",
        "this",
        "from",
        "into",
        "your",
        "our",
    }
)
POLICY_ANCHOR_PHRASES = (
    "attendance check",
    "front desk",
    "support can reissue",
    "reissue building access",
    "guest bookings",
    "day-pass refunds",
    "tool certification",
    "certification badge",
    "confirm the booking",
    "booking window",
    "bench bookings",
    "membership lead",
)


def _iso_now() -> str:
    """Return the current UTC timestamp in ISO-8601 form."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _read_utf8_text(path: Path) -> str:
    """Read one UTF-8 text file."""
    return path.read_text(encoding="utf-8")


def build_round_diff(before_text: str, after_text: str) -> str:
    """Render a unified diff for the mutable instruction artifact."""
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


def _extract_policy_override_descriptions(instructions: str) -> tuple[str, ...]:
    """Read policy override bullets that a mutation added to the instructions."""
    override_descriptions: list[str] = []
    in_override_section = False
    for raw_line in instructions.splitlines():
        stripped = raw_line.strip()
        if stripped.lower() in POLICY_OVERRIDE_HEADERS:
            in_override_section = True
            continue
        if not in_override_section:
            continue
        if not stripped:
            if override_descriptions:
                break
            continue
        if stripped.startswith("- "):
            override_descriptions.append(stripped[2:].strip())
            continue
        if override_descriptions:
            break
    return tuple(description for description in override_descriptions if description)


def _policy_terms(text: str) -> set[str]:
    """Extract normalized terms for lightweight policy matching."""
    terms = set(re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)?", text.lower()))
    return {term for term in terms if len(term) > 2 and term not in POLICY_STOPWORDS}


def _policy_keywords_from_description(description: str) -> tuple[str, ...]:
    """Derive a few evaluator keywords from one policy description."""
    normalized = description.strip().rstrip(".").lower()
    keywords: list[str] = [normalized]

    duration_match = re.search(
        r"\b\d+\s*(?:hour|hours|minute|minutes)\b",
        normalized,
    )
    if duration_match:
        keywords.append(duration_match.group(0))

    for phrase in POLICY_ANCHOR_PHRASES:
        if phrase in normalized:
            keywords.append(phrase)

    tokens = re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)?", normalized)
    if len(tokens) >= 2:
        keywords.append(" ".join(tokens[:2]))
    if len(tokens) >= 4:
        keywords.append(" ".join(tokens[-2:]))

    return tuple(dict.fromkeys(keyword for keyword in keywords if keyword))


def _override_policy_points(
    profile: SelectionProfile,
    instructions: str,
) -> tuple[PolicyPoint, ...]:
    """Apply instruction-level policy corrections to the active context pack."""
    override_descriptions = _extract_policy_override_descriptions(instructions)
    if not override_descriptions:
        return profile.context.required_policy_points

    updated_points = list(profile.context.required_policy_points)
    used_indexes: set[int] = set()
    appended_points: list[PolicyPoint] = []

    for description in override_descriptions:
        override_terms = _policy_terms(description)
        best_index: int | None = None
        best_score = 0
        for index, policy in enumerate(updated_points):
            if index in used_indexes:
                continue
            score = len(override_terms & _policy_terms(policy.description))
            if score > best_score:
                best_index = index
                best_score = score

        if best_index is None:
            appended_points.append(
                PolicyPoint(
                    slug=f"override_{len(appended_points) + 1}",
                    description=description,
                    keywords=_policy_keywords_from_description(description),
                )
            )
            continue

        existing_policy = updated_points[best_index]
        preserved_keywords = tuple(
            keyword
            for keyword in existing_policy.keywords
            if not any(character.isdigit() for character in keyword)
        )
        updated_points[best_index] = PolicyPoint(
            slug=existing_policy.slug,
            description=description,
            keywords=tuple(
                dict.fromkeys(
                    _policy_keywords_from_description(description) + preserved_keywords
                )
            ),
        )
        used_indexes.add(best_index)

    return tuple(updated_points + appended_points)


def _effective_profile_for_instructions(
    profile: SelectionProfile,
    instructions: str,
) -> SelectionProfile:
    """Return a profile whose policy points reflect instruction-level corrections."""
    effective_policy_points = _override_policy_points(profile, instructions)
    if effective_policy_points == profile.context.required_policy_points:
        return profile
    return replace(
        profile,
        context=replace(
            profile.context,
            required_policy_points=effective_policy_points,
        ),
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


def load_mutable_instructions(readme_path: Path = README_PATH) -> str:
    """Extract the mutable instruction block from the example README."""
    lines = _read_utf8_text(readme_path).splitlines()
    in_section = False
    in_fence = False
    captured: list[str] = []

    for line in lines:
        if line.strip() == "## Mutable Instructions":
            in_section = True
            continue
        if in_section and line.startswith("## ") and not in_fence:
            break
        if not in_section:
            continue
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            captured.append(line)

    if not captured:
        raise ValueError(
            "Could not find a fenced mutable instruction block in README.md"
        )
    return "\n".join(captured).strip()


def _preference_brief(
    profile: SelectionProfile, catalog: PromptEvolutionCatalog
) -> str:
    """Render selected preferences as instruction bullets."""
    return "\n".join(profile.preference_lines(catalog))


def _scenario_slug(profile: SelectionProfile) -> str | None:
    """Return the active scenario slug when the run came from a scenario."""
    if profile.scenario is None:
        return None
    return profile.scenario.slug


def _scenario_brief(profile: SelectionProfile) -> str:
    """Render scenario facts for the generation prompt when available."""
    if profile.scenario is None:
        return ""
    scenario = profile.scenario
    facts = "\n".join(f"- {item}" for item in scenario.customer_facts)
    risk_flags = "\n".join(f"- {item}" for item in scenario.risk_flags)
    criteria = "\n".join(f"- {item}" for item in scenario.success_criteria)
    return (
        f"## Scenario Case\n"
        f"Case: {scenario.label}\n"
        f"Customer Facts\n{facts}\n\n"
        f"Risk Flags\n{risk_flags}\n\n"
        f"Success Criteria\n{criteria}\n\n"
    )


def build_generation_system_prompt(
    instructions: str,
    catalog: PromptEvolutionCatalog,
    profile: SelectionProfile,
) -> str:
    """Build the system prompt that Hermes uses to draft the reply."""
    effective_profile = _effective_profile_for_instructions(profile, instructions)
    policies = "\n".join(
        f"- {policy.description}"
        for policy in effective_profile.context.required_policy_points
    )
    forbidden = "\n".join(
        f"- {claim}" for claim in effective_profile.context.forbidden_claims
    )
    return (
        f"{instructions}\n\n"
        f"{_scenario_brief(effective_profile)}"
        f"## Context Pack\n"
        f"Context: {effective_profile.context.label}\n"
        f"Service Summary: {effective_profile.context.service_summary}\n"
        f"Brand Voice: {effective_profile.context.brand_voice}\n"
        f"Escalation Path: {effective_profile.context.escalation_path}\n\n"
        f"## Selected Preferences\n{_preference_brief(effective_profile, catalog)}\n\n"
        f"## Required Policy Points\n{policies}\n\n"
        f"## Forbidden Claims\n{forbidden}\n"
    )


def build_generation_user_prompt(profile: SelectionProfile) -> str:
    """Build the user prompt Hermes sees for the customer issue."""
    return (
        "Draft one customer-ready reply for this issue. Do not explain your reasoning. "
        "Return only the final message.\n\n"
        f"Customer problem:\n{profile.problem}\n"
    )


def build_user_feedback_guide(
    catalog: PromptEvolutionCatalog,
    profile: SelectionProfile,
) -> str:
    """Explain what follow-up feedback the user can give after the first draft."""
    first_policy = profile.context.required_policy_points[0].description
    example_preference_line = profile.preference_lines(catalog)[0].removeprefix("- ")
    context_terms = ", ".join(profile.context.reference_terms[:3])
    return (
        "What you can ask to improve next:\n"
        "- Preference fit: ask it to stay closer to "
        f"{example_preference_line}.\n"
        '  If you say "make it warmer", expect softer wording and more empathy.\n'
        "- Structure: ask for bullets, short paragraphs, or a checklist.\n"
        '  If you say "switch to bullets", expect the next draft to change layout first.\n'
        f"- Context grounding: ask it to mention policy or service terms such as {context_terms}.\n"
        '  If you say "mention '
        f'{first_policy.lower()} earlier", expect that policy to move closer to the top.\n'
        "- Closing move: ask for one direct question, one next step, or a named owner.\n"
        '  If you say "end with one clear question", expect a stronger closing action.\n'
        "You can also give feedback like: make it shorter, sound more direct, "
        "cite tool certification earlier, or offer two options."
    )


MUTATION_SYSTEM_PROMPT = (
    "You refine instruction prompts for a support-reply agent. "
    "Keep the instructions concise, concrete, and reusable. "
    "Return only the revised instructions inside one ```text fenced block."
)


def build_mutation_user_prompt(
    current_instructions: str,
    profile: SelectionProfile,
    evaluation: EvaluationResult,
    response_text: str,
    user_feedback: str | None = None,
) -> str:
    """Build the mutation brief Hermes uses to improve the instructions."""
    issues = "\n".join(f"- {issue}" for issue in evaluation.issues) or "- None"
    strengths = "\n".join(f"- {item}" for item in evaluation.strengths) or "- None"
    preference_lines = "\n".join(
        f"- {axis}={value}" for axis, value in profile.selected_preferences.items()
    )
    feedback_block = ""
    if user_feedback:
        feedback_block = f"User feedback for the next draft:\n- {user_feedback}\n\n"
    strategies = select_strategies(evaluation)
    playbook_brief = render_brief(strategies, profile)
    return (
        f"Current instructions:\n```text\n{current_instructions}\n```\n\n"
        f"Context: {profile.context.label}\n"
        f"Selected preferences:\n{preference_lines}\n\n"
        f"Customer problem:\n{profile.problem}\n\n"
        f"Candidate response:\n{response_text}\n\n"
        f"{feedback_block}"
        f"Strengths:\n{strengths}\n\n"
        f"Issues to fix:\n{issues}\n\n"
        f"Mutation playbook brief:\n{playbook_brief}\n\n"
        "Revise the instructions so the next draft is more policy-grounded and closer "
        "to the chosen preferences."
    )


def _extract_text_fence(text: str) -> str:
    """Extract a fenced text block and fall back to the raw response."""
    marker = "```text"
    if marker not in text:
        return text.strip()
    _, _, remainder = text.partition(marker)
    fenced, _, _ = remainder.partition("```")
    return fenced.strip()


def _serialize_round(
    round_number: int,
    instructions: str,
    response_text: str,
    evaluation: EvaluationResult,
    user_feedback: str | None = None,
) -> dict[str, Any]:
    """Convert one round into a JSON-safe history record."""
    payload = {
        "round": round_number,
        "instructions": instructions,
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
    profile: SelectionProfile,
    history: list[dict[str, Any]],
    trace_metadata: dict[str, Any] | None = None,
) -> None:
    """Persist the latest session, best instructions, and best response."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    best = _best_round(history)
    active_trace_metadata = trace_metadata or _existing_trace_metadata()
    session_payload = {
        "generated_at": _iso_now(),
        "problem": profile.problem,
        "scenario": asdict(profile.scenario) if profile.scenario else None,
        "context": asdict(profile.context),
        "selected_preferences": profile.selected_preferences,
        "rounds": history,
        "best_round": best["round"],
    }
    if active_trace_metadata is not None:
        session_payload["trace"] = active_trace_metadata
    (OUTPUT_DIR / "latest_session.json").write_text(
        json.dumps(session_payload, indent=2),
        encoding="utf-8",
    )
    (OUTPUT_DIR / "best_instructions.md").write_text(
        str(best["instructions"]),
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


def save_outputs(profile: SelectionProfile, history: list[dict[str, Any]]) -> None:
    """Persist prompt evolution outputs after extra feedback-driven revisions."""
    _write_outputs(profile, history)


def reset_outputs() -> None:
    """Delete the prompt evolution output directory if it exists."""
    if not OUTPUT_DIR.exists():
        return
    import shutil  # pylint: disable=import-outside-toplevel

    shutil.rmtree(OUTPUT_DIR)


def run_prompt_evolution(  # pylint: disable=too-many-locals,too-many-arguments,too-many-statements
    catalog: PromptEvolutionCatalog,
    profile: SelectionProfile,
    *,
    max_iterations: int = 3,
    runner: HermesAgentRunner | None = None,
    log_sink: LogSink | None = None,
    run_instance: str | None = None,
    use_reranker: bool = False,
    candidate_count: int = 3,
) -> list[dict[str, Any]]:
    """Run the instruction-mutation loop until the score stops improving or maxes out."""
    active_runner = runner or HermesAgentRunner.from_env()
    trace_recorder = TraceRecorder(output_dir=OUTPUT_DIR, run_instance=run_instance)
    scenario_slug = _scenario_slug(profile)
    current_instructions = load_mutable_instructions()
    history: list[dict[str, Any]] = []
    pending_mutation_diff: str | None = None

    trace_recorder.record_event(
        "loop",
        "started",
        scenario_slug=scenario_slug,
        context_slug=profile.context.slug,
        max_iterations=max_iterations,
        preference_count=len(profile.selected_preferences),
    )

    for round_number in range(1, max_iterations + 1):
        round_logs: list[str] = []
        llm_requests: list[dict[str, Any]] = []
        round_task_id = f"prompt-evolution-draft-{round_number}"
        effective_profile = _effective_profile_for_instructions(
            profile,
            current_instructions,
        )
        system_prompt = build_generation_system_prompt(
            current_instructions,
            catalog,
            effective_profile,
        )
        user_prompt = build_generation_user_prompt(profile)

        _emit_log(
            round_logs,
            log_sink,
            "ROUND_START",
            f"Prompt Evolution round {round_number}/{max_iterations}.",
        )
        trace_recorder.record_event(
            "round",
            "started",
            round=round_number,
            scenario_slug=scenario_slug,
        )
        if pending_mutation_diff is not None:
            _emit_log(round_logs, log_sink, "INSTRUCTION_DIFF", pending_mutation_diff)
        _emit_log(
            round_logs,
            log_sink,
            "REQUESTING_LLM_DRAFT",
            "provider="
            f"{getattr(active_runner, 'provider', None)} "
            "model="
            f"{getattr(active_runner, 'model', None)} "
            f"task={round_task_id}",
        )
        if use_reranker and candidate_count > 1:
            rerank_result = rerank_drafts(
                catalog=catalog,
                profile=effective_profile,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                candidate_count=candidate_count,
                runner=active_runner,
                base_task_id=f"prompt-evolution-rerank-{round_number}",
            )
            best_candidate = rerank_result.best
            draft_result = HermesResponse(
                text=best_candidate.response_text,
                messages=[],
                task_id=best_candidate.task_id,
                raw_output="",
            )
            entry_extra_rerank: dict[str, Any] | None = {
                "candidate_count": len(rerank_result.candidates),
                "best_candidate_index": rerank_result.best_index,
                "candidate_scores": [
                    {
                        "index": candidate.candidate_index,
                        "score": candidate.evaluation.total_score,
                        "total": candidate.evaluation.max_score,
                        "task_id": candidate.task_id,
                    }
                    for candidate in rerank_result.candidates
                ],
            }
            _emit_log(
                round_logs,
                log_sink,
                "RERANK_SELECTED",
                f"best candidate {rerank_result.best_index + 1}"
                f"/{len(rerank_result.candidates)}",
            )
        else:
            draft_result = active_runner.run_text(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                task_id=round_task_id,
            )
            entry_extra_rerank = None
        draft_request_record = _build_llm_request_record(
            active_runner,
            request_kind="draft",
            task_id=round_task_id,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response=draft_result,
        )
        llm_requests.append(draft_request_record)
        trace_recorder.record_llm_request(
            round_number=round_number,
            request=draft_request_record,
            scenario_slug=scenario_slug,
        )
        _emit_log(
            round_logs,
            log_sink,
            "DRAFT_RECEIVED",
            f"Received {len(draft_result.text)} characters from the LLM.",
        )
        evaluation = evaluate_response(effective_profile, draft_result.text)
        entry = _serialize_round(
            round_number,
            current_instructions,
            draft_result.text,
            evaluation,
        )
        entry["logs"] = round_logs
        entry["llm"] = _build_llm_summary(active_runner, llm_requests)
        if entry_extra_rerank is not None:
            entry["rerank"] = entry_extra_rerank
        if pending_mutation_diff is not None:
            entry["mutation_diff"] = pending_mutation_diff
            pending_mutation_diff = None
        history.append(entry)
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
            scenario_slug=scenario_slug,
        )
        if evaluation.total_score >= evaluation.max_score:
            break
        mutation_task_id = f"prompt-evolution-mutation-{round_number}"
        mutation_user_prompt = build_mutation_user_prompt(
            current_instructions,
            profile,
            evaluation,
            draft_result.text,
        )
        _emit_log(
            round_logs,
            log_sink,
            "REQUESTING_LLM_MUTATION",
            "provider="
            f"{getattr(active_runner, 'provider', None)} "
            "model="
            f"{getattr(active_runner, 'model', None)} "
            f"task={mutation_task_id}",
        )
        mutation_result = active_runner.run_text(
            system_prompt=MUTATION_SYSTEM_PROMPT,
            user_prompt=mutation_user_prompt,
            task_id=mutation_task_id,
        )
        mutation_request_record = _build_llm_request_record(
            active_runner,
            request_kind="mutation",
            task_id=mutation_task_id,
            system_prompt=MUTATION_SYSTEM_PROMPT,
            user_prompt=mutation_user_prompt,
            response=mutation_result,
        )
        llm_requests.append(mutation_request_record)
        trace_recorder.record_llm_request(
            round_number=round_number,
            request=mutation_request_record,
            scenario_slug=scenario_slug,
        )
        entry["llm"] = _build_llm_summary(active_runner, llm_requests)
        updated_instructions = _extract_text_fence(mutation_result.text)
        pending_mutation_diff = build_round_diff(
            current_instructions,
            updated_instructions,
        )
        _emit_log(
            round_logs,
            log_sink,
            "INSTRUCTION_DIFF",
            pending_mutation_diff,
        )
        trace_recorder.record_event(
            "instruction_mutation",
            "prepared",
            round=round_number,
            scenario_slug=scenario_slug,
            changed=current_instructions != updated_instructions,
            diff_chars=len(pending_mutation_diff),
        )
        current_instructions = updated_instructions

    best = _best_round(history)
    trace_recorder.record_event(
        "loop",
        "completed",
        scenario_slug=scenario_slug,
        rounds=len(history),
        best_round=best["round"],
        best_score=best["score"],
        best_total=best["total"],
    )
    _write_outputs(profile, history, trace_metadata=trace_recorder.metadata())
    return history


def run_feedback_refinement(  # pylint: disable=too-many-arguments,too-many-locals
    catalog: PromptEvolutionCatalog,
    profile: SelectionProfile,
    *,
    current_instructions: str,
    current_response: str,
    round_number: int,
    user_feedback: str,
    runner: HermesAgentRunner | None = None,
    log_sink: LogSink | None = None,
) -> dict[str, Any]:
    """Run one extra prompt-evolution revision using explicit user feedback."""
    active_runner = runner or HermesAgentRunner.from_env()
    current_profile = _effective_profile_for_instructions(
        profile,
        current_instructions,
    )
    evaluation = evaluate_response(current_profile, current_response)
    round_logs: list[str] = []
    llm_requests: list[dict[str, Any]] = []
    mutation_task_id = f"prompt-evolution-feedback-mutation-{round_number}"
    mutation_user_prompt = build_mutation_user_prompt(
        current_instructions,
        profile,
        evaluation,
        current_response,
        user_feedback=user_feedback,
    )
    _emit_log(
        round_logs,
        log_sink,
        "REQUESTING_LLM_MUTATION",
        "provider="
        f"{getattr(active_runner, 'provider', None)} "
        "model="
        f"{getattr(active_runner, 'model', None)} "
        f"task={mutation_task_id}",
    )
    mutation_result = active_runner.run_text(
        system_prompt=MUTATION_SYSTEM_PROMPT,
        user_prompt=mutation_user_prompt,
        task_id=mutation_task_id,
    )
    llm_requests.append(
        _build_llm_request_record(
            active_runner,
            request_kind="mutation",
            task_id=mutation_task_id,
            system_prompt=MUTATION_SYSTEM_PROMPT,
            user_prompt=mutation_user_prompt,
            response=mutation_result,
        )
    )
    updated_instructions = _extract_text_fence(mutation_result.text)
    mutation_diff = build_round_diff(current_instructions, updated_instructions)
    _emit_log(round_logs, log_sink, "INSTRUCTION_DIFF", mutation_diff)
    draft_task_id = f"prompt-evolution-feedback-draft-{round_number}"
    updated_profile = _effective_profile_for_instructions(
        profile,
        updated_instructions,
    )
    system_prompt = build_generation_system_prompt(
        updated_instructions,
        catalog,
        updated_profile,
    )
    user_prompt = build_generation_user_prompt(profile)
    _emit_log(
        round_logs,
        log_sink,
        "REQUESTING_LLM_DRAFT",
        "provider="
        f"{getattr(active_runner, 'provider', None)} "
        "model="
        f"{getattr(active_runner, 'model', None)} "
        f"task={draft_task_id}",
    )
    draft_result = active_runner.run_text(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        task_id=draft_task_id,
    )
    llm_requests.append(
        _build_llm_request_record(
            active_runner,
            request_kind="draft",
            task_id=draft_task_id,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response=draft_result,
        )
    )
    updated_evaluation = evaluate_response(updated_profile, draft_result.text)
    entry = _serialize_round(
        round_number,
        updated_instructions,
        draft_result.text,
        updated_evaluation,
        user_feedback=user_feedback,
    )
    entry["logs"] = round_logs
    entry["llm"] = _build_llm_summary(active_runner, llm_requests)
    entry["mutation_diff"] = mutation_diff
    return entry
