"""Load Prompt Evolution contexts and preference catalogs."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class PolicyPoint:
    """One policy point the response must mention when relevant."""

    slug: str
    description: str
    keywords: tuple[str, ...]


@dataclass(frozen=True)
class ContextPack:
    """One predefined support context pack."""

    slug: str
    label: str
    service_summary: str
    brand_voice: str
    escalation_path: str
    reference_terms: tuple[str, ...]
    forbidden_claims: tuple[str, ...]
    required_policy_points: tuple[PolicyPoint, ...]


@dataclass(frozen=True)
class PreferenceOption:
    """One allowed option inside a preference axis."""

    slug: str
    label: str
    instruction: str
    signals: tuple[str, ...]


@dataclass(frozen=True)
class PreferenceAxis:
    """One user-selectable preference axis."""

    slug: str
    label: str
    description: str
    options: dict[str, PreferenceOption]


@dataclass(frozen=True)
class ScenarioCase:
    """One named support-desk scenario for a runnable prompt evolution demo."""

    slug: str
    label: str
    context_slug: str
    customer_problem: str
    default_preferences: dict[str, str]
    customer_facts: tuple[str, ...]
    risk_flags: tuple[str, ...]
    expected_policy_slugs: tuple[str, ...]
    success_criteria: tuple[str, ...]
    operator_notes: tuple[str, ...]


@dataclass(frozen=True)
class PromptEvolutionCatalog:
    """All predefined contexts and preference axes for the example."""

    contexts: dict[str, ContextPack]
    preference_axes: dict[str, PreferenceAxis]
    scenarios: dict[str, ScenarioCase] = field(default_factory=dict)


@dataclass(frozen=True)
class SelectionProfile:
    """The user-selected problem, context, and preferences for one run."""

    problem: str
    context: ContextPack
    selected_preferences: dict[str, str]
    resolved_preferences: dict[str, PreferenceOption] = field(default_factory=dict)
    scenario: ScenarioCase | None = None

    def preference_lines(self, catalog: PromptEvolutionCatalog) -> list[str]:
        """Render the chosen preferences as human-readable bullet lines."""
        lines: list[str] = []
        for axis_slug, option_slug in self.selected_preferences.items():
            axis = catalog.preference_axes[axis_slug]
            option = self.resolved_preferences.get(axis_slug, axis.options[option_slug])
            lines.append(f"- {axis.label}: {option.label} — {option.instruction}")
        return lines


def _load_json(path: Path) -> dict[str, Any]:
    """Read one JSON file from disk using UTF-8."""
    return json.loads(path.read_text(encoding="utf-8"))


def _load_context(path: Path) -> ContextPack:
    """Convert one context JSON file into a typed context pack."""
    payload = _load_json(path)
    policies = tuple(
        PolicyPoint(
            slug=str(item["slug"]),
            description=str(item["description"]),
            keywords=tuple(str(keyword) for keyword in item.get("keywords", [])),
        )
        for item in payload.get("required_policy_points", [])
    )
    return ContextPack(
        slug=str(payload["slug"]),
        label=str(payload["label"]),
        service_summary=str(payload["service_summary"]),
        brand_voice=str(payload["brand_voice"]),
        escalation_path=str(payload["escalation_path"]),
        reference_terms=tuple(str(item) for item in payload.get("reference_terms", [])),
        forbidden_claims=tuple(
            str(item) for item in payload.get("forbidden_claims", [])
        ),
        required_policy_points=policies,
    )


def _load_preference_axis(path: Path) -> PreferenceAxis:
    """Convert one preference JSON file into a typed preference axis."""
    payload = _load_json(path)
    options = {
        str(option["slug"]): PreferenceOption(
            slug=str(option["slug"]),
            label=str(option["label"]),
            instruction=str(option["instruction"]),
            signals=tuple(str(signal) for signal in option.get("signals", [])),
        )
        for option in payload.get("options", [])
    }
    return PreferenceAxis(
        slug=str(payload["slug"]),
        label=str(payload["label"]),
        description=str(payload["description"]),
        options=options,
    )


def _load_scenario(path: Path) -> ScenarioCase:
    """Convert one scenario JSON file into a typed support-desk case."""
    payload = _load_json(path)
    return ScenarioCase(
        slug=str(payload["slug"]),
        label=str(payload["label"]),
        context_slug=str(payload["context_slug"]),
        customer_problem=str(payload["customer_problem"]),
        default_preferences={
            str(axis): str(option)
            for axis, option in payload.get("default_preferences", {}).items()
        },
        customer_facts=tuple(str(item) for item in payload.get("customer_facts", [])),
        risk_flags=tuple(str(item) for item in payload.get("risk_flags", [])),
        expected_policy_slugs=tuple(
            str(item) for item in payload.get("expected_policy_slugs", [])
        ),
        success_criteria=tuple(
            str(item) for item in payload.get("success_criteria", [])
        ),
        operator_notes=tuple(str(item) for item in payload.get("operator_notes", [])),
    )


def load_catalog(data_dir: Path) -> PromptEvolutionCatalog:
    """Load the shipped context and preference catalogs from `.data/`."""
    contexts_dir = data_dir / "contexts"
    preferences_dir = data_dir / "preferences"
    scenarios_dir = data_dir / "scenarios"

    contexts = {
        context.slug: context
        for context in (
            _load_context(path) for path in sorted(contexts_dir.glob("*.json"))
        )
    }
    preference_axes = {
        axis.slug: axis
        for axis in (
            _load_preference_axis(path)
            for path in sorted(preferences_dir.glob("*.json"))
        )
    }
    scenarios = {
        scenario.slug: scenario
        for scenario in (
            _load_scenario(path) for path in sorted(scenarios_dir.glob("*.json"))
        )
    }
    return PromptEvolutionCatalog(
        contexts=contexts,
        preference_axes=preference_axes,
        scenarios=scenarios,
    )


def parse_preference_pairs(pairs: list[str]) -> dict[str, str]:
    """Parse repeated `axis=value` pairs from the CLI."""
    parsed: dict[str, str] = {}
    for item in pairs:
        if "=" not in item:
            raise ValueError(f"Invalid preference '{item}'. Use axis=value.")
        axis, option = item.split("=", 1)
        parsed[axis.strip()] = option.strip()
    return parsed


def resolve_selection_profile(
    catalog: PromptEvolutionCatalog,
    *,
    problem: str,
    context_slug: str,
    preference_pairs: list[str],
    scenario: ScenarioCase | None = None,
) -> SelectionProfile:
    """Validate the user's choices and build one selection profile."""
    cleaned_problem = problem.strip()
    if not cleaned_problem:
        raise ValueError("The problem text cannot be empty.")

    if context_slug not in catalog.contexts:
        options = ", ".join(sorted(catalog.contexts))
        raise ValueError(f"Unknown context '{context_slug}'. Choose from: {options}")

    selected_preferences = parse_preference_pairs(preference_pairs)
    if len(selected_preferences) < 2:
        raise ValueError("Select at least two preferences for prompt evolution.")

    resolved_preferences: dict[str, PreferenceOption] = {}
    for axis_slug, option_slug in selected_preferences.items():
        axis = catalog.preference_axes.get(axis_slug)
        if axis is None:
            options = ", ".join(sorted(catalog.preference_axes))
            raise ValueError(
                f"Unknown preference axis '{axis_slug}'. Choose from: {options}"
            )
        if option_slug not in axis.options:
            options = ", ".join(sorted(axis.options))
            raise ValueError(
                f"Unknown option '{option_slug}' for axis '{axis_slug}'. Choose from: {options}"
            )
        resolved_preferences[axis_slug] = axis.options[option_slug]

    return SelectionProfile(
        problem=cleaned_problem,
        context=catalog.contexts[context_slug],
        selected_preferences=selected_preferences,
        resolved_preferences=resolved_preferences,
        scenario=scenario,
    )


def _preference_pairs_from_mapping(preferences: dict[str, str]) -> list[str]:
    """Render a preference mapping as stable CLI-style pairs."""
    return [f"{axis}={option}" for axis, option in preferences.items()]


def resolve_scenario_profile(
    catalog: PromptEvolutionCatalog,
    *,
    scenario_slug: str,
    preference_pairs: list[str] | None = None,
    problem: str | None = None,
    context_slug: str | None = None,
) -> SelectionProfile:
    """Build a selection profile from one named scenario plus optional overrides."""
    scenario = catalog.scenarios.get(scenario_slug)
    if scenario is None:
        options = ", ".join(sorted(catalog.scenarios)) or "no scenarios loaded"
        raise ValueError(f"Unknown scenario '{scenario_slug}'. Choose from: {options}")

    selected_preferences = dict(scenario.default_preferences)
    selected_preferences.update(parse_preference_pairs(list(preference_pairs or [])))
    return resolve_selection_profile(
        catalog,
        problem=problem or scenario.customer_problem,
        context_slug=context_slug or scenario.context_slug,
        preference_pairs=_preference_pairs_from_mapping(selected_preferences),
        scenario=scenario,
    )


def describe_catalog(catalog: PromptEvolutionCatalog) -> str:
    """Return a compact, learner-friendly catalog listing for the CLI."""
    lines = ["Contexts:"]
    for context in catalog.contexts.values():
        lines.append(f"- {context.slug}: {context.label}")
    lines.append("")
    lines.append("Preference axes:")
    for axis in catalog.preference_axes.values():
        options = ", ".join(sorted(axis.options))
        lines.append(f"- {axis.slug}: {options}")
    if catalog.scenarios:
        lines.append("")
        lines.append("Scenarios:")
        for scenario in catalog.scenarios.values():
            lines.append(f"- {scenario.slug}: {scenario.label}")
    return "\n".join(lines)


def describe_scenarios(catalog: PromptEvolutionCatalog) -> str:
    """Return a detailed listing of support-desk scenario cases."""
    lines = ["Scenarios:"]
    for scenario in catalog.scenarios.values():
        defaults = ", ".join(
            f"{axis}={option}" for axis, option in scenario.default_preferences.items()
        )
        lines.append(f"- {scenario.slug}: {scenario.label}")
        lines.append(f"  Context: {scenario.context_slug}")
        lines.append(f"  Defaults: {defaults}")
        lines.append(f"  Problem: {scenario.customer_problem}")
    return "\n".join(lines)
