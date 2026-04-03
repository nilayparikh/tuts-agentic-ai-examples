"""Transport Agent A2A Server -- Step 2 in the sequential pipeline.

Receives food recommendations from Step 1 and plans transportation
to visit those locations. Demonstrates how sequential agents share
context through chained output.

Port: 11202
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
logger = logging.getLogger("transport")

PORT = 11202

# Simulated transport data
TRANSPORT_DATA = {
    "san francisco": {
        "options": ["BART rapid transit", "Muni bus/streetcar", "Cable cars", "Uber/Lyft"],
        "tips": "BART is fastest for airport. Cable cars for tourist areas.",
    },
    "new york": {
        "options": ["Subway (MTA)", "Yellow cabs", "NYC Ferry", "Citi Bike"],
        "tips": "Subway is fastest. Get a MetroCard for unlimited rides.",
    },
    "tokyo": {
        "options": ["JR Yamanote Line", "Tokyo Metro", "Taxi", "Suica/Pasmo card"],
        "tips": "Get a Suica card at any station. Yamanote Line circles the city.",
    },
    "paris": {
        "options": ["Metro", "RER trains", "Bus", "Velib bikes"],
        "tips": "Metro is fastest. Buy a carnet of 10 tickets for savings.",
    },
}


class TransportAgent:
    """Plan transportation based on food locations from the previous step."""

    def __init__(self) -> None:
        """Initialize the agent."""
        pass

    def plan_transport(self, query: str) -> str:
        """Create a transport plan from the query and context."""
        logger.info("Transport planning: %s", query[:80])

        request_data = _parse_request_payload(query)
        city_key = request_data.get("city", "unknown")
        transport = TRANSPORT_DATA.get(city_key)
        answer = json.dumps(
            _build_transport_payload(city_key, transport),
            indent=2,
        )

        logger.info("Transport plan: %d chars", len(answer))
        return answer


def _build_transport_payload(city_key: str, transport: dict | None) -> dict:
    """Create a structured transport payload from demo data."""
    if not city_key or not transport:
        return {
            "agent": "TransportAgent",
            "city": city_key or "unknown",
            "kind": "transport_options",
            "items": [],
            "tip": "The demo has no transport data for this request.",
        }

    return {
        "agent": "TransportAgent",
        "city": city_key,
        "kind": "transport_options",
        "items": transport.get("options", [])[:3],
        "tip": transport.get("tips", ""),
    }


def _parse_request_payload(query: str) -> dict:
    """Parse sequential transport input, accepting JSON or plain text."""
    try:
        payload = json.loads(query)
    except json.JSONDecodeError:
        return {"city": _extract_city(query)}

    if not isinstance(payload, dict):
        return {"city": _extract_city(query)}

    food_result = payload.get("food_result", {})
    if isinstance(food_result, dict):
        city = str(food_result.get("city", "")).strip().lower()
        if city:
            return {"city": city}

    original_query = str(payload.get("original_query", ""))
    return {"city": _extract_city(original_query)}


def _extract_city(text: str) -> str:
    """Extract a known city name from text (case-insensitive)."""
    lower = text.lower()
    for city in TRANSPORT_DATA:
        if city in lower:
            return city
    return "unknown"


# A2A server setup
agent_card = AgentCard(
    name="TransportAgent",
    description="Plans transportation routes between food destinations.",
    url=f"http://127.0.0.1:{PORT}/",
    version="1.0.0",
    capabilities=AgentCapabilities(streaming=False),
    default_input_modes=["text"],
    default_output_modes=["text"],
    skills=[
        AgentSkill(
            id="transport_planning",
            name="Transport Planning",
            description="Plan transport routes given food/activity locations.",
            tags=["transport", "routing"],
            examples=["Plan transport for visiting restaurants in SF"],
        ),
    ],
)


class TransportExecutor(AgentExecutor):
    """A2A executor for the TransportAgent."""

    def __init__(self) -> None:
        """Initialize."""
        self._agent = TransportAgent()

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Handle A2A request."""
        user_text = context.get_user_input().strip()
        result = self._agent.plan_transport(user_text)
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
