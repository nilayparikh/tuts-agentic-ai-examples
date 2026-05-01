"""Fixed-referee CLI entry for Prompt Evolution.

Mirrors `cleanloop/prepare.py`. CleanLoop's prepare module wraps the fixed
judge so the CLI can score the current `clean_data.py` genome against the
reference output without running the full mutation loop. Prompt Evolution's
analog scores a candidate reply against the deterministic evaluator and an
optional gold reference response.

Use this when you want to confirm an instruction prompt produces a passing
reply before opening the loop, or to compare a draft response against the
shipped `.gold/<scenario>.md` baseline.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from prompt_evolution.config import (
    PromptEvolutionCatalog,
    SelectionProfile,
    load_catalog,
    resolve_scenario_profile,
)
from prompt_evolution.evaluator import EvaluationResult, evaluate_response

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EXAMPLE_ROOT = PROJECT_ROOT / "prompt_evolution"
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

    profile: SelectionProfile
    candidate_evaluation: EvaluationResult
    gold_comparison: GoldComparison


def _load_gold(scenario_slug: str) -> str | None:
    """Load the gold reference response for a scenario when available."""
    if not GOLD_DIR.exists():
        return None
    candidate = GOLD_DIR / f"{scenario_slug}.md"
    if not candidate.exists():
        return None
    return candidate.read_text(encoding="utf-8")


def evaluate_candidate(
    catalog: PromptEvolutionCatalog,
    *,
    scenario_slug: str,
    candidate_text: str,
    preference_pairs: list[str] | None = None,
) -> PrepareResult:
    """Score a candidate reply for a named scenario against the evaluator and gold."""
    profile = resolve_scenario_profile(
        catalog,
        scenario_slug=scenario_slug,
        preference_pairs=list(preference_pairs or []),
    )
    candidate_eval = evaluate_response(profile, candidate_text)
    gold_text = _load_gold(scenario_slug)
    if gold_text is None:
        comparison = GoldComparison(
            has_gold=False,
            gold_score=0,
            gold_total=candidate_eval.max_score,
            candidate_score=candidate_eval.total_score,
            candidate_total=candidate_eval.max_score,
        )
    else:
        gold_eval = evaluate_response(profile, gold_text)
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
    lines = [
        f"Scenario: {result.profile.scenario.slug if result.profile.scenario else '-'}",
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
        lines.append("Gold reference: not available for this scenario.")
    return "\n".join(lines)


def main(scenario_slug: str, candidate_path: Path | str) -> int:
    """CLI entrypoint that scores a candidate reply file."""
    catalog = load_catalog(DATA_DIR)
    candidate_text = Path(candidate_path).read_text(encoding="utf-8")
    result = evaluate_candidate(
        catalog,
        scenario_slug=scenario_slug,
        candidate_text=candidate_text,
    )
    print(render_result(result))
    return 0 if result.candidate_evaluation.total_score >= 0 else 1
