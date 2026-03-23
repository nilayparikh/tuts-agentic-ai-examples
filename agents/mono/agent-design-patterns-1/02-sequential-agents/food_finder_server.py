"""Food Finder A2A Agent -- Step 1 in the sequential pipeline.

Searches for restaurants and food options in a given city.
Its output is passed to the Transport Agent as context.

Port: 11201
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
logger = logging.getLogger("food-finder")

PORT = 11201

# Simulated food data
FOOD_DATA = {
    "san francisco": [
        {"name": "Tartine Bakery", "cuisine": "French bakery", "area": "Mission District"},
        {"name": "Swan Oyster Depot", "cuisine": "Seafood", "area": "Nob Hill"},
        {"name": "Nopa", "cuisine": "California", "area": "Western Addition"},
        {"name": "Marufuku Ramen", "cuisine": "Japanese", "area": "Japantown"},
    ],
    "new york": [
        {"name": "Di Fara Pizza", "cuisine": "Italian", "area": "Brooklyn"},
        {"name": "Peter Luger", "cuisine": "Steakhouse", "area": "Williamsburg"},
        {"name": "Le Bernardin", "cuisine": "French seafood", "area": "Midtown"},
    ],
    "tokyo": [
        {"name": "Sukiyabashi Jiro", "cuisine": "Sushi", "area": "Ginza"},
        {"name": "Ichiran Ramen", "cuisine": "Ramen", "area": "Shibuya"},
        {"name": "Tsukiji Outer Market", "cuisine": "Street food", "area": "Tsukiji"},
        {"name": "Gonpachi", "cuisine": "Izakaya", "area": "Roppongi"},
    ],
    "paris": [
        {"name": "Le Comptoir du Pantheon", "cuisine": "French bistro", "area": "Latin Quarter"},
        {"name": "L'As du Fallafel", "cuisine": "Middle Eastern", "area": "Le Marais"},
        {"name": "Bouillon Chartier", "cuisine": "Traditional French", "area": "Grands Boulevards"},
    ],
}


class FoodFinderAgent:
    """Find restaurants and food options for a city."""

    def __init__(self) -> None:
        """Initialize the agent."""
        pass

    def find_food(self, query: str) -> str:
        """Search for food options based on the query."""
        logger.info("Food search for: %s", query[:60])

        # Extract city from query
        city_key = ""
        for city in FOOD_DATA:
            if city in query.lower():
                city_key = city
                break

        restaurants = FOOD_DATA.get(city_key, [])
        result = _build_food_payload(city_key, restaurants)
        payload = json.dumps(result, indent=2)
        logger.info("Food results: %d chars", len(payload))
        return payload


def _build_food_payload(city_key: str, restaurants: list[dict]) -> dict:
    """Create a structured food payload from demo data."""
    if not city_key or not restaurants:
        return {
            "agent": "FoodFinder",
            "city": city_key or "unknown",
            "kind": "food_options",
            "items": [],
            "note": "The demo has no matching restaurant data for this request.",
        }

    return {
        "agent": "FoodFinder",
        "city": city_key,
        "kind": "food_options",
        "items": restaurants[:3],
        "note": "Choose one stop based on cuisine and neighborhood.",
    }


# A2A server setup
agent_card = AgentCard(
    name="FoodFinderAgent",
    description="Finds restaurants and food options for trip planning.",
    url=f"http://localhost:{PORT}/",
    version="1.0.0",
    capabilities=AgentCapabilities(streaming=False),
    default_input_modes=["text"],
    default_output_modes=["text"],
    skills=[
        AgentSkill(
            id="food_search",
            name="Food Search",
            description="Search for restaurants and food options in a city.",
            tags=["food", "restaurants"],
            examples=["Find restaurants in San Francisco"],
        ),
    ],
)


class FoodFinderExecutor(AgentExecutor):
    """A2A executor for the FoodFinderAgent."""

    def __init__(self) -> None:
        """Initialize."""
        self._agent = FoodFinderAgent()

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Handle A2A request."""
        user_text = context.get_user_input().strip()
        result = self._agent.find_food(user_text)
        await event_queue.enqueue_event(new_agent_text_message(result))

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Handle cancellation."""


def main() -> None:
    """Start the Food Finder A2A server."""
    logger.info("Starting FoodFinderAgent on port %d", PORT)
    handler = DefaultRequestHandler(
        agent_executor=FoodFinderExecutor(),
        task_store=InMemoryTaskStore(),
    )
    server = A2AStarletteApplication(agent_card=agent_card, http_handler=handler)
    uvicorn.run(server.build(), host="0.0.0.0", port=PORT, log_level="warning")


if __name__ == "__main__":
    main()
