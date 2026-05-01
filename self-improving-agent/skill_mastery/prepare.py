"""Fixed-referee CLI entry for Skill Mastery.

Mirrors `cleanloop/prepare.py` and `prompt_evolution/prepare.py`. CleanLoop
scores the current genome against a reference output. Skill Mastery's analog
scores a candidate reply for one named use case against the deterministic
evaluator and an optional gold reference response.

Use this when you want to confirm a candidate reply produces a passing score
before opening the full habit loop, or to compare a draft response against
the shipped `.gold/<usecase>.md` baseline.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from skill_mastery.config import (
    SkillMasteryCatalog,
    SkillMasteryProfile,
    load_catalog,
    resolve_usecase_profile,
)
from skill_mastery.evaluator import SkillEvaluationResult, evaluate_response
from skill_mastery.learner import learn_reusable_habits
from skill_mastery.selector import select_habits

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EXAMPLE_ROOT = PROJECT_ROOT / "skill_mastery"
DATA_DIR = EXAMPLE_ROOT / ".data"
GOLD_DIR = EXAMPLE_ROOT / ".gold"


@dataclass(frozen=True)
class GoldComparison:
    """Comparison between a candidate reply and a gold reference."""

    has_gold: bool
    gold_score: int
    gold_total: int
    candidate_score: int
    candidate_total: int

    @property
    def candidate_meets_gold(self) -> bool:
        """Return whether the candidate matches or beats the gold score."""
        if not self.has_gold:
            return self.candidate_score >= self.candidate_total
        return self.candidate_score >= self.gold_score


@dataclass(frozen=True)
class PrepareResult:
    """Aggregate result for one prepare-style evaluation."""

    profile: SkillMasteryProfile
    candidate_evaluation: SkillEvaluationResult
    gold_comparison: GoldComparison


def _load_gold(usecase_slug: str, gold_dir: Path = GOLD_DIR) -> str | None:
    """Load the gold reference response for a use case when available."""
    if not gold_dir.exists():
        return None
    candidate = gold_dir / f"{usecase_slug}.md"
    if not candidate.exists():
        return None
    return candidate.read_text(encoding="utf-8")


def evaluate_candidate(
    catalog: SkillMasteryCatalog,
    *,
    usecase_slug: str,
    candidate_text: str,
    gold_dir: Path = GOLD_DIR,
) -> PrepareResult:
    """Score a candidate reply for a named use case against evaluator and gold."""
    profile = resolve_usecase_profile(
        catalog,
        usecase_slug=usecase_slug,
    )
    learned = learn_reusable_habits(catalog)
    selected = select_habits(profile, learned)
    candidate_eval = evaluate_response(profile, selected, candidate_text)
    gold_text = _load_gold(usecase_slug, gold_dir=gold_dir)
    if gold_text is None:
        comparison = GoldComparison(
            has_gold=False,
            gold_score=0,
            gold_total=candidate_eval.max_score,
            candidate_score=candidate_eval.total_score,
            candidate_total=candidate_eval.max_score,
        )
    else:
        gold_eval = evaluate_response(profile, selected, gold_text)
        comparison = GoldComparison(
            has_gold=True,
            gold_score=gold_eval.total_score,
            gold_total=gold_eval.max_score,
            candidate_score=candidate_eval.total_score,
            candidate_total=candidate_eval.max_score,
        )
    return PrepareResult(
        profile=profile,
        candidate_evaluation=candidate_eval,
        gold_comparison=comparison,
    )


def render_result(result: PrepareResult) -> str:
    """Render the prepare result as plain-text learner output."""
    cand = result.candidate_evaluation
    comp = result.gold_comparison
    usecase = result.profile.usecase
    lines = [
        f"Use case: {usecase.slug if usecase else '-'}",
        f"Candidate score: {cand.total_score}/{cand.max_score}",
    ]
    if cand.issues:
        lines.append("Issues:")
        lines.extend(f"  - {issue}" for issue in cand.issues)
    if cand.strengths:
        lines.append("Strengths:")
        lines.extend(f"  + {item}" for item in cand.strengths[:5])
    if comp.has_gold:
        lines.append(
            f"Gold reference score: {comp.gold_score}/{comp.gold_total} "
            f"(candidate meets gold: {comp.candidate_meets_gold})"
        )
    else:
        lines.append("Gold reference: not available for this use case.")
    return "\n".join(lines)


def main(usecase_slug: str, candidate_path: Path | str) -> int:
    """CLI entrypoint that scores a candidate reply file."""
    catalog = load_catalog(DATA_DIR)
    candidate_text = Path(candidate_path).read_text(encoding="utf-8")
    result = evaluate_candidate(
        catalog,
        usecase_slug=usecase_slug,
        candidate_text=candidate_text,
    )
    print(render_result(result))
    return 0 if result.candidate_evaluation.total_score >= 0 else 1
