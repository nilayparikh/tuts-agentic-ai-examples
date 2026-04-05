"""Generator Agent A2A server — produces trip plans.

Takes a trip planning query and produces a draft plan. When feedback
is provided (from the Critic), it refines the plan accordingly.

Requires:
    - Ollama running at http://127.0.0.1:11434 with qwen3.5:0.8b pulled

Port: 11401
"""

import logging
import os

import uvicorn
from openai import OpenAI
from dotenv import load_dotenv

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.apps import A2AStarletteApplication
from a2a.server.events import EventQueue
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from a2a.utils import new_agent_text_message

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")
logger = logging.getLogger("generator")

load_dotenv()

PORT = 11401
OLLAMA_BASE = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434/v1")
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY", "unused")
MODEL = os.getenv("OLLAMA_MODEL", "qwen3.5:0.8b")


class GeneratorAgent:
    """Produces trip plans, optionally refining based on critique feedback."""

    def __init__(self) -> None:
        """Initialize the OpenAI client for Ollama."""
        self._client = OpenAI(base_url=OLLAMA_BASE, api_key=OLLAMA_API_KEY)

    def process(self, user_input: str) -> str:
        """Generate or refine a trip plan."""
        logger.info("Generating plan for: %s", user_input[:80])

        response = self._client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a trip planning assistant. "
                        "Generate a concise trip plan covering hotel, "
                        "2-3 attractions, dining, and transport tips. "
                        "If feedback from a critic is included, revise "
                        "your plan to address every point raised. "
                        "Keep the answer under 180 words. "
                        "Use plain text only. No markdown. "
                        "Do NOT wrap your response in <think> tags."
                    ),
                },
                {"role": "user", "content": user_input},
            ],
            extra_body={"reasoning": {"effort": "none"}},
            max_tokens=384,
        )
        answer = response.choices[0].message.content or "No plan generated."
        if "<think>" in answer:
            parts = answer.split("</think>")
            answer = parts[-1].strip() if len(parts) > 1 else answer
        logger.info("Plan generated (%d chars)", len(answer))
        return answer


# ---------------------------------------------------------------------------
# A2A server wiring
# ---------------------------------------------------------------------------

agent_card = AgentCard(
    name="GeneratorAgent",
    description="Generates and refines trip plans based on queries and feedback.",
    url=f"http://127.0.0.1:{PORT}/",
    version="1.0.0",
    capabilities=AgentCapabilities(streaming=False),
    default_input_modes=["text"],
    default_output_modes=["text"],
    skills=[
        AgentSkill(
            id="trip_generation",
            name="Trip Plan Generation",
            description="Generate a trip plan for a city.",
            tags=["travel", "generation"],
            examples=["Plan a weekend trip to San Francisco"],
        ),
    ],
)


class GeneratorExecutor(AgentExecutor):
    """A2A executor for the Generator."""

    def __init__(self) -> None:
        """Initialize."""
        self._agent = GeneratorAgent()

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Handle A2A request."""
        user_text = context.get_user_input().strip()
        result = self._agent.process(user_text)
        await event_queue.enqueue_event(new_agent_text_message(result))

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Handle cancellation."""


def main() -> None:
    """Start the Generator A2A server."""
    logger.info("Starting GeneratorAgent on port %d", PORT)
    handler = DefaultRequestHandler(
        agent_executor=GeneratorExecutor(),
        task_store=InMemoryTaskStore(),
    )
    server = A2AStarletteApplication(agent_card=agent_card, http_handler=handler)
    uvicorn.run(server.build(), host="0.0.0.0", port=PORT, log_level="warning")


if __name__ == "__main__":
    main()
