"""Synthesizer A2A Agent -- merges parallel results into a day plan.

Receives combined results from all parallel finders and produces
a unified day itinerary using Ollama. If Ollama is unavailable or
returns an empty response, the agent falls back to a deterministic
formatter so the A2A request still completes.

Optional environment overrides:
    - OLLAMA_BASE_URL (defaults to http://127.0.0.1:11434/v1)
    - OLLAMA_API_KEY (defaults to unused)
    - OLLAMA_MODEL (defaults to qwen3.5:0.8b)

If these variables are not set, the server uses the defaults above.

Port: 11304
"""

import json
import logging
import os
from typing import Any

import uvicorn
from dotenv import load_dotenv
from openai import OpenAI

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.apps import A2AStarletteApplication
from a2a.server.events import EventQueue
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from a2a.utils import new_agent_text_message

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")
logger = logging.getLogger("synthesizer")

load_dotenv()

PORT = 11304
OLLAMA_BASE = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434/v1")
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY", "unused")
MODEL = os.getenv("OLLAMA_MODEL", "qwen3.5:0.8b")
SYSTEM_PROMPT = (
    "You are a city itinerary synthesizer. Build a concise plain-text day plan "
    "using only the structured specialist results provided by the user. Do not "
    "invent venues, cuisines, or neighborhoods. Do not use markdown bullets or "
    "headings beyond plain text labels. Do not wrap your answer in <think> tags."
)


class SynthesizerAgent:
    """Merges parallel agent outputs into a cohesive day plan."""

    def __init__(self, client: Any | None = None) -> None:
        """Initialize the Ollama-compatible OpenAI client."""
        self._client = client or OpenAI(base_url=OLLAMA_BASE, api_key=OLLAMA_API_KEY)

    def process(self, combined_input: str) -> str:
        """Synthesize multiple finder results into one plan."""
        logger.info("Synthesizing results (input length=%d)", len(combined_input))

        fallback_plan = _format_day_plan(combined_input)
        answer = self._generate_plan(combined_input, fallback_plan)
        logger.info("Synthesized plan generated (length=%d)", len(answer))
        return answer

    def _generate_plan(self, combined_input: str, fallback_plan: str) -> str:
        """Call Ollama for the final natural-language synthesis."""
        try:
            response = self._client.chat.completions.create(
                model=MODEL,
                messages=_build_messages(combined_input, fallback_plan),
                extra_body={"reasoning": {"effort": "none"}},
                max_tokens=1200,
            )
        except Exception as exc:
            logger.warning("Ollama synthesis failed: %s", exc)
            return fallback_plan

        answer = _extract_model_text(response)
        if answer:
            return answer

        logger.warning("Ollama synthesis returned an empty response. Using fallback plan.")
        return fallback_plan


def _build_messages(combined_input: str, fallback_plan: str) -> list[dict[str, str]]:
    """Build the prompt payload for the synthesis model."""
    payload = _parse_payload(combined_input)
    request = payload.get("original_query", "")
    structured_results = json.dumps(payload.get("results", {}), indent=2)
    user_prompt = (
        f"User request:\n{request}\n\n"
        f"Structured specialist results:\n{structured_results}\n\n"
        "Use only the provided specialist facts. If one category has no options, "
        "say so plainly. Keep the answer compact and practical.\n\n"
        f"Deterministic fallback plan for reference:\n{fallback_plan}"
    )
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]


def _extract_model_text(response: Any) -> str:
    """Extract and normalize text returned by the Ollama chat completion."""
    choices = getattr(response, "choices", [])
    if not choices:
        return ""

    message = getattr(choices[0], "message", None)
    content = getattr(message, "content", "") if message is not None else ""
    if not isinstance(content, str):
        return ""

    return _strip_think_tags(content).strip()


def _strip_think_tags(text: str) -> str:
    """Remove model reasoning tags when they appear in Ollama output."""
    if "<think>" not in text:
        return text
    if "</think>" in text:
        return text.split("</think>", maxsplit=1)[-1]
    return text.replace("<think>", "")


def _parse_payload(combined_input: str) -> dict:
    """Parse the orchestrator payload for synthesis."""
    try:
        parsed = json.loads(combined_input)
    except json.JSONDecodeError:
        return {"original_query": combined_input, "results": {}}
    return parsed if isinstance(parsed, dict) else {"original_query": combined_input, "results": {}}


def _format_museum_item(item: dict) -> str:
    """Format one museum item."""
    return f"{item.get('name', 'Unknown')} ({item.get('type', 'Unknown')}, {item.get('area', 'Unknown')})"


def _format_restaurant_item(item: dict) -> str:
    """Format one restaurant item."""
    return f"{item.get('name', 'Unknown')} ({item.get('cuisine', 'Unknown')}, {item.get('area', 'Unknown')})"


def _format_concert_item(item: dict) -> str:
    """Format one concert item."""
    return f"{item.get('name', 'Unknown')} ({item.get('genre', 'Unknown')}, {item.get('venue', 'Unknown')})"


def _add_choice_block(lines: list[str], title: str, items: list, formatter, note: str) -> None:
    """Append a formatted choice block to the plan."""
    lines.append(title)
    if items:
        lines.append(f"- Primary: {formatter(items[0])}")
        if len(items) > 1:
            alternates = "; ".join(formatter(item) for item in items[1:])
            lines.append(f"- Alternates: {alternates}")
        if note:
            lines.append(f"- Note: {note}")
    else:
        lines.append(f"- {note or 'Unavailable in demo data.'}")


def _format_day_plan(combined_input: str) -> str:
    """Build a deterministic day plan from specialist outputs."""
    payload = _parse_payload(combined_input)
    results = payload.get("results", {})
    museum_payload = results.get("MuseumFinder", {})
    restaurant_payload = results.get("RestaurantFinder", {})
    concert_payload = results.get("ConcertFinder", {})

    lines = ["Day plan:", f"Request: {payload.get('original_query', '')}", ""]
    _add_choice_block(
        lines,
        "Morning - Museums:",
        museum_payload.get("items", []),
        _format_museum_item,
        museum_payload.get("note", "Museum data unavailable."),
    )
    lines.append("")
    _add_choice_block(
        lines,
        "Afternoon - Food:",
        restaurant_payload.get("items", []),
        _format_restaurant_item,
        restaurant_payload.get("note", "Restaurant data unavailable."),
    )
    lines.append("")
    _add_choice_block(
        lines,
        "Evening - Live event:",
        concert_payload.get("items", []),
        _format_concert_item,
        concert_payload.get("note", "Concert data unavailable."),
    )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# A2A server wiring
# ---------------------------------------------------------------------------

agent_card = AgentCard(
    name="SynthesizerAgent",
    description="Merges parallel agent results into a unified day plan.",
    url=f"http://127.0.0.1:{PORT}/",
    version="1.0.0",
    capabilities=AgentCapabilities(streaming=False),
    default_input_modes=["text"],
    default_output_modes=["text"],
    skills=[
        AgentSkill(
            id="synthesize",
            name="Synthesize Results",
            description="Merge multiple specialist outputs into a day plan.",
            tags=["synthesis", "planning"],
            examples=["Combine museum, concert, and restaurant recommendations"],
        ),
    ],
)


class SynthesizerExecutor(AgentExecutor):
    """A2A executor for SynthesizerAgent."""

    def __init__(self) -> None:
        """Initialize the agent."""
        self._agent = SynthesizerAgent()

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Handle an A2A request."""
        user_text = context.get_user_input().strip()
        logger.info("A2A request (length=%d)", len(user_text))
        result = self._agent.process(user_text)
        await event_queue.enqueue_event(new_agent_text_message(result))

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Handle cancellation."""
        logger.info("Request cancelled")


def main() -> None:
    """Start the A2A agent server."""
    logger.info("Starting SynthesizerAgent on port %d", PORT)
    handler = DefaultRequestHandler(
        agent_executor=SynthesizerExecutor(),
        task_store=InMemoryTaskStore(),
    )
    server = A2AStarletteApplication(agent_card=agent_card, http_handler=handler)
    uvicorn.run(server.build(), host="0.0.0.0", port=PORT, log_level="warning")


if __name__ == "__main__":
    main()
