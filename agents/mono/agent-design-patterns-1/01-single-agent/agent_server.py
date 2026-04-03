"""Single Agent A2A server — Trip Planner with tools.

Demonstrates the single agent pattern: one LLM decides which tools
to call and in what order. The agent has three tools (search_attractions,
search_restaurants, get_weather) and autonomously decides execution flow.

Requires:
    - Ollama running at http://127.0.0.1:11434 with gemma4:e2b pulled

Port: 11100
"""

import json
import logging
import os
import re

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
logger = logging.getLogger("single-agent")

load_dotenv()

PORT = 11100
OLLAMA_BASE = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434/v1")
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY", "unused")
MODEL = os.getenv("OLLAMA_MODEL", "gemma4:e2b")

# ---------------------------------------------------------------------------
# Tool definitions (simulated data for demo)
# ---------------------------------------------------------------------------

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_attractions",
            "description": "Search for tourist attractions in a city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name"},
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_restaurants",
            "description": "Search for restaurants in a city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name"},
                    "cuisine": {"type": "string", "description": "Cuisine type (optional)"},
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather forecast for a city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name"},
                },
                "required": ["city"],
            },
        },
    },
]


def search_attractions(city: str) -> str:
    """Return simulated attraction results for a city."""
    data = {
        "san francisco": [
            "Golden Gate Bridge - iconic suspension bridge",
            "Alcatraz Island - historic federal penitentiary",
            "Fisherman's Wharf - waterfront dining and shops",
        ],
        "new york": [
            "Statue of Liberty - symbol of freedom",
            "Central Park - 843-acre urban park",
            "Times Square - entertainment hub",
        ],
    }
    results = data.get(city.lower(), [f"Popular landmarks in {city}"])
    logger.info("TOOL search_attractions(%s) -> %d results", city, len(results))
    return json.dumps({"city": city, "attractions": results})


def search_restaurants(city: str, cuisine: str = "") -> str:
    """Return simulated restaurant results for a city."""
    data = {
        "san francisco": [
            "Tartine Bakery - artisan bakery and cafe",
            "Swan Oyster Depot - classic seafood counter",
            "Nopa - California cuisine in Western Addition",
        ],
        "new york": [
            "Di Fara Pizza - legendary Brooklyn pizza",
            "Peter Luger - classic steakhouse",
            "Le Bernardin - fine French seafood",
        ],
    }
    results = data.get(city.lower(), [f"Top restaurants in {city}"])
    suffix = f" ({cuisine})" if cuisine else ""
    logger.info("TOOL search_restaurants(%s%s) -> %d results", city, suffix, len(results))
    return json.dumps({"city": city, "cuisine": cuisine, "restaurants": results})


def get_weather(city: str) -> str:
    """Return simulated weather data for a city."""
    data = {
        "san francisco": {"temp": "62F", "condition": "Partly cloudy", "wind": "15mph W"},
        "new york": {"temp": "78F", "condition": "Sunny", "wind": "8mph SE"},
    }
    weather = data.get(city.lower(), {"temp": "72F", "condition": "Clear", "wind": "5mph"})
    logger.info("TOOL get_weather(%s) -> %s", city, weather["condition"])
    return json.dumps({"city": city, **weather})


TOOL_MAP = {
    "search_attractions": search_attractions,
    "search_restaurants": search_restaurants,
    "get_weather": get_weather,
}

RAW_TOOL_PATTERN = re.compile(
    r"(?:search_attractions|search_restaurants|get_weather)\s*(?:\{|\()",
    re.IGNORECASE,
)


def _looks_like_raw_tool_text(text: str) -> bool:
    """Detect plain-text tool syntax returned instead of an actual plan."""
    return bool(RAW_TOOL_PATTERN.search(text))


def _extract_city_from_query(query: str) -> str:
    """Extract a destination city from the user query when possible."""
    for city in ["San Francisco", "New York"]:
        if city.lower() in query.lower():
            return city

    match = re.search(r"\b(?:to|in)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)", query)
    if match:
        return match.group(1)
    return "the destination"


def _select_fallback_tools(query: str) -> list[str]:
    """Choose which local tools to invoke for a deterministic fallback."""
    lower_query = query.lower()
    selected = []

    if any(word in lower_query for word in ["attraction", "things to do", "trip", "weekend"]):
        selected.append("search_attractions")
    if any(word in lower_query for word in ["restaurant", "food", "dining", "trip", "weekend"]):
        selected.append("search_restaurants")
    if any(word in lower_query for word in ["weather", "forecast", "trip", "weekend"]):
        selected.append("get_weather")

    return selected or ["search_attractions", "search_restaurants", "get_weather"]


def _parse_tool_json(text: str) -> dict:
    """Parse a JSON tool response into a dict."""
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def _build_fallback_plan(query: str) -> str:
    """Create a grounded response when the model emits raw tool syntax."""
    city = _extract_city_from_query(query)
    requested_tools = _select_fallback_tools(query)
    results = {}

    for tool_name in requested_tools:
        if tool_name == "search_restaurants":
            results[tool_name] = _parse_tool_json(search_restaurants(city))
        elif tool_name == "search_attractions":
            results[tool_name] = _parse_tool_json(search_attractions(city))
        elif tool_name == "get_weather":
            results[tool_name] = _parse_tool_json(get_weather(city))

    lines = [f"Trip summary for {city}:"]

    attractions = results.get("search_attractions", {}).get("attractions", [])
    if attractions:
        lines.append(f"Attractions: {attractions[0]}")
        if len(attractions) > 1:
            lines.append(f"More to do: {'; '.join(attractions[1:])}")

    restaurants = results.get("search_restaurants", {}).get("restaurants", [])
    if restaurants:
        lines.append(f"Food: {restaurants[0]}")
        if len(restaurants) > 1:
            lines.append(f"More food options: {'; '.join(restaurants[1:])}")

    weather = results.get("get_weather", {})
    if weather:
        lines.append(
            "Weather: "
            f"{weather.get('temp', 'Unknown')}, {weather.get('condition', 'Unknown')}, "
            f"wind {weather.get('wind', 'Unknown')}"
        )

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Agent logic
# ---------------------------------------------------------------------------

class TripPlannerAgent:
    """Single agent that uses LLM to decide tool calls dynamically."""

    def __init__(self) -> None:
        """Initialize the OpenAI client for Ollama."""
        self._client = OpenAI(base_url=OLLAMA_BASE, api_key=OLLAMA_API_KEY)

    def process(self, user_query: str) -> str:
        """Process a trip planning query with tool-use loop."""
        logger.info("Processing query: %s", user_query)

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful trip planning assistant. "
                    "Use the available tools to research the destination, "
                    "then provide a concise trip plan. "
                    "Do not use markdown formatting. Keep your response plain text. "
                    "Do NOT wrap your response in <think> tags."
                ),
            },
            {"role": "user", "content": user_query},
        ]

        # Tool-use loop (max 5 iterations to prevent infinite loops)
        for iteration in range(5):
            logger.info("LLM call iteration %d", iteration + 1)
            response = self._client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=TOOLS,
                extra_body={"reasoning": {"effort": "none"}},
                max_tokens=2048,
            )

            choice = response.choices[0]

            if choice.finish_reason == "tool_calls" and choice.message.tool_calls:
                # LLM wants to call tools
                messages.append(choice.message)
                for tool_call in choice.message.tool_calls:
                    fn_name = tool_call.function.name
                    fn_args = json.loads(tool_call.function.arguments)
                    logger.info("LLM requested tool: %s(%s)", fn_name, fn_args)

                    fn = TOOL_MAP.get(fn_name)
                    if fn:
                        result = fn(**fn_args)
                    else:
                        result = json.dumps({"error": f"Unknown tool: {fn_name}"})

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result,
                    })
            else:
                # LLM produced a final answer
                answer = choice.message.content or "No response generated."
                # Strip <think> tags if present
                if "<think>" in answer:
                    parts = answer.split("</think>")
                    answer = parts[-1].strip() if len(parts) > 1 else answer
                if _looks_like_raw_tool_text(answer):
                    logger.info("Model returned raw tool text; using deterministic fallback")
                    return _build_fallback_plan(user_query)
                logger.info("Final answer produced (length=%d)", len(answer))
                return answer

        logger.info("Iteration limit reached; using deterministic fallback")
        return _build_fallback_plan(user_query)


# ---------------------------------------------------------------------------
# A2A server wiring
# ---------------------------------------------------------------------------

agent_card = AgentCard(
    name="TripPlannerAgent",
    description="Plans trips by searching attractions, restaurants, and weather.",
    url=f"http://127.0.0.1:{PORT}/",
    version="1.0.0",
    capabilities=AgentCapabilities(streaming=False),
    default_input_modes=["text"],
    default_output_modes=["text"],
    skills=[
        AgentSkill(
            id="trip_planning",
            name="Trip Planning",
            description="Plan a trip to any city with attractions, food, and weather.",
            tags=["travel", "planning"],
            examples=["Plan a trip to San Francisco"],
        ),
    ],
)


class TripPlannerExecutor(AgentExecutor):
    """A2A executor that delegates to the TripPlannerAgent."""

    def __init__(self) -> None:
        """Initialize the agent."""
        self._agent = TripPlannerAgent()

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Handle an A2A request."""
        user_text = context.get_user_input().strip()
        logger.info("A2A request received: %s", user_text[:80])
        result = self._agent.process(user_text)
        await event_queue.enqueue_event(new_agent_text_message(result))

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Handle cancellation."""
        logger.info("Request cancelled")


def main() -> None:
    """Start the A2A agent server."""
    logger.info("Starting TripPlannerAgent on port %d", PORT)
    handler = DefaultRequestHandler(
        agent_executor=TripPlannerExecutor(),
        task_store=InMemoryTaskStore(),
    )
    server = A2AStarletteApplication(agent_card=agent_card, http_handler=handler)
    uvicorn.run(server.build(), host="0.0.0.0", port=PORT, log_level="warning")


if __name__ == "__main__":
    main()
