"""Critic Agent A2A server — evaluates trip plans.

Receives a trip plan and evaluates it against quality criteria:
  1. Must include a hotel recommendation
  2. Must list at least 2 attractions
  3. Must mention dining or restaurants
  4. Must include transport or getting-around tips

Returns PASS if all criteria met, or specific improvement feedback.

Requires:
    - Ollama running at http://127.0.0.1:11434 with qwen3.5:0.8b pulled

Port: 11402
"""

import logging

import uvicorn
from openai import OpenAI

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.apps import A2AStarletteApplication
from a2a.server.events import EventQueue
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from a2a.utils import new_agent_text_message

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")
logger = logging.getLogger("critic")

PORT = 11402
OLLAMA_BASE = "http://127.0.0.1:11434/v1"
MODEL = "qwen3.5:0.8b"


class CriticAgent:
    """Evaluates trip plans against quality criteria."""

    def __init__(self) -> None:
        """Initialize the OpenAI client for Ollama."""
        self._client = OpenAI(base_url=OLLAMA_BASE, api_key="unused")

    def process(self, plan_text: str) -> str:
        """Evaluate a trip plan. Returns PASS or improvement feedback."""
        logger.info("Critiquing plan (%d chars)", len(plan_text))
        lower_text = plan_text.lower()
        feedback = []

        if not any(word in lower_text for word in ["hotel", "accommodation", "stay"]):
            feedback.append("Add a hotel or accommodation recommendation.")

        attraction_hits = sum(
            1
            for word in [
                "attraction", "museum", "bridge", "park", "temple", "tower", "wharf",
            ]
            if word in lower_text
        )
        if attraction_hits < 2:
            feedback.append("Include at least two attractions or activities.")

        if not any(word in lower_text for word in ["restaurant", "dining", "food", "breakfast", "lunch", "dinner"]):
            feedback.append("Mention dining, restaurants, or food.")

        if not any(word in lower_text for word in ["transport", "train", "metro", "subway", "bus", "taxi", "walk"]):
            feedback.append("Include transport or getting-around tips.")

        if not feedback:
            logger.info("Critique result: PASS")
            return "PASS"

        answer = " ".join(feedback)
        logger.info("Critique result: %s", answer[:80])
        return answer


# ---------------------------------------------------------------------------
# A2A server wiring
# ---------------------------------------------------------------------------

agent_card = AgentCard(
    name="CriticAgent",
    description="Evaluates trip plans against quality criteria.",
    url=f"http://localhost:{PORT}/",
    version="1.0.0",
    capabilities=AgentCapabilities(streaming=False),
    default_input_modes=["text"],
    default_output_modes=["text"],
    skills=[
        AgentSkill(
            id="plan_critique",
            name="Plan Critique",
            description="Evaluate a trip plan for completeness.",
            tags=["evaluation", "quality"],
            examples=["Evaluate this trip plan"],
        ),
    ],
)


class CriticExecutor(AgentExecutor):
    """A2A executor for the Critic."""

    def __init__(self) -> None:
        """Initialize."""
        self._agent = CriticAgent()

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Handle A2A request."""
        user_text = context.get_user_input().strip()
        result = self._agent.process(user_text)
        await event_queue.enqueue_event(new_agent_text_message(result))

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Handle cancellation."""


def main() -> None:
    """Start the Critic A2A server."""
    logger.info("Starting CriticAgent on port %d", PORT)
    handler = DefaultRequestHandler(
        agent_executor=CriticExecutor(),
        task_store=InMemoryTaskStore(),
    )
    server = A2AStarletteApplication(agent_card=agent_card, http_handler=handler)
    uvicorn.run(server.build(), host="0.0.0.0", port=PORT, log_level="warning")


if __name__ == "__main__":
    main()
