"""
ComplianceAgent A2A Server — port 10103.

Wraps ComplianceAgent as a standards-compliant A2A server.

Usage:
    python compliance_server.py
"""

# pylint: disable=wrong-import-position,wrong-import-order

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

from compliance_agent import ComplianceAgent  # noqa: E402

SERVER_PORT = 10103


class ComplianceExecutor(AgentExecutor):
    """Bridge A2A protocol to ComplianceAgent.check()."""

    def __init__(self) -> None:
        self._agent = ComplianceAgent()

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """Handle an incoming A2A task — check compliance."""
        user_text = context.get_user_input().strip()
        result = await self._agent.check(user_text)
        await event_queue.enqueue_event(new_agent_text_message(result))

    async def cancel(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """Cancellation is not supported."""
        raise NotImplementedError("cancel not supported")


agent_card = AgentCard(
    name="ComplianceAgent",
    description="Checks loan applications against FHA, VA, and conventional regulatory requirements.",
    url=f"http://localhost:{SERVER_PORT}/",
    version="1.0.0",
    capabilities=AgentCapabilities(streaming=False),
    default_input_modes=["text"],
    default_output_modes=["text"],
    skills=[
        AgentSkill(
            id="check_compliance",
            name="Check Loan Compliance",
            description="Validate against lending regulations and flag non-compliant aspects.",
            tags=["loan", "compliance", "fha", "va", "conventional"],
            examples=["Check compliance for this loan application"],
        )
    ],
)

request_handler = DefaultRequestHandler(
    agent_executor=ComplianceExecutor(),
    task_store=InMemoryTaskStore(),
)

server = A2AStarletteApplication(
    agent_card=agent_card,
    http_handler=request_handler,
)

if __name__ == "__main__":
    print(f"Starting ComplianceAgent A2A server on port {SERVER_PORT} …")
    print(f"  Agent Card : http://localhost:{SERVER_PORT}/.well-known/agent.json")
    uvicorn.run(server.build(), host="0.0.0.0", port=SERVER_PORT)
