# pylint: disable=wrong-import-position,duplicate-code
# pylint: disable=too-few-public-methods,protected-access

"""Regression tests for the CleanLoop local verify command."""

from __future__ import annotations

import io
import sys
import unittest
import warnings
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from cleanloop import verify
from cleanloop import util as cleanloop_util


class CleanLoopVerifyTests(unittest.TestCase):
    """Keep learner-facing verify output stable and actionable."""

    def test_build_llm_client_adds_model_info_for_openai_compatible_v1(self) -> None:
        """Pass model_info for non-OpenAI models behind a standard /v1 endpoint."""
        captured_kwargs: dict[str, object] = {}

        class FakeOpenAIChatCompletionClient:
            """Capture constructor kwargs without importing AutoGen internals."""

            def __init__(self, **kwargs: object) -> None:
                captured_kwargs.update(kwargs)

        fake_openai_module = mock.Mock()
        fake_openai_module.OpenAIChatCompletionClient = FakeOpenAIChatCompletionClient

        with mock.patch.object(
            cleanloop_util,
            "_resolve_llm_env",
            return_value={
                "endpoint": "https://integrate.api.nvidia.com/v1",
                "api_key": "secret",
                "api_version": "2024-06-01",
                "model": "deepseek-ai/deepseek-v4-pro",
                "endpoint_var": "LLM_ENDPOINT",
                "api_key_var": "LLM_API_KEY",
            },
        ):
            with mock.patch.object(
                cleanloop_util.importlib,
                "import_module",
                return_value=fake_openai_module,
            ):
                cleanloop_util._build_llm_client(
                    "https://integrate.api.nvidia.com/v1",
                    "secret",
                    "2024-06-01",
                )

        self.assertEqual(
            captured_kwargs["base_url"],
            "https://integrate.api.nvidia.com/v1",
        )
        self.assertIn("model_info", captured_kwargs)
        self.assertIsInstance(captured_kwargs["model_info"], dict)

    def test_check_credentials_reports_missing_endpoint_without_crashing(self) -> None:
        """Return a friendly failure when the local .env does not resolve."""
        stdout = io.StringIO()

        with redirect_stdout(stdout):
            with mock.patch.object(
                verify.util,
                "resolve_llm_env",
                side_effect=RuntimeError(
                    "Missing LLM endpoint. Set LLM_ENDPOINT in cleanloop/.env."
                ),
            ):
                result = verify.check_credentials()

        self.assertFalse(result)
        output = stdout.getvalue()
        self.assertIn("[FAIL]", output)
        self.assertIn("Missing LLM endpoint", output)

    def test_check_llm_call_suppresses_provider_warning_noise(self) -> None:
        """Hide provider warning spam so verify output stays readable."""
        stdout = io.StringIO()
        stderr = io.StringIO()
        config = {
            "endpoint": "https://models.github.ai/inference",
            "api_key": "secret",
            "api_version": "2024-06-01",
            "model": "microsoft/Phi-4",
        }

        def _fake_completion(*_args: object, **_kwargs: object) -> str:
            warnings.warn(
                (
                    "Resolved model mismatch: microsoft/Phi-4 != phi4. "
                    "Model mapping in autogen_ext.models.openai may be incorrect."
                ),
                UserWarning,
                stacklevel=1,
            )
            return "hello"

        with redirect_stdout(stdout), redirect_stderr(stderr):
            with mock.patch.object(verify.util, "resolve_llm_env", return_value=config):
                with mock.patch.object(
                    verify.util, "build_llm_client", return_value=object()
                ):
                    with mock.patch.object(
                        verify.util,
                        "create_text_completion",
                        side_effect=_fake_completion,
                    ):
                        result = verify.check_llm_call()

        self.assertTrue(result)
        self.assertIn("[OK] LLM replied: hello", stdout.getvalue())
        self.assertEqual("", stderr.getvalue())

    def test_check_llm_call_passes_verify_timeout_to_completion(self) -> None:
        """Forward the verify timeout budget into the live completion helper."""
        stdout = io.StringIO()
        config = {
            "endpoint": "https://integrate.api.nvidia.com/v1",
            "api_key": "secret",
            "api_version": "2024-06-01",
            "model": "deepseek-ai/deepseek-v4-pro",
        }

        with redirect_stdout(stdout):
            with mock.patch.dict(
                cleanloop_util.os.environ,
                {"CLEANLOOP_VERIFY_TIMEOUT_SECONDS": "12"},
                clear=False,
            ):
                with mock.patch.object(
                    verify.util, "resolve_llm_env", return_value=config
                ):
                    with mock.patch.object(
                        verify.util, "build_llm_client", return_value=object()
                    ):
                        with mock.patch.object(
                            verify.util,
                            "create_text_completion",
                            return_value="hello",
                        ) as create_completion:
                            result = verify.check_llm_call()

        self.assertTrue(result)
        self.assertEqual(
            12,
            create_completion.call_args.kwargs["timeout_seconds"],
        )


if __name__ == "__main__":
    unittest.main()
