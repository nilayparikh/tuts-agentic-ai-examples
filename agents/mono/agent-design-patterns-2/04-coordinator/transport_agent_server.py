"""Transport Agent A2A server — handles transport queries.

Specialist agent for the Coordinator pattern. Answers transport
and getting-around queries for any city.

Requires:
    - Ollama running at http://127.0.0.1:11434 with gemma4:e2b pulled

Port: 11412
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
logger = logging.getLogger("transport-agent")

PORT = 11412

TRANSPORT_DATA = {
    "san francisco": [
        "BART - rapid transit connecting airport to downtown",
        "Muni - buses and streetcars covering the city",
        "Cable Cars - iconic transit on steep hills",
    ],
    "new york": [
        "MTA Subway - 24/7 rapid transit, MetroCard or OMNY",
        "Yellow Cabs - metered taxis across the city",
        "Citi Bike - bike share, 1200+ stations",
    ],
    "paris": [
        "Metro - 16 lines covering entire city, Navigo pass",
        "RER - suburban trains to airports and outskirts",
        "Velib - public bike sharing system",
    ],
    "tokyo": [
        "JR Yamanote Line - circular loop connecting major stations",
        "Tokyo Metro - 9 subway lines, IC card (Suica/Pasmo)",
        "Shinkansen - bullet train for day trips from Tokyo Station",
    ],
}


class TransportAgent:
    """Answers transport and getting-around queries using simulated data + LLM."""

    def __init__(self) -> None:
        """Initialize the agent."""
        pass

    def process(self, query: str) -> str:
        """Answer a transport-related query."""
        logger.info("TransportAgent processing: %s", query[:60])

        for city, transport in TRANSPORT_DATA.items():
            if city in query.lower():
                return json.dumps(_build_transport_payload(city, transport), indent=2)
        return json.dumps(_build_transport_payload("unknown", []), indent=2)


def _build_transport_payload(city: str, transport: list[str]) -> dict:
    """Create a structured transport payload for coordinator routing."""
    items = [_split_label_and_detail(entry) for entry in transport[:3]]
    note = "Specialist returned curated transport options." if items else "The demo has no transport data for this request."
    return {
        "agent": "TransportAgent",
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
    name="TransportAgent",
    description="Specialist for transport, transit, and getting-around advice.",
    url=f"http://127.0.0.1:{PORT}/",
    version="1.0.0",
    capabilities=AgentCapabilities(streaming=False),
    default_input_modes=["text"],
    default_output_modes=["text"],
    skills=[
        AgentSkill(
            id="transport_specialist",
            name="Transport Specialist",
            description="Answer transport and transit queries for travel.",
            tags=["transport", "transit"],
            examples=["How to get around Tokyo"],
        ),
    ],
)


class TransportExecutor(AgentExecutor):
    """A2A executor for Transport Agent."""

    def __init__(self) -> None:
        """Initialize."""
        self._agent = TransportAgent()

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Handle A2A request."""
        user_text = context.get_user_input().strip()
        result = self._agent.process(user_text)
        await event_queue.enqueue_event(new_agent_text_message(result))

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Handle cancellation."""


def main() -> None:
    """Start the Transport Agent A2A server."""
    logger.info("Starting TransportAgent on port %d", PORT)
    handler = DefaultRequestHandler(
        agent_executor=TransportExecutor(),
        task_store=InMemoryTaskStore(),
    )
    server = A2AStarletteApplication(agent_card=agent_card, http_handler=handler)
    uvicorn.run(server.build(), host="0.0.0.0", port=PORT, log_level="warning")


if __name__ == "__main__":
    main()
