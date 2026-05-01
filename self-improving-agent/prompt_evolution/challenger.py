"""Adversarial scenario challenger for Prompt Evolution.

Mirrors `cleanloop/challenger.py`. CleanLoop's challenger generates
adversarial CSV rows that stress the deterministic genome. Prompt
Evolution's analog generates harder *scenario variants* — variants that
keep the same context pack but tighten risk flags, add forbidden
promises, or escalate the customer problem.

The challenger does not call the model. It transforms an existing
scenario in deterministic ways so the test is reproducible. The output
is a new :class:`ScenarioCase` that the loop can run as if it were a
shipped scenario.
"""

from __future__ import annotations

from dataclasses import replace
from typing import Iterable

from prompt_evolution.config import ContextPack, PromptEvolutionCatalog, ScenarioCase

ESCALATION_TIERS = (
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
    base_scenario: ScenarioCase,
    *,
    tier_index: int,
) -> ScenarioCase:
    """Return a new scenario based on `base_scenario` with the requested tier."""
    if tier_index < 1 or tier_index > len(ESCALATION_TIERS):
        raise ValueError(f"tier_index must be between 1 and {len(ESCALATION_TIERS)}")
    tier = ESCALATION_TIERS[tier_index - 1]
    new_slug = f"{base_scenario.slug}_t{tier_index}"
    new_label = f"{base_scenario.label} ({tier['label_suffix']})"
    new_problem = f"{tier['fact_prefix']}{base_scenario.customer_problem}"
    new_facts = tuple(
        list(base_scenario.customer_facts)
        + [
            f"Adversarial tier: {tier['label_suffix']}.",
            "The customer is escalating tone in this round.",
        ]
    )
    new_risk_flags = tuple(
        list(base_scenario.risk_flags) + list(tier["extra_risk_flags"])
    )
    new_criteria = tuple(
        list(base_scenario.success_criteria) + list(tier["extra_success_criteria"])
    )
    return replace(
        base_scenario,
        slug=new_slug,
        label=new_label,
        customer_problem=new_problem,
        customer_facts=new_facts,
        risk_flags=new_risk_flags,
        success_criteria=new_criteria,
    )


def generate_variants(
    base_scenario: ScenarioCase,
    *,
    tiers: Iterable[int] = (1, 2, 3),
) -> tuple[ScenarioCase, ...]:
    """Return multiple adversarial variants for one base scenario."""
    return tuple(generate_variant(base_scenario, tier_index=tier) for tier in tiers)


def attach_variants(
    catalog: PromptEvolutionCatalog,
    variants: Iterable[ScenarioCase],
) -> PromptEvolutionCatalog:
    """Return a new catalog that includes the generated variants."""
    new_scenarios = dict(catalog.scenarios)
    for variant in variants:
        if variant.context_slug not in catalog.contexts:
            raise ValueError(
                f"Variant '{variant.slug}' references unknown context "
                f"'{variant.context_slug}'."
            )
        new_scenarios[variant.slug] = variant
    return PromptEvolutionCatalog(
        contexts=dict(catalog.contexts),
        preference_axes=dict(catalog.preference_axes),
        scenarios=new_scenarios,
    )


def render_variant_summary(variants: Iterable[ScenarioCase]) -> str:
    """Render a plain-text overview of generated adversarial variants."""
    lines = ["Generated adversarial scenario variants:"]
    for variant in variants:
        lines.append(f"  - {variant.slug}: {variant.label}")
    return "\n".join(lines)


def context_for_scenario(
    catalog: PromptEvolutionCatalog,
    scenario: ScenarioCase,
) -> ContextPack:
    """Return the context pack used by the supplied scenario."""
    return catalog.contexts[scenario.context_slug]
