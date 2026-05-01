"""Regression and behavior tests for the Prompt Evolution example."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from importlib import import_module
from pathlib import Path
from unittest import mock

# pylint: disable=wrong-import-position,too-few-public-methods,import-error

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from cleanloop import loop as cleanloop_loop
import util


class PromptEvolutionParserTests(unittest.TestCase):
    """Verify the unified CLI accepts the new prompt evolution example flow."""

    def test_parser_accepts_prompt_evolution_loop_arguments(self) -> None:
        """Parse context, multiple preferences, and a free-text problem."""
        parser = util.build_parser()

        args = parser.parse_args(
            [
                "-e",
                "prompt_evolution",
                "loop",
                "--context",
                "coworking_membership",
                "--preference",
                "tone=warm",
                "--preference",
                "structure=bullets",
                "--preference",
                "initiative=next_step",
                "--problem",
                "A member says their guest booking vanished before tonight's workshop.",
            ]
        )

        self.assertEqual(args.example, "prompt_evolution")
        self.assertEqual(args.context, "coworking_membership")
        self.assertEqual(
            args.preference,
            ["tone=warm", "structure=bullets", "initiative=next_step"],
        )
        self.assertIn("guest booking vanished", args.problem)

    def test_parser_accepts_prompt_evolution_scenario_argument(self) -> None:
        """Parse a predefined Prompt Evolution support-desk scenario."""
        parser = util.build_parser()

        args = parser.parse_args(
            [
                "-e",
                "prompt_evolution",
                "loop",
                "--scenario",
                "makerspace_missing_booking",
                "--preference",
                "tone=direct",
            ]
        )

        self.assertEqual(args.example, "prompt_evolution")
        self.assertEqual(args.scenario, "makerspace_missing_booking")
        self.assertEqual(args.preference, ["tone=direct"])


class PromptEvolutionCatalogTests(unittest.TestCase):
    """Verify the shipped prompt evolution example exposes real selection data."""

    def test_shipped_catalog_exposes_contexts_and_preference_axes(self) -> None:
        """Load the real .data catalog with predefined contexts and preference selections."""
        config = import_module("prompt_evolution.config")

        catalog = config.load_catalog(PROJECT_ROOT / "prompt_evolution" / ".data")

        self.assertIn("coworking_membership", catalog.contexts)
        self.assertIn("tone", catalog.preference_axes)
        self.assertIn("structure", catalog.preference_axes)
        self.assertIn("initiative", catalog.preference_axes)

    def test_catalog_now_includes_more_diverse_contexts_and_axes(self) -> None:
        """Ship broader service domains and richer preference axes that still compose cleanly."""
        config = import_module("prompt_evolution.config")

        catalog = config.load_catalog(PROJECT_ROOT / "prompt_evolution" / ".data")

        self.assertIn("makerspace_frontdesk", catalog.contexts)
        self.assertIn("language_school", catalog.contexts)
        self.assertIn("pet_boarding", catalog.contexts)
        self.assertIn("evidence", catalog.preference_axes)
        self.assertIn("closing", catalog.preference_axes)

    def test_catalog_loads_named_support_desk_scenarios(self) -> None:
        """Load scenario cases with default preferences and success criteria."""
        config = import_module("prompt_evolution.config")

        catalog = config.load_catalog(PROJECT_ROOT / "prompt_evolution" / ".data")
        scenario = catalog.scenarios["makerspace_missing_booking"]

        self.assertEqual(scenario.context_slug, "makerspace_frontdesk")
        self.assertIn("laser cutter", scenario.customer_problem.lower())
        self.assertEqual(scenario.default_preferences["structure"], "bullets")
        self.assertIn("certification_gate", scenario.expected_policy_slugs)
        self.assertTrue(scenario.success_criteria)

    def test_scenario_profile_uses_defaults_and_cli_overrides(self) -> None:
        """Build a runnable selection profile from a named scenario."""
        config = import_module("prompt_evolution.config")

        catalog = config.load_catalog(PROJECT_ROOT / "prompt_evolution" / ".data")
        profile = config.resolve_scenario_profile(
            catalog,
            scenario_slug="makerspace_missing_booking",
            preference_pairs=["tone=warm", "closing=confirm_back"],
        )

        self.assertEqual(profile.scenario.slug, "makerspace_missing_booking")
        self.assertEqual(profile.context.slug, "makerspace_frontdesk")
        self.assertEqual(profile.selected_preferences["tone"], "warm")
        self.assertEqual(profile.selected_preferences["structure"], "bullets")
        self.assertEqual(profile.selected_preferences["closing"], "confirm_back")


class PromptEvolutionEvaluatorTests(unittest.TestCase):
    """Verify prompt evolution scoring stays deterministic and preference-aware."""

    def test_evaluator_flags_policy_and_format_mismatches(self) -> None:
        """Penalize replies that ignore required policy points and chosen structure."""
        config = import_module("prompt_evolution.config")
        evaluator = import_module("prompt_evolution.evaluator")

        catalog = config.load_catalog(PROJECT_ROOT / "prompt_evolution" / ".data")
        profile = config.SelectionProfile(
            problem=(
                "A member says their guest booking vanished before tonight's workshop "
                "and asks for an instant refund."
            ),
            context=catalog.contexts["coworking_membership"],
            selected_preferences={
                "tone": "warm",
                "structure": "bullets",
                "initiative": "next_step",
            },
        )

        result = evaluator.evaluate_response(
            profile,
            "We will fix this soon. Refund approved immediately.",
        )

        self.assertLess(result.total_score, result.max_score)
        self.assertTrue(any("policy" in issue.lower() for issue in result.issues))
        self.assertTrue(any("bullet" in issue.lower() for issue in result.issues))

    def test_evaluator_scores_new_preference_axes(self) -> None:
        """Score richer axes such as evidence style and closing behavior."""
        config = import_module("prompt_evolution.config")
        evaluator = import_module("prompt_evolution.evaluator")

        catalog = config.load_catalog(PROJECT_ROOT / "prompt_evolution" / ".data")
        profile = config.resolve_selection_profile(
            catalog,
            problem=(
                "A member says their laser cutter booking vanished and asks whether "
                "they can still use the bench tonight."
            ),
            context_slug="makerspace_frontdesk",
            preference_pairs=[
                "tone=direct",
                "structure=bullets",
                "initiative=next_step",
                "evidence=policy_first",
                "closing=confirm_back",
            ],
        )

        result = evaluator.evaluate_response(
            profile,
            "- Here's what I found.\n"
            "- Bench bookings open 24 hours before the slot and require an active "
            "tool certification.\n"
            "- Next step: please reply with the tool name and your certification "
            "badge number so I can confirm the booking.",
        )

        self.assertEqual(result.total_score, result.max_score)


class PromptEvolutionFeedbackTests(unittest.TestCase):
    """Verify Prompt Evolution supports iterative user feedback after a baseline draft."""

    def test_review_guidance_explains_what_feedback_to_give(self) -> None:
        """Show example asks, expected effects, and alternate feedback paths."""
        config = import_module("prompt_evolution.config")
        loop_module = import_module("prompt_evolution.loop")

        catalog = config.load_catalog(PROJECT_ROOT / "prompt_evolution" / ".data")
        profile = config.resolve_selection_profile(
            catalog,
            problem="A makerspace member says their booking vanished before open lab.",
            context_slug="makerspace_frontdesk",
            preference_pairs=[
                "tone=direct",
                "structure=bullets",
                "initiative=next_step",
            ],
        )

        guidance = loop_module.build_user_feedback_guide(catalog, profile)

        self.assertIn("what you can ask to improve", guidance.lower())
        self.assertIn("if you say", guidance.lower())
        self.assertIn("expect", guidance.lower())
        self.assertIn("tool certification", guidance.lower())

    def test_refinement_round_records_user_feedback_and_revises_output(self) -> None:
        """Use one user feedback string to run one more refinement pass."""
        config = import_module("prompt_evolution.config")
        loop_module = import_module("prompt_evolution.loop")

        class FakeRunner:
            """Return queued Hermes responses and capture prompts."""

            def __init__(self) -> None:
                self.calls: list[tuple[str, str, str]] = []
                self._responses = iter(
                    [
                        type(
                            "Response",
                            (),
                            {
                                "text": (
                                    "```text\nUse bullet points and lead with the "
                                    "booking window plus certification gate.\n```"
                                )
                            },
                        )(),
                        type(
                            "Response",
                            (),
                            {
                                "text": (
                                    "- Bench bookings open 24 hours before the slot.\n"
                                    "- Active tool certification is required before "
                                    "access is confirmed.\n"
                                    "- Please reply with your badge number so I can "
                                    "confirm the next step."
                                )
                            },
                        )(),
                    ]
                )

            def run_text(self, *, system_prompt: str, user_prompt: str, task_id: str):
                """Return the next fake Hermes response."""
                self.calls.append((system_prompt, user_prompt, task_id))
                return next(self._responses)

        catalog = config.load_catalog(PROJECT_ROOT / "prompt_evolution" / ".data")
        profile = config.resolve_selection_profile(
            catalog,
            problem="A makerspace member says their booking vanished before open lab.",
            context_slug="makerspace_frontdesk",
            preference_pairs=[
                "tone=direct",
                "structure=bullets",
                "initiative=next_step",
            ],
        )
        runner = FakeRunner()

        updated = loop_module.run_feedback_refinement(
            catalog,
            profile,
            current_instructions="Keep replies brief.",
            current_response="We can help.",
            round_number=2,
            user_feedback=(
                "Make it more concrete. Mention tool certification earlier and end "
                "with one clear question."
            ),
            runner=runner,
        )

        self.assertEqual(updated["round"], 2)
        self.assertEqual(
            updated["user_feedback"],
            (
                "Make it more concrete. Mention tool certification earlier and end "
                "with one clear question."
            ),
        )
        self.assertIn("tool certification earlier", runner.calls[0][1].lower())
        self.assertIn("certification", updated["response"].lower())

    def test_feedback_refinement_overrides_stale_policy_values_in_next_draft(
        self,
    ) -> None:
        """Use corrected policy details instead of the original context value."""
        config = import_module("prompt_evolution.config")
        loop_module = import_module("prompt_evolution.loop")

        class FakeRunner:
            """Return a mutation response and capture the follow-up draft prompt."""

            def __init__(self) -> None:
                self.calls: list[tuple[str, str, str]] = []
                self._responses = iter(
                    [
                        type(
                            "Response",
                            (),
                            {
                                "text": (
                                    "```text\n"
                                    "Keep replies warm and specific.\n\n"
                                    "Additional Policy Details:\n"
                                    "- Guest bookings are held for 2 hours before "
                                    "release.\n"
                                    "- Day-pass refunds are reviewed after an "
                                    "attendance check.\n"
                                    "- The front desk or support can reissue building "
                                    "access.\n"
                                    "```"
                                )
                            },
                        )(),
                        type(
                            "Response",
                            (),
                            {
                                "text": (
                                    "- Guest bookings are held for 2 hours before release.\n"
                                    "- Day-pass refunds are reviewed after an "
                                    "attendance check.\n"
                                    "- The front desk or support can reissue "
                                    "building access.\n"
                                    "- Next step: please stop by the front desk so "
                                    "we can confirm the booking."
                                )
                            },
                        )(),
                    ]
                )

            def run_text(self, *, system_prompt: str, user_prompt: str, task_id: str):
                """Return the next fake Hermes response."""
                self.calls.append((system_prompt, user_prompt, task_id))
                return next(self._responses)

        catalog = config.load_catalog(PROJECT_ROOT / "prompt_evolution" / ".data")
        profile = config.resolve_selection_profile(
            catalog,
            problem="A member says their guest booking vanished before tonight's workshop.",
            context_slug="coworking_membership",
            preference_pairs=[
                "tone=warm",
                "structure=bullets",
                "initiative=next_step",
            ],
        )
        runner = FakeRunner()

        updated = loop_module.run_feedback_refinement(
            catalog,
            profile,
            current_instructions="Keep replies brief.",
            current_response="We can help.",
            round_number=2,
            user_feedback="Guest bookings are held for 2 hours, not 15 minutes.",
            runner=runner,
        )

        follow_up_system_prompt = runner.calls[1][0]
        self.assertIn("2 hours", follow_up_system_prompt)
        self.assertNotIn("15 minutes", follow_up_system_prompt)
        self.assertFalse(any("15 minutes" in issue for issue in updated["issues"]))
        self.assertTrue(any("2 hours" in item for item in updated["strengths"]))


class PromptEvolutionTraceTests(unittest.TestCase):
    """Verify Prompt Evolution emits verbose traces, diffs, and dashboard-ready data."""

    def test_loop_records_llm_requests_logs_and_instruction_diffs(self) -> None:
        """Persist round traces that show the LLM calls and how instructions changed."""
        config = import_module("prompt_evolution.config")
        loop_module = import_module("prompt_evolution.loop")

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
                                    "```text\nKeep replies direct.\nMention active "
                                    "tool certification before the next step.\n```"
                                )
                            },
                        )(),
                        type(
                            "Response",
                            (),
                            {
                                "text": (
                                    "- Bench bookings open 24 hours before the slot.\n"
                                    "- Active tool certification is required before "
                                    "the booking can be confirmed.\n"
                                    "- Please reply with your badge number so I can "
                                    "confirm the next step."
                                )
                            },
                        )(),
                    ]
                )

            def run_text(self, *, system_prompt: str, user_prompt: str, task_id: str):
                """Return the next fake Hermes response."""
                self.calls.append((system_prompt, user_prompt, task_id))
                return next(self._responses)

        catalog = config.load_catalog(PROJECT_ROOT / "prompt_evolution" / ".data")
        profile = config.resolve_selection_profile(
            catalog,
            problem="A makerspace member says their booking vanished before open lab.",
            context_slug="makerspace_frontdesk",
            preference_pairs=[
                "tone=direct",
                "structure=bullets",
                "initiative=next_step",
            ],
        )
        runner = FakeRunner()
        logs: list[str] = []

        with tempfile.TemporaryDirectory() as tmp_dir:
            with mock.patch.object(loop_module, "OUTPUT_DIR", Path(tmp_dir)):
                with mock.patch.object(
                    loop_module,
                    "load_mutable_instructions",
                    return_value="Keep replies short.",
                ):
                    history = loop_module.run_prompt_evolution(
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
                self.assertIn("-Keep replies short.", history[1]["mutation_diff"])
                self.assertIn(
                    "+Mention active tool certification before the next step.",
                    history[1]["mutation_diff"],
                )
                self.assertTrue((Path(tmp_dir) / "latest_mutation.diff").exists())

        joined_logs = "\n".join(logs)
        self.assertIn("REQUESTING_LLM_DRAFT", joined_logs)
        self.assertIn("REQUESTING_LLM_MUTATION", joined_logs)
        self.assertIn("INSTRUCTION_DIFF", joined_logs)

    def test_loop_writes_scenario_metadata_and_jsonl_trace_artifacts(self) -> None:
        """Persist scenario context plus structured trace files for observability."""
        config = import_module("prompt_evolution.config")
        loop_module = import_module("prompt_evolution.loop")

        class FakeRunner:
            """Return one complete response and expose simple request metadata."""

            model = "demo-model"
            provider = "custom"
            base_url = "http://localhost:5272/v1"

            def __init__(self) -> None:
                self.last_call: tuple[str, str, str] | None = None

            def run_text(self, *, system_prompt: str, user_prompt: str, task_id: str):
                """Return a fake response that satisfies the makerspace scenario."""
                self.last_call = (system_prompt, user_prompt, task_id)
                return type(
                    "Response",
                    (),
                    {
                        "text": (
                            "- Here's what I found.\n"
                            "- Bench bookings open 24 hours before the slot and "
                            "require active tool certification.\n"
                            "- Next step: please reply with the tool name and "
                            "your certification badge so I can confirm the booking."
                        )
                    },
                )()

        catalog = config.load_catalog(PROJECT_ROOT / "prompt_evolution" / ".data")
        profile = config.resolve_scenario_profile(
            catalog,
            scenario_slug="makerspace_missing_booking",
            preference_pairs=["tone=direct"],
        )

        with tempfile.TemporaryDirectory() as tmp_dir:
            with mock.patch.object(loop_module, "OUTPUT_DIR", Path(tmp_dir)):
                with mock.patch.object(
                    loop_module,
                    "load_mutable_instructions",
                    return_value="Keep replies direct.",
                ):
                    loop_module.run_prompt_evolution(
                        catalog,
                        profile,
                        max_iterations=1,
                        runner=FakeRunner(),
                        run_instance="scenario-smoke",
                    )

                session_payload = json.loads(
                    (Path(tmp_dir) / "latest_session.json").read_text(encoding="utf-8")
                )
                trace_dir = Path(tmp_dir) / "traces"

                self.assertEqual(
                    session_payload["scenario"]["slug"],
                    "makerspace_missing_booking",
                )
                self.assertEqual(
                    session_payload["trace"]["run_instance"],
                    "scenario-smoke",
                )
                self.assertTrue((trace_dir / "run_events.jsonl").exists())
                self.assertTrue((trace_dir / "llm_requests.jsonl").exists())
                self.assertTrue((trace_dir / "evaluator_events.jsonl").exists())
                self.assertTrue(
                    (
                        trace_dir / "runs" / "scenario-smoke" / "run_events.jsonl"
                    ).exists()
                )

    def test_dashboard_helpers_expose_round_diffs(self) -> None:
        """Provide a dashboard helper that renders the mutable instruction diff."""
        dashboard = import_module("prompt_evolution.dashboard")

        diff_text = dashboard.build_round_diff(
            "Keep replies short.\n",
            "Keep replies direct.\nMention active tool certification early.\n",
        )

        self.assertIn("-Keep replies short.", diff_text)
        self.assertIn("+Keep replies direct.", diff_text)

    def test_dashboard_script_runs_without_project_root_already_on_sys_path(
        self,
    ) -> None:
        """Allow the dashboard script to run outside the repo root."""
        dashboard_dir = PROJECT_ROOT / "prompt_evolution"
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
                key: value for key, value in os.environ.items() if key != "PYTHONPATH"
            },
        )

        self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)


class CleanLoopAgendaTests(unittest.TestCase):
    """Verify CleanLoop uses README.md as the human-readable agenda artifact."""

    def test_system_prompt_refers_to_readme_instead_of_program_file(self) -> None:
        """Expose README.md in the system prompt and remove stale program.md references."""
        prompt = cleanloop_loop.build_system_prompt("finance")

        self.assertIn("README.md", prompt)
        self.assertNotIn("program.md", prompt)
