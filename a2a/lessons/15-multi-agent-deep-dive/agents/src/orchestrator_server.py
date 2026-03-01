"""
MasterOrchestrator A2A Server — port 10100.

Wraps MasterOrchestrator as a standards-compliant A2A server. Accepts
loan application JSON and routes through the full agent pipeline.

Usage:
    python orchestrator_server.py
"""

# pylint: disable=wrong-import-position,wrong-import-order

import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]

_SRC = Path(__file__).parent.resolve()
sys.path.insert(0, str(_SRC))

import logging  # noqa: E402

import uvicorn  # noqa: E402
from dotenv import find_dotenv, load_dotenv  # noqa: E402

load_dotenv(find_dotenv(raise_error_if_not_found=False))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)-18s %(levelname)-7s %(message)s",
    datefmt="%H:%M:%S",
)

from a2a.server.agent_execution import AgentExecutor, RequestContext  # noqa: E402
from a2a.server.apps import A2AStarletteApplication  # noqa: E402
from a2a.server.events import EventQueue  # noqa: E402
from a2a.server.request_handlers import DefaultRequestHandler  # noqa: E402
from a2a.server.tasks import InMemoryTaskStore  # noqa: E402
from a2a.types import AgentCapabilities, AgentCard, AgentSkill  # noqa: E402
from a2a.utils import new_agent_text_message  # noqa: E402

from orchestrator import MasterOrchestrator  # noqa: E402

SERVER_PORT = 10100


class OrchestratorExecutor(AgentExecutor):
    """Bridge A2A protocol to MasterOrchestrator.process_application()."""

    def __init__(self) -> None:
        self._orchestrator = MasterOrchestrator()
        self._discovered = False

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """Handle an incoming A2A task — process a loan application."""
        # Lazy discovery on first request
        if not self._discovered:
            await self._orchestrator.discover_agents()
            self._discovered = True

        user_text = context.get_user_input().strip()

        try:
            application = json.loads(user_text)
        except json.JSONDecodeError:
            await event_queue.enqueue_event(
                new_agent_text_message(
                    '{"error": "Invalid JSON. Send a loan application object."}'
                )
            )
            return

        result = await self._orchestrator.process_application(application)
        await event_queue.enqueue_event(
            new_agent_text_message(json.dumps(result, indent=2))
        )

    async def cancel(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """Cancellation is not supported."""
        raise NotImplementedError("cancel not supported")


agent_card = AgentCard(
    name="LoanApprovalOrchestrator",
    description=(
        "Multi-agent loan approval pipeline. Routes applications through "
        "intake, risk scoring, compliance, decisioning, and optional "
        "human-in-the-loop escalation."
    ),
    url=f"http://localhost:{SERVER_PORT}/",
    version="1.0.0",
    capabilities=AgentCapabilities(streaming=False),
    default_input_modes=["text"],
    default_output_modes=["text"],
    skills=[
        AgentSkill(
            id="process_loan",
            name="Process Loan Application",
            description=(
                "Run a loan application through the full multi-agent pipeline: "
                "intake → risk scoring → compliance → decision → escalation."
            ),
            tags=["loan", "approval", "orchestration", "multi-agent"],
            examples=["Process this loan application JSON"],
        )
    ],
)

request_handler = DefaultRequestHandler(
    agent_executor=OrchestratorExecutor(),
    task_store=InMemoryTaskStore(),
)

server = A2AStarletteApplication(
    agent_card=agent_card,
    http_handler=request_handler,
)

if __name__ == "__main__":
    print(f"Starting LoanApprovalOrchestrator A2A server on port {SERVER_PORT} …")
    print(f"  Agent Card : http://localhost:{SERVER_PORT}/.well-known/agent.json")
    print()
    print("Pipeline agents expected on:")
    print("  IntakeAgent       : http://localhost:10101/")
    print("  RiskScorerAgent   : http://localhost:10102/")
    print("  ComplianceAgent   : http://localhost:10103/")
    print("  DecisionAgent     : http://localhost:10104/")
    print("  EscalationAgent   : http://localhost:10105/")
    print()
    uvicorn.run(server.build(), host="0.0.0.0", port=SERVER_PORT)
