"""Food Agent A2A server — handles food and dining queries.

Specialist agent for the Coordinator pattern. Answers food-related
queries for any city.

Requires:
    - Ollama running at http://127.0.0.1:11434 with qwen3.5:0.8b pulled

Port: 11411
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
logger = logging.getLogger("food-agent")

PORT = 11411

FOOD_DATA = {
    "san francisco": [
        "Tartine Bakery - artisan bakery, Mission District",
        "Swan Oyster Depot - classic seafood counter, Nob Hill",
        "Nopa - California cuisine, Western Addition",
    ],
    "new york": [
        "Di Fara Pizza - legendary Brooklyn pizza",
        "Peter Luger - classic steakhouse, Williamsburg",
        "Le Bernardin - fine French seafood, Midtown",
    ],
    "paris": [
        "Le Comptoir du Pantheon - classic bistro, Latin Quarter",
        "L'As du Fallafel - best falafel, Le Marais",
        "Bouillon Chartier - historic Parisian canteen",
    ],
    "tokyo": [
        "Tsukiji Outer Market - fresh sushi and street food",
        "Ichiran Ramen - tonkotsu ramen, Shibuya",
        "Gonpachi - yakitori and soba, Roppongi",
    ],
}


class FoodAgent:
    """Answers food and dining queries using simulated data + LLM."""

    def __init__(self) -> None:
        """Initialize the agent."""
        pass

    def process(self, query: str) -> str:
        """Answer a food-related query."""
        logger.info("FoodAgent processing: %s", query[:60])

        for city, restaurants in FOOD_DATA.items():
            if city in query.lower():
                return json.dumps(_build_food_payload(city, restaurants), indent=2)
        return json.dumps(_build_food_payload("unknown", []), indent=2)


def _build_food_payload(city: str, restaurants: list[str]) -> dict:
    """Create a structured food payload for coordinator routing."""
    items = [_split_label_and_detail(entry) for entry in restaurants[:3]]
    note = "Specialist returned curated food options." if items else "The demo has no food data for this request."
    return {
        "agent": "FoodAgent",
        "city": city,
        "kind": "food_options",
        "items": items,
        "note": note,
    }


def _split_label_and_detail(entry: str) -> dict:
    """Split a display string into name and details."""
    name, _, detail = entry.partition(" - ")
    return {"name": name, "details": detail or name}


agent_card = AgentCard(
    name="FoodAgent",
    description="Specialist for food, dining, and restaurant recommendations.",
    url=f"http://127.0.0.1:{PORT}/",
    version="1.0.0",
    capabilities=AgentCapabilities(streaming=False),
    default_input_modes=["text"],
    default_output_modes=["text"],
    skills=[
        AgentSkill(
            id="food_specialist",
            name="Food Specialist",
            description="Answer food and dining queries for travel.",
            tags=["food", "dining"],
            examples=["Best restaurants in Paris"],
        ),
    ],
)


class FoodExecutor(AgentExecutor):
    """A2A executor for Food Agent."""

    def __init__(self) -> None:
        """Initialize."""
        self._agent = FoodAgent()

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Handle A2A request."""
        user_text = context.get_user_input().strip()
        result = self._agent.process(user_text)
        await event_queue.enqueue_event(new_agent_text_message(result))

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Handle cancellation."""


def main() -> None:
    """Start the Food Agent A2A server."""
    logger.info("Starting FoodAgent on port %d", PORT)
    handler = DefaultRequestHandler(
        agent_executor=FoodExecutor(),
        task_store=InMemoryTaskStore(),
    )
    server = A2AStarletteApplication(agent_card=agent_card, http_handler=handler)
    uvicorn.run(server.build(), host="0.0.0.0", port=PORT, log_level="warning")


if __name__ == "__main__":
    main()
