"""
Lesson 12 — A2A Server wrapping the OpenAI Agents SDK OrchestratorAgent.

Usage:
    python server.py          # starts on http://localhost:10005

Reuses ``loan_data.py`` and ``validation_rules.py`` from ``_common/src``.

Environment variables required (loaded from ``_examples/a2a/.env``):
    AZURE_OPENAI_ENDPOINT
    AZURE_AI_API_KEY
    AZURE_AI_MODEL_DEPLOYMENT_NAME
"""

# mypy: disable-error-code=import-not-found

from __future__ import annotations

# pylint: disable=wrong-import-position,wrong-import-order

import os
import sys
from pathlib import Path

# ─── path setup: reuse _common shared data & rules ──────────────────────────
_COMMON = str(Path(__file__).resolve().parents[2] / "_common" / "src")
_PROJECT_ROOT = str(Path(__file__).resolve().parents[3])
if _COMMON not in sys.path:
    sys.path.insert(0, _COMMON)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

_THIS_SRC = str(Path(__file__).resolve().parent)
if _THIS_SRC not in sys.path:
    sys.path.insert(0, _THIS_SRC)

# ─── load .env ────────────────────────────────────────────────────────────────
from dotenv import load_dotenv  # noqa: E402


def _load_env_file() -> None:
    """Load environment values from the lesson-level .env file if present."""
    # Preferred location in this repo: _examples/a2a/.env
    candidate_paths = [
        Path(__file__).resolve().parents[3] / ".env",
        # Backward-compatible fallback for older docs/scripts.
        Path(__file__).resolve().parents[4] / ".env",
    ]
    for env_path in candidate_paths:
        if env_path.exists():
            load_dotenv(env_path)
            return

    # Keep startup working when vars are provided by shell/CI environment.
    load_dotenv()


def _require_env(name: str) -> str:
    """Return a required environment variable or raise a helpful error."""
    value = os.environ.get(name)
    if value:
        return value
    raise RuntimeError(
        "Missing required environment variable: "
        f"{name}. Configure _examples/a2a/.env (copy from .env.example) "
        "or export the variable in your shell before running server.py."
    )


_load_env_file()

# ─── configure OpenAI Agents SDK for Azure ────────────────────────────────────────
from agents import (
    set_default_openai_api,
    set_default_openai_client,
    set_tracing_disabled,
)  # noqa: E402
from openai import AsyncAzureOpenAI  # noqa: E402

_azure_client = AsyncAzureOpenAI(
    azure_endpoint=_require_env("AZURE_OPENAI_ENDPOINT"),
    api_key=_require_env("AZURE_AI_API_KEY"),
    api_version="2025-04-01-preview",
)
set_default_openai_client(_azure_client)
set_default_openai_api("chat_completions")
set_tracing_disabled(True)  # disable tracing to avoid 401s against api.openai.com

# ─── imports ──────────────────────────────────────────────────────────────────
from a2a.server.agent_execution import AgentExecutor, RequestContext  # noqa: E402
from a2a.server.events import EventQueue  # noqa: E402
from a2a.server.request_handlers import DefaultRequestHandler  # noqa: E402
from a2a.server.tasks import InMemoryTaskStore  # noqa: E402
from a2a.types import (  # noqa: E402
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)
from a2a.server.apps import A2AStarletteApplication  # noqa: E402
from a2a.utils import new_agent_text_message  # noqa: E402

from loan_data import APPLICANT_INDEX  # noqa: E402
from orchestrator import OrchestratorAgent  # noqa: E402

# ─── constants ────────────────────────────────────────────────────────────────
SERVER_HOST = "localhost"
SERVER_PORT = 10005

# ─── AgentExecutor ────────────────────────────────────────────────────────────


class LoanValidatorExecutor(AgentExecutor):
    """Bridges A2A request → OpenAI Agents SDK OrchestratorAgent → A2A response."""

    def __init__(self) -> None:
        self._orchestrator = OrchestratorAgent()

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        user_text = context.get_user_input().strip()

        # Extract applicant ID
        app_id: str | None = None
        for token in user_text.split():
            if token in APPLICANT_INDEX:
                app_id = token
                break

        if app_id is None:
            await event_queue.enqueue_event(
                new_agent_text_message(
                    f"Please provide an applicant ID.  "
                    f"Supported: {list(APPLICANT_INDEX.keys())}"
                )
            )
            return

        application = APPLICANT_INDEX[app_id]
        report = await self._orchestrator.validate(application)
        await event_queue.enqueue_event(new_agent_text_message(str(report)))

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Cancellation is not supported for this synchronous validator."""
        raise NotImplementedError("cancel not supported")


# ─── Agent Card ───────────────────────────────────────────────────────────────

SKILL = AgentSkill(
    id="loan-validation",
    name="Loan Application Pre-Screening",
    description=(
        "Run hard-fail and advisory rule checks on a mortgage application, "
        "then generate a structured validation report."
    ),
    tags=["loan", "validation", "mortgage", "openai-agents"],
    examples=[
        "Validate loan application APP-1001",
        "Run pre-screening for APP-1002",
    ],
)

AGENT_CARD = AgentCard(
    name="LoanValidatorOpenAIAgents",
    description=(
        "Mortgage application pre-screening agent "
        "powered by the OpenAI Agents SDK and Kimi-K2."
    ),
    url=f"http://{SERVER_HOST}:{SERVER_PORT}",
    version="1.0.0",
    capabilities=AgentCapabilities(streaming=False),
    skills=[SKILL],
    default_input_modes=["text"],
    default_output_modes=["text"],
)


# ─── main ─────────────────────────────────────────────────────────────────────


def main() -> None:
    """Start the OpenAI Agents SDK Loan Validator A2A server."""
    executor = LoanValidatorExecutor()
    request_handler = DefaultRequestHandler(
        agent_executor=executor,
        task_store=InMemoryTaskStore(),
    )

    a2a_app = A2AStarletteApplication(
        agent_card=AGENT_CARD,
        http_handler=request_handler,
    )

    import uvicorn  # pylint: disable=import-outside-toplevel

    print(
        "OpenAI Agents SDK Loan Validator A2A server on "
        f"http://{SERVER_HOST}:{SERVER_PORT}"
    )
    uvicorn.run(a2a_app.build(), host=SERVER_HOST, port=SERVER_PORT)


if __name__ == "__main__":
    main()
