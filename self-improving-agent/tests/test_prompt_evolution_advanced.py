"""Tests for advanced prompt evolution modules.

Covers mutation playbook routing, reranker selection, autonomy ladder,
challenger variants, status snapshot, and reset workflow.
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

# pylint: disable=wrong-import-position,too-few-public-methods,import-error

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from prompt_evolution import (
    autonomy,
    challenger,
    config as pe_config,
    evaluator,
    history_store,
    mutation_playbook,
    prepare,
    reset_workflow,
    status_snapshot,
)
from prompt_evolution.config import resolve_scenario_profile
from prompt_evolution.evaluator import EvaluationResult

CATALOG = pe_config.load_catalog(PROJECT_ROOT / "prompt_evolution" / ".data")
GOLD_DIR = PROJECT_ROOT / "prompt_evolution" / ".gold"


def _profile(slug: str = "makerspace_missing_booking"):
    """Build a default selection profile for `slug`."""
    return resolve_scenario_profile(CATALOG, scenario_slug=slug, preference_pairs=[])


class MutationPlaybookTests(unittest.TestCase):
    """Verify playbook routes evaluator issues to bounded strategies."""

    def test_select_strategies_returns_default_when_no_issues(self) -> None:
        """Empty issue list should still return at least one bounded strategy."""
        empty_eval = EvaluationResult(
            total_score=10, max_score=10, issues=[], strengths=[]
        )
        strategies = mutation_playbook.select_strategies(empty_eval)
        self.assertGreaterEqual(len(strategies), 1)

    def test_select_strategies_routes_policy_gap(self) -> None:
        """A 'Missing policy coverage' issue triggers the policy strategy."""
        evaluation = EvaluationResult(
            total_score=2,
            max_score=10,
            issues=["Missing policy coverage: Bench bookings open 24 hours before."],
            strengths=[],
        )
        names = {
            strategy.slug
            for strategy in mutation_playbook.select_strategies(evaluation)
        }
        self.assertIn("policy_coverage", names)

    def test_render_brief_includes_strategy_names(self) -> None:
        """The rendered brief should mention each selected strategy by name."""
        evaluation = EvaluationResult(
            total_score=0,
            max_score=10,
            issues=["Forbidden policy promise detected: bench restored automatically"],
            strengths=[],
        )
        strategies = mutation_playbook.select_strategies(evaluation)
        text = mutation_playbook.render_brief(strategies, _profile())
        for strategy in strategies:
            self.assertIn(strategy.label, text)


class AutonomyLadderTests(unittest.TestCase):
    """Verify the autonomy decision logic."""

    def test_high_consistent_score_grants_autonomous_or_human_gated(self) -> None:
        """A high stable score should land at AUTONOMOUS or HUMAN_GATED tier."""
        snapshots = [autonomy.RoundSnapshot(score=10, total=10) for _ in range(5)]
        decision = autonomy.evaluate_ladder(snapshots)
        self.assertIn(decision.level, {autonomy.AUTONOMOUS, autonomy.HUMAN_GATED})

    def test_low_score_falls_back_to_supervised(self) -> None:
        """Consistently low scores stay in supervised tier."""
        snapshots = [autonomy.RoundSnapshot(score=2, total=10) for _ in range(3)]
        decision = autonomy.evaluate_ladder(snapshots)
        self.assertEqual(decision.level, autonomy.SUPERVISED)


class ChallengerTests(unittest.TestCase):
    """Verify adversarial variant generation."""

    def test_generate_variants_returns_one_per_level(self) -> None:
        """The challenger must emit one variant per requested level."""
        case = CATALOG.scenarios["makerspace_missing_booking"]
        variants = challenger.generate_variants(case, tiers=[1, 2, 3])
        self.assertEqual(len(variants), 3)
        for variant in variants:
            self.assertNotEqual(variant.label, case.label)


class HistoryStoreTests(unittest.TestCase):
    """Verify durable round history persistence."""

    def test_append_then_load_round_trips(self) -> None:
        """Records appended to the store should be reloaded in order."""
        with tempfile.TemporaryDirectory() as tmp:
            store = history_store.HistoryStore(output_dir=Path(tmp))
            store.append({"round": 1, "score": 4})
            store.append({"round": 2, "score": 7})
            records = store.load()
        self.assertEqual([record["round"] for record in records], [1, 2])

    def test_select_best_picks_highest_score(self) -> None:
        """Best selection prefers the highest score then highest round."""
        records = [
            {"round": 1, "score": 4},
            {"round": 2, "score": 7},
            {"round": 3, "score": 7},
        ]
        best = history_store.select_best(records)
        self.assertEqual(best, {"round": 3, "score": 7})


class PrepareTests(unittest.TestCase):
    """Verify candidate evaluation against gold targets."""

    def test_evaluate_candidate_against_gold(self) -> None:
        """The shipped gold reply should evaluate to the maximum score."""
        slug = "makerspace_missing_booking"
        candidate_text = (GOLD_DIR / f"{slug}.md").read_text(encoding="utf-8")
        result = prepare.evaluate_candidate(
            CATALOG,
            scenario_slug=slug,
            candidate_text=candidate_text,
        )
        self.assertEqual(
            result.candidate_evaluation.total_score,
            result.candidate_evaluation.max_score,
        )


class StatusSnapshotTests(unittest.TestCase):
    """Verify the status snapshot inspects project state."""

    def test_collect_status_returns_payload(self) -> None:
        """Status payload should expose data, environment, and output sections."""
        status = status_snapshot.collect_status()
        payload = status_snapshot.status_payload(status)
        self.assertIn("catalog", payload)
        self.assertIn("environment", payload)
        self.assertIn("output", payload)


class ResetWorkflowTests(unittest.TestCase):
    """Verify reset preserves the gold directory."""

    def test_reset_preserves_gold_directory(self) -> None:
        """Reset should delete generated outputs and leave protected names alone."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            output_dir = tmp_path / ".output"
            output_dir.mkdir()
            (output_dir / "session.json").write_text("{}", encoding="utf-8")
            (output_dir / ".gitignore").write_text("*\n", encoding="utf-8")

            report = reset_workflow.reset(output_dir=output_dir)
        self.assertTrue(any("session.json" in path for path in report.deleted_paths))
        self.assertTrue(any(".gitignore" in path for path in report.preserved_paths))


class GoldRepliesTests(unittest.TestCase):
    """Verify all shipped gold replies score the maximum."""

    def test_all_gold_replies_score_max(self) -> None:
        """Every gold reply must hit the evaluator maximum for its scenario."""
        for slug in (
            "makerspace_missing_booking",
            "coworking_guest_refund",
            "hotel_late_credit",
            "pet_medication_update",
        ):
            with self.subTest(scenario=slug):
                profile = _profile(slug)
                text = (GOLD_DIR / f"{slug}.md").read_text(encoding="utf-8")
                result = evaluator.evaluate_response(profile, text)
                self.assertEqual(
                    result.total_score,
                    result.max_score,
                    msg=f"{slug} issues: {result.issues}",
                )


if __name__ == "__main__":  # pragma: no cover
    # Keep linters happy by referencing imports used only for typing.
    _ = json
    unittest.main()
