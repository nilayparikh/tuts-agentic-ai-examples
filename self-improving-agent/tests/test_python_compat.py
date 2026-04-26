# pyright: reportMissingImports=false, reportMissingModuleSource=false, reportPrivateUsage=false
# mypy: disable-error-code=import-not-found
# pylint: disable=protected-access

import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from importlib import import_module
from pathlib import Path
from typing import Any, cast
from unittest import mock

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

cleanloop_loop = cast(Any, import_module("cleanloop.loop"))
cleanloop_datasets = cast(Any, import_module("cleanloop.datasets"))
util = cast(Any, import_module("util"))


class SupportedPythonVersionTests(unittest.TestCase):
    """Verify the setup gate accepts the intended interpreter versions."""

    def test_accepts_python_3_11(self) -> None:
        """Accept Python 3.11 for local setup and execution."""
        self.assertTrue(util._is_supported_python((3, 11, 9)))

    def test_accepts_python_3_12(self) -> None:
        """Accept Python 3.12 for local setup and execution."""
        self.assertTrue(util._is_supported_python((3, 12, 0)))

    def test_rejects_python_3_10(self) -> None:
        """Reject Python versions older than 3.11."""
        self.assertFalse(util._is_supported_python((3, 10, 14)))


class VerificationEnvironmentTests(unittest.TestCase):
    """Verify setup and verify operate on the intended environment."""

    def test_prefers_venv_python_when_present(self) -> None:
        """Use the project venv interpreter for verification when it exists."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            venv_dir = Path(tmp_dir) / ".venv"
            scripts_dir = venv_dir / "Scripts"
            scripts_dir.mkdir(parents=True)
            python_path = scripts_dir / "python.exe"
            python_path.write_text("", encoding="utf-8")

            with mock.patch.object(util, "VENV_DIR", venv_dir):
                with mock.patch("platform.system", return_value="Windows"):
                    self.assertEqual(util._get_verify_python_path(), python_path)

    def test_reports_broken_venv_as_not_ready(self) -> None:
        """Treat a bare .venv directory without executables as broken."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            venv_dir = Path(tmp_dir) / ".venv"
            venv_dir.mkdir()

            with mock.patch.object(util, "VENV_DIR", venv_dir):
                self.assertFalse(util._venv_is_ready())

    def test_reexecs_runtime_commands_into_venv(self) -> None:
        """Bootstrap non-setup commands into the project venv when available."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            venv_dir = Path(tmp_dir) / ".venv"
            scripts_dir = venv_dir / "Scripts"
            scripts_dir.mkdir(parents=True)
            python_path = scripts_dir / "python.exe"
            python_path.write_text("", encoding="utf-8")
            pip_path = scripts_dir / "pip.exe"
            pip_path.write_text("", encoding="utf-8")

            with mock.patch.object(util, "VENV_DIR", venv_dir):
                with mock.patch("platform.system", return_value="Windows"):
                    self.assertTrue(
                        util._should_bootstrap_to_venv(
                            ["util.py", "-e", "cleanloop", "loop"],
                            current_python=Path("C:/Python311/python.exe"),
                        )
                    )

    def test_counts_utf8_rows_without_default_codepage_crash(self) -> None:
        """Read UTF-8 CSV input without relying on the platform default codec."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            csv_path = Path(tmp_dir) / "sample.csv"
            csv_path.write_text(
                "date,product,price,quantity\n"
                "2024-05-01,Keyboard,149.99,2\n"
                "2024-05-02,Gift,FREE 🎁,1\n",
                encoding="utf-8",
            )

            self.assertEqual(util._count_data_rows(csv_path), 2)


class LoggingCompatibilityTests(unittest.TestCase):
    """Verify the shared logger stays safe on Windows code-page output."""

    def test_status_prefixes_are_ascii(self) -> None:
        """Use ASCII-only prefixes so redirected output does not crash."""
        for kind in ["ok", "warn", "fail", "info"]:
            util._status_prefix(kind).encode("ascii")


class InteractiveReviewLoopTests(unittest.TestCase):
    """Verify the shared CLI review loop can collect iterative feedback."""

    def test_interactive_review_runs_until_user_accepts_output(self) -> None:
        """Prompt for more feedback after the intermediate output until the user is happy."""
        first_round = {
            "round": 1,
            "response": "Draft one.",
            "score": 3,
            "total": 5,
            "issues": ["Needs a clearer next step."],
        }
        second_round = {
            "round": 2,
            "response": "Draft two.",
            "score": 5,
            "total": 5,
            "issues": [],
            "user_feedback": "Make the next step clearer.",
        }
        refine_once = mock.Mock(return_value=second_round)

        with mock.patch(
            "builtins.input", side_effect=["n", "Make the next step clearer.", "y"]
        ):
            stream = io.StringIO()
            with redirect_stdout(stream):
                history = util._interactive_review_loop(
                    example_label="Prompt Evolution",
                    initial_history=[first_round],
                    guidance_text=(
                        "What you can ask to improve: tone, structure, policy grounding."
                    ),
                    refine_once=refine_once,
                )

        self.assertEqual([item["round"] for item in history], [1, 2])
        self.assertEqual(history[-1]["response"], "Draft two.")
        refine_once.assert_called_once_with(
            "Make the next step clearer.",
            first_round,
            2,
        )
        rendered = stream.getvalue().lower()
        self.assertIn("what you can ask to improve", rendered)
        self.assertIn("are you happy", rendered)


class CleanLoopAutoGenRuntimeTests(unittest.TestCase):
    """Verify the CleanLoop example owns its AutoGen runtime boundary."""

    def test_cleanloop_local_cli_accepts_verify_command(self) -> None:
        """Expose a CleanLoop-local verify command from cleanloop/util.py."""
        cleanloop_local_util = cast(Any, import_module("cleanloop.util"))

        args = cleanloop_local_util.build_parser().parse_args(["verify"])

        self.assertEqual(args.command, "verify")

    def test_cleanloop_local_cli_bootstraps_to_parent_venv(self) -> None:
        """Reuse the shared example venv when launched from the cleanloop folder."""
        cleanloop_local_util = cast(Any, import_module("cleanloop.util"))

        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_root = Path(tmp_dir)
            venv_dir = temp_root / ".venv"
            scripts_dir = venv_dir / "Scripts"
            scripts_dir.mkdir(parents=True)
            python_path = scripts_dir / "python.exe"
            python_path.write_text("", encoding="utf-8")

            with mock.patch.object(cleanloop_local_util, "VENV_DIR", venv_dir):
                with mock.patch("platform.system", return_value="Windows"):
                    should_bootstrap = cleanloop_local_util._should_bootstrap_to_venv(
                        ["util.py", "verify"],
                        current_python=Path("C:/Python311/python.exe"),
                    )

        self.assertTrue(should_bootstrap)

    def test_propose_fix_delegates_to_autogen_runtime(self) -> None:
        """Keep the loop contract stable while routing proposal generation through AutoGen."""
        attempt = {
            "label": "AutoGen proposer",
            "model": "demo-model",
            "max_tokens": 2200,
            "code_found": True,
            "hypothesis": "Normalize invoice values before merge",
            "usage": {
                "prompt_tokens": 11,
                "completion_tokens": 22,
                "total_tokens": 33,
            },
            "prompt_chars": 120,
            "response_chars": 240,
            "messages": [],
            "response_preview": "Structured mutation proposal",
        }

        with mock.patch.object(
            cleanloop_loop.autogen_runtime,
            "propose_single_mutation",
            return_value=(
                "def clean(input_dir, output_path):\n    return None",
                "Normalize invoice values before merge",
                attempt,
            ),
        ) as propose_single_mutation:
            code, hypothesis, diagnostics = cleanloop_loop._propose_fix(
                client=object(),
                model="demo-model",
                system_prompt="system",
                genome_code="def clean(input_dir, output_path):\n    pass\n",
                results={"failed": ["value_is_numeric: bad row"], "passed": []},
                history=[],
                dataset_name="finance",
                metacognition={"focus_area": "value_normalization"},
            )

        self.assertEqual(code, "def clean(input_dir, output_path):\n    return None")
        self.assertEqual(hypothesis, "Normalize invoice values before merge")
        self.assertEqual(diagnostics["selected_attempt"], "AutoGen proposer")
        self.assertEqual(diagnostics["total_tokens"], 33)
        attempt_diagnostics = cast(list[dict[str, object]], diagnostics["attempts"])
        self.assertEqual(len(attempt_diagnostics), 1)
        self.assertTrue(attempt_diagnostics[0]["code_found"])
        propose_single_mutation.assert_called_once()

    def test_cleanloop_local_util_prefers_example_env_file(self) -> None:
        """Load CleanLoop credentials from the example-local .env before falling back upward."""
        cleanloop_local_util = cast(Any, import_module("cleanloop.util"))

        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_root = Path(tmp_dir)
            env_path = temp_root / ".env"
            env_path.write_text(
                "LLM_ENDPOINT=https://models.github.ai/inference\n"
                "LLM_API_KEY=local-demo-key\n"
                "MODEL_NAME=demo-model\n",
                encoding="utf-8",
            )
            fallback_env_path = temp_root / "fallback.env"
            fallback_env_path.write_text(
                "LLM_ENDPOINT=https://example.openai.azure.com\n"
                "LLM_API_KEY=fallback-key\n"
                "MODEL_NAME=fallback-model\n",
                encoding="utf-8",
            )

            with mock.patch.object(cleanloop_local_util, "ENV_FILE", env_path):
                with mock.patch.object(
                    cleanloop_local_util, "FALLBACK_ENV_FILE", fallback_env_path
                ):
                    with mock.patch.dict(os.environ, {}, clear=True):
                        cleanloop_local_util.load_env()
                        config = cleanloop_local_util.resolve_llm_env()

        self.assertEqual(config["endpoint"], "https://models.github.ai/inference")
        self.assertEqual(config["api_key"], "local-demo-key")
        self.assertEqual(config["model"], "demo-model")


class ExampleDashboardRoutingTests(unittest.TestCase):
    """Verify non-CleanLoop examples expose their own dashboard routes."""

    def test_parser_accepts_prompt_evolution_and_skill_mastery_dashboards(self) -> None:
        """Route the shared dashboard command to the example-specific dashboard handlers."""
        prompt_args = util.build_parser().parse_args(
            ["-e", "prompt_evolution", "dashboard"]
        )
        mastery_args = util.build_parser().parse_args(
            ["-e", "skill_mastery", "dashboard"]
        )

        self.assertEqual(prompt_args.example, "prompt_evolution")
        self.assertEqual(prompt_args.command, "dashboard")
        self.assertEqual(mastery_args.example, "skill_mastery")
        self.assertEqual(mastery_args.command, "dashboard")
        self.assertIn("dashboard", util.EXAMPLE_COMMANDS["prompt_evolution"])
        self.assertIn("dashboard", util.EXAMPLE_COMMANDS["skill_mastery"])


class EndpointSelectionTests(unittest.TestCase):
    """Verify endpoint detection chooses the right LLM client family."""

    def test_detects_azure_openai_endpoint(self) -> None:
        """Recognize Azure OpenAI resource endpoints."""
        self.assertTrue(util._is_azure_openai_endpoint("https://demo.openai.azure.com"))

    def test_ignores_foundry_local_endpoint(self) -> None:
        """Treat local OpenAI-compatible endpoints as non-Azure-OpenAI."""
        self.assertFalse(util._is_azure_openai_endpoint("http://localhost:5272/v1"))

    def test_normalizes_azure_openai_base_endpoint_to_v1(self) -> None:
        """Append /openai/v1 for bare Azure OpenAI resource endpoints."""
        self.assertEqual(
            util._normalize_endpoint("https://tuts.openai.azure.com"),
            "https://tuts.openai.azure.com/openai/v1",
        )

    def test_resolves_agnostic_llm_env_names(self) -> None:
        """Accept provider-agnostic LLM_* credentials for OpenAI-compatible providers."""
        with mock.patch.dict(
            util.os.environ,
            {
                "LLM_ENDPOINT": "https://models.github.ai/inference",
                "LLM_API_KEY": "github-demo-key",
                "MODEL_NAME": "openai/gpt-4.1-mini",
            },
            clear=True,
        ):
            resolved = util._resolve_llm_env()

        self.assertEqual(resolved["endpoint"], "https://models.github.ai/inference")
        self.assertEqual(resolved["api_key"], "github-demo-key")
        self.assertEqual(resolved["model"], "openai/gpt-4.1-mini")
        self.assertEqual(resolved["api_version"], "2024-12-01-preview")
        self.assertEqual(resolved["endpoint_var"], "LLM_ENDPOINT")
        self.assertEqual(resolved["api_key_var"], "LLM_API_KEY")


class ProbeResponseTests(unittest.TestCase):
    """Verify the LLM health probe handles sparse response payloads."""

    def test_normalizes_missing_probe_text(self) -> None:
        """Treat a successful completion with no text content as an empty reply."""
        self.assertEqual(util._normalize_probe_reply(None), "(empty reply)")


class CapacityRetryTests(unittest.TestCase):
    """Verify transient Azure capacity throttles are retried and explained."""

    def test_retries_capacity_error_then_returns_response(self) -> None:
        """Retry a transient 429 capacity rejection and return the later success."""

        class CapacityError(Exception):
            """Stub 429 error with the same fields we inspect in production."""

            def __init__(self, message: str) -> None:
                super().__init__(message)
                self.status_code = 429

        response = object()
        create = mock.Mock(
            side_effect=[CapacityError("maximum concurrent capacity"), response]
        )
        completions = mock.Mock(create=create)
        client = mock.Mock()
        client.chat.completions = completions

        with mock.patch("time.sleep") as sleep_mock:
            result = util._create_chat_completion_with_backoff(
                client,
                model="demo-model",
                messages=[{"role": "user", "content": "hello"}],
                max_attempts=2,
                base_delay_seconds=0.01,
                temperature=0,
            )

        self.assertIs(result, response)
        self.assertEqual(create.call_count, 2)
        sleep_mock.assert_called_once()

    def test_formats_capacity_error_as_endpoint_busy(self) -> None:
        """Explain 429 concurrency rejections as deployment saturation, not model failure."""

        class CapacityError(Exception):
            """Stub 429 error with the same fields we inspect in production."""

            def __init__(self, message: str) -> None:
                super().__init__(message)
                self.status_code = 429

        message = util._format_llm_exception(
            CapacityError("Server at maximum concurrent capacity (8). Try again later.")
        )

        self.assertIn("Endpoint busy (429 capacity)", message)
        self.assertIn("Server at maximum concurrent capacity", message)


class FormattingTests(unittest.TestCase):
    """Verify display formatting for sensitive values."""

    def test_masks_api_key_with_two_visible_chars(self) -> None:
        """Show only the first two and last two characters of API keys."""
        self.assertEqual(util._mask_secret("ABCDEFGH"), "AB****GH")


class Utf8TextLoadingTests(unittest.TestCase):
    """Verify prompt sources load as UTF-8 instead of the platform default codec."""

    def test_cleanloop_reads_utf8_prompt_files(self) -> None:
        """Load agenda text with UTF-8 even when it includes non-ASCII characters."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            readme_path = Path(tmp_dir) / "README.md"
            readme_path.write_text("Use the gift line: FREE 🎁\n", encoding="utf-8")

            loaded = cleanloop_loop._read_utf8_text(readme_path)

            self.assertIn("FREE 🎁", loaded)


class LoopResilienceTests(unittest.TestCase):
    """Verify the loop can start from a broken genome."""

    def test_run_loop_accepts_agnostic_llm_env_names(self) -> None:
        """Use LLM_* credentials when provider-branded names are absent."""
        baseline = {
            "passed": ["can_read_output", "has_required_columns"],
            "failed": ["matches_reference_output: matched=10, missing=5, unexpected=3"],
            "score": 2,
            "total": 3,
            "metrics": {
                "reference_rows": 15,
                "output_rows": 13,
                "matched_rows": 10,
                "missing_rows": 5,
                "unexpected_rows": 3,
                "cleanliness_score": 0.666667,
                "output_precision": 0.769231,
            },
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_root = Path(tmp_dir)
            genome_path = temp_root / "clean_data.py"
            genome_path.write_text(
                "def clean(input_dir, output_path):\n    return None\n",
                encoding="utf-8",
            )

            with mock.patch.dict(
                os.environ,
                {
                    "LLM_ENDPOINT": "https://models.github.ai/inference",
                    "LLM_API_KEY": "demo-key",
                    "MODEL_NAME": "demo-model",
                },
                clear=True,
            ):
                with mock.patch.object(
                    cleanloop_loop.util,
                    "_build_llm_client",
                    return_value=object(),
                ):
                    with mock.patch.object(
                        cleanloop_loop, "OUTPUT_DIR", temp_root / ".output"
                    ):
                        with mock.patch.object(
                            cleanloop_loop, "GENOME_PATH", genome_path
                        ):
                            with mock.patch.object(
                                cleanloop_loop,
                                "_run_and_evaluate",
                                return_value=baseline,
                            ):
                                with mock.patch.object(
                                    cleanloop_loop,
                                    "_propose_fix",
                                    return_value=(None, "hold steady", {}),
                                ):
                                    with mock.patch.object(
                                        cleanloop_loop, "_git_commit"
                                    ):
                                        with mock.patch.object(
                                            cleanloop_loop, "_git_revert"
                                        ):
                                            history = cleanloop_loop.run_loop(
                                                max_iterations=1
                                            )

        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["action"], "skip")

    def test_extract_usage_stats_reads_response_token_counts(self) -> None:
        """Capture prompt, completion, and total token counts from an LLM response."""

        class Usage:
            """Stub usage payload."""

            prompt_tokens = 123
            completion_tokens = 45
            total_tokens = 168

        class Response:
            """Stub response payload."""

            usage = Usage()

        self.assertEqual(
            cleanloop_loop._extract_usage_stats(Response()),
            {
                "prompt_tokens": 123,
                "completion_tokens": 45,
                "total_tokens": 168,
            },
        )

    def test_propose_fix_returns_attempt_diagnostics(self) -> None:
        """Return code, hypothesis, and per-attempt LLM diagnostics."""

        attempt = {
            "label": "AutoGen proposer",
            "model": "demo-model",
            "max_tokens": 2200,
            "code_found": True,
            "hypothesis": "Normalize rows",
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 20,
                "total_tokens": 30,
            },
            "prompt_chars": 100,
            "response_chars": 180,
            "messages": [],
            "response_preview": "Structured mutation proposal",
        }

        with mock.patch.object(
            cleanloop_loop.autogen_runtime,
            "propose_single_mutation",
            return_value=(
                "def clean(x, y):\n    return None",
                "Normalize rows",
                attempt,
            ),
        ):
            code, hypothesis, diagnostics = cleanloop_loop._propose_fix(
                client=object(),
                model="demo-model",
                system_prompt="system",
                genome_code="def clean(x, y):\n    pass\n",
                results={"failed": ["price_is_numeric: bad row"], "passed": []},
                history=[],
                dataset_name="finance",
            )

        self.assertEqual(code, "def clean(x, y):\n    return None")
        self.assertEqual(hypothesis, "Normalize rows")
        self.assertEqual(diagnostics["selected_attempt"], "AutoGen proposer")
        self.assertEqual(diagnostics["total_tokens"], 30)
        attempt_diagnostics = cast(list[dict[str, object]], diagnostics["attempts"])
        self.assertEqual(len(attempt_diagnostics), 1)
        self.assertTrue(attempt_diagnostics[0]["code_found"])

    def test_extract_code_accepts_unclosed_python_fence(self) -> None:
        """Treat the rest of the reply as code when the closing fence is missing."""
        code = cleanloop_loop._extract_code(
            "Hypothesis: parse every row\n\n```python\ndef clean(x, y):\n    return None\n"
        )

        self.assertEqual(code, "def clean(x, y):\n    return None")

    def test_starter_genome_handles_shipped_input_without_crashing(self) -> None:
        """The shipped starter genome should produce an output file, not raise on row shape issues."""
        clean_data = cast(Any, import_module("cleanloop.clean_data"))

        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = Path(tmp_dir) / "master.csv"

            clean_data.clean(PROJECT_ROOT / "cleanloop" / ".input", output_path)

            self.assertTrue(output_path.exists())

    def test_converts_genome_crash_into_failed_result(self) -> None:
        """Return a failed eval payload instead of raising on genome execution errors."""

        class BrokenGenome:
            """Stub genome module that always crashes."""

            @staticmethod
            def clean(_input_dir, _output_path) -> None:
                raise RuntimeError("csv parse failed")

        class Referee:
            """Stub referee used only to satisfy the helper signature."""

            @staticmethod
            def evaluate(_output_path):
                return {
                    "passed": ["can_read_output"],
                    "failed": [],
                    "score": 1,
                    "total": 1,
                }

        with tempfile.TemporaryDirectory() as tmp_dir:
            results = cleanloop_loop._run_and_evaluate(
                BrokenGenome,
                Referee,
                PROJECT_ROOT / "cleanloop" / ".input",
                Path(tmp_dir) / "finance_master.csv",
            )

        self.assertEqual(results["score"], 0)
        self.assertEqual(results["total"], 1)
        self.assertIn("can_run_genome", results["failed"][0])

    def test_builds_compact_retry_prompt_with_failure_context(self) -> None:
        """Include the failure and current genome in the compact retry prompt."""
        system_prompt, user_prompt = cleanloop_loop._build_compact_retry_prompts(
            "def clean(x, y):\n    pass\n",
            {"failed": ["can_run_genome: parser error"]},
        )

        self.assertIn("Return ONLY the complete clean_data.py", system_prompt)
        self.assertIn("parser error", user_prompt)
        self.assertIn("def clean(x, y)", user_prompt)

    def test_finance_prompts_warn_about_scalar_and_currency_failures(self) -> None:
        """Guide finance repair attempts away from brittle scalar and currency parsing."""
        system_prompt = cleanloop_loop.build_system_prompt("finance")
        _, user_prompt = cleanloop_loop._build_compact_retry_prompts(
            "def clean(x, y):\n    pass\n",
            {"failed": ["can_run_genome: 'float' object has no attribute 'strip'"]},
        )

        self.assertIn("Values may already be floats or NaN", system_prompt)
        self.assertIn("currency symbols or accounting markers", system_prompt)
        self.assertIn("Never call .strip() on raw pandas scalars", system_prompt)
        self.assertIn("coerce float or NaN values safely before trimming", user_prompt)


class CleanLoopDatasetTests(unittest.TestCase):
    """Verify CleanLoop now operates as a single finance arena."""

    def _copy_reference_output(self, dataset_name: str, target_path: Path) -> None:
        """Copy one canonical gold output into a temp output path."""
        source = PROJECT_ROOT / "cleanloop" / ".gold" / f"{dataset_name}_expected.csv"
        target_path.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")

    def test_dashboard_launches_streamlit_without_interactive_prompt(self) -> None:
        """Launch Streamlit in headless mode with usage stats disabled."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_dir = Path(tmp_dir)
            history_path = cleanloop_datasets.get_history_path(output_dir)
            history_path.write_text("[]", encoding="utf-8")

            args = mock.Mock()
            with mock.patch.object(util, "_ensure_in_venv"):
                with mock.patch.object(util, "_output_dir", return_value=output_dir):
                    with mock.patch.object(
                        util, "_get_bin_path", return_value=Path("streamlit.exe")
                    ):
                        with mock.patch.object(util.os, "execve") as execve_mock:
                            util.cmd_dashboard(args)

        execve_mock.assert_called_once()
        executable, argv, env = execve_mock.call_args.args
        self.assertEqual(executable, "streamlit.exe")
        self.assertIn("--server.headless=true", argv)
        self.assertIn("--browser.gatherUsageStats=false", argv)
        self.assertEqual(env["STREAMLIT_SERVER_HEADLESS"], "true")
        self.assertEqual(env["STREAMLIT_BROWSER_GATHER_USAGE_STATS"], "false")

    def test_run_loop_records_before_and_after_judge_metrics(self) -> None:
        """Persist per-round judge metrics so the dashboard can render richer comparisons."""
        baseline = {
            "passed": ["can_read_output", "has_required_columns"],
            "failed": ["matches_reference_output: matched=10, missing=5, unexpected=3"],
            "score": 2,
            "total": 3,
            "metrics": {
                "reference_rows": 15,
                "output_rows": 13,
                "matched_rows": 10,
                "missing_rows": 5,
                "unexpected_rows": 3,
                "cleanliness_score": 0.666667,
                "output_precision": 0.769231,
            },
        }
        improved = {
            "passed": [
                "can_read_output",
                "has_required_columns",
                "matches_reference_output: matched all 15 reference rows",
            ],
            "failed": [],
            "score": 3,
            "total": 3,
            "metrics": {
                "reference_rows": 15,
                "output_rows": 15,
                "matched_rows": 15,
                "missing_rows": 0,
                "unexpected_rows": 0,
                "cleanliness_score": 1.0,
                "output_precision": 1.0,
            },
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_root = Path(tmp_dir)
            genome_path = temp_root / "clean_data.py"
            genome_path.write_text(
                "def clean(input_dir, output_path):\n    return None\n",
                encoding="utf-8",
            )

            with mock.patch.dict(
                os.environ,
                {
                    "AZURE_ENDPOINT": "https://example.openai.azure.com",
                    "AZURE_API_KEY": "demo-key",
                    "MODEL_NAME": "demo-model",
                },
                clear=False,
            ):
                with mock.patch.object(
                    cleanloop_loop.util, "_build_llm_client", return_value=object()
                ):
                    with mock.patch.object(
                        cleanloop_loop, "OUTPUT_DIR", temp_root / ".output"
                    ):
                        with mock.patch.object(
                            cleanloop_loop, "GENOME_PATH", genome_path
                        ):
                            with mock.patch.object(
                                cleanloop_loop,
                                "_run_and_evaluate",
                                side_effect=[baseline, improved],
                            ):
                                with mock.patch.object(
                                    cleanloop_loop,
                                    "_propose_fix",
                                    return_value=(
                                        "def clean(input_dir, output_path):\n    return 'ok'\n",
                                        "normalize rows",
                                        {
                                            "selected_attempt": "CleanLoop proposal",
                                            "attempts": [],
                                            "prompt_tokens": 10,
                                            "completion_tokens": 5,
                                            "total_tokens": 15,
                                        },
                                    ),
                                ):
                                    with mock.patch.object(
                                        cleanloop_loop, "_git_commit"
                                    ):
                                        with mock.patch.object(
                                            cleanloop_loop, "_git_revert"
                                        ):
                                            with mock.patch.object(
                                                cleanloop_loop,
                                                "_artifact_manifest",
                                                return_value={
                                                    "output_csv": "cleanloop/.output/finance_master.csv"
                                                },
                                            ):
                                                history = cleanloop_loop.run_loop(
                                                    max_iterations=1
                                                )

        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["before_metrics"]["missing_rows"], 5)
        self.assertEqual(history[0]["before_metrics"]["unexpected_rows"], 3)
        self.assertEqual(history[0]["metrics"]["matched_rows"], 15)
        self.assertEqual(history[0]["metrics"]["cleanliness_score"], 1.0)
        self.assertIn("return None", history[0]["genome_before"])
        self.assertIn("return 'ok'", history[0]["genome_after"])

    def test_dashboard_metric_rows_include_recall_and_precision_deltas(self) -> None:
        """Build dashboard rows with richer judge metrics than raw exact-match counters."""
        dashboard_metrics = import_module("cleanloop.dashboard_metrics")

        rows = dashboard_metrics.build_judge_metric_rows(
            [
                {
                    "round": 1,
                    "action": "commit",
                    "before_metrics": {
                        "reference_rows": 20,
                        "output_rows": 18,
                        "matched_rows": 12,
                        "missing_rows": 8,
                        "unexpected_rows": 6,
                        "cleanliness_score": 0.6,
                        "output_precision": 0.666667,
                    },
                    "metrics": {
                        "reference_rows": 20,
                        "output_rows": 20,
                        "matched_rows": 18,
                        "missing_rows": 2,
                        "unexpected_rows": 2,
                        "cleanliness_score": 0.9,
                        "output_precision": 0.9,
                    },
                }
            ]
        )

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["Round"], 1)
        self.assertEqual(rows[0]["Before Recall %"], 60.0)
        self.assertEqual(rows[0]["After Recall %"], 90.0)
        self.assertEqual(rows[0]["Precision Delta %"], 23.33)
        self.assertEqual(rows[0]["Missing Rows Delta"], -6)
        self.assertEqual(rows[0]["Unexpected Rows Delta"], -4)

    def test_dashboard_attempt_rows_flag_token_exhaustion(self) -> None:
        """Explain when a model spends its whole token budget and still returns no code."""
        dashboard_metrics = import_module("cleanloop.dashboard_metrics")

        rows = dashboard_metrics.build_attempt_outcome_rows(
            [
                {
                    "round": 1,
                    "llm": {
                        "attempts": [
                            {
                                "label": "CleanLoop proposal",
                                "code_found": False,
                                "response_chars": 0,
                                "usage": {
                                    "completion_tokens": 2200,
                                    "total_tokens": 2600,
                                },
                            }
                        ]
                    },
                }
            ],
            token_budget=2200,
        )

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["Round"], 1)
        self.assertEqual(
            rows[0]["Diagnosis"], "token budget exhausted before code output"
        )

    def test_dashboard_builds_mutable_genome_diff_rows(self) -> None:
        """Render a unified diff for the mutable genome on each mutation round."""
        dashboard_metrics = import_module("cleanloop.dashboard_metrics")

        rows = dashboard_metrics.build_mutation_diff_rows(
            [
                {
                    "round": 2,
                    "action": "commit",
                    "genome_before": "def clean(input_dir, output_path):\n    return None\n",
                    "genome_after": (
                        "def clean(input_dir, output_path):\n"
                        "    cleaned = []\n"
                        "    return cleaned\n"
                    ),
                }
            ]
        )

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["Round"], 2)
        self.assertEqual(rows[0]["Action"], "commit")
        self.assertIn("--- before/clean_data.py", rows[0]["Diff"])
        self.assertIn("+++ after/clean_data.py", rows[0]["Diff"])
        self.assertIn("+    cleaned = []", rows[0]["Diff"])
        self.assertIn("-    return None", rows[0]["Diff"])

    def test_build_metacognition_snapshot_prioritizes_value_cleanup(self) -> None:
        """Summarize recurring finance failures into a concrete focus area."""
        snapshot = cleanloop_loop._build_metacognition_snapshot(
            history=[
                {
                    "failed": [
                        "value_is_numeric: 10 non-numeric or missing values in value",
                        "matches_reference_output: matched=45, missing=12, unexpected=9",
                    ]
                }
            ],
            results={
                "failed": [
                    "value_is_numeric: 8 non-numeric or missing values in value",
                    "matches_reference_output: matched=49, missing=8, unexpected=5",
                ]
            },
        )

        self.assertEqual(snapshot["focus_area"], "value_normalization")
        self.assertGreaterEqual(snapshot["repeated_failure_count"], 2)
        self.assertIn("currency", snapshot["guidance"])

    def test_run_loop_persists_metacognition_snapshot(self) -> None:
        """Write the current strategy snapshot so learners can inspect the loop's focus."""
        baseline = {
            "passed": ["can_read_output", "has_required_columns"],
            "failed": [
                "value_is_numeric: 8 non-numeric or missing values in value",
                "matches_reference_output: matched=49, missing=8, unexpected=5",
            ],
            "score": 2,
            "total": 4,
            "metrics": {
                "reference_rows": 57,
                "output_rows": 54,
                "matched_rows": 49,
                "missing_rows": 8,
                "unexpected_rows": 5,
                "cleanliness_score": 0.859649,
                "output_precision": 0.907407,
            },
        }
        llm_diagnostics = {
            "selected_attempt": "none",
            "attempts": [],
            "prompt_tokens": None,
            "completion_tokens": None,
            "total_tokens": None,
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_root = Path(tmp_dir)
            genome_path = temp_root / "clean_data.py"
            genome_path.write_text(
                "def clean(input_dir, output_path):\n    return None\n",
                encoding="utf-8",
            )
            output_dir = temp_root / ".output"

            with mock.patch.dict(
                os.environ,
                {
                    "AZURE_ENDPOINT": "https://example.openai.azure.com",
                    "AZURE_API_KEY": "demo-key",
                    "MODEL_NAME": "demo-model",
                },
                clear=False,
            ):
                with mock.patch.object(
                    cleanloop_loop.util, "_build_llm_client", return_value=object()
                ):
                    with mock.patch.object(cleanloop_loop, "OUTPUT_DIR", output_dir):
                        with mock.patch.object(
                            cleanloop_loop, "GENOME_PATH", genome_path
                        ):
                            with mock.patch.object(
                                cleanloop_loop,
                                "_run_and_evaluate",
                                return_value=baseline,
                            ):
                                with mock.patch.object(
                                    cleanloop_loop,
                                    "_propose_fix",
                                    return_value=(None, "hold steady", llm_diagnostics),
                                ):
                                    with mock.patch.object(
                                        cleanloop_loop, "_git_commit"
                                    ):
                                        with mock.patch.object(
                                            cleanloop_loop, "_git_revert"
                                        ):
                                            history = cleanloop_loop.run_loop(
                                                max_iterations=1
                                            )

            strategy_path = output_dir / "finance_strategy.json"
            snapshot = json.loads(strategy_path.read_text(encoding="utf-8"))

        self.assertEqual(
            history[0]["metacognition"]["focus_area"], "value_normalization"
        )
        self.assertEqual(snapshot["focus_area"], "value_normalization")
        self.assertIn("recent_failures", snapshot)

    def test_run_loop_records_capacity_error_as_skip_history_entry(self) -> None:
        """Convert proposal capacity failures into a skip round instead of crashing the loop."""
        baseline = {
            "passed": ["can_read_output", "has_required_columns"],
            "failed": ["matches_reference_output: matched=10, missing=5, unexpected=3"],
            "score": 2,
            "total": 3,
            "metrics": {
                "reference_rows": 15,
                "output_rows": 13,
                "matched_rows": 10,
                "missing_rows": 5,
                "unexpected_rows": 3,
                "cleanliness_score": 0.666667,
                "output_precision": 0.769231,
            },
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_root = Path(tmp_dir)
            genome_path = temp_root / "clean_data.py"
            genome_path.write_text(
                "def clean(input_dir, output_path):\n    return None\n",
                encoding="utf-8",
            )

            with mock.patch.dict(
                os.environ,
                {
                    "AZURE_ENDPOINT": "https://example.openai.azure.com",
                    "AZURE_API_KEY": "demo-key",
                    "MODEL_NAME": "demo-model",
                },
                clear=False,
            ):
                with mock.patch.object(
                    cleanloop_loop.util, "_build_llm_client", return_value=object()
                ):
                    with mock.patch.object(
                        cleanloop_loop, "OUTPUT_DIR", temp_root / ".output"
                    ):
                        with mock.patch.object(
                            cleanloop_loop, "GENOME_PATH", genome_path
                        ):
                            with mock.patch.object(
                                cleanloop_loop,
                                "_run_and_evaluate",
                                return_value=baseline,
                            ):
                                with mock.patch.object(
                                    cleanloop_loop,
                                    "_propose_fix",
                                    side_effect=RuntimeError(
                                        "Endpoint busy (429 capacity): demo saturation"
                                    ),
                                ):
                                    with mock.patch.object(
                                        cleanloop_loop, "_git_commit"
                                    ):
                                        with mock.patch.object(
                                            cleanloop_loop, "_git_revert"
                                        ):
                                            with mock.patch.object(
                                                cleanloop_loop,
                                                "_artifact_manifest",
                                                return_value={
                                                    "output_csv": "cleanloop/.output/finance_master.csv"
                                                },
                                            ):
                                                history = cleanloop_loop.run_loop(
                                                    max_iterations=1
                                                )

        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["action"], "skip")
        self.assertIn("429 capacity", history[0]["llm"]["error"])
        self.assertEqual(history[0]["before_metrics"]["missing_rows"], 5)

    def test_run_loop_restores_baseline_output_after_revert(self) -> None:
        """Restore the last good dataset CSV when a candidate mutation is reverted."""
        baseline = {
            "passed": ["can_read_output", "has_required_columns"],
            "failed": ["matches_reference_output: matched=10, missing=5, unexpected=3"],
            "score": 2,
            "total": 3,
            "metrics": {
                "reference_rows": 15,
                "output_rows": 13,
                "matched_rows": 10,
                "missing_rows": 5,
                "unexpected_rows": 3,
                "cleanliness_score": 0.666667,
                "output_precision": 0.769231,
            },
        }
        candidate = {
            "passed": ["has_required_columns"],
            "failed": ["matches_reference_output: matched=0, missing=15, unexpected=0"],
            "score": 1,
            "total": 3,
            "metrics": {
                "reference_rows": 15,
                "output_rows": 0,
                "matched_rows": 0,
                "missing_rows": 15,
                "unexpected_rows": 0,
                "cleanliness_score": 0.0,
                "output_precision": 0.0,
            },
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_root = Path(tmp_dir)
            genome_path = temp_root / "clean_data.py"
            baseline_genome_text = (
                "def clean(input_dir, output_path):\n    return None\n"
            )
            genome_path.write_text(baseline_genome_text, encoding="utf-8")
            starter_path = temp_root / "clean_data_starter.py"
            starter_path.write_text(baseline_genome_text, encoding="utf-8")
            output_dir = temp_root / ".output"
            baseline_output_path = output_dir / "finance_master.csv"
            baseline_output_text = (
                "date,entity,value,category\n"
                "2024-01-15,Acme Manufacturing,15000.0,paid\n"
            )

            def fake_run_and_evaluate(_clean_data, _prepare, _input_dir, output_path):
                if not output_path.exists():
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    output_path.write_text(baseline_output_text, encoding="utf-8")
                    return baseline
                output_path.write_text(
                    "date,product,price,quantity\n", encoding="utf-8"
                )
                return candidate

            with mock.patch.dict(
                os.environ,
                {
                    "AZURE_ENDPOINT": "https://example.openai.azure.com",
                    "AZURE_API_KEY": "demo-key",
                    "MODEL_NAME": "demo-model",
                },
                clear=False,
            ):
                with mock.patch.object(
                    cleanloop_loop.util, "_build_llm_client", return_value=object()
                ):
                    with mock.patch.object(cleanloop_loop, "OUTPUT_DIR", output_dir):
                        with mock.patch.object(
                            cleanloop_loop, "GENOME_PATH", genome_path
                        ):
                            with mock.patch.object(
                                cleanloop_loop,
                                "STARTER_GENOME_PATH",
                                starter_path,
                            ):
                                with mock.patch.object(
                                    cleanloop_loop,
                                    "_run_and_evaluate",
                                    side_effect=fake_run_and_evaluate,
                                ):
                                    with mock.patch.object(
                                        cleanloop_loop,
                                        "_propose_fix",
                                        return_value=(
                                            "def clean(input_dir, output_path):\n    return 'bad'\n",
                                            "bad mutation",
                                            {
                                                "selected_attempt": "CleanLoop proposal",
                                                "attempts": [],
                                                "prompt_tokens": 10,
                                                "completion_tokens": 5,
                                                "total_tokens": 15,
                                            },
                                        ),
                                    ):
                                        with mock.patch.object(
                                            cleanloop_loop.importlib,
                                            "reload",
                                            return_value=None,
                                        ):
                                            with mock.patch.object(
                                                cleanloop_loop, "_git_commit"
                                            ):
                                                with mock.patch.object(
                                                    cleanloop_loop, "_git_revert"
                                                ):
                                                    with mock.patch.object(
                                                        cleanloop_loop,
                                                        "_artifact_manifest",
                                                        return_value={
                                                            "output_csv": "cleanloop/.output/finance_master.csv"
                                                        },
                                                    ):
                                                        history = (
                                                            cleanloop_loop.run_loop(
                                                                max_iterations=1
                                                            )
                                                        )

            restored_output = baseline_output_path.read_text(encoding="utf-8")
            restored_genome = genome_path.read_text(encoding="utf-8")

        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["action"], "revert")
        self.assertEqual(restored_output, baseline_output_text)
        self.assertEqual(restored_genome, baseline_genome_text)
        self.assertEqual(history[0]["before_score"], 2)
        self.assertEqual(history[0]["score"], 1)

    def test_run_loop_reverts_invalid_candidate_without_crashing(self) -> None:
        """Treat malformed candidate code as a reverted mutation instead of a fatal error."""
        baseline = {
            "passed": ["can_read_output", "has_required_columns"],
            "failed": ["matches_reference_output: matched=10, missing=5, unexpected=3"],
            "score": 2,
            "total": 3,
            "metrics": {
                "reference_rows": 15,
                "output_rows": 13,
                "matched_rows": 10,
                "missing_rows": 5,
                "unexpected_rows": 3,
                "cleanliness_score": 0.666667,
                "output_precision": 0.769231,
            },
        }
        llm_diagnostics = {
            "selected_attempt": "CleanLoop proposal",
            "attempts": [],
            "prompt_tokens": 10,
            "completion_tokens": 5,
            "total_tokens": 15,
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_root = Path(tmp_dir)
            genome_path = temp_root / "clean_data.py"
            baseline_genome_text = (
                "def clean(input_dir, output_path):\n    return None\n"
            )
            genome_path.write_text(baseline_genome_text, encoding="utf-8")
            starter_path = temp_root / "clean_data_starter.py"
            starter_path.write_text(baseline_genome_text, encoding="utf-8")
            output_dir = temp_root / ".output"
            baseline_output_path = output_dir / "finance_master.csv"
            baseline_output_text = (
                "date,entity,value,category\n"
                "2024-01-15,Acme Manufacturing,15000.0,paid\n"
            )
            broken_code = (
                "def clean(input_dir, output_path):\n    return 'unterminated\n"
            )

            cleanloop_package = import_module("cleanloop")
            original_clean_data = getattr(cleanloop_package, "clean_data", None)
            original_clean_data_module = sys.modules.get("cleanloop.clean_data")
            clean_data_spec = cleanloop_loop.importlib.util.spec_from_file_location(
                "cleanloop.clean_data",
                genome_path,
            )
            self.assertIsNotNone(clean_data_spec)
            self.assertIsNotNone(clean_data_spec.loader)
            temp_clean_data = cleanloop_loop.importlib.util.module_from_spec(
                clean_data_spec
            )
            clean_data_spec.loader.exec_module(temp_clean_data)
            sys.modules["cleanloop.clean_data"] = temp_clean_data
            setattr(cleanloop_package, "clean_data", temp_clean_data)

            def fake_run_and_evaluate(_clean_data, _prepare, _input_dir, output_path):
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_text(baseline_output_text, encoding="utf-8")
                return baseline

            try:
                with mock.patch.dict(
                    os.environ,
                    {
                        "AZURE_ENDPOINT": "https://example.openai.azure.com",
                        "AZURE_API_KEY": "demo-key",
                        "MODEL_NAME": "demo-model",
                    },
                    clear=False,
                ):
                    with mock.patch.object(
                        cleanloop_loop.util,
                        "_build_llm_client",
                        return_value=object(),
                    ):
                        with mock.patch.object(
                            cleanloop_loop, "OUTPUT_DIR", output_dir
                        ):
                            with mock.patch.object(
                                cleanloop_loop, "GENOME_PATH", genome_path
                            ):
                                with mock.patch.object(
                                    cleanloop_loop,
                                    "STARTER_GENOME_PATH",
                                    starter_path,
                                ):
                                    with mock.patch.object(
                                        cleanloop_loop,
                                        "_run_and_evaluate",
                                        side_effect=fake_run_and_evaluate,
                                    ):
                                        with mock.patch.object(
                                            cleanloop_loop,
                                            "_propose_fix",
                                            return_value=(
                                                broken_code,
                                                "bad mutation",
                                                llm_diagnostics,
                                            ),
                                        ):
                                            with mock.patch.object(
                                                cleanloop_loop, "_git_commit"
                                            ):
                                                with mock.patch.object(
                                                    cleanloop_loop, "_git_revert"
                                                ):
                                                    with mock.patch.object(
                                                        cleanloop_loop,
                                                        "_artifact_manifest",
                                                        return_value={
                                                            "output_csv": "cleanloop/.output/finance_master.csv"
                                                        },
                                                    ):
                                                        history = (
                                                            cleanloop_loop.run_loop(
                                                                max_iterations=1
                                                            )
                                                        )
            finally:
                if original_clean_data_module is None:
                    del sys.modules["cleanloop.clean_data"]
                else:
                    sys.modules["cleanloop.clean_data"] = original_clean_data_module

                if original_clean_data is None:
                    delattr(cleanloop_package, "clean_data")
                else:
                    setattr(cleanloop_package, "clean_data", original_clean_data)

            restored_output = baseline_output_path.read_text(encoding="utf-8")
            restored_genome = genome_path.read_text(encoding="utf-8")

        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["action"], "revert")
        self.assertEqual(history[0]["score"], 0)
        self.assertEqual(history[0]["total"], 1)
        self.assertIn("can_run_genome", history[0]["failed"][0])
        self.assertIn("unterminated string literal", history[0]["failed"][0])
        self.assertEqual(restored_output, baseline_output_text)
        self.assertEqual(restored_genome, baseline_genome_text)

    def test_run_loop_prints_learning_trace_for_no_code_round(self) -> None:
        """Print per-attempt diagnostics so blank gaps are explained in the console."""
        baseline = {
            "passed": [
                "can_read_output",
                "has_required_columns",
                "date_is_parseable",
                "no_nan_date",
                "no_nan_product",
            ],
            "failed": [
                "price_is_numeric: 58 non-numeric or missing values in price",
                "no_nan_price: 3 NaN values in price",
                "matches_reference_output: matched=11, missing=71, unexpected=80",
            ],
            "score": 5,
            "total": 8,
            "metrics": {
                "reference_rows": 82,
                "output_rows": 91,
                "matched_rows": 11,
                "missing_rows": 71,
                "unexpected_rows": 80,
                "cleanliness_score": 0.134146,
                "output_precision": 0.120879,
            },
        }

        llm_diagnostics = {
            "selected_attempt": "none",
            "attempts": [
                {
                    "label": "CleanLoop proposal",
                    "max_tokens": 2200,
                    "code_found": False,
                    "response_chars": 0,
                    "usage": {
                        "prompt_tokens": 1944,
                        "completion_tokens": 2200,
                        "total_tokens": 4144,
                    },
                },
                {
                    "label": "CleanLoop compact retry",
                    "max_tokens": 1200,
                    "code_found": False,
                    "response_chars": 0,
                    "usage": {
                        "prompt_tokens": 1405,
                        "completion_tokens": 1200,
                        "total_tokens": 2605,
                    },
                },
            ],
            "prompt_tokens": 3349,
            "completion_tokens": 3400,
            "total_tokens": 6749,
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_root = Path(tmp_dir)
            genome_path = temp_root / "clean_data.py"
            genome_path.write_text(
                "def clean(input_dir, output_path):\n    return None\n",
                encoding="utf-8",
            )
            stream = io.StringIO()

            with mock.patch.dict(
                os.environ,
                {
                    "AZURE_ENDPOINT": "https://example.openai.azure.com",
                    "AZURE_API_KEY": "demo-key",
                    "MODEL_NAME": "demo-model",
                },
                clear=False,
            ):
                with mock.patch.object(
                    cleanloop_loop.util, "_build_llm_client", return_value=object()
                ):
                    with mock.patch.object(
                        cleanloop_loop, "OUTPUT_DIR", temp_root / ".output"
                    ):
                        with mock.patch.object(
                            cleanloop_loop, "GENOME_PATH", genome_path
                        ):
                            with mock.patch.object(
                                cleanloop_loop,
                                "_run_and_evaluate",
                                return_value=baseline,
                            ):
                                with mock.patch.object(
                                    cleanloop_loop,
                                    "_propose_fix",
                                    return_value=(
                                        None,
                                        "no hypothesis",
                                        llm_diagnostics,
                                    ),
                                ):
                                    with mock.patch.object(
                                        cleanloop_loop, "_git_commit"
                                    ):
                                        with mock.patch.object(
                                            cleanloop_loop, "_git_revert"
                                        ):
                                            with mock.patch.object(
                                                cleanloop_loop,
                                                "_artifact_manifest",
                                                return_value={
                                                    "output_csv": "cleanloop/.output/finance_master.csv"
                                                },
                                            ):
                                                with redirect_stdout(stream):
                                                    cleanloop_loop.run_loop(
                                                        max_iterations=1
                                                    )

        output = stream.getvalue()
        self.assertIn("[REQUESTING_LLM_PROPOSAL]", output)
        self.assertIn("[LLM_ATTEMPT] Attempt 1/2: CleanLoop proposal", output)
        self.assertIn(
            "[ATTEMPT_DIAGNOSIS] token budget exhausted before code output", output
        )
        self.assertIn("[LLM_ATTEMPT] Attempt 2/2: CleanLoop compact retry", output)
        self.assertIn(
            "[NO_CODE_RETURNED] No candidate code returned after 2 attempts", output
        )

    def test_prepare_fresh_run_restores_starter_genome_and_clears_finance_artifacts(
        self,
    ) -> None:
        """Reset each loop run to the starter genome and remove stale finance artifacts."""
        config = cleanloop_datasets.get_dataset_config()

        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_root = Path(tmp_dir)
            starter_path = temp_root / "clean_data_starter.py"
            genome_path = temp_root / "clean_data.py"
            output_path = temp_root / "finance_master.csv"
            history_path = temp_root / "finance_eval_history.json"

            starter_path.write_text(
                "def clean(input_dir, output_path):\n    return 'starter'\n",
                encoding="utf-8",
            )
            genome_path.write_text(
                "def clean(input_dir, output_path):\n    return 'mutated'\n",
                encoding="utf-8",
            )
            output_path.write_text("stale-output", encoding="utf-8")
            history_path.write_text("stale-history", encoding="utf-8")

            round_logs = cleanloop_loop._prepare_fresh_run(
                config,
                output_path,
                history_path,
                genome_path=genome_path,
                starter_genome_path=starter_path,
            )
            restored_genome = genome_path.read_text(encoding="utf-8")
            starter_genome = starter_path.read_text(encoding="utf-8")
            output_exists = output_path.exists()
            history_exists = history_path.exists()

        self.assertEqual(restored_genome, starter_genome)
        self.assertFalse(output_exists)
        self.assertFalse(history_exists)
        self.assertEqual(round_logs[0]["tag"], "FRESH_START")
        self.assertEqual(round_logs[1]["tag"], "RESET_DATASET_ARTIFACTS")
        self.assertEqual(round_logs[2]["tag"], "RESTORE_STARTER_GENOME")

    def test_dashboard_log_rows_include_token_columns(self) -> None:
        """Flatten structured round logs for a dashboard log table."""
        dashboard_metrics = import_module("cleanloop.dashboard_metrics")

        rows = dashboard_metrics.build_log_rows(
            [
                {
                    "round": 2,
                    "logs": [
                        {
                            "tag": "REQUESTING_LLM_PROPOSAL",
                            "message": "Requesting proposal from demo-model",
                        },
                        {
                            "tag": "TOKEN_USAGE",
                            "message": "Attempt 1 token usage",
                            "prompt_tokens": 1944,
                            "completion_tokens": 2200,
                            "total_tokens": 4144,
                        },
                    ],
                }
            ]
        )

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["Round"], 2)
        self.assertEqual(rows[0]["Tag"], "REQUESTING_LLM_PROPOSAL")
        self.assertIsNone(rows[0]["Prompt Tokens"])
        self.assertEqual(rows[1]["Completion Tokens"], 2200)
        self.assertEqual(rows[1]["Total Tokens"], 4144)

    def test_propose_fix_uses_reduced_completion_budgets(self) -> None:
        """Use smaller completion budgets so one round does not over-request model output."""
        calls: list[int] = []

        def fake_proposal(*_args, **kwargs):
            calls.append(kwargs["max_tokens"])
            attempt = {
                "label": "AutoGen proposer",
                "model": "demo-model",
                "max_tokens": kwargs["max_tokens"],
                "code_found": True,
                "hypothesis": "Compact AutoGen proposal",
                "usage": {
                    "prompt_tokens": 10,
                    "completion_tokens": 20,
                    "total_tokens": 30,
                },
                "prompt_chars": 100,
                "response_chars": 180,
                "messages": [],
                "response_preview": "Structured mutation proposal",
            }
            return (
                "def clean(x, y):\n    return None",
                "Compact AutoGen proposal",
                attempt,
            )

        with mock.patch.object(
            cleanloop_loop.autogen_runtime,
            "propose_single_mutation",
            side_effect=fake_proposal,
        ):
            code, hypothesis, diagnostics = cleanloop_loop._propose_fix(
                client=object(),
                model="demo-model",
                system_prompt="system",
                genome_code="def clean(x, y):\n    pass\n",
                results={"failed": ["price_is_numeric: bad row"], "passed": []},
                history=[],
                dataset_name="finance",
            )

        self.assertEqual(calls, [2200])
        self.assertEqual(code, "def clean(x, y):\n    return None")
        self.assertEqual(hypothesis, "Compact AutoGen proposal")
        self.assertEqual(diagnostics["selected_attempt"], "AutoGen proposer")

    def test_parser_does_not_expose_cleanloop_dataset_flag(self) -> None:
        """Finance-only CleanLoop no longer accepts per-dataset CLI routing."""
        parser = util.build_parser()

        args = parser.parse_args(["-e", "cleanloop", "loop"])

        self.assertFalse(hasattr(args, "dataset"))

    def test_parser_exposes_all_runnable_examples(self) -> None:
        """The CLI should route CleanLoop, Prompt Evolution, and Skill Mastery."""
        parser = util.build_parser()

        example_action = next(
            action for action in parser._actions if action.dest == "example"
        )

        self.assertEqual(
            list(example_action.choices),
            ["cleanloop", "prompt_evolution", "skill_mastery"],
        )
        self.assertEqual(
            sorted(util.EXAMPLE_COMMANDS.keys()),
            ["cleanloop", "prompt_evolution", "skill_mastery"],
        )

    def test_finance_dataset_is_the_only_cleanloop_arena(self) -> None:
        """Resolve CleanLoop to the finance arena without external routing."""
        config = cleanloop_datasets.get_dataset_config()

        self.assertEqual(config.name, "finance")
        self.assertEqual(config.output_filename, "finance_master.csv")
        self.assertEqual(config.history_filename, "finance_eval_history.json")
        self.assertGreaterEqual(len(config.input_filenames), 4)
        self.assertTrue(all("stocks" not in name for name in config.input_filenames))
        self.assertEqual(
            list(config.input_filenames),
            [
                "finance_invoices.csv",
                "finance_invoices_flags.csv",
                "finance_invoices_regional.csv",
                "finance_invoices_collections.csv",
                "finance_invoices_adjustments.csv",
            ],
        )

    def test_non_finance_dataset_names_are_rejected(self) -> None:
        """Reject the removed sales and sensors arenas."""
        with self.assertRaises(ValueError):
            cleanloop_datasets.get_dataset_config("sales")

        with self.assertRaises(ValueError):
            cleanloop_datasets.get_dataset_config("sensors")

    def test_finance_reference_output_passes_referee(self) -> None:
        """The canonical finance output should fully satisfy the immutable judge."""
        prepare = cast(Any, import_module("cleanloop.prepare"))

        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = Path(tmp_dir) / "finance_master.csv"

            self._copy_reference_output("finance", output_path)
            results = prepare.evaluate(output_path)

        self.assertEqual(results["failed"], [])
        self.assertEqual(results.get("metrics", {}).get("cleanliness_score"), 1.0)

    def test_finance_starter_genome_requires_improvement(self) -> None:
        """The shipped starter genome should fail the stronger finance judge."""
        clean_data = cast(Any, import_module("cleanloop.clean_data"))
        prepare = cast(Any, import_module("cleanloop.prepare"))

        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = Path(tmp_dir) / "finance_master.csv"

            clean_data.clean(PROJECT_ROOT / "cleanloop" / ".input", output_path)
            results = prepare.evaluate(output_path)

        self.assertGreater(len(results["failed"]), 0)
        self.assertLess(results.get("metrics", {}).get("cleanliness_score", 1.0), 1.0)

    def test_finance_reference_path_detection_is_stable(self) -> None:
        """Treat every CleanLoop output as the finance arena after the simplification."""
        output_path = Path("finance_master.csv")

        self.assertEqual(
            cleanloop_datasets.detect_dataset_from_output_path(output_path), "finance"
        )


if __name__ == "__main__":
    unittest.main()
