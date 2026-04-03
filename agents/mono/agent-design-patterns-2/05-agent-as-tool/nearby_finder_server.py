"""Nearby Finder sub-agent A2A server (used as a tool).

Lightweight agent that returns nearby attractions for a city.
Called as a stateless tool by the Primary Agent.

Requires:
    - Ollama running at http://127.0.0.1:11434 with gemma4:e2b pulled

Port: 11423
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
logger = logging.getLogger("nearby-finder-tool")

PORT = 11423

ATTRACTION_DATA = {
    "san francisco": [
        "Golden Gate Bridge - iconic suspension bridge",
        "Alcatraz Island - historic penitentiary",
        "Fisherman's Wharf - waterfront dining and shops",
    ],
    "new york": [
        "Statue of Liberty - symbol of freedom",
        "Central Park - 843-acre urban park",
        "Times Square - entertainment hub",
    ],
    "paris": [
        "Eiffel Tower - iconic landmark",
        "Louvre Museum - world's largest art museum",
        "Notre-Dame Cathedral - Gothic masterpiece",
    ],
    "tokyo": [
        "Senso-ji Temple - oldest temple in Tokyo",
        "Shibuya Crossing - world's busiest intersection",
        "Meiji Shrine - Shinto shrine in Harajuku",
    ],
}


class NearbyFinderTool:
    """Returns nearby attractions — designed for tool-style use."""

    def __init__(self) -> None:
        """Initialize the agent."""
        pass

    def process(self, query: str) -> str:
        """Return nearby attraction recommendations."""
        logger.info("NearbyFinderTool: %s", query[:60])

        for city, attractions in ATTRACTION_DATA.items():
            if city in query.lower():
                return json.dumps(_build_attraction_payload(city, attractions), indent=2)
        return json.dumps(_build_attraction_payload("unknown", []), indent=2)


def _build_attraction_payload(city: str, attractions: list[str]) -> dict:
    """Create a structured nearby-attractions payload."""
    items = [_split_label_and_detail(entry) for entry in attractions[:3]]
    note = "Tool returned curated attractions." if items else "No demo attraction data is available for this request."
    return {
        "agent": "NearbyFinderTool",
        "city": city,
        "kind": "attraction_options",
        "items": items,
        "note": note,
    }


def _split_label_and_detail(entry: str) -> dict:
    """Split a display string into name and details."""
    name, _, detail = entry.partition(" - ")
    return {"name": name, "details": detail or name}


agent_card = AgentCard(
    name="NearbyFinderTool",
    description="Returns nearby attractions for a city (tool-style agent).",
    url=f"http://127.0.0.1:{PORT}/",
    version="1.0.0",
    capabilities=AgentCapabilities(streaming=False),
    default_input_modes=["text"],
    default_output_modes=["text"],
    skills=[
        AgentSkill(
            id="nearby_tool",
            name="Nearby Finder",
            description="Get top attractions for a city.",
            tags=["attractions", "tool"],
            examples=["attractions in Paris"],
        ),
    ],
)


class NearbyFinderExecutor(AgentExecutor):
    """A2A executor for Nearby Finder tool agent."""

    def __init__(self) -> None:
        """Initialize."""
        self._agent = NearbyFinderTool()

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Handle A2A request."""
        user_text = context.get_user_input().strip()
        result = self._agent.process(user_text)
        await event_queue.enqueue_event(new_agent_text_message(result))

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Handle cancellation."""


def main() -> None:
    """Start the Nearby Finder tool agent server."""
    logger.info("Starting NearbyFinderTool on port %d", PORT)
    handler = DefaultRequestHandler(
        agent_executor=NearbyFinderExecutor(),
        task_store=InMemoryTaskStore(),
    )
    server = A2AStarletteApplication(agent_card=agent_card, http_handler=handler)
    uvicorn.run(server.build(), host="0.0.0.0", port=PORT, log_level="warning")


if __name__ == "__main__":
    main()
