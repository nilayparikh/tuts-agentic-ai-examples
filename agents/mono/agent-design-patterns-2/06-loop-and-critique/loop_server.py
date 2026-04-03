"""Loop Orchestrator A2A server — iterative refinement.

Implements the Loop & Critique pattern:
  1. Send query to Generator -> get draft plan
  2. Send plan to Critic -> get feedback
  3. If Critic says PASS, return the plan
  4. Otherwise, send feedback + original query back to Generator
  5. Repeat up to MAX_ITERATIONS times

Requires:
    - GeneratorAgent running on port 11401
    - CriticAgent running on port 11402

Port: 11403
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
logger = logging.getLogger("loop-orchestrator")

PORT = 11403
MAX_ITERATIONS = 3

GENERATOR_PORT = 11401
CRITIC_PORT = 11402


async def call_agent(name: str, port: int, payload: str) -> str:
    """Send a message to an A2A agent and return the text response."""
    url = f"http://127.0.0.1:{port}/"
    rpc_request = {
        "jsonrpc": "2.0",
        "id": f"loop-{name}",
        "method": "message/send",
        "params": {
            "message": {
                "role": "user",
                "parts": [{"kind": "text", "text": payload}],
                "messageId": f"msg-loop-{name}",
            }
        },
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        resp = await client.post(url, json=rpc_request)
        rpc_response = resp.json()

    result = rpc_response.get("result", {})
    return _extract_text(result)


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


class LoopOrchestrator:
    """Loops between Generator and Critic until quality criteria are met."""

    async def process(self, user_query: str) -> str:
        """Run the generate-critique loop."""
        logger.info("Loop start: %s", user_query[:60])

        current_input = user_query

        for iteration in range(1, MAX_ITERATIONS + 1):
            logger.info("=== Iteration %d/%d ===", iteration, MAX_ITERATIONS)

            # Step 1: Generate
            logger.info("Calling Generator...")
            plan = await call_agent("Generator", GENERATOR_PORT, current_input)
            logger.info("Generator produced %d chars", len(plan))

            # Step 2: Critique
            logger.info("Calling Critic...")
            feedback = await call_agent("Critic", CRITIC_PORT, plan)
            logger.info("Critic response: %s", feedback[:80])

            # Step 3: Check if passed
            if "PASS" in feedback.upper():
                logger.info("Critic approved on iteration %d", iteration)
                return (
                    f"LOOP & CRITIQUE RESULT (approved on iteration {iteration})\n"
                    f"{'=' * 50}\n\n"
                    f"{plan}"
                )

            # Step 4: Prepare refined input with feedback
            logger.info("Critic requested improvements, looping...")
            current_input = (
                f"Original request: {user_query}\n\n"
                f"Your previous plan:\n{plan}\n\n"
                f"Critic feedback (address ALL points):\n{feedback}\n\n"
                f"Please revise the plan to address the feedback."
            )

        # Max iterations reached — return last plan with warning
        logger.info("Max iterations reached, returning last plan")
        return (
            f"LOOP & CRITIQUE RESULT (max {MAX_ITERATIONS} iterations reached)\n"
            f"{'=' * 50}\n\n"
            f"Last plan:\n{plan}\n\n"
            f"Last feedback:\n{feedback}"
        )


# ---------------------------------------------------------------------------
# A2A server wiring
# ---------------------------------------------------------------------------

agent_card = AgentCard(
    name="LoopOrchestrator",
    description="Iteratively refines trip plans using generate-critique loop.",
    url=f"http://127.0.0.1:{PORT}/",
    version="1.0.0",
    capabilities=AgentCapabilities(streaming=False),
    default_input_modes=["text"],
    default_output_modes=["text"],
    skills=[
        AgentSkill(
            id="loop_critique",
            name="Loop and Critique",
            description="Generate and refine a trip plan until quality criteria pass.",
            tags=["loop", "critique", "refinement"],
            examples=["Plan a trip to Paris with hotel, food, and transport"],
        ),
    ],
)


class LoopExecutor(AgentExecutor):
    """A2A executor for the loop orchestrator."""

    def __init__(self) -> None:
        """Initialize."""
        self._orchestrator = LoopOrchestrator()

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Handle A2A request."""
        user_text = context.get_user_input().strip()
        result = await self._orchestrator.process(user_text)
        await event_queue.enqueue_event(new_agent_text_message(result))

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Handle cancellation."""


def main() -> None:
    """Start the Loop Orchestrator A2A server."""
    logger.info("Starting LoopOrchestrator on port %d", PORT)
    handler = DefaultRequestHandler(
        agent_executor=LoopExecutor(),
        task_store=InMemoryTaskStore(),
    )
    server = A2AStarletteApplication(agent_card=agent_card, http_handler=handler)
    uvicorn.run(server.build(), host="0.0.0.0", port=PORT, log_level="warning")


if __name__ == "__main__":
    main()
