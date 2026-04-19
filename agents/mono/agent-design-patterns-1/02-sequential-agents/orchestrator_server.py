"""Sequential Orchestrator A2A Server.

Chains the Food Finder and Transport agents in a fixed order:
  Step 1: Food Finder  ->  Step 2: Transport Agent

The output of Step 1 is injected as context into Step 2,
demonstrating deterministic sequential execution via A2A.

Port: 11203
"""

import json
import logging

import httpx
import uvicorn

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.apps import A2AStarletteApplication
from a2a.server.events import EventQueue
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from a2a.utils import new_agent_text_message

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")
logger = logging.getLogger("orchestrator")

PORT = 11203

PIPELINE = [
    {"name": "FoodFinder", "port": 11201},
    {"name": "TransportAgent", "port": 11202},
]


async def call_agent(name: str, port: int, payload: str) -> str:
    """Send a message to an A2A agent and return the text response."""
    url = f"http://127.0.0.1:{port}/"
    rpc_request = {
        "jsonrpc": "2.0",
        "id": f"seq-{name}",
        "method": "message/send",
        "params": {
            "message": {
                "role": "user",
                "parts": [{"kind": "text", "text": payload}],
                "messageId": f"msg-{name}",
            }
        },
    }

    logger.info("Calling %s on port %d...", name, port)
    async with httpx.AsyncClient(timeout=120.0) as client:
        resp = await client.post(url, json=rpc_request)
        rpc_response = resp.json()

    result = rpc_response.get("result", {})
    text = _extract_text(result)
    logger.info("%s responded: %d chars", name, len(text))
    return text


def _extract_text(result: dict) -> str:
    """Extract text from an A2A response result."""
    if isinstance(result, dict):
        if result.get("kind") == "message":
            parts = result.get("parts", [])
            return parts[0].get("text", "") if parts else ""
        artifacts = result.get("artifacts", [])
        if artifacts:
            parts = artifacts[0].get("parts", [])
            return parts[0].get("text", "") if parts else ""
        status = result.get("status", {})
        msg = status.get("message", {})
        if isinstance(msg, dict):
            parts = msg.get("parts", [])
            return parts[0].get("text", "") if parts else ""
    return json.dumps(result)


class SequentialOrchestrator:
    """Runs agents in a fixed sequential order, passing output as context."""

    async def process(self, user_query: str) -> str:
        """Execute the sequential pipeline."""
        logger.info("Sequential pipeline start: %s", user_query[:60])

        # Step 1: Food Finder
        logger.info("STEP 1/2: Calling FoodFinder...")
        food_result = await call_agent("FoodFinder", 11201, user_query)
        food_payload = _parse_json_payload(food_result)
        logger.info("FoodFinder result: %d chars", len(food_result))

        # Step 2: Transport Agent — inject food context into the query
        logger.info("STEP 2/2: Calling TransportAgent with food context...")
        transport_query = json.dumps(
            {
                "original_query": user_query,
                "food_result": food_payload,
            },
            indent=2,
        )
        transport_result = await call_agent(
            "TransportAgent", 11202, transport_query,
        )
        transport_payload = _parse_json_payload(transport_result)
        logger.info("TransportAgent result: %d chars", len(transport_result))

        combined = _format_trip_plan(user_query, food_payload, transport_payload)

        logger.info("Sequential pipeline complete")
        return combined


def _parse_json_payload(payload: str) -> dict:
    """Parse a JSON payload from a specialist agent."""
    try:
        parsed = json.loads(payload)
    except json.JSONDecodeError:
        return {"raw": payload, "items": [], "note": "Agent returned non-JSON text."}
    return parsed if isinstance(parsed, dict) else {"raw": payload, "items": []}


def _format_food_item(item: dict) -> str:
    """Format one structured food item."""
    return f"{item.get('name', 'Unknown')} ({item.get('cuisine', 'Unknown')}, {item.get('area', 'Unknown')})"


def _format_trip_plan(user_query: str, food_payload: dict, transport_payload: dict) -> str:
    """Render a richer sequential trip plan from structured payloads."""
    food_items = food_payload.get("items", [])
    transport_items = transport_payload.get("items", [])
    lines = [
        "TRIP PLAN (Sequential Pipeline)",
        "=" * 40,
        f"Request: {user_query}",
        "",
        f"City: {str(food_payload.get('city', 'unknown')).title()}",
        "",
        "STEP 1 - Food Recommendations:",
    ]
    if food_items:
        for item in food_items:
            lines.append(f"- {_format_food_item(item)}")
        lines.append(f"Note: {food_payload.get('note', '')}")
    else:
        lines.append(f"- {food_payload.get('note', 'Food data unavailable.')}")

    lines.extend(["", "STEP 2 - Transport Plan:"])
    if transport_items:
        for item in transport_items:
            lines.append(f"- {item}")
        lines.append(f"Tip: {transport_payload.get('tip', 'No transport tip available.')}")
    else:
        lines.append(f"- {transport_payload.get('tip', 'Transport data unavailable.')}")

    return "\n".join(lines)


# A2A server setup
agent_card = AgentCard(
    name="SequentialOrchestrator",
    description="Chains Food Finder and Transport agents in sequence.",
    url=f"http://127.0.0.1:{PORT}/",
    version="1.0.0",
    capabilities=AgentCapabilities(streaming=False),
    default_input_modes=["text"],
    default_output_modes=["text"],
    skills=[
        AgentSkill(
            id="sequential_trip",
            name="Sequential Trip Planning",
            description="Plan a trip with food first, then transport.",
            tags=["travel", "sequential"],
            examples=["Plan a trip to San Francisco"],
        ),
    ],
)


class SequentialExecutor(AgentExecutor):
    """A2A executor for the sequential orchestrator."""

    def __init__(self) -> None:
        """Initialize."""
        self._orchestrator = SequentialOrchestrator()

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Handle A2A request."""
        user_text = context.get_user_input().strip()
        result = await self._orchestrator.process(user_text)
        await event_queue.enqueue_event(new_agent_text_message(result))

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Handle cancellation."""


def main() -> None:
    """Start the Sequential Orchestrator A2A server."""
    logger.info("Starting SequentialOrchestrator on port %d", PORT)
    handler = DefaultRequestHandler(
        agent_executor=SequentialExecutor(),
        task_store=InMemoryTaskStore(),
    )
    server = A2AStarletteApplication(agent_card=agent_card, http_handler=handler)
    uvicorn.run(server.build(), host="0.0.0.0", port=PORT, log_level="warning")


if __name__ == "__main__":
    main()
