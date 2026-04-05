"""Transport Finder sub-agent A2A server (used as a tool).

Lightweight agent that returns transport info for a city.
Called as a stateless tool by the Primary Agent.

Requires:
    - Ollama running at http://127.0.0.1:11434 with gemma4:e2b pulled

Port: 11422
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
logger = logging.getLogger("transport-finder-tool")

PORT = 11422

TRANSPORT_DATA = {
    "san francisco": [
        "BART - rapid transit connecting airport to downtown",
        "Muni - buses and streetcars covering the city",
        "Cable Cars - iconic transit on steep hills",
    ],
    "new york": [
        "MTA Subway - 24/7 rapid transit",
        "Yellow Cabs - metered taxis city-wide",
        "Citi Bike - bike share, 1200+ stations",
    ],
    "paris": [
        "Metro - 16 lines, Navigo pass",
        "RER - suburban trains to airports",
        "Velib - bike sharing",
    ],
    "tokyo": [
        "JR Yamanote Line - circular loop",
        "Tokyo Metro - 9 subway lines, IC card",
        "Shinkansen - bullet train for day trips",
    ],
}


class TransportFinderTool:
    """Returns transport recommendations — designed for tool-style use."""

    def __init__(self) -> None:
        """Initialize the agent."""
        pass

    def process(self, query: str) -> str:
        """Return transport recommendations."""
        logger.info("TransportFinderTool: %s", query[:60])

        for city, transport in TRANSPORT_DATA.items():
            if city in query.lower():
                return json.dumps(_build_transport_payload(city, transport), indent=2)
        return json.dumps(_build_transport_payload("unknown", []), indent=2)


def _build_transport_payload(city: str, transport: list[str]) -> dict:
    """Create a structured transport tool payload."""
    items = [_split_label_and_detail(entry) for entry in transport[:3]]
    note = "Tool returned curated transport options." if items else "No demo transport data is available for this request."
    return {
        "agent": "TransportFinderTool",
        "city": city,
        "kind": "transport_options",
        "items": items,
        "note": note,
    }


def _split_label_and_detail(entry: str) -> dict:
    """Split a display string into name and details."""
    name, _, detail = entry.partition(" - ")
    return {"name": name, "details": detail or name}


agent_card = AgentCard(
    name="TransportFinderTool",
    description="Returns transport options for a city (tool-style agent).",
    url=f"http://127.0.0.1:{PORT}/",
    version="1.0.0",
    capabilities=AgentCapabilities(streaming=False),
    default_input_modes=["text"],
    default_output_modes=["text"],
    skills=[
        AgentSkill(
            id="transport_tool",
            name="Transport Finder",
            description="Get transport options for a city.",
            tags=["transport", "tool"],
            examples=["transport in Tokyo"],
        ),
    ],
)


class TransportFinderExecutor(AgentExecutor):
    """A2A executor for Transport Finder tool agent."""

    def __init__(self) -> None:
        """Initialize."""
        self._agent = TransportFinderTool()

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Handle A2A request."""
        user_text = context.get_user_input().strip()
        result = self._agent.process(user_text)
        await event_queue.enqueue_event(new_agent_text_message(result))

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Handle cancellation."""


def main() -> None:
    """Start the Transport Finder tool agent server."""
    logger.info("Starting TransportFinderTool on port %d", PORT)
    handler = DefaultRequestHandler(
        agent_executor=TransportFinderExecutor(),
        task_store=InMemoryTaskStore(),
    )
    server = A2AStarletteApplication(agent_card=agent_card, http_handler=handler)
    uvicorn.run(server.build(), host="0.0.0.0", port=PORT, log_level="warning")


if __name__ == "__main__":
    main()
