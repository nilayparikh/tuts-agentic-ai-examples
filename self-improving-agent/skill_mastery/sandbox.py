"""Sandbox runner for one isolated Skill Mastery round.

Mirrors `cleanloop/sandbox.py` and `prompt_evolution/sandbox.py`. CleanLoop's
sandbox runs the genome in a constrained subprocess. Skill Mastery's analog
runs one habit-composition draft + one evaluation in the current process with
explicit Hermes iteration and time clamps. There is no subprocess because the
LLM call already lives behind a network boundary.

The sandbox is the right surface for "is the current habit catalog
producing a passing reply?" without committing to a multi-round loop or to
interactive review.
"""

from __future__ import annotations

import time
from dataclasses import dataclass

from prompt_evolution.hermes_client import HermesAgentRunner
from skill_mastery.config import SkillMasteryCatalog, SkillMasteryProfile
from skill_mastery.evaluator import SkillEvaluationResult, evaluate_response
from skill_mastery.learner import LearnedHabit, learn_reusable_habits
from skill_mastery.loop import (
    build_generation_system_prompt,
    build_generation_user_prompt,
)
from skill_mastery.selector import select_habits


@dataclass(frozen=True)
class SandboxResult:
    """One sandbox round outcome for Skill Mastery."""

    response_text: str
    evaluation: SkillEvaluationResult
    selected_habits: tuple[LearnedHabit, ...]
    elapsed_seconds: float
    timed_out: bool
    iteration_clamp: int


def run_one_round(
    catalog: SkillMasteryCatalog,
    profile: SkillMasteryProfile,
    *,
    timeout_seconds: float = 60.0,
    max_iterations: int = 4,
    runner: HermesAgentRunner | None = None,
) -> SandboxResult:
    """Run one isolated draft + evaluation pass with explicit clamps."""
    if runner is None:
        base_runner = HermesAgentRunner.from_env()
        runner = HermesAgentRunner(
            model=base_runner.model,
            base_url=base_runner.base_url,
            api_key=base_runner.api_key,
            max_iterations=max_iterations,
        )
    learned = learn_reusable_habits(catalog)
    selected = select_habits(profile, learned)
    system_prompt = build_generation_system_prompt(profile, selected)
    user_prompt = build_generation_user_prompt(profile)
    start = time.monotonic()
    timed_out = False
    response_text = ""
    try:
        response = runner.run_text(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            task_id="skill-mastery-sandbox-round",
        )
        response_text = response.text
    except Exception as exc:  # pylint: disable=broad-except
        response_text = f"[sandbox_error] {exc}"
    elapsed = time.monotonic() - start
    if elapsed > timeout_seconds:
        timed_out = True
    evaluation = evaluate_response(profile, selected, response_text)
    return SandboxResult(
        response_text=response_text,
        evaluation=evaluation,
        selected_habits=tuple(selected),
        elapsed_seconds=elapsed,
        timed_out=timed_out,
        iteration_clamp=max_iterations,
    )


def render_result(result: SandboxResult) -> str:
    """Render the sandbox result as plain-text learner output."""
    eval_result = result.evaluation
    lines = [
        f"Sandbox round: score {eval_result.total_score}/{eval_result.max_score}",
        f"  selected habits: {', '.join(h.slug for h in result.selected_habits)}",
        f"  elapsed:         {result.elapsed_seconds:.2f}s",
        f"  timeout exceeded: {result.timed_out}",
        f"  iteration clamp: {result.iteration_clamp}",
    ]
    if eval_result.issues:
        lines.append("  issues:")
        lines.extend(f"    - {issue}" for issue in eval_result.issues[:5])
    return "\n".join(lines)
