"""Learn reusable habits from shipped demonstration traces."""

from __future__ import annotations

from dataclasses import dataclass

from skill_mastery.config import HabitDefinition, SkillMasteryCatalog


@dataclass(frozen=True)
class LearnedHabit:
    """A habit promoted from the shipped demonstrations."""

    slug: str
    label: str
    instruction: str
    trigger_keywords: tuple[str, ...]
    success_signals: tuple[str, ...]
    stop_condition: str
    support: int
    successful_uses: int
    context_coverage: int
    mastery_score: int


def _to_learned_habit(
    definition: HabitDefinition,
    *,
    support: int,
    successful_uses: int,
    context_coverage: int,
) -> LearnedHabit:
    """Build one learned habit from a seed definition and usage counts."""
    failures = support - successful_uses
    mastery_score = (successful_uses * 2) + context_coverage - failures
    return LearnedHabit(
        slug=definition.slug,
        label=definition.label,
        instruction=definition.instruction,
        trigger_keywords=definition.trigger_keywords,
        success_signals=definition.success_signals,
        stop_condition=definition.stop_condition,
        support=support,
        successful_uses=successful_uses,
        context_coverage=context_coverage,
        mastery_score=mastery_score,
    )


def learn_reusable_habits(
    catalog: SkillMasteryCatalog,
    *,
    minimum_successes: int = 2,
    minimum_context_coverage: int = 2,
) -> list[LearnedHabit]:
    """Promote habits that succeed across more than one shipped context."""
    learned: list[LearnedHabit] = []
    for slug, definition in catalog.habit_definitions.items():
        used = [demo for demo in catalog.demonstrations if slug in demo.habits_used]
        successful = [demo for demo in used if demo.outcome == "successful"]
        support = len(used)
        successful_uses = len(successful)
        context_coverage = len({demo.context_slug for demo in successful})
        if successful_uses < minimum_successes:
            continue
        if context_coverage < minimum_context_coverage:
            continue
        learned.append(
            _to_learned_habit(
                definition,
                support=support,
                successful_uses=successful_uses,
                context_coverage=context_coverage,
            )
        )
    learned.sort(key=lambda habit: (-habit.mastery_score, habit.slug))
    return learned
