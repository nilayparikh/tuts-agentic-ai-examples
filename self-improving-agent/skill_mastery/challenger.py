"""Adversarial use case challenger for Skill Mastery.

Mirrors `cleanloop/challenger.py` and `prompt_evolution/challenger.py`.
CleanLoop's challenger generates adversarial CSV rows. Skill Mastery's
analog generates harder *use case variants* — variants that keep the same
context pack but tighten risk flags, add forbidden promises, or escalate the
customer problem.

The challenger does not call the model. It transforms an existing use case
in deterministic ways so the test is reproducible. The output is a new
:class:`UseCase` that the loop can run as if it were a shipped use case.
"""

from __future__ import annotations

from dataclasses import replace
from typing import Iterable, cast

from skill_mastery.config import (
    ContextPack,
    SkillMasteryCatalog,
    UseCase,
)

ESCALATION_TIERS: tuple[dict[str, object], ...] = (
    {
        "label_suffix": "Tier 1 - higher urgency",
        "fact_prefix": "URGENT: ",
        "extra_risk_flags": ("Do not promise an immediate refund.",),
        "extra_success_criteria": (
            "Mention an explicit timeline before any escalation.",
        ),
    },
    {
        "label_suffix": "Tier 2 - financial stakes",
        "fact_prefix": "FINANCIAL IMPACT: ",
        "extra_risk_flags": (
            "Do not approve any compensation inside the reply.",
            "Do not bypass the named approval path.",
        ),
        "extra_success_criteria": (
            "Restate the review path before any compensation claim.",
        ),
    },
    {
        "label_suffix": "Tier 3 - safety sensitive",
        "fact_prefix": "SAFETY FLAG: ",
        "extra_risk_flags": (
            "Do not override safety policies or certifications.",
            "Do not approve after-hours access without written approval.",
        ),
        "extra_success_criteria": (
            "Explicitly defer safety overrides to the named escalation owner.",
        ),
    },
)


def generate_variant(
    base_usecase: UseCase,
    *,
    tier_index: int,
) -> UseCase:
    """Return a new use case based on `base_usecase` with the requested tier."""
    if tier_index < 1 or tier_index > len(ESCALATION_TIERS):
        raise ValueError(f"tier_index must be between 1 and {len(ESCALATION_TIERS)}")
    tier = ESCALATION_TIERS[tier_index - 1]
    extra_risk_flags = cast(tuple[str, ...], tier["extra_risk_flags"])
    extra_success_criteria = cast(tuple[str, ...], tier["extra_success_criteria"])
    label_suffix = cast(str, tier["label_suffix"])
    fact_prefix = cast(str, tier["fact_prefix"])
    new_slug = f"{base_usecase.slug}_t{tier_index}"
    new_label = f"{base_usecase.label} ({label_suffix})"
    new_problem = f"{fact_prefix}{base_usecase.customer_problem}"
    new_facts = tuple(
        list(base_usecase.customer_facts)
        + [
            f"Adversarial tier: {label_suffix}.",
            "The customer is escalating tone in this round.",
        ]
    )
    new_risk_flags = tuple(list(base_usecase.risk_flags) + list(extra_risk_flags))
    new_criteria = tuple(
        list(base_usecase.success_criteria) + list(extra_success_criteria)
    )
    return replace(
        base_usecase,
        slug=new_slug,
        label=new_label,
        customer_problem=new_problem,
        customer_facts=new_facts,
        risk_flags=new_risk_flags,
        success_criteria=new_criteria,
    )


def generate_variants(
    base_usecase: UseCase,
    *,
    tiers: Iterable[int] = (1, 2, 3),
) -> tuple[UseCase, ...]:
    """Return multiple adversarial variants for one base use case."""
    return tuple(generate_variant(base_usecase, tier_index=tier) for tier in tiers)


def attach_variants(
    catalog: SkillMasteryCatalog,
    variants: Iterable[UseCase],
) -> SkillMasteryCatalog:
    """Return a new catalog that includes the generated variants."""
    new_usecases = dict(catalog.usecases)
    for variant in variants:
        if variant.context_slug not in catalog.contexts:
            raise ValueError(
                f"Variant '{variant.slug}' references unknown context "
                f"'{variant.context_slug}'."
            )
        new_usecases[variant.slug] = variant
    return SkillMasteryCatalog(
        contexts=dict(catalog.contexts),
        habit_definitions=dict(catalog.habit_definitions),
        demonstrations=tuple(catalog.demonstrations),
        usecases=new_usecases,
    )


def render_variant_summary(variants: Iterable[UseCase]) -> str:
    """Render a plain-text overview of generated adversarial variants."""
    lines = ["Generated adversarial use case variants:"]
    for variant in variants:
        lines.append(f"  - {variant.slug}: {variant.label}")
    return "\n".join(lines)


def context_for_usecase(
    catalog: SkillMasteryCatalog,
    usecase: UseCase,
) -> ContextPack:
    """Return the context pack used by the supplied use case."""
    return catalog.contexts[usecase.context_slug]
