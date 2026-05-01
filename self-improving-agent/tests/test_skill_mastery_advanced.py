"""Tests for the advanced Skill Mastery modules."""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from typing import Any

# pylint: disable=import-error,wrong-import-position

from skill_mastery.autonomy import (
    AUTONOMOUS,
    HUMAN_GATED,
    SUPERVISED,
    RoundSnapshot,
    evaluate_ladder,
    render_decision,
)
from skill_mastery.challenger import (
    attach_variants,
    context_for_usecase,
    generate_variant,
    generate_variants,
    render_variant_summary,
)
from skill_mastery.config import (
    SkillMasteryCatalog,
    load_catalog,
    resolve_usecase_profile,
)
from skill_mastery.dashboard_artifacts import load_artifacts
from skill_mastery.dashboard_metrics import (
    compute_issue_distribution,
    compute_session_metrics,
)
from skill_mastery.evaluator import SkillEvaluationResult, evaluate_response
from skill_mastery.history_store import HistoryStore, filter_by_session, select_best
from skill_mastery.learner import learn_reusable_habits
from skill_mastery.mutation_playbook import (
    DEFAULT_FALLBACK,
    POLICY_COVERAGE,
    HABIT_SIGNAL,
    FORBIDDEN_GUARD,
    CONTEXT_GROUNDING,
    categorize_issues,
    render_brief,
    select_strategies,
)
from skill_mastery.prepare import evaluate_candidate
from skill_mastery.reranker import (
    CandidateScore,
    RerankResult,
    rerank_drafts,
)
from skill_mastery.reset_workflow import reset, render_report
from skill_mastery.sandbox import SandboxResult, render_result
from skill_mastery.selector import select_habits
from skill_mastery.status_snapshot import collect_status, status_payload

_DATA_DIR = Path(__file__).resolve().parent.parent / "skill_mastery" / ".data"


def _catalog() -> SkillMasteryCatalog:
    return load_catalog(_DATA_DIR)


def _first_usecase(catalog: SkillMasteryCatalog) -> Any:
    return next(iter(catalog.usecases.values()))


def _profile_for_first(catalog: SkillMasteryCatalog) -> Any:
    case = _first_usecase(catalog)
    return resolve_usecase_profile(catalog, usecase_slug=case.slug)


class FakeHermesResponse:
    def __init__(self, text: str) -> None:
        self.text = text
        self.messages: list[dict[str, str]] = []
        self.raw_output: list[Any] = []


class AutonomyLadderTests(unittest.TestCase):
    def test_empty_rounds_return_supervised(self) -> None:
        decision = evaluate_ladder([])
        self.assertEqual(decision.level, SUPERVISED)
        joined = " ".join(decision.notes).lower()
        self.assertIn("no rounds observed", joined)

    def test_high_stable_promotes_to_autonomous(self) -> None:
        snapshots = [RoundSnapshot(score=8, total=8) for _ in range(5)]
        decision = evaluate_ladder(snapshots)
        self.assertEqual(decision.level, AUTONOMOUS)

    def test_high_but_unstable_demotes_to_human_gated(self) -> None:
        snapshots = [
            RoundSnapshot(score=8, total=8),
            RoundSnapshot(score=8, total=8),
            RoundSnapshot(score=4, total=8),
        ]
        decision = evaluate_ladder(snapshots)
        self.assertEqual(decision.level, HUMAN_GATED)

    def test_render_decision_returns_text(self) -> None:
        decision = evaluate_ladder([RoundSnapshot(score=4, total=8)])
        text = render_decision(decision)
        self.assertIn("Autonomy", text)


class ChallengerTests(unittest.TestCase):
    def test_invalid_tier_raises(self) -> None:
        catalog = _catalog()
        case = _first_usecase(catalog)
        with self.assertRaises(ValueError):
            generate_variant(case, tier_index=0)
        with self.assertRaises(ValueError):
            generate_variant(case, tier_index=4)

    def test_generate_variants_returns_three(self) -> None:
        catalog = _catalog()
        case = _first_usecase(catalog)
        variants = generate_variants(case)
        self.assertEqual(len(variants), 3)

    def test_attach_variants_extends_catalog(self) -> None:
        catalog = _catalog()
        case = _first_usecase(catalog)
        variants = generate_variants(case)
        new_catalog = attach_variants(catalog, variants)
        self.assertGreater(len(new_catalog.usecases), len(catalog.usecases))

    def test_render_summary_includes_slug(self) -> None:
        catalog = _catalog()
        case = _first_usecase(catalog)
        variants = generate_variants(case)
        text = render_variant_summary(variants)
        self.assertIn(variants[0].slug, text)

    def test_context_for_usecase_returns_pack(self) -> None:
        catalog = _catalog()
        case = _first_usecase(catalog)
        ctx = context_for_usecase(catalog, case)
        self.assertEqual(ctx.slug, case.context_slug)


class RerankerTests(unittest.TestCase):
    def _profile_and_habits(self) -> tuple[Any, list[Any]]:
        catalog = _catalog()
        profile = _profile_for_first(catalog)
        habits = learn_reusable_habits(catalog)
        selected = select_habits(profile, habits)
        return profile, selected

    def test_invalid_candidate_count_raises(self) -> None:
        profile, selected = self._profile_and_habits()
        with self.assertRaises(ValueError):
            rerank_drafts(
                profile=profile,
                selected_habits=selected,
                system_prompt="sys",
                user_prompt="usr",
                candidate_count=0,
            )

    def test_higher_score_wins_with_tie_break(self) -> None:
        profile, selected = self._profile_and_habits()
        outputs = [
            "weak reply.",
            "another weak reply.",
            "weak reply.",
        ]
        index_holder = {"i": 0}

        def fake_draft(system: str, user: str, task: str) -> FakeHermesResponse:
            del system, user, task
            text = outputs[index_holder["i"]]
            index_holder["i"] += 1
            return FakeHermesResponse(text)

        result = rerank_drafts(
            profile=profile,
            selected_habits=selected,
            system_prompt="sys",
            user_prompt="usr",
            candidate_count=3,
            draft_function=fake_draft,
        )
        self.assertIsInstance(result, RerankResult)
        self.assertIsInstance(result.best, CandidateScore)
        self.assertEqual(result.best_index, 0)


class HistoryStoreTests(unittest.TestCase):
    def test_append_and_load_roundtrip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = HistoryStore(output_dir=Path(tmp))
            store.append({"round": 1, "score": 5, "total": 8})
            store.append_many(
                [
                    {"round": 2, "score": 7, "total": 8},
                    {"round": 3, "score": 7, "total": 8},
                ]
            )
            records = store.load()
            self.assertEqual(len(records), 3)
            best = select_best(records)
            self.assertIsNotNone(best)
            assert best is not None
            self.assertEqual(best["score"], 7)
            self.assertEqual(best["round"], 3)
            store.reset()
            self.assertEqual(store.load(), [])

    def test_filter_by_session(self) -> None:
        records = [
            {"session_id": "a", "round": 1},
            {"session_id": "b", "round": 1},
            {"session_id": "a", "round": 2},
        ]
        filtered = filter_by_session(records, "a")
        self.assertEqual(len(filtered), 2)


class MutationPlaybookTests(unittest.TestCase):
    @staticmethod
    def _result(issues: list[str]) -> SkillEvaluationResult:
        return SkillEvaluationResult(
            total_score=0, max_score=8, issues=issues, strengths=[]
        )

    def test_policy_coverage_trigger(self) -> None:
        chosen = select_strategies(
            self._result(["Missing policy coverage: fees are non-refundable."])
        )
        self.assertIn(POLICY_COVERAGE, chosen)

    def test_habit_signal_trigger(self) -> None:
        chosen = select_strategies(self._result(["Missing habit signal: empathy"]))
        self.assertIn(HABIT_SIGNAL, chosen)

    def test_forbidden_guard_trigger(self) -> None:
        chosen = select_strategies(
            self._result(["Forbidden promise detected: guaranteed refund"])
        )
        self.assertIn(FORBIDDEN_GUARD, chosen)

    def test_context_grounding_trigger(self) -> None:
        chosen = select_strategies(
            self._result(["Missing grounding from the selected service context."])
        )
        self.assertIn(CONTEXT_GROUNDING, chosen)

    def test_default_fallback_when_no_match(self) -> None:
        chosen = select_strategies(self._result(["Some unmatched issue"]))
        self.assertEqual(tuple(chosen), (DEFAULT_FALLBACK,))

    def test_render_brief_includes_directives(self) -> None:
        catalog = _catalog()
        profile = _profile_for_first(catalog)
        habits = learn_reusable_habits(catalog)
        selected = select_habits(profile, habits)
        chosen = select_strategies(self._result(["Missing habit signal: empathy"]))
        brief = render_brief(chosen, profile, selected)
        self.assertIn("1.", brief)
        self.assertTrue(any(h.slug in brief for h in selected))

    def test_categorize_issues_buckets(self) -> None:
        result = self._result(
            [
                "Missing policy coverage: x",
                "Missing habit signal: y",
                "unrelated",
            ]
        )
        buckets = categorize_issues(result)
        self.assertIn(POLICY_COVERAGE.slug, buckets)
        self.assertIn(HABIT_SIGNAL.slug, buckets)


class PrepareTests(unittest.TestCase):
    def test_candidate_meets_gold(self) -> None:
        catalog = _catalog()
        slug = next(iter(catalog.usecases.keys()))
        gold_path = _DATA_DIR.parent / ".gold" / f"{slug}.md"
        if not gold_path.exists():
            self.skipTest(f"no gold reply for {slug}")
        candidate_text = gold_path.read_text(encoding="utf-8")
        result = evaluate_candidate(
            catalog,
            usecase_slug=slug,
            candidate_text=candidate_text,
        )
        self.assertTrue(result.gold_comparison.has_gold)
        self.assertTrue(result.gold_comparison.candidate_meets_gold)


class ResetWorkflowTests(unittest.TestCase):
    def test_reset_preserves_protected_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = Path(tmp)
            (out_dir / ".gitignore").write_text("*\n", encoding="utf-8")
            (out_dir / "README.md").write_text("# stays\n", encoding="utf-8")
            (out_dir / "transient.json").write_text("{}", encoding="utf-8")
            (out_dir / "traces").mkdir()
            (out_dir / "traces" / "events.jsonl").write_text("{}\n", encoding="utf-8")

            report = reset(output_dir=out_dir)
            text = render_report(report)

            self.assertTrue((out_dir / ".gitignore").exists())
            self.assertTrue((out_dir / "README.md").exists())
            self.assertFalse((out_dir / "transient.json").exists())
            self.assertFalse((out_dir / "traces").exists())
            self.assertIn("Gold references kept", text)


class StatusSnapshotTests(unittest.TestCase):
    def test_collect_status_counts_artifacts(self) -> None:
        status = collect_status(data_dir=_DATA_DIR)
        self.assertEqual(status.catalog.contexts, 3)
        self.assertEqual(status.catalog.usecases, 3)
        self.assertGreaterEqual(status.catalog.gold_references, 0)
        payload = status_payload(status)
        self.assertIn("catalog", payload)


class SandboxResultTests(unittest.TestCase):
    def test_render_result_includes_habit_slugs(self) -> None:
        catalog = _catalog()
        profile = _profile_for_first(catalog)
        habits = learn_reusable_habits(catalog)
        selected = tuple(select_habits(profile, habits))
        evaluation = evaluate_response(profile, list(selected), "draft")
        result = SandboxResult(
            response_text="draft",
            evaluation=evaluation,
            selected_habits=selected,
            elapsed_seconds=0.1,
            timed_out=False,
            iteration_clamp=4,
        )
        text = render_result(result)
        self.assertIn(selected[0].slug, text)


class DashboardArtifactsTests(unittest.TestCase):
    def test_load_artifacts_with_synthetic_jsonl(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            session = base / "session.json"
            session.write_text(
                json.dumps({"best_round": 2, "rounds": [{"round": 1}, {"round": 2}]}),
                encoding="utf-8",
            )
            traces = base / "traces"
            traces.mkdir()
            (traces / "run_events.jsonl").write_text(
                json.dumps({"event": "round_start", "round": 1}) + "\n",
                encoding="utf-8",
            )
            (traces / "habit_events.jsonl").write_text("", encoding="utf-8")
            (traces / "llm_requests.jsonl").write_text(
                json.dumps({"task_id": "t1"}) + "\n",
                encoding="utf-8",
            )
            (traces / "evaluator_events.jsonl").write_text(
                json.dumps({"score": 4, "total": 8}) + "\n",
                encoding="utf-8",
            )
            artifacts = load_artifacts(session_path=session, trace_dir=traces)
            self.assertEqual(len(artifacts.run_events), 1)
            self.assertEqual(len(artifacts.llm_requests), 1)
            metrics = compute_session_metrics(artifacts)
            self.assertEqual(metrics.llm_request_count, 1)
            distribution = compute_issue_distribution(artifacts)
            self.assertGreaterEqual(distribution.rounds_clean, 0)


class CliRegistrationTests(unittest.TestCase):
    def test_skill_mastery_commands_registered(self) -> None:
        os.environ.setdefault("SKILL_MASTERY_TEST", "1")
        import util  # type: ignore  # pylint: disable=import-outside-toplevel

        sm = util.EXAMPLE_COMMANDS["skill_mastery"]
        for key in (
            "catalog",
            "usecases",
            "loop",
            "dashboard",
            "evaluate",
            "sandbox",
            "autonomy",
            "challenge",
            "verify",
            "status",
            "reset",
        ):
            self.assertIn(key, sm)


if __name__ == "__main__":
    unittest.main()
