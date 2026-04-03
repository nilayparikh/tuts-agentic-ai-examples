"""Concert Finder A2A Agent -- parallel specialist.

Searches for concerts and live music events in a given city.

Port: 11302
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
logger = logging.getLogger("concert-finder")

PORT = 11302

# Simulated concert/event data
CONCERT_DATA = {
    "san francisco": [
        {"name": "Jazz at The Fillmore", "genre": "Jazz", "venue": "The Fillmore"},
        {"name": "SF Symphony Gala", "genre": "Classical", "venue": "Davies Hall"},
        {"name": "Indie Night at Bottom of the Hill", "genre": "Indie Rock", "venue": "Bottom of the Hill"},
    ],
    "new york": [
        {"name": "Broadway Show - Hamilton", "genre": "Musical", "venue": "Richard Rodgers Theatre"},
        {"name": "Jazz at Blue Note", "genre": "Jazz", "venue": "Blue Note"},
        {"name": "Philharmonic Concert", "genre": "Classical", "venue": "Lincoln Center"},
    ],
    "paris": [
        {"name": "Opera at Palais Garnier", "genre": "Opera", "venue": "Palais Garnier"},
        {"name": "Jazz at Le Duc des Lombards", "genre": "Jazz", "venue": "Le Duc des Lombards"},
        {"name": "Chanson Night", "genre": "French Pop", "venue": "Olympia"},
    ],
    "tokyo": [
        {"name": "J-Pop Live at Budokan", "genre": "J-Pop", "venue": "Nippon Budokan"},
        {"name": "Jazz at Blue Note Tokyo", "genre": "Jazz", "venue": "Blue Note Tokyo"},
        {"name": "Traditional Taiko Drums", "genre": "Traditional", "venue": "National Theatre"},
    ],
}


class ConcertFinderAgent:
    """Finds concerts and live music events in a city."""

    def __init__(self) -> None:
        """Initialize the agent."""
        pass

    def process(self, query: str) -> str:
        """Find concerts based on the query."""
        logger.info("Processing query: %s", query[:80])

        city_key = _extract_city(query)
        concerts = CONCERT_DATA.get(city_key, [])
        logger.info("Found %d events for '%s'", len(concerts), city_key)
        answer = json.dumps(_build_concert_payload(city_key, concerts), indent=2)
        logger.info("Response generated (length=%d)", len(answer))
        return answer


def _build_concert_payload(city_key: str, concerts: list[dict]) -> dict:
    """Create a structured concert payload."""
    if not city_key or not concerts:
        return {
            "agent": "ConcertFinder",
            "city": city_key or "unknown",
            "kind": "concert_options",
            "items": [],
            "note": "Concert data is unavailable in this demo for the requested city.",
        }

    return {
        "agent": "ConcertFinder",
        "city": city_key,
        "kind": "concert_options",
        "items": concerts[:3],
        "note": "Use the live event as the evening anchor.",
    }


def _extract_city(text: str) -> str:
    """Extract a known city name from text (case-insensitive)."""
    lower = text.lower()
    for city in CONCERT_DATA:
        if city in lower:
            return city
    return "unknown"


# ---------------------------------------------------------------------------
# A2A server wiring
# ---------------------------------------------------------------------------

agent_card = AgentCard(
    name="ConcertFinderAgent",
    description="Finds concerts and live music events in a city.",
    url=f"http://127.0.0.1:{PORT}/",
    version="1.0.0",
    capabilities=AgentCapabilities(streaming=False),
    default_input_modes=["text"],
    default_output_modes=["text"],
    skills=[
        AgentSkill(
            id="concert_search",
            name="Concert Search",
            description="Find concerts and live events in any city.",
            tags=["concerts", "music", "events"],
            examples=["Find concerts in New York"],
        ),
    ],
)


class ConcertFinderExecutor(AgentExecutor):
    """A2A executor for ConcertFinderAgent."""

    def __init__(self) -> None:
        """Initialize the agent."""
        self._agent = ConcertFinderAgent()

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
    logger.info("Starting ConcertFinderAgent on port %d", PORT)
    handler = DefaultRequestHandler(
        agent_executor=ConcertFinderExecutor(),
        task_store=InMemoryTaskStore(),
    )
    server = A2AStarletteApplication(agent_card=agent_card, http_handler=handler)
    uvicorn.run(server.build(), host="0.0.0.0", port=PORT, log_level="warning")


if __name__ == "__main__":
    main()
