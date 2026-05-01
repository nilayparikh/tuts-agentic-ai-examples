"""Autonomy ladder for the Skill Mastery loop.

Mirrors `cleanloop/autonomy.py` and `prompt_evolution/autonomy.py`. CleanLoop
rates the genome's trustworthiness. Skill Mastery's analog rates the trust
level of the current habit catalog: it watches whether the deterministic
evaluator score for habit-composed replies stays high and stable across
several sandbox rounds.

This is a teaching surface. The autonomy levels are advisory. They tell a
learner whether the current habit cards look safe to run with less oversight,
more rerank, or hands-on review.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

# Trust levels — increasing autonomy as scores stabilize at the ceiling.
SUPERVISED = "SUPERVISED"
HUMAN_GATED = "HUMAN_GATED"
AUTONOMOUS = "AUTONOMOUS"


@dataclass(frozen=True)
class RoundSnapshot:
    """One round's score for autonomy evaluation."""

    score: int
    total: int


@dataclass(frozen=True)
class AutonomyDecision:
    """Trust ladder decision derived from one or more round snapshots."""

    level: str
    score_ratio: float
    stability_ratio: float
    rounds_observed: int
    notes: tuple[str, ...]


def _normalize(snapshots: Sequence[RoundSnapshot]) -> list[float]:
    """Return per-round score ratios for stability math."""
    ratios: list[float] = []
    for snapshot in snapshots:
        if snapshot.total <= 0:
            ratios.append(0.0)
        else:
            ratios.append(snapshot.score / snapshot.total)
    return ratios


def evaluate_ladder(
    snapshots: Sequence[RoundSnapshot],
    *,
    autonomous_threshold: float = 0.95,
    human_gated_threshold: float = 0.75,
    stability_threshold: float = 0.05,
) -> AutonomyDecision:
    """Decide a trust level from a sequence of round snapshots."""
    if not snapshots:
        return AutonomyDecision(
            level=SUPERVISED,
            score_ratio=0.0,
            stability_ratio=0.0,
            rounds_observed=0,
            notes=("no rounds observed",),
        )
    ratios = _normalize(snapshots)
    average = sum(ratios) / len(ratios)
    if len(ratios) >= 2:
        spread = max(ratios) - min(ratios)
    else:
        spread = 0.0
    notes: list[str] = []
    if average >= autonomous_threshold and spread <= stability_threshold:
        level = AUTONOMOUS
        notes.append("high score stability across rounds")
    elif average >= human_gated_threshold:
        level = HUMAN_GATED
        notes.append("acceptable mean score with visible variance")
    else:
        level = SUPERVISED
        notes.append("score below threshold; keep oversight on")
    if spread > stability_threshold and level == AUTONOMOUS:
        level = HUMAN_GATED
        notes.append("downgraded due to score variance")
    return AutonomyDecision(
        level=level,
        score_ratio=average,
        stability_ratio=spread,
        rounds_observed=len(snapshots),
        notes=tuple(notes),
    )


def render_decision(decision: AutonomyDecision) -> str:
    """Render an autonomy decision as plain-text learner output."""
    lines = [
        f"Autonomy: {decision.level}",
        f"  rounds observed:   {decision.rounds_observed}",
        f"  mean score ratio:  {decision.score_ratio:.2f}",
        f"  stability spread:  {decision.stability_ratio:.2f}",
    ]
    if decision.notes:
        lines.append("  notes:")
        lines.extend(f"    - {note}" for note in decision.notes)
    return "\n".join(lines)
