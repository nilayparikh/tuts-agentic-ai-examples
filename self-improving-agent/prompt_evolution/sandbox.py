"""Sandbox runner for one isolated Prompt Evolution round.

Mirrors `cleanloop/sandbox.py`. CleanLoop's sandbox exists so a learner can
run the genome in a constrained subprocess with a hard timeout, separate
from the main loop. Prompt Evolution's analog runs one draft + one
evaluation in the current process with explicit Hermes iteration and time
clamps. It does not start a subprocess, because the LLM call already lives
behind a network boundary.

The sandbox is the right surface for "is the instruction prompt currently
working?" without committing to a multi-round loop or to interactive review.
"""

from __future__ import annotations

import time
from dataclasses import dataclass

from prompt_evolution.config import PromptEvolutionCatalog, SelectionProfile
from prompt_evolution.evaluator import EvaluationResult, evaluate_response
from prompt_evolution.hermes_client import HermesAgentRunner
from prompt_evolution.loop import (
    build_generation_system_prompt,
    build_generation_user_prompt,
    load_mutable_instructions,
)


@dataclass(frozen=True)
class SandboxResult:
    """One sandbox round outcome."""

    response_text: str
    evaluation: EvaluationResult
    elapsed_seconds: float
    timed_out: bool
    iteration_clamp: int


def run_one_round(
    catalog: PromptEvolutionCatalog,
    profile: SelectionProfile,
    *,
    timeout_seconds: float = 60.0,
    max_iterations: int = 4,
    runner: HermesAgentRunner | None = None,
) -> SandboxResult:
    """Run one isolated draft + evaluation pass with explicit clamps."""
    if runner is None:
        runner = HermesAgentRunner.from_env()
        # Apply the iteration clamp explicitly so the sandbox never silently
        # exceeds the configured Hermes auxiliary call budget.
        runner = HermesAgentRunner(
            model=runner.model,
            base_url=runner.base_url,
            api_key=runner.api_key,
            max_iterations=max_iterations,
        )
    instructions = load_mutable_instructions()
    system_prompt = build_generation_system_prompt(instructions, catalog, profile)
    user_prompt = build_generation_user_prompt(profile)
    start = time.monotonic()
    timed_out = False
    response_text = ""
    try:
        response = runner.run_text(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            task_id="prompt-evolution-sandbox-round",
        )
        response_text = response.text
    except Exception as exc:  # pylint: disable=broad-except
        # The CLI surfaces structured failures rather than crashing.
        response_text = f"[sandbox_error] {exc}"
    elapsed = time.monotonic() - start
    if elapsed > timeout_seconds:
        timed_out = True
    evaluation = evaluate_response(profile, response_text)
    return SandboxResult(
        response_text=response_text,
        evaluation=evaluation,
        elapsed_seconds=elapsed,
        timed_out=timed_out,
        iteration_clamp=max_iterations,
    )


def render_result(result: SandboxResult) -> str:
    """Render the sandbox result as plain-text learner output."""
    eval_result = result.evaluation
    lines = [
        f"Sandbox round: score {eval_result.total_score}/{eval_result.max_score}",
        f"  elapsed:        {result.elapsed_seconds:.2f}s",
        f"  timeout exceeded: {result.timed_out}",
        f"  iteration clamp: {result.iteration_clamp}",
    ]
    if eval_result.issues:
        lines.append("  issues:")
        lines.extend(f"    - {issue}" for issue in eval_result.issues[:5])
    return "\n".join(lines)
