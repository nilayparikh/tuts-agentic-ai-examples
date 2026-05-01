"""Best-of-N draft reranker for Prompt Evolution.

Mirrors `cleanloop/reranker.py`. CleanLoop generates several candidate
mutation proposals and keeps the highest-scoring one against the fixed judge.
Prompt Evolution's analog generates several candidate replies for a single
instruction prompt and keeps the highest-scoring one against the deterministic
evaluator. The instruction prompt does not change during reranking. Only the
candidate reply varies, exposing the model's intra-prompt variance.

This is a teaching surface, not an optimizer. It exists to show learners that
re-sampling alone can rescue a borderline reply when the instruction prompt
itself is sound.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from prompt_evolution.config import PromptEvolutionCatalog, SelectionProfile
from prompt_evolution.evaluator import EvaluationResult, evaluate_response
from prompt_evolution.hermes_client import HermesAgentRunner, HermesResponse


@dataclass(frozen=True)
class CandidateScore:
    """One scored draft candidate produced by the reranker."""

    candidate_index: int
    response_text: str
    evaluation: EvaluationResult
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
    catalog: PromptEvolutionCatalog,
    profile: SelectionProfile,
    system_prompt: str,
    user_prompt: str,
    candidate_count: int = 3,
    runner: HermesAgentRunner | None = None,
    draft_function: DraftFunction | None = None,
    base_task_id: str = "prompt-evolution-rerank",
) -> RerankResult:
    """Generate multiple drafts under one instruction prompt and pick the best."""
    if candidate_count < 1:
        raise ValueError("candidate_count must be at least 1")
    if draft_function is None:
        active_runner = runner or HermesAgentRunner.from_env()
        draft_function = _default_draft(active_runner)
    _ = catalog  # Reserved for future preference-aware variation.
    candidates: list[CandidateScore] = []
    for index in range(candidate_count):
        task_id = f"{base_task_id}-{index + 1}"
        response = draft_function(system_prompt, user_prompt, task_id)
        evaluation = evaluate_response(profile, response.text)
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
