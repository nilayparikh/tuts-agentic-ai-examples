"""Load Skill Mastery contexts, habit seeds, and demonstration traces."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class PolicyPoint:
    """One policy point a strong response should cover when relevant."""

    slug: str
    description: str
    keywords: tuple[str, ...]


@dataclass(frozen=True)
class ContextPack:
    """One support context used by the Skill Mastery example."""

    slug: str
    label: str
    service_summary: str
    escalation_path: str
    reference_terms: tuple[str, ...]
    forbidden_claims: tuple[str, ...]
    required_policy_points: tuple[PolicyPoint, ...]


@dataclass(frozen=True)
class HabitDefinition:
    """One reusable habit seed inspired by MaestroMotif-style skill cards."""

    slug: str
    label: str
    instruction: str
    trigger_keywords: tuple[str, ...]
    success_signals: tuple[str, ...]
    stop_condition: str


@dataclass(frozen=True)
class DemonstrationRecord:
    """One shipped demonstration trace showing which habits were used."""

    id: str
    context_slug: str
    problem: str
    response: str
    outcome: str
    habits_used: tuple[str, ...]


@dataclass(frozen=True)
class SkillMasteryCatalog:
    """All contexts, habit seeds, and traces for the Skill Mastery example."""

    contexts: dict[str, ContextPack]
    habit_definitions: dict[str, HabitDefinition]
    demonstrations: tuple[DemonstrationRecord, ...]


@dataclass(frozen=True)
class SkillMasteryProfile:
    """The context and problem for one Skill Mastery run."""

    problem: str
    context: ContextPack


def _load_json(path: Path) -> Any:
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
        escalation_path=str(payload["escalation_path"]),
        reference_terms=tuple(str(item) for item in payload.get("reference_terms", [])),
        forbidden_claims=tuple(str(item) for item in payload.get("forbidden_claims", [])),
        required_policy_points=policies,
    )


def _load_habit_definitions(path: Path) -> dict[str, HabitDefinition]:
    """Convert the shipped habit seed list into typed habit definitions."""
    payload = _load_json(path)
    return {
        str(item["slug"]): HabitDefinition(
            slug=str(item["slug"]),
            label=str(item["label"]),
            instruction=str(item["instruction"]),
            trigger_keywords=tuple(str(keyword) for keyword in item.get("trigger_keywords", [])),
            success_signals=tuple(str(signal) for signal in item.get("success_signals", [])),
            stop_condition=str(item["stop_condition"]),
        )
        for item in payload
    }


def _load_demonstrations(path: Path) -> tuple[DemonstrationRecord, ...]:
    """Convert the shipped demonstration list into typed records."""
    payload = _load_json(path)
    return tuple(
        DemonstrationRecord(
            id=str(item["id"]),
            context_slug=str(item["context_slug"]),
            problem=str(item["problem"]),
            response=str(item["response"]),
            outcome=str(item["outcome"]),
            habits_used=tuple(str(habit) for habit in item.get("habits_used", [])),
        )
        for item in payload
    )


def load_catalog(data_dir: Path) -> SkillMasteryCatalog:
    """Load the shipped contexts, habits, and traces from `.data/`."""
    contexts_dir = data_dir / "contexts"
    contexts = {
        context.slug: context
        for context in (_load_context(path) for path in sorted(contexts_dir.glob("*.json")))
    }
    habit_definitions = _load_habit_definitions(data_dir / "habits.json")
    demonstrations = _load_demonstrations(data_dir / "demonstrations.json")
    return SkillMasteryCatalog(
        contexts=contexts,
        habit_definitions=habit_definitions,
        demonstrations=demonstrations,
    )


def resolve_skill_profile(
    catalog: SkillMasteryCatalog,
    *,
    context_slug: str,
    problem: str,
) -> SkillMasteryProfile:
    """Validate the user's choices and build one Skill Mastery profile."""
    cleaned_problem = problem.strip()
    if not cleaned_problem:
        raise ValueError("The problem text cannot be empty.")
    if context_slug not in catalog.contexts:
        options = ", ".join(sorted(catalog.contexts))
        raise ValueError(f"Unknown context '{context_slug}'. Choose from: {options}")
    return SkillMasteryProfile(problem=cleaned_problem, context=catalog.contexts[context_slug])


def describe_catalog(catalog: SkillMasteryCatalog) -> str:
    """Return a compact catalog listing for the Skill Mastery CLI."""
    lines = ["Contexts:"]
    for context in catalog.contexts.values():
        lines.append(f"- {context.slug}: {context.label}")
    lines.append("")
    lines.append("Habit seeds:")
    for habit in catalog.habit_definitions.values():
        lines.append(f"- {habit.slug}: {habit.label}")
    lines.append("")
    lines.append(f"Demonstrations: {len(catalog.demonstrations)}")
    return "\n".join(lines)
