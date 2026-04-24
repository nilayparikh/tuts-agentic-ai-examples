"""Select which learned habits fit a new Skill Mastery problem."""

from __future__ import annotations

from skill_mastery.config import SkillMasteryProfile
from skill_mastery.learner import LearnedHabit


def _match_score(problem_text: str, habit: LearnedHabit) -> int:
    """Score how strongly one learned habit matches the current problem."""
    score = 0
    for keyword in habit.trigger_keywords:
        if keyword.lower() in problem_text:
            score += 2
    if habit.slug in {"mirror_issue", "offer_checkpoint"}:
        score += 2
    if habit.slug == "cite_policy_gate" and any(
        token in problem_text for token in ("booking", "pickup", "transfer", "access")
    ):
        score += 2
    if habit.slug == "name_owner" and any(
        token in problem_text for token in ("review", "manager", "lead", "coordinator")
    ):
        score += 1
    return score


def select_habits(
    profile: SkillMasteryProfile,
    learned_habits: list[LearnedHabit],
    *,
    limit: int = 3,
) -> list[LearnedHabit]:
    """Select the highest-signal habits for the current problem."""
    lowered_problem = profile.problem.lower()
    ranked = sorted(
        learned_habits,
        key=lambda habit: (-_match_score(lowered_problem, habit), -habit.mastery_score, habit.slug),
    )
    selected = [habit for habit in ranked if _match_score(lowered_problem, habit) > 0][:limit]
    if selected:
        return selected
    return ranked[:limit]
