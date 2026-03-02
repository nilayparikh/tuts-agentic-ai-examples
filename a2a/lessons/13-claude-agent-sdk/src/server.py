"""
Lesson 13 — A2A Server wrapping the Claude-style OrchestratorAgent.

Usage:
    python server.py          # starts on http://localhost:10006

Reuses ``loan_data.py`` and ``validation_rules.py`` from ``_common/src``.

Environment variables required (loaded from ``_examples/.env``):
    AZURE_OPENAI_ENDPOINT
    AZURE_AI_API_KEY
    AZURE_AI_MODEL_DEPLOYMENT_NAME
"""

# mypy: disable-error-code=import-not-found

from __future__ import annotations

# pylint: disable=wrong-import-position,wrong-import-order

import sys
from pathlib import Path

# ─── path setup: reuse _common shared data & rules ───────────────────────────
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

load_dotenv(Path(__file__).resolve().parents[4] / ".env")

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
SERVER_PORT = 10006


# ─── AgentExecutor ────────────────────────────────────────────────────────────


class LoanValidatorExecutor(AgentExecutor):
    """Bridges A2A request → Claude-style OrchestratorAgent → A2A response.

    Maintains per-task OrchestratorAgent instances to preserve conversation
    state across multi-turn interactions (Claude-style memory pattern).
    """

    def __init__(self) -> None:
        self._agents: dict[str, OrchestratorAgent] = {}

    def _get_agent(self, task_id: str) -> OrchestratorAgent:
        """Return (or create) an OrchestratorAgent instance for the given task."""
        if task_id not in self._agents:
            self._agents[task_id] = OrchestratorAgent()
        return self._agents[task_id]

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

        # Get a per-task agent (Claude-style: isolated conversation state)
        task_id = getattr(context, "task_id", "default")
        agent = self._get_agent(task_id)

        application = APPLICANT_INDEX[app_id]
        report = await agent.validate(application)
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
        "then generate a structured validation report using Claude-style "
        "agent patterns (manual tool-call loop, conversation memory)."
    ),
    tags=["loan", "validation", "mortgage", "claude-agent-sdk"],
    examples=[
        "Validate loan application APP-2024-001",
        "Run pre-screening for APP-2024-004",
    ],
)

AGENT_CARD = AgentCard(
    name="LoanValidatorClaudeStyle",
    description=(
        "Mortgage application pre-screening agent using Claude-style agent "
        "patterns (JSON schema tools, explicit tool dispatch, conversation "
        "memory) powered by Kimi-K2-Thinking via Azure AI Foundry."
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
    """Start the Claude-style Loan Validator A2A server."""
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
        "Claude-style Loan Validator A2A server on "
        f"http://{SERVER_HOST}:{SERVER_PORT}"
    )
    uvicorn.run(a2a_app.build(), host=SERVER_HOST, port=SERVER_PORT)


if __name__ == "__main__":
    main()
