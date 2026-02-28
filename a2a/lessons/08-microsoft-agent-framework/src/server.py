"""
Lesson 08 — A2A server wrapping the OrchestratorAgent.

Exposes the loan validator as a standards-compliant A2A server on port 10008.
Other agents (e.g. LangGraph, CrewAI, Google ADK) can discover and call it via
the A2A protocol — demonstrating cross-framework interoperability.

Usage (from lessons/08-microsoft-agent-framework/src/):
    python server.py

Endpoints:
    GET  http://localhost:10008/.well-known/agent.json   → Agent Card
    POST http://localhost:10008/                         → JSON-RPC (message/send)
"""

# pylint: disable=wrong-import-position,wrong-import-order

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]

# ── Ensure src/ is on the path ────────────────────────────────────
_SRC = Path(__file__).parent.resolve()
sys.path.insert(0, str(_SRC))

import uvicorn  # noqa: E402
from dotenv import find_dotenv, load_dotenv  # noqa: E402

load_dotenv(find_dotenv(raise_error_if_not_found=False))

from a2a.server.agent_execution import AgentExecutor, RequestContext  # noqa: E402
from a2a.server.apps import A2AStarletteApplication  # noqa: E402
from a2a.server.events import EventQueue  # noqa: E402
from a2a.server.request_handlers import DefaultRequestHandler  # noqa: E402
from a2a.server.tasks import InMemoryTaskStore  # noqa: E402
from a2a.types import AgentCapabilities, AgentCard, AgentSkill  # noqa: E402
from a2a.utils import new_agent_text_message  # noqa: E402

from loan_data import APPLICANT_INDEX  # noqa: E402
from orchestrator import OrchestratorAgent, ValidationReport  # noqa: E402

SERVER_PORT = 10008


class LoanValidatorExecutor(AgentExecutor):
    """Bridges the A2A protocol to OrchestratorAgent.validate()."""

    def __init__(self) -> None:
        self._agent = OrchestratorAgent()

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """Handle an incoming A2A message/send request."""
        user_text = context.get_user_input().strip()

        # Accept an applicant_id token anywhere in the input text
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

        app = APPLICANT_INDEX[app_id]
        report: ValidationReport = await self._agent.validate(app)
        await event_queue.enqueue_event(new_agent_text_message(str(report)))

    async def cancel(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """Cancellation is not supported for this synchronous validator."""
        raise NotImplementedError("cancel not supported")


# ─── Agent Card ───────────────────────────────────────────────────────────────

agent_card = AgentCard(
    name="LoanValidatorOrchestrator",
    description=(
        "Pre-screens residential mortgage applications using deterministic "
        "business rules and Kimi-K2-Thinking reasoning to produce APPROVED / "
        "NEEDS_REVIEW / DECLINED verdicts with full justification."
    ),
    url=f"http://localhost:{SERVER_PORT}/",
    version="1.0.0",
    capabilities=AgentCapabilities(streaming=False),
    default_input_modes=["text"],
    default_output_modes=["text"],
    skills=[
        AgentSkill(
            id="validate_loan",
            name="Validate Loan Application",
            description=(
                "Run hard/soft business-rule checks and LLM reasoning "
                "on a loan application."
            ),
            tags=["loan", "validation", "underwriting", "mortgage", "fha"],
            examples=[
                "APP-2024-001",
                "APP-2024-003",
            ],
        )
    ],
)

# ─── Wire up and run ──────────────────────────────────────────────────────────

request_handler = DefaultRequestHandler(
    agent_executor=LoanValidatorExecutor(),
    task_store=InMemoryTaskStore(),
)

server = A2AStarletteApplication(
    agent_card=agent_card,
    http_handler=request_handler,
)

if __name__ == "__main__":
    print(f"Starting LoanValidatorOrchestrator A2A server on port {SERVER_PORT} …")
    print(f"  Agent Card : http://localhost:{SERVER_PORT}/.well-known/agent.json")
    print(f"  JSON-RPC   : POST http://localhost:{SERVER_PORT}/")
    print()
    uvicorn.run(server.build(), host="0.0.0.0", port=SERVER_PORT)
