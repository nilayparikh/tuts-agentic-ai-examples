"""Deterministic scoring for Skill Mastery response drafts."""

from __future__ import annotations

from dataclasses import dataclass

from skill_mastery.config import SkillMasteryProfile
from skill_mastery.learner import LearnedHabit


@dataclass(frozen=True)
class SkillEvaluationResult:
    """Scoring summary for one Skill Mastery draft."""

    total_score: int
    max_score: int
    issues: list[str]
    strengths: list[str]


def _contains_any(text: str, phrases: tuple[str, ...]) -> bool:
    """Return whether any configured phrase appears in the normalized text."""
    return any(phrase.lower() in text for phrase in phrases)


def evaluate_response(
    profile: SkillMasteryProfile,
    selected_habits: list[LearnedHabit],
    response_text: str,
) -> SkillEvaluationResult:
    """Score a reply against the context policy points and selected habits."""
    normalized = response_text.lower()
    total_score = 0
    max_score = 0
    issues: list[str] = []
    strengths: list[str] = []

    for policy in profile.context.required_policy_points:
        max_score += 2
        if _contains_any(normalized, policy.keywords):
            total_score += 2
            strengths.append(f"Policy covered: {policy.description}")
        else:
            issues.append(f"Missing policy coverage: {policy.description}")

    max_score += 1
    if _contains_any(normalized, profile.context.reference_terms):
        total_score += 1
        strengths.append("Grounds the reply in the selected service context.")
    else:
        issues.append("Missing grounding from the selected service context.")

    for habit in selected_habits:
        max_score += 1
        if _contains_any(normalized, habit.success_signals):
            total_score += 1
            strengths.append(f"Habit applied: {habit.label}")
        else:
            issues.append(f"Missing habit signal: {habit.label}")

    for claim in profile.context.forbidden_claims:
        if claim.lower() in normalized:
            issues.append(f"Forbidden promise detected: {claim}")
            total_score = max(total_score - 1, 0)

    return SkillEvaluationResult(
        total_score=total_score,
        max_score=max_score,
        issues=issues,
        strengths=strengths,
    )
