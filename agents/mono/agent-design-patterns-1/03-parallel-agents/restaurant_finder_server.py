"""Restaurant Finder A2A Agent -- parallel specialist.

Searches for restaurants and dining options in a given city.

Port: 11303
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
logger = logging.getLogger("restaurant-finder")

PORT = 11303

# Simulated restaurant data
RESTAURANT_DATA = {
    "san francisco": [
        {"name": "Tartine Bakery", "cuisine": "French bakery", "area": "Mission"},
        {"name": "Swan Oyster Depot", "cuisine": "Seafood", "area": "Nob Hill"},
        {"name": "Nopa", "cuisine": "California", "area": "Western Addition"},
        {"name": "Zuni Cafe", "cuisine": "Mediterranean", "area": "Hayes Valley"},
    ],
    "new york": [
        {"name": "Di Fara Pizza", "cuisine": "Italian", "area": "Brooklyn"},
        {"name": "Peter Luger", "cuisine": "Steakhouse", "area": "Williamsburg"},
        {"name": "Le Bernardin", "cuisine": "French seafood", "area": "Midtown"},
        {"name": "Xi'an Famous Foods", "cuisine": "Chinese", "area": "Multiple"},
    ],
    "paris": [
        {"name": "Le Comptoir du Pantheon", "cuisine": "French bistro", "area": "Latin Quarter"},
        {"name": "L'As du Fallafel", "cuisine": "Middle Eastern", "area": "Le Marais"},
        {"name": "Bouillon Chartier", "cuisine": "Traditional French", "area": "Grands Boulevards"},
        {"name": "Pink Mamma", "cuisine": "Italian", "area": "Oberkampf"},
    ],
    "tokyo": [
        {"name": "Sukiyabashi Jiro", "cuisine": "Sushi", "area": "Ginza"},
        {"name": "Ichiran Ramen", "cuisine": "Ramen", "area": "Shibuya"},
        {"name": "Tsukiji Outer Market", "cuisine": "Street food", "area": "Tsukiji"},
        {"name": "Gonpachi", "cuisine": "Izakaya", "area": "Roppongi"},
    ],
}


class RestaurantFinderAgent:
    """Finds restaurants and dining options in a city."""

    def __init__(self) -> None:
        """Initialize the agent."""
        pass

    def process(self, query: str) -> str:
        """Find restaurants based on the query."""
        logger.info("Processing query: %s", query[:80])

        city_key = _extract_city(query)
        restaurants = RESTAURANT_DATA.get(city_key, [])
        logger.info("Found %d restaurants for '%s'", len(restaurants), city_key)
        answer = json.dumps(_build_restaurant_payload(city_key, restaurants), indent=2)
        logger.info("Response generated (length=%d)", len(answer))
        return answer


def _build_restaurant_payload(city_key: str, restaurants: list[dict]) -> dict:
    """Create a structured restaurant payload."""
    if not city_key or not restaurants:
        return {
            "agent": "RestaurantFinder",
            "city": city_key or "unknown",
            "kind": "restaurant_options",
            "items": [],
            "note": "Restaurant data is unavailable in this demo for the requested city.",
        }

    return {
        "agent": "RestaurantFinder",
        "city": city_key,
        "kind": "restaurant_options",
        "items": restaurants[:3],
        "note": "Use the food stop as the afternoon break between activities.",
    }


def _extract_city(text: str) -> str:
    """Extract a known city name from text (case-insensitive)."""
    lower = text.lower()
    for city in RESTAURANT_DATA:
        if city in lower:
            return city
    return "unknown"


# ---------------------------------------------------------------------------
# A2A server wiring
# ---------------------------------------------------------------------------

agent_card = AgentCard(
    name="RestaurantFinderAgent",
    description="Finds restaurants and dining options in a city.",
    url=f"http://127.0.0.1:{PORT}/",
    version="1.0.0",
    capabilities=AgentCapabilities(streaming=False),
    default_input_modes=["text"],
    default_output_modes=["text"],
    skills=[
        AgentSkill(
            id="restaurant_search",
            name="Restaurant Search",
            description="Find restaurants and dining in any city.",
            tags=["restaurants", "food", "dining"],
            examples=["Find restaurants in Tokyo"],
        ),
    ],
)


class RestaurantFinderExecutor(AgentExecutor):
    """A2A executor for RestaurantFinderAgent."""

    def __init__(self) -> None:
        """Initialize the agent."""
        self._agent = RestaurantFinderAgent()

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Handle an A2A request."""
        user_text = context.get_user_input().strip()
        logger.info("A2A request: %s", user_text[:80])
        result = self._agent.process(user_text)
        await event_queue.enqueue_event(new_agent_text_message(result))

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Handle cancellation."""
        logger.info("Request cancelled")


def main() -> None:
    """Start the A2A agent server."""
    logger.info("Starting RestaurantFinderAgent on port %d", PORT)
    handler = DefaultRequestHandler(
        agent_executor=RestaurantFinderExecutor(),
        task_store=InMemoryTaskStore(),
    )
    server = A2AStarletteApplication(agent_card=agent_card, http_handler=handler)
    uvicorn.run(server.build(), host="0.0.0.0", port=PORT, log_level="warning")


if __name__ == "__main__":
    main()
