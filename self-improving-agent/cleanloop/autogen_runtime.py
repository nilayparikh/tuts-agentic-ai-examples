"""AutoGen-backed proposal, judge, and observability helpers for CleanLoop."""

# pylint: disable=too-many-arguments,too-many-locals

from __future__ import annotations

import asyncio
import importlib
import json
from typing import Any, Callable, TypeVar, TypedDict

from pydantic import BaseModel, Field


class MutationProposal(BaseModel):
    """Structured mutation proposal returned by the AutoGen proposer."""

    hypothesis: str = Field(
        description="One-line explanation of the intended mutation."
    )
    clean_data_py: str = Field(description="The complete clean_data.py file content.")
    mutation_summary: str = Field(description="Short summary of what changed and why.")


class CandidateSelection(BaseModel):
    """Judge decision for reranked candidate mutations."""

    selected_index: int = Field(description="1-based index of the winning candidate.")
    rationale: str = Field(description="Why this candidate is the best next genome.")


class CandidateRecord(TypedDict):
    """Candidate mutation with evaluation metadata."""

    index: int
    style: str
    score: int
    total: int
    hypothesis: str
    code: str
    attempt: dict[str, object]


StructuredOutputT = TypeVar("StructuredOutputT", bound=BaseModel)


def summarize_attempts(
    attempts: list[dict[str, object]],
    *,
    selected_label: str | None = None,
    judge: dict[str, object] | None = None,
) -> dict[str, object]:
    """Summarize one or more AutoGen attempts into the loop dashboard shape."""
    prompt_tokens = 0
    completion_tokens = 0
    total_tokens = 0
    saw_usage = False
    selected_attempt = selected_label or "none"

    for attempt in attempts:
        usage = attempt.get("usage")
        if not isinstance(usage, dict):
            continue
        attempt_prompt = usage.get("prompt_tokens")
        attempt_completion = usage.get("completion_tokens")
        attempt_total = usage.get("total_tokens")
        if isinstance(attempt_prompt, int):
            prompt_tokens += attempt_prompt
            saw_usage = True
        if isinstance(attempt_completion, int):
            completion_tokens += attempt_completion
            saw_usage = True
        if isinstance(attempt_total, int):
            total_tokens += attempt_total
            saw_usage = True
        if selected_attempt == "none" and attempt.get("code_found"):
            selected_attempt = str(attempt.get("label", "none"))

    summary: dict[str, object] = {
        "selected_attempt": selected_attempt,
        "attempts": attempts,
        "prompt_tokens": prompt_tokens if saw_usage else None,
        "completion_tokens": completion_tokens if saw_usage else None,
        "total_tokens": total_tokens if saw_usage else None,
    }
    if judge is not None:
        summary["judge"] = judge
    return summary


def propose_single_mutation(
    client: Any,
    model: str,
    system_prompt: str,
    user_prompt: str,
    *,
    label: str = "AutoGen proposer",
    max_tokens: int = 2200,
) -> tuple[str | None, str, dict[str, object]]:  # pylint: disable=too-many-arguments
    """Generate one structured mutation proposal with AutoGen."""
    # Keep the proposer path strongly typed so the loop can safely read the
    # structured fields instead of treating every response as a generic blob.
    proposal, events, usage = _run_structured_agent(
        client=client,
        system_prompt=system_prompt,
        task=user_prompt,
        output_type=MutationProposal,
        agent_name="cleanloop_proposer",
    )
    code = proposal.clean_data_py.strip() or None
    hypothesis = proposal.hypothesis.strip() or "no hypothesis"
    response_preview = proposal.model_dump_json(indent=2)
    attempt = {
        "label": label,
        "model": model,
        "max_tokens": max_tokens,
        "code_found": bool(code),
        "hypothesis": hypothesis,
        "usage": usage,
        "prompt_chars": len(system_prompt) + len(user_prompt),
        "response_chars": len(response_preview),
        "messages": [
            {
                "role": "system",
                "chars": len(system_prompt),
                "lines": len(system_prompt.splitlines()),
                "preview": system_prompt[:180],
            },
            {
                "role": "user",
                "chars": len(user_prompt),
                "lines": len(user_prompt.splitlines()),
                "preview": user_prompt[:180],
            },
        ],
        "response_preview": response_preview[:400],
        "autogen_events": events,
        "mutation_summary": proposal.mutation_summary,
    }
    return code, hypothesis, attempt


def propose_reranked_mutation(
    client: Any,
    model: str,
    system_prompt: str,
    user_prompt: str,
    *,
    n_candidates: int,
    evaluate_candidate: Callable[[str], tuple[int, int]],
) -> tuple[str | None, str, dict[str, object]]:
    """Generate multiple candidates, score them, and judge the best survivor."""
    candidate_styles = [
        (
            "conservative",
            "Make the smallest safe mutation that preserves the existing genome shape.",
        ),
        (
            "value-first",
            "Prioritize numeric value normalization and accounting markers first.",
        ),
        (
            "reconciliation-first",
            "Prioritize missing and unexpected row reconciliation first.",
        ),
        (
            "date-first",
            "Prioritize mixed date parsing and stable row retention first.",
        ),
        (
            "bold",
            "Allow a broader refactor inside clean() if it improves correctness "
            "without touching imports.",
        ),
    ]
    attempts: list[dict[str, object]] = []
    candidates: list[CandidateRecord] = []

    for index, (style_name, style_instruction) in enumerate(
        candidate_styles[:n_candidates], start=1
    ):
        code, hypothesis, attempt = propose_single_mutation(
            client,
            model,
            f"{system_prompt}\n\n## Candidate Style\n{style_instruction}",
            user_prompt,
            label=f"AutoGen candidate {index}: {style_name}",
        )
        if not code:
            attempts.append(attempt)
            continue

        score, total = evaluate_candidate(code)
        attempt["candidate_index"] = index
        attempt["candidate_style"] = style_name
        attempt["candidate_score"] = score
        attempt["candidate_total"] = total
        attempts.append(attempt)
        candidates.append(
            {
                "index": index,
                "style": style_name,
                "score": score,
                "total": total,
                "hypothesis": hypothesis,
                "code": code,
                "attempt": attempt,
            }
        )

    if not candidates:
        return None, "no hypothesis", summarize_attempts(attempts)

    best_candidates = sorted(
        candidates, key=lambda item: (item["score"], -item["index"]), reverse=True
    )
    selected = best_candidates[0]
    judge_summary: dict[str, object] | None = None

    tied_candidates = [
        candidate
        for candidate in best_candidates
        if candidate["score"] == selected["score"]
    ]
    if len(tied_candidates) > 1:
        # Deterministic score gets candidates to the tie. The judge only breaks
        # ties between equally scoring mutations by preferring the safer change.
        judge_decision, events, usage = _run_structured_agent(
            client=client,
            system_prompt=(
                "You are the CleanLoop judge. Pick the safest mutation with "
                "the best score. Favor higher fixed-evaluation score first, "
                "then prefer the narrower hypothesis."
            ),
            task=_build_judge_task(tied_candidates),
            output_type=CandidateSelection,
            agent_name="cleanloop_judge",
        )
        judge_winner = next(
            (
                candidate
                for candidate in tied_candidates
                if candidate["index"] == int(judge_decision.selected_index)
            ),
            selected,
        )
        selected = judge_winner
        judge_summary = {
            "selected_index": judge_decision.selected_index,
            "rationale": judge_decision.rationale,
            "usage": usage,
            "events": events,
        }

    selected_attempt = selected["attempt"]
    diagnostics = summarize_attempts(
        attempts,
        selected_label=str(selected_attempt.get("label", "none")),
        judge=judge_summary,
    )
    return (
        str(selected["code"]),
        str(selected["hypothesis"]),
        diagnostics,
    )


def _build_judge_task(candidates: list[CandidateRecord]) -> str:
    """Build the selection task for the AutoGen judge agent."""
    lines = [
        "Pick the best candidate using 1-based indexing.",
        "Favor higher fixed judge score first. Break ties using the safer, "
        "narrower mutation.",
        "",
        "Candidates:",
    ]
    for candidate in candidates:
        lines.append(
            (
                f"- {candidate['index']}: style={candidate['style']}, "
                f"score={candidate['score']}/{candidate['total']}, "
                f"hypothesis={candidate['hypothesis']}"
            )
        )
    return "\n".join(lines)


def _run_structured_agent(
    *,
    client: Any,
    system_prompt: str,
    task: str,
    output_type: type[StructuredOutputT],
    agent_name: str,
) -> tuple[StructuredOutputT, list[dict[str, object]], dict[str, int | None]]:
    """Run one AutoGen agent task and return structured output plus observability."""
    return _run_coro(
        _run_structured_agent_async(
            client=client,
            system_prompt=system_prompt,
            task=task,
            output_type=output_type,
            agent_name=agent_name,
        )
    )


async def _run_structured_agent_async(
    *,
    client: Any,
    system_prompt: str,
    task: str,
    output_type: type[StructuredOutputT],
    agent_name: str,
) -> tuple[StructuredOutputT, list[dict[str, object]], dict[str, int | None]]:
    """Async worker for one structured AutoGen task."""
    assistant_agent_class, structured_message_class = _require_autogen_types()
    agent = assistant_agent_class(
        name=agent_name,
        model_client=client,
        system_message=system_prompt,
        output_content_type=output_type,
        model_client_stream=True,
    )

    events: list[dict[str, object]] = []
    final_task_result = None
    try:
        async for message in agent.run_stream(task=task):
            events.append(_serialize_stream_event(message))
            if message.__class__.__name__ == "TaskResult":
                final_task_result = message
    except Exception as exc:  # pylint: disable=broad-exception-caught
        if _requires_json_object_fallback(exc):
            return await _run_json_object_fallback(
                client=client,
                system_prompt=system_prompt,
                task=task,
                output_type=output_type,
                agent_name=agent_name,
                original_error=exc,
            )
        raise

    if final_task_result is None:
        raise RuntimeError(
            "AutoGen did not return a TaskResult for the mutation request."
        )

    final_message = final_task_result.messages[-1]
    if not isinstance(final_message, structured_message_class):
        raise RuntimeError(
            f"AutoGen returned {final_message.__class__.__name__} instead of structured output."
        )

    content = final_message.content
    if not isinstance(content, output_type):
        content = output_type.model_validate(content)
    usage = _usage_from_task_result(final_task_result)
    return content, events, usage


async def _run_json_object_fallback(
    *,
    client: Any,
    system_prompt: str,
    task: str,
    output_type: type[StructuredOutputT],
    agent_name: str,
    original_error: Exception,
) -> tuple[StructuredOutputT, list[dict[str, object]], dict[str, int | None]]:
    """Fallback to model-client JSON mode when provider rejects json_schema output."""
    models_module = importlib.import_module("autogen_core.models")
    system_message_class = getattr(models_module, "SystemMessage")
    user_message_class = getattr(models_module, "UserMessage")
    schema = json.dumps(output_type.model_json_schema(), indent=2)
    fallback_prompt = (
        f"{task}\n\n"
        "Return only one JSON object that matches this schema exactly. "
        "Do not wrap it in markdown fences.\n\n"
        f"JSON Schema:\n{schema}"
    )
    response = await client.create(
        messages=[
            system_message_class(content=system_prompt),
            user_message_class(content=fallback_prompt, source="user"),
        ],
        extra_create_args={"response_format": {"type": "json_object"}},
    )
    content = getattr(response, "content", "")
    if not isinstance(content, str):
        raise RuntimeError(
            "AutoGen JSON fallback expected a text response but received "
            f"{type(content).__name__}."
        )
    parsed = output_type.model_validate(json.loads(content))
    events: list[dict[str, object]] = [
        {
            "type": "StructuredOutputFallback",
            "source": agent_name,
            "preview": str(original_error)[:180],
        },
        {
            "type": "JsonObjectResponse",
            "source": agent_name,
            "preview": content[:180],
        },
    ]
    return parsed, events, _usage_from_response(response)


def _require_autogen_types() -> tuple[Any, Any]:
    """Import the AutoGen agent/message classes on demand."""
    try:
        agents_module = importlib.import_module("autogen_agentchat.agents")
        messages_module = importlib.import_module("autogen_agentchat.messages")
    except ImportError as exc:
        raise RuntimeError(
            "AutoGen dependencies are not installed. Run pip install -r ../requirements.txt "
            "from cleanloop/, or python ../util.py setup from the example root."
        ) from exc

    return getattr(agents_module, "AssistantAgent"), getattr(
        messages_module, "StructuredMessage"
    )


def _requires_json_object_fallback(exc: Exception) -> bool:
    """Return whether a provider rejected AutoGen json_schema structured output."""
    text = str(exc).lower()
    return "json_schema" in text and "json_object" in text


def _usage_from_response(response: Any) -> dict[str, int | None]:
    """Extract token usage from a direct model client response."""
    usage = getattr(response, "usage", None)
    if usage is None:
        return {
            "prompt_tokens": None,
            "completion_tokens": None,
            "total_tokens": None,
        }
    prompt_tokens = getattr(usage, "prompt_tokens", None)
    completion_tokens = getattr(usage, "completion_tokens", None)
    total_tokens = getattr(usage, "total_tokens", None)
    return {
        "prompt_tokens": prompt_tokens if isinstance(prompt_tokens, int) else None,
        "completion_tokens": (
            completion_tokens if isinstance(completion_tokens, int) else None
        ),
        "total_tokens": total_tokens if isinstance(total_tokens, int) else None,
    }


def _usage_from_task_result(task_result: Any) -> dict[str, int | None]:
    """Aggregate token usage from the final AutoGen task result."""
    prompt_tokens = 0
    completion_tokens = 0
    saw_usage = False
    for message in getattr(task_result, "messages", []):
        models_usage = getattr(message, "models_usage", None)
        if models_usage is None:
            continue
        prompt_value = getattr(models_usage, "prompt_tokens", None)
        completion_value = getattr(models_usage, "completion_tokens", None)
        if isinstance(prompt_value, int):
            prompt_tokens += prompt_value
            saw_usage = True
        if isinstance(completion_value, int):
            completion_tokens += completion_value
            saw_usage = True
    return {
        "prompt_tokens": prompt_tokens if saw_usage else None,
        "completion_tokens": completion_tokens if saw_usage else None,
        "total_tokens": (prompt_tokens + completion_tokens) if saw_usage else None,
    }


def _serialize_stream_event(message: Any) -> dict[str, object]:
    """Convert one AutoGen stream event into a history-safe snapshot."""
    content = getattr(message, "content", None)
    preview = _preview_content(content)
    return {
        "type": message.__class__.__name__,
        "source": getattr(message, "source", None),
        "preview": preview[:180],
    }


def _preview_content(content: Any) -> str:
    """Return a compact printable preview for one AutoGen message payload."""
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if hasattr(content, "model_dump_json"):
        return str(content.model_dump_json(indent=2))
    if hasattr(content, "model_dump"):
        return json.dumps(content.model_dump(), indent=2)
    return str(content)


def _run_coro(coro: Any) -> Any:
    """Run an async coroutine from the synchronous lesson runtime."""
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)
    raise RuntimeError(
        "CleanLoop AutoGen helpers cannot run inside an existing event loop."
    )
