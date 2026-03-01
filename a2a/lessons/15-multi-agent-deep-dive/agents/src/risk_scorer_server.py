"""
RiskScorerAgent A2A Server — port 10102.

Wraps RiskScorerAgent as a standards-compliant A2A server.

Usage:
    python risk_scorer_server.py
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

from risk_scorer import RiskScorerAgent  # noqa: E402

SERVER_PORT = 10102


class RiskScorerExecutor(AgentExecutor):
    """Bridge A2A protocol to RiskScorerAgent.score()."""

    def __init__(self) -> None:
        self._agent = RiskScorerAgent()

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """Handle an incoming A2A task — score the loan application."""
        user_text = context.get_user_input().strip()
        result = await self._agent.score(user_text)
        await event_queue.enqueue_event(new_agent_text_message(result))

    async def cancel(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """Cancellation is not supported."""
        raise NotImplementedError("cancel not supported")


agent_card = AgentCard(
    name="RiskScorerAgent",
    description=(
        "Computes a 0-100 risk score for loan applications using "
        "deterministic rules (40%) and LLM reasoning (60%)."
    ),
    url=f"http://localhost:{SERVER_PORT}/",
    version="1.0.0",
    capabilities=AgentCapabilities(streaming=False),
    default_input_modes=["text"],
    default_output_modes=["text"],
    skills=[
        AgentSkill(
            id="score_risk",
            name="Score Loan Risk",
            description="Compute composite risk score from rules and LLM assessment.",
            tags=["loan", "risk", "scoring", "llm"],
            examples=["Score this loan application"],
        )
    ],
)

request_handler = DefaultRequestHandler(
    agent_executor=RiskScorerExecutor(),
    task_store=InMemoryTaskStore(),
)

server = A2AStarletteApplication(
    agent_card=agent_card,
    http_handler=request_handler,
)

if __name__ == "__main__":
    print(f"Starting RiskScorerAgent A2A server on port {SERVER_PORT} …")
    print(f"  Agent Card : http://localhost:{SERVER_PORT}/.well-known/agent.json")
    uvicorn.run(server.build(), host="0.0.0.0", port=SERVER_PORT)
