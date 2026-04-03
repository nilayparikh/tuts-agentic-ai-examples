"""Parallel Orchestrator A2A Agent.

Fans out queries to three specialist agents concurrently, collects
their results, and forwards the combined output to the Synthesizer
agent for a unified day plan.

Port: 11305
"""

import asyncio
import json
import logging
import uuid

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
logger = logging.getLogger("parallel-orchestrator")

PORT = 11305

FINDER_AGENTS = [
    {"name": "MuseumFinder", "url": "http://127.0.0.1:11301"},
    {"name": "ConcertFinder", "url": "http://127.0.0.1:11302"},
    {"name": "RestaurantFinder", "url": "http://127.0.0.1:11303"},
]
SYNTHESIZER_URL = "http://127.0.0.1:11304"


async def call_agent(base_url: str, query: str, agent_name: str) -> str:
    """Send a query to an A2A agent and return the text response."""
    msg_id = str(uuid.uuid4())
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "message/send",
        "params": {
            "message": {
                "role": "user",
                "parts": [{"kind": "text", "text": query}],
                "messageId": msg_id,
            }
        },
    }

    logger.info("Calling %s at %s", agent_name, base_url)
    async with httpx.AsyncClient(timeout=90.0) as client:
        resp = await client.post(base_url, json=payload)
        resp.raise_for_status()
        result = resp.json()

    text = _extract_text(result)
    logger.info("%s responded (length=%d)", agent_name, len(text))
    return text


def _extract_text(response: dict) -> str:
    """Extract text content from an A2A JSON-RPC response."""
    result = response.get("result", {})

    # Check for message-style response (kind: message)
    if isinstance(result, dict) and result.get("kind") == "message":
        parts = result.get("parts", [])
        if parts:
            return parts[0].get("text", "")

    # Check artifacts
    for artifact in result.get("artifacts", []):
        for part in artifact.get("parts", []):
            text = part.get("text", "")
            if text:
                return text

    # Fall back to status message
    status = result.get("status", {})
    msg = status.get("message", {})
    if isinstance(msg, dict):
        parts = msg.get("parts", [])
        if parts:
            return parts[0].get("text", "")

    return json.dumps(response)


class ParallelOrchestrator:
    """Orchestrator that fans out to finders in parallel, then synthesizes."""

    async def process(self, query: str) -> str:
        """Execute the parallel fan-out and synthesis pipeline."""
        logger.info("Starting parallel fan-out for: %s", query[:80])

        # Fan out to all finders concurrently
        tasks = [
            call_agent(agent["url"], query, agent["name"])
            for agent in FINDER_AGENTS
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Collect results, handling any failures
        combined_results = {}
        for agent, result in zip(FINDER_AGENTS, results):
            if isinstance(result, Exception):
                logger.error("%s failed: %s", agent["name"], result)
                combined_results[agent["name"]] = {
                    "agent": agent["name"],
                    "items": [],
                    "note": "Could not retrieve results.",
                }
            else:
                combined_results[agent["name"]] = _parse_json_payload(result)

        combined_text = json.dumps(
            {
                "original_query": query,
                "results": combined_results,
            },
            indent=2,
        )
        logger.info(
            "All finders complete. Combined length=%d. Sending to Synthesizer.",
            len(combined_text),
        )

        synthesized = await call_agent(
            SYNTHESIZER_URL, combined_text, "Synthesizer",
        )
        return synthesized


def _parse_json_payload(payload: str) -> dict:
    """Parse one specialist JSON payload."""
    try:
        parsed = json.loads(payload)
    except json.JSONDecodeError:
        return {"raw": payload, "items": [], "note": "Agent returned non-JSON text."}
    return parsed if isinstance(parsed, dict) else {"raw": payload, "items": []}


# ---------------------------------------------------------------------------
# A2A server wiring
# ---------------------------------------------------------------------------

agent_card = AgentCard(
    name="ParallelOrchestrator",
    description=(
        "Orchestrates parallel lookups across museum, concert, and restaurant "
        "finders, then synthesizes results into a day plan."
    ),
    url=f"http://127.0.0.1:{PORT}/",
    version="1.0.0",
    capabilities=AgentCapabilities(streaming=False),
    default_input_modes=["text"],
    default_output_modes=["text"],
    skills=[
        AgentSkill(
            id="parallel_planning",
            name="Parallel City Planning",
            description="Plan a city visit using parallel specialist agents.",
            tags=["planning", "parallel", "orchestration"],
            examples=["Plan a day in San Francisco with museums, concerts, and food"],
        ),
    ],
)


class ParallelOrchestratorExecutor(AgentExecutor):
    """A2A executor for the ParallelOrchestrator."""

    def __init__(self) -> None:
        """Initialize the orchestrator."""
        self._orchestrator = ParallelOrchestrator()

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Handle an A2A request."""
        user_text = context.get_user_input().strip()
        logger.info("A2A request: %s", user_text[:80])
        result = await self._orchestrator.process(user_text)
        await event_queue.enqueue_event(new_agent_text_message(result))

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Handle cancellation."""
        logger.info("Request cancelled")


def main() -> None:
    """Start the A2A orchestrator server."""
    logger.info("Starting ParallelOrchestrator on port %d", PORT)
    handler = DefaultRequestHandler(
        agent_executor=ParallelOrchestratorExecutor(),
        task_store=InMemoryTaskStore(),
    )
    server = A2AStarletteApplication(agent_card=agent_card, http_handler=handler)
    uvicorn.run(server.build(), host="0.0.0.0", port=PORT, log_level="warning")


if __name__ == "__main__":
    main()
