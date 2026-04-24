"""Regression and behavior tests for the Skill Mastery example."""

import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from importlib import import_module
from pathlib import Path
from unittest import mock

# pylint: disable=wrong-import-position,too-few-public-methods,import-error,protected-access

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import util


class SkillMasteryParserTests(unittest.TestCase):
    """Verify the unified CLI accepts the new Skill Mastery example flow."""

    def test_parser_accepts_skill_mastery_loop_arguments(self) -> None:
        """Parse a context and problem statement for the Skill Mastery loop."""
        parser = util.build_parser()

        args = parser.parse_args(
            [
                "-e",
                "skill_mastery",
                "loop",
                "--context",
                "makerspace_frontdesk",
                "--problem",
                "A member's laser cutter booking disappeared before open lab tonight.",
            ]
        )

        self.assertEqual(args.example, "skill_mastery")
        self.assertEqual(args.context, "makerspace_frontdesk")
        self.assertIn("laser cutter booking", args.problem)


class SkillMasteryCatalogTests(unittest.TestCase):
    """Verify the shipped Skill Mastery example exposes reusable-habit data."""

    def test_catalog_exposes_contexts_habits_and_demonstrations(self) -> None:
        """Load the real .data packs for contexts, habit seeds, and demonstration traces."""
        config = import_module("skill_mastery.config")

        catalog = config.load_catalog(PROJECT_ROOT / "skill_mastery" / ".data")

        self.assertIn("makerspace_frontdesk", catalog.contexts)
        self.assertIn("mirror_issue", catalog.habit_definitions)
        self.assertGreaterEqual(len(catalog.demonstrations), 6)


class SkillMasteryLearningTests(unittest.TestCase):
    """Verify the example learns reusable habits from successful traces."""

    def test_learning_promotes_reusable_habits(self) -> None:
        """Learn habits that succeed across more than one shipped context."""
        config = import_module("skill_mastery.config")
        learner = import_module("skill_mastery.learner")

        catalog = config.load_catalog(PROJECT_ROOT / "skill_mastery" / ".data")
        habits = learner.learn_reusable_habits(catalog)
        habit_slugs = [habit.slug for habit in habits]

        self.assertIn("mirror_issue", habit_slugs)
        self.assertIn("offer_checkpoint", habit_slugs)
        self.assertTrue(any(habit.context_coverage >= 2 for habit in habits))


class SkillMasterySelectionTests(unittest.TestCase):
    """Verify the example selects the right habits for a new issue."""

    def test_selector_chooses_habits_for_booking_and_access_problems(self) -> None:
        """Select policy and checkpoint habits for a makerspace access issue."""
        config = import_module("skill_mastery.config")
        learner = import_module("skill_mastery.learner")
        selector = import_module("skill_mastery.selector")

        catalog = config.load_catalog(PROJECT_ROOT / "skill_mastery" / ".data")
        profile = config.resolve_skill_profile(
            catalog,
            context_slug="makerspace_frontdesk",
            problem=(
                "My laser cutter booking vanished and I need access tonight for the open lab."
            ),
        )
        habits = learner.learn_reusable_habits(catalog)
        selected = selector.select_habits(profile, habits)
        selected_slugs = [habit.slug for habit in selected]

        self.assertIn("cite_policy_gate", selected_slugs)
        self.assertIn("offer_checkpoint", selected_slugs)


class SkillMasteryFeedbackTests(unittest.TestCase):
    """Verify Skill Mastery supports iterative user feedback after the baseline reply."""

    def test_review_guidance_explains_feedback_paths_and_expected_changes(self) -> None:
        """Show what the user can ask for and what kind of revision to expect."""
        config = import_module("skill_mastery.config")
        learner = import_module("skill_mastery.learner")
        selector = import_module("skill_mastery.selector")
        loop_module = import_module("skill_mastery.loop")

        catalog = config.load_catalog(PROJECT_ROOT / "skill_mastery" / ".data")
        profile = config.resolve_skill_profile(
            catalog,
            context_slug="makerspace_frontdesk",
            problem=(
                "My laser cutter booking vanished and I need access tonight for the "
                "open lab."
            ),
        )
        selected = selector.select_habits(profile, learner.learn_reusable_habits(catalog))

        guidance = loop_module.build_user_feedback_guide(profile, selected)

        self.assertIn("what you can ask to improve", guidance.lower())
        self.assertIn("if you ask", guidance.lower())
        self.assertIn("expect", guidance.lower())
        self.assertIn("habit", guidance.lower())

    def test_refinement_round_records_user_feedback_and_revises_reply(self) -> None:
        """Use one user feedback string to run one more Skill Mastery revision pass."""
        config = import_module("skill_mastery.config")
        learner = import_module("skill_mastery.learner")
        selector = import_module("skill_mastery.selector")
        loop_module = import_module("skill_mastery.loop")

        class FakeRunner:
            """Return one queued Hermes revision and capture prompts."""

            def __init__(self) -> None:
                self.calls: list[tuple[str, str, str]] = []

            def run_text(self, *, system_prompt: str, user_prompt: str, task_id: str):
                """Return the fake Skill Mastery revision response."""
                self.calls.append((system_prompt, user_prompt, task_id))
                return type(
                    "Response",
                    (),
                    {
                        "text": (
                            "It sounds like your booking vanished before open lab tonight. "
                            "Active tool certification is required before access is "
                            "confirmed, and bench bookings open 24 hours before the "
                            "slot. Please reply with your badge number so I can confirm "
                            "the next step."
                        )
                    },
                )()

        catalog = config.load_catalog(PROJECT_ROOT / "skill_mastery" / ".data")
        profile = config.resolve_skill_profile(
            catalog,
            context_slug="makerspace_frontdesk",
            problem="My laser cutter booking vanished and I need access tonight for the open lab.",
        )
        selected = selector.select_habits(profile, learner.learn_reusable_habits(catalog))
        runner = FakeRunner()

        updated = loop_module.run_feedback_refinement(
            profile,
            selected,
            current_response="We can help.",
            round_number=2,
            user_feedback=(
                "Be more direct. Lead with the missing booking, mention "
                "certification, and end with one confirmation question."
            ),
            runner=runner,
        )

        self.assertEqual(updated["round"], 2)
        self.assertEqual(
            updated["user_feedback"],
            (
                "Be more direct. Lead with the missing booking, mention "
                "certification, and end with one confirmation question."
            ),
        )
        self.assertIn("end with one confirmation question", runner.calls[0][1].lower())
        self.assertIn("certification", updated["response"].lower())

    def test_best_history_round_prefers_latest_round_on_tied_score(self) -> None:
        """Treat the newest round as the current best output when scores tie."""
        best_round = util._best_history_round(
            [
                {"round": 2, "score": 8, "total": 8, "response": "old best"},
                {"round": 3, "score": 8, "total": 8, "response": "new best"},
            ]
        )

        self.assertEqual(best_round["round"], 3)
        self.assertEqual(best_round["response"], "new best")

    def test_interactive_review_uses_latest_feedback_round_even_if_score_drops(self) -> None:
        """Show and select the latest feedback round instead of an older higher-scoring round."""

        def refine_once(
            feedback: str, current_round: dict[str, object], next_round: int
        ) -> dict[str, object]:
            self.assertEqual(feedback, "add callback")
            self.assertEqual(current_round["round"], 1)
            self.assertEqual(next_round, 2)
            return {
                "round": 2,
                "score": 5,
                "total": 8,
                "response": "Please email us or request a callback.",
                "issues": [],
            }

        stdout = io.StringIO()
        with mock.patch("builtins.input", side_effect=["n", "add callback", "y"]):
            with mock.patch("sys.stdout", new=stdout):
                history = util._interactive_review_loop(
                    example_label="Skill Mastery",
                    initial_history=[
                        {
                            "round": 1,
                            "score": 6,
                            "total": 8,
                            "response": "Old response.",
                            "issues": [],
                        }
                    ],
                    guidance_text="Guide",
                    refine_once=refine_once,
                )

        self.assertTrue(history[-1]["selected"])
        self.assertEqual(history[-1]["round"], 2)
        self.assertIn("round 2, score 5/8", stdout.getvalue())
        self.assertIn("Please email us or request a callback.", stdout.getvalue())


class SkillMasteryTraceTests(unittest.TestCase):
    """Verify Skill Mastery emits verbose traces, diffs, and dashboard-ready data."""

    def test_loop_records_llm_requests_logs_and_response_diffs(self) -> None:
        """Persist round traces that show the LLM calls and how the reply changed."""
        config = import_module("skill_mastery.config")
        loop_module = import_module("skill_mastery.loop")

        class FakeRunner:
            """Return queued responses and expose simple request metadata."""

            model = "demo-model"
            provider = "custom"
            base_url = "http://localhost:5272/v1"

            def __init__(self) -> None:
                self.calls: list[tuple[str, str, str]] = []
                self._responses = iter(
                    [
                        type(
                            "Response",
                            (),
                            {"text": "We can help with the booking issue."},
                        )(),
                        type(
                            "Response",
                            (),
                            {
                                "text": (
                                    "It sounds like your booking vanished before open "
                                    "lab. Active tool certification is required before "
                                    "access is confirmed, and bench bookings open 24 "
                                    "hours before the slot. Please reply with your badge "
                                    "number so I can confirm the next step."
                                )
                            },
                        )(),
                    ]
                )

            def run_text(self, *, system_prompt: str, user_prompt: str, task_id: str):
                """Return the next fake Skill Mastery response."""
                self.calls.append((system_prompt, user_prompt, task_id))
                return next(self._responses)

        catalog = config.load_catalog(PROJECT_ROOT / "skill_mastery" / ".data")
        profile = config.resolve_skill_profile(
            catalog,
            context_slug="makerspace_frontdesk",
            problem="My laser cutter booking vanished and I need access tonight for the open lab.",
        )
        runner = FakeRunner()
        logs: list[str] = []

        with tempfile.TemporaryDirectory() as tmp_dir:
            with mock.patch.object(loop_module, "OUTPUT_DIR", Path(tmp_dir)):
                history = loop_module.run_skill_mastery(
                    catalog,
                    profile,
                    max_iterations=2,
                    runner=runner,
                    log_sink=logs.append,
                )

                self.assertEqual(len(history), 2)
                self.assertIn("llm", history[0])
                self.assertIn("requests", history[0]["llm"])
                self.assertTrue(history[0]["llm"]["requests"])
                self.assertIn("mutation_diff", history[1])
                self.assertIn(
                    "-We can help with the booking issue.",
                    history[1]["mutation_diff"],
                )
                self.assertIn(
                    "+It sounds like your booking vanished before open lab.",
                    history[1]["mutation_diff"],
                )
                self.assertTrue((Path(tmp_dir) / "latest_mutation.diff").exists())

        joined_logs = "\n".join(logs)
        self.assertIn("REQUESTING_LLM_DRAFT", joined_logs)
        self.assertIn("REQUESTING_LLM_REVISION", joined_logs)
        self.assertIn("RESPONSE_DIFF", joined_logs)

    def test_dashboard_helpers_expose_round_diffs(self) -> None:
        """Provide a dashboard helper that renders the response diff."""
        dashboard = import_module("skill_mastery.dashboard")

        diff_text = dashboard.build_round_diff(
            "We can help.\n",
            "We can help.\nPlease confirm your badge number.\n",
        )

        self.assertIn(" We can help.", diff_text)
        self.assertIn("+Please confirm your badge number.", diff_text)

    def test_dashboard_script_runs_without_project_root_already_on_sys_path(self) -> None:
        """Allow the dashboard script to run outside the repo root."""
        dashboard_dir = PROJECT_ROOT / "skill_mastery"
        result = subprocess.run(
            [
                sys.executable,
                "-c",
                "import runpy; runpy.run_path('dashboard.py', run_name='__test__')",
            ],
            cwd=dashboard_dir,
            capture_output=True,
            text=True,
            check=False,
            env={
                key: value
                for key, value in os.environ.items()
                if key != "PYTHONPATH"
            },
        )

        self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)

    def test_save_outputs_prefers_user_selected_round_over_higher_score(self) -> None:
        """Persist the accepted round when interactive review selected it."""
        config = import_module("skill_mastery.config")
        learner = import_module("skill_mastery.learner")
        selector = import_module("skill_mastery.selector")
        loop_module = import_module("skill_mastery.loop")

        catalog = config.load_catalog(PROJECT_ROOT / "skill_mastery" / ".data")
        profile = config.resolve_skill_profile(
            catalog,
            context_slug="makerspace_frontdesk",
            problem=(
                "My laser cutter booking vanished and I need access tonight for the "
                "open lab."
            ),
        )
        learned_habits = learner.learn_reusable_habits(catalog)
        selected_habits = selector.select_habits(profile, learned_habits)

        with tempfile.TemporaryDirectory() as tmp_dir:
            with mock.patch.object(loop_module, "OUTPUT_DIR", Path(tmp_dir)):
                loop_module.save_outputs(
                    profile,
                    learned_habits,
                    selected_habits,
                    [
                        {
                            "round": 1,
                            "score": 6,
                            "total": 8,
                            "response": "Older higher-scored response.",
                            "issues": [],
                        },
                        {
                            "round": 2,
                            "score": 5,
                            "total": 8,
                            "response": "Accepted callback response.",
                            "issues": [],
                            "selected": True,
                        },
                    ],
                )

                latest_session = json.loads(
                    (Path(tmp_dir) / "latest_session.json").read_text(encoding="utf-8")
                )
                best_response = (Path(tmp_dir) / "best_response.md").read_text(
                    encoding="utf-8"
                )

        self.assertEqual(latest_session["best_round"], 2)
        self.assertEqual(best_response, "Accepted callback response.")
