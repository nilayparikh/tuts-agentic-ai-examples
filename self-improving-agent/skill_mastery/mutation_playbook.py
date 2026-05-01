"""Habit composition mutation playbook for Skill Mastery.

Mirrors `cleanloop/mutation_playbook.py` and `prompt_evolution/mutation_playbook.py`
for the habit-mastery loop. CleanLoop routes anomalous CSV rows through bounded
repair rules. Skill Mastery routes evaluator issues through bounded mutation
strategies before letting Hermes rewrite the reply from scratch.

Each strategy is small, deterministic, and addresses one observable failure
mode: missing policy coverage, missing habit signal, forbidden promise,
context grounding gap, or generic refinement. The playbook chooses the
strategies, lists them in priority order, and renders a focused mutation
brief that the LLM uses for the next revision.

This keeps the mutation surface readable. Hermes still owns the language
rewrite; the playbook owns *which* rewrite to ask for.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from skill_mastery.config import SkillMasteryProfile
from skill_mastery.evaluator import SkillEvaluationResult
from skill_mastery.learner import LearnedHabit


@dataclass(frozen=True)
class MutationStrategy:
    """One bounded habit-composition mutation strategy."""

    slug: str
    label: str
    directive: str
    triggers: tuple[str, ...]


POLICY_COVERAGE = MutationStrategy(
    slug="policy_coverage",
    label="Tighten policy coverage",
    directive=(
        "Make the next reply explicitly reference the missing required "
        "policy points. Do not invent new policies."
    ),
    triggers=("missing policy",),
)

HABIT_SIGNAL = MutationStrategy(
    slug="habit_signal",
    label="Apply the missing habit signal",
    directive=(
        "Make the next reply apply each selected habit card so its success "
        "signal text appears at least once."
    ),
    triggers=("missing habit signal",),
)

FORBIDDEN_GUARD = MutationStrategy(
    slug="forbidden_guard",
    label="Reinforce forbidden-claim guard",
    directive=(
        "Make the next reply avoid the forbidden claims. Restate the named "
        "review path the agent should explain instead."
    ),
    triggers=("forbidden promise",),
)

CONTEXT_GROUNDING = MutationStrategy(
    slug="context_grounding",
    label="Add context grounding",
    directive=(
        "Make the next reply cite at least one reference term or service "
        "detail from the active context pack."
    ),
    triggers=("missing grounding", "missing context"),
)

DEFAULT_FALLBACK = MutationStrategy(
    slug="general_refinement",
    label="General refinement",
    directive=(
        "Make the next reply more policy-grounded and tighter on the "
        "selected habit cards without overpromising."
    ),
    triggers=(),
)

ALL_STRATEGIES: tuple[MutationStrategy, ...] = (
    POLICY_COVERAGE,
    HABIT_SIGNAL,
    FORBIDDEN_GUARD,
    CONTEXT_GROUNDING,
)


def select_strategies(
    evaluation: SkillEvaluationResult,
    *,
    max_strategies: int = 3,
) -> tuple[MutationStrategy, ...]:
    """Pick the bounded set of strategies that address the active issues."""
    chosen: list[MutationStrategy] = []
    issues_lower = [issue.lower() for issue in evaluation.issues]
    for strategy in ALL_STRATEGIES:
        if any(
            trigger in issue for issue in issues_lower for trigger in strategy.triggers
        ):
            chosen.append(strategy)
        if len(chosen) >= max_strategies:
            break
    if not chosen:
        chosen.append(DEFAULT_FALLBACK)
    return tuple(chosen)


def render_brief(
    strategies: Sequence[MutationStrategy],
    profile: SkillMasteryProfile,
    selected_habits: Sequence[LearnedHabit],
) -> str:
    """Render a focused mutation brief from the selected strategies."""
    if not strategies:
        return DEFAULT_FALLBACK.directive
    lines: list[str] = ["Apply these habit-composition strategies in order:"]
    for index, strategy in enumerate(strategies, start=1):
        lines.append(f"{index}. {strategy.label} - {strategy.directive}")
    if profile.context.required_policy_points:
        names = ", ".join(
            policy.slug for policy in profile.context.required_policy_points
        )
        lines.append("")
        lines.append(f"Active required policy slugs: {names}.")
    if profile.context.forbidden_claims:
        names = ", ".join(profile.context.forbidden_claims)
        lines.append(f"Forbidden claims to guard: {names}.")
    if selected_habits:
        names = ", ".join(habit.slug for habit in selected_habits)
        lines.append(f"Selected habit cards: {names}.")
    return "\n".join(lines)


def categorize_issues(evaluation: SkillEvaluationResult) -> dict[str, list[str]]:
    """Bucket evaluator issues into strategy categories for dashboard rendering."""
    buckets: dict[str, list[str]] = {strategy.slug: [] for strategy in ALL_STRATEGIES}
    buckets[DEFAULT_FALLBACK.slug] = []
    for issue in evaluation.issues:
        lowered = issue.lower()
        matched = False
        for strategy in ALL_STRATEGIES:
            if any(trigger in lowered for trigger in strategy.triggers):
                buckets[strategy.slug].append(issue)
                matched = True
                break
        if not matched:
            buckets[DEFAULT_FALLBACK.slug].append(issue)
    return buckets
