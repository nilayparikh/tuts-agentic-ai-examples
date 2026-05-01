"""Best-of-N draft reranker for Skill Mastery.

Mirrors `cleanloop/reranker.py` and `prompt_evolution/reranker.py`. CleanLoop
keeps the highest-scoring mutation candidate against its fixed judge. Skill
Mastery's analog keeps the highest-scoring candidate reply for one habit
selection against the deterministic evaluator. The selected habits do not
change during reranking. Only the candidate reply varies, exposing the
model's intra-prompt variance.

This is a teaching surface, not an optimizer. It exists to show learners that
re-sampling alone can rescue a borderline reply when the habit cards
themselves are sound.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from prompt_evolution.hermes_client import HermesAgentRunner, HermesResponse
from skill_mastery.config import SkillMasteryProfile
from skill_mastery.evaluator import SkillEvaluationResult, evaluate_response
from skill_mastery.learner import LearnedHabit


@dataclass(frozen=True)
class CandidateScore:
    """One scored draft candidate produced by the reranker."""

    candidate_index: int
    response_text: str
    evaluation: SkillEvaluationResult
    task_id: str


@dataclass(frozen=True)
class RerankResult:
    """Aggregate output from a best-of-N rerank pass."""

    candidates: tuple[CandidateScore, ...]
    best_index: int

    @property
    def best(self) -> CandidateScore:
        """Return the winning candidate."""
        return self.candidates[self.best_index]


DraftFunction = Callable[[str, str, str], HermesResponse]


def _default_draft(
    runner: HermesAgentRunner,
) -> DraftFunction:
    """Return a draft function bound to a Hermes runner instance."""

    def _run(system_prompt: str, user_prompt: str, task_id: str) -> HermesResponse:
        return runner.run_text(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            task_id=task_id,
        )

    return _run


def rerank_drafts(  # pylint: disable=too-many-arguments
    *,
    profile: SkillMasteryProfile,
    selected_habits: list[LearnedHabit],
    system_prompt: str,
    user_prompt: str,
    candidate_count: int = 3,
    runner: HermesAgentRunner | None = None,
    draft_function: DraftFunction | None = None,
    base_task_id: str = "skill-mastery-rerank",
) -> RerankResult:
    """Generate multiple drafts under one habit selection and pick the best."""
    if candidate_count < 1:
        raise ValueError("candidate_count must be at least 1")
    if draft_function is None:
        active_runner = runner or HermesAgentRunner.from_env()
        draft_function = _default_draft(active_runner)
    candidates: list[CandidateScore] = []
    for index in range(candidate_count):
        task_id = f"{base_task_id}-{index + 1}"
        response = draft_function(system_prompt, user_prompt, task_id)
        evaluation = evaluate_response(profile, selected_habits, response.text)
        candidates.append(
            CandidateScore(
                candidate_index=index,
                response_text=response.text,
                evaluation=evaluation,
                task_id=task_id,
            )
        )
    best_index = max(
        range(len(candidates)),
        key=lambda i: (
            candidates[i].evaluation.total_score,
            -i,
        ),
    )
    return RerankResult(candidates=tuple(candidates), best_index=best_index)


def render_summary(result: RerankResult) -> str:
    """Render a compact text summary of the rerank outcome."""
    lines: list[str] = ["Reranker candidates:"]
    for candidate in result.candidates:
        marker = "*" if candidate.candidate_index == result.best_index else " "
        score = candidate.evaluation.total_score
        total = candidate.evaluation.max_score
        lines.append(
            f"  {marker} candidate {candidate.candidate_index + 1}: "
            f"score {score}/{total} task={candidate.task_id}"
        )
    return "\n".join(lines)
