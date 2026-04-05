"""Cost Agent A2A server — handles budget and pricing queries.

Specialist agent for the Coordinator pattern. Provides budget
estimates and cost breakdowns for travel.

Requires:
    - Ollama running at http://127.0.0.1:11434 with gemma4:e2b pulled

Port: 11413
"""

import json
import logging

import uvicorn

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.apps import A2AStarletteApplication
from a2a.server.events import EventQueue
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from a2a.utils import new_agent_text_message

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")
logger = logging.getLogger("cost-agent")

PORT = 11413

COST_DATA = {
    "san francisco": {
        "hotel_per_night": "$150-300",
        "meal_average": "$20-50",
        "transit_day_pass": "$5 (Muni)",
        "attractions": "$0-40 per venue",
    },
    "new york": {
        "hotel_per_night": "$200-400",
        "meal_average": "$15-60",
        "transit_day_pass": "$33 (unlimited MetroCard)",
        "attractions": "$0-45 per venue",
    },
    "paris": {
        "hotel_per_night": "EUR 120-280",
        "meal_average": "EUR 15-45",
        "transit_day_pass": "EUR 16.10 (Navigo jour)",
        "attractions": "EUR 0-17 per venue",
    },
    "tokyo": {
        "hotel_per_night": "JPY 8000-25000",
        "meal_average": "JPY 800-3000",
        "transit_day_pass": "JPY 600 (Tokyo Metro)",
        "attractions": "JPY 0-2000 per venue",
    },
}


class CostAgent:
    """Provides budget estimates and cost breakdowns."""

    def __init__(self) -> None:
        """Initialize the agent."""
        pass

    def process(self, query: str) -> str:
        """Answer a budget or cost query."""
        logger.info("CostAgent processing: %s", query[:60])

        for city, costs in COST_DATA.items():
            if city in query.lower():
                return json.dumps(_build_cost_payload(city, costs), indent=2)

        return json.dumps(_build_cost_payload("unknown", {}), indent=2)


def _build_cost_payload(city: str, costs: dict[str, str]) -> dict:
    """Create a structured cost payload for coordinator routing."""
    items = [
        {
            "label": key.replace("_", " ").title(),
            "value": value,
        }
        for key, value in list(costs.items())[:4]
    ]
    note = "Specialist returned typical budget ranges." if items else "The demo has no budget data for this request."
    return {
        "agent": "CostAgent",
        "city": city,
        "kind": "cost_estimate",
        "items": items,
        "note": note,
    }


agent_card = AgentCard(
    name="CostAgent",
    description="Specialist for travel budgets, pricing, and cost estimates.",
    url=f"http://127.0.0.1:{PORT}/",
    version="1.0.0",
    capabilities=AgentCapabilities(streaming=False),
    default_input_modes=["text"],
    default_output_modes=["text"],
    skills=[
        AgentSkill(
            id="cost_specialist",
            name="Cost Specialist",
            description="Provide budget estimates for travel.",
            tags=["budget", "cost"],
            examples=["How much does a weekend in Paris cost"],
        ),
    ],
)


class CostExecutor(AgentExecutor):
    """A2A executor for Cost Agent."""

    def __init__(self) -> None:
        """Initialize."""
        self._agent = CostAgent()

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Handle A2A request."""
        user_text = context.get_user_input().strip()
        result = self._agent.process(user_text)
        await event_queue.enqueue_event(new_agent_text_message(result))

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Handle cancellation."""


def main() -> None:
    """Start the Cost Agent A2A server."""
    logger.info("Starting CostAgent on port %d", PORT)
    handler = DefaultRequestHandler(
        agent_executor=CostExecutor(),
        task_store=InMemoryTaskStore(),
    )
    server = A2AStarletteApplication(agent_card=agent_card, http_handler=handler)
    uvicorn.run(server.build(), host="0.0.0.0", port=PORT, log_level="warning")


if __name__ == "__main__":
    main()
