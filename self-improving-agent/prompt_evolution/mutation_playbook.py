"""Instruction mutation playbook for Prompt Evolution.

Mirrors `cleanloop/mutation_playbook.py` for the support-desk loop. CleanLoop
routes anomalous CSV rows through bounded repair rules before letting the
model invent a new pipeline. Prompt Evolution routes evaluator issues through
bounded mutation strategies before letting Hermes rewrite an entire
instruction prompt from scratch.

Each strategy is small, deterministic, and addresses one observable failure
mode: missing policy coverage, forbidden promises, structure mismatches,
preference drift, or context grounding gaps. The playbook chooses the
strategies, lists them in priority order, and renders a focused mutation
brief that the LLM uses for the next refinement.

This keeps the mutation surface readable. Hermes still owns the language
rewrite; the playbook owns *which* rewrite to ask for.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from prompt_evolution.config import SelectionProfile
from prompt_evolution.evaluator import EvaluationResult


@dataclass(frozen=True)
class MutationStrategy:
    """One bounded instruction-mutation strategy."""

    slug: str
    label: str
    directive: str
    triggers: tuple[str, ...]


POLICY_COVERAGE = MutationStrategy(
    slug="policy_coverage",
    label="Tighten policy coverage",
    directive=(
        "Update the instructions so the next draft must explicitly reference "
        "the missing required policy points. Do not invent new policies."
    ),
    triggers=("missing policy",),
)

FORBIDDEN_GUARD = MutationStrategy(
    slug="forbidden_guard",
    label="Reinforce forbidden-claim guard",
    directive=(
        "Update the instructions so the next draft must avoid the forbidden "
        "claims. Restate the review path the agent should explain instead."
    ),
    triggers=("forbidden policy promise",),
)

STRUCTURE_FIX = MutationStrategy(
    slug="structure_fix",
    label="Correct response structure",
    directive=(
        "Update the instructions so the next draft uses the chosen "
        "structure preference. Make the formatting requirement concrete."
    ),
    triggers=("structure mismatch",),
)

CONTEXT_GROUNDING = MutationStrategy(
    slug="context_grounding",
    label="Add context grounding",
    directive=(
        "Update the instructions so the next draft cites at least one "
        "reference term or service detail from the active context pack."
    ),
    triggers=("missing context grounding",),
)

PREFERENCE_FIT = MutationStrategy(
    slug="preference_fit",
    label="Improve preference fit",
    directive=(
        "Update the instructions so the next draft matches the selected "
        "preference axes (tone, initiative, evidence, closing, detail) "
        "without dropping policy coverage."
    ),
    triggers=("mismatch for", "tone mismatch", "detail level mismatch"),
)

DEFAULT_FALLBACK = MutationStrategy(
    slug="general_refinement",
    label="General refinement",
    directive=(
        "Update the instructions so the next draft is more policy-grounded "
        "and closer to the chosen preferences."
    ),
    triggers=(),
)

ALL_STRATEGIES: tuple[MutationStrategy, ...] = (
    POLICY_COVERAGE,
    FORBIDDEN_GUARD,
    STRUCTURE_FIX,
    CONTEXT_GROUNDING,
    PREFERENCE_FIT,
)


def select_strategies(
    evaluation: EvaluationResult,
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
    profile: SelectionProfile,
) -> str:
    """Render a focused mutation brief from the selected strategies."""
    if not strategies:
        return DEFAULT_FALLBACK.directive
    lines: list[str] = ["Apply these instruction-mutation strategies in order:"]
    for index, strategy in enumerate(strategies, start=1):
        lines.append(f"{index}. {strategy.label} — {strategy.directive}")
    if profile.context.required_policy_points:
        names = ", ".join(
            policy.slug for policy in profile.context.required_policy_points
        )
        lines.append("")
        lines.append(f"Active required policy slugs: {names}.")
    if profile.context.forbidden_claims:
        names = ", ".join(profile.context.forbidden_claims)
        lines.append(f"Forbidden claims to guard: {names}.")
    return "\n".join(lines)


def categorize_issues(evaluation: EvaluationResult) -> dict[str, list[str]]:
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
