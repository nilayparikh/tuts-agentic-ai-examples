"""Museum Finder A2A Agent -- parallel specialist.

Searches for museums and galleries in a given city.

Port: 11301
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
logger = logging.getLogger("museum-finder")

PORT = 11301

# Simulated museum data
MUSEUM_DATA = {
    "san francisco": [
        {"name": "SFMOMA", "type": "Modern art", "area": "SoMa"},
        {"name": "de Young Museum", "type": "Fine arts", "area": "Golden Gate Park"},
        {"name": "Exploratorium", "type": "Science", "area": "Embarcadero"},
    ],
    "new york": [
        {"name": "The Met", "type": "Encyclopedic", "area": "Upper East Side"},
        {"name": "MoMA", "type": "Modern art", "area": "Midtown"},
        {"name": "Guggenheim", "type": "Modern/Contemporary", "area": "Upper East Side"},
    ],
    "paris": [
        {"name": "Louvre", "type": "Encyclopedic", "area": "1st arrondissement"},
        {"name": "Musee d'Orsay", "type": "Impressionist", "area": "7th arrondissement"},
        {"name": "Centre Pompidou", "type": "Modern art", "area": "4th arrondissement"},
    ],
    "tokyo": [
        {"name": "Tokyo National Museum", "type": "Japanese art", "area": "Ueno"},
        {"name": "teamLab Borderless", "type": "Digital art", "area": "Odaiba"},
        {"name": "Mori Art Museum", "type": "Contemporary", "area": "Roppongi"},
    ],
}


class MuseumFinderAgent:
    """Finds museums and galleries in a city using LLM and simulated data."""

    def __init__(self) -> None:
        """Initialize the agent."""
        pass

    def process(self, query: str) -> str:
        """Find museums based on the query."""
        logger.info("Processing query: %s", query[:80])

        # Extract city from query via simple keyword matching
        city_key = _extract_city(query)
        museums = MUSEUM_DATA.get(city_key, [])
        logger.info("Found %d museums for '%s'", len(museums), city_key)
        answer = json.dumps(_build_museum_payload(city_key, museums), indent=2)
        logger.info("Response generated (length=%d)", len(answer))
        return answer


def _build_museum_payload(city_key: str, museums: list[dict]) -> dict:
    """Create a structured museum payload."""
    if not city_key or not museums:
        return {
            "agent": "MuseumFinder",
            "city": city_key or "unknown",
            "kind": "museum_options",
            "items": [],
            "note": "Museum data is unavailable in this demo for the requested city.",
        }

    return {
        "agent": "MuseumFinder",
        "city": city_key,
        "kind": "museum_options",
        "items": museums[:3],
        "note": "Start the day with a culture stop near the listed area.",
    }


def _extract_city(text: str) -> str:
    """Extract a known city name from text (case-insensitive)."""
    lower = text.lower()
    for city in MUSEUM_DATA:
        if city in lower:
            return city
    return "unknown"


# ---------------------------------------------------------------------------
# A2A server wiring
# ---------------------------------------------------------------------------

agent_card = AgentCard(
    name="MuseumFinderAgent",
    description="Finds museums and galleries in a city.",
    url=f"http://127.0.0.1:{PORT}/",
    version="1.0.0",
    capabilities=AgentCapabilities(streaming=False),
    default_input_modes=["text"],
    default_output_modes=["text"],
    skills=[
        AgentSkill(
            id="museum_search",
            name="Museum Search",
            description="Find museums and galleries in any city.",
            tags=["museums", "culture"],
            examples=["Find museums in Paris"],
        ),
    ],
)


class MuseumFinderExecutor(AgentExecutor):
    """A2A executor for MuseumFinderAgent."""

    def __init__(self) -> None:
        """Initialize the agent."""
        self._agent = MuseumFinderAgent()

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
    logger.info("Starting MuseumFinderAgent on port %d", PORT)
    handler = DefaultRequestHandler(
        agent_executor=MuseumFinderExecutor(),
        task_store=InMemoryTaskStore(),
    )
    server = A2AStarletteApplication(agent_card=agent_card, http_handler=handler)
    uvicorn.run(server.build(), host="0.0.0.0", port=PORT, log_level="warning")


if __name__ == "__main__":
    main()
