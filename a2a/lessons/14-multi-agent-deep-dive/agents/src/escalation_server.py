"""
EscalationAgent A2A Server + REST API — port 10105 (A2A) + 8080 (REST).

Wraps EscalationAgent as an A2A server and also serves the REST API
for the React approval frontend on a separate port.

Usage:
    python escalation_server.py
"""

# pylint: disable=wrong-import-position,wrong-import-order

import asyncio
import os
import sys
import threading
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

from escalation_agent import EscalationAgent, create_rest_app  # noqa: E402

A2A_PORT = 10105
REST_PORT = int(os.getenv("ESCALATION_API_PORT", "8080"))


class EscalationExecutor(AgentExecutor):
    """Bridge A2A protocol to EscalationAgent.escalate()."""

    def __init__(self) -> None:
        self._agent = EscalationAgent()

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """Handle an incoming A2A task — escalate for human review."""
        user_text = context.get_user_input().strip()
        result = await self._agent.escalate(user_text)
        await event_queue.enqueue_event(new_agent_text_message(result))

    async def cancel(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """Cancellation is not supported."""
        raise NotImplementedError("cancel not supported")


agent_card = AgentCard(
    name="EscalationAgent",
    description=(
        "Queues borderline loan applications for human review. "
        "Exposes a REST API for the React approval dashboard."
    ),
    url=f"http://localhost:{A2A_PORT}/",
    version="1.0.0",
    capabilities=AgentCapabilities(streaming=False),
    default_input_modes=["text"],
    default_output_modes=["text"],
    skills=[
        AgentSkill(
            id="escalate_application",
            name="Escalate for Human Review",
            description="Queue a borderline loan application for human review.",
            tags=["loan", "escalation", "human-in-the-loop"],
            examples=["Escalate this application for review"],
        )
    ],
)

request_handler = DefaultRequestHandler(
    agent_executor=EscalationExecutor(),
    task_store=InMemoryTaskStore(),
)

a2a_server = A2AStarletteApplication(
    agent_card=agent_card,
    http_handler=request_handler,
)


def _run_rest_api() -> None:
    """Run the REST API on a separate thread."""
    rest_app = create_rest_app()
    uvicorn.run(rest_app, host="0.0.0.0", port=REST_PORT, log_level="info")


if __name__ == "__main__":
    print(f"Starting EscalationAgent A2A server on port {A2A_PORT} …")
    print(f"  Agent Card : http://localhost:{A2A_PORT}/.well-known/agent.json")
    print(f"Starting Escalation REST API on port {REST_PORT} …")
    print(f"  Pending    : GET  http://localhost:{REST_PORT}/api/escalations/pending")
    print(
        f"  Decide     : POST http://localhost:{REST_PORT}/api/escalations/{{id}}/decide"
    )
    print()

    # Start REST API in background thread
    rest_thread = threading.Thread(target=_run_rest_api, daemon=True)
    rest_thread.start()

    # Run A2A server in main thread
    uvicorn.run(a2a_server.build(), host="0.0.0.0", port=A2A_PORT)
