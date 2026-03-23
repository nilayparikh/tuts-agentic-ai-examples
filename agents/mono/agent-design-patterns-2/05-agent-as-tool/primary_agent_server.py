"""Primary Agent A2A server — uses sub-agents as tools.

Demonstrates the Agent-as-Tool pattern: the Primary Agent has three
sub-agents registered as OpenAI-style tools. When the LLM decides to
call a tool, the Primary Agent dispatches an A2A request to the
corresponding sub-agent and returns the result as a tool response.

Sub-agents:
  - FoodFinderTool (port 11421)
  - TransportFinderTool (port 11422)
  - NearbyFinderTool (port 11423)

Requires:
    - All sub-agents running (ports 11421-11423)
    - Ollama running at http://127.0.0.1:11434 with qwen3.5:0.8b pulled

Port: 11424
"""

import json
import logging

import httpx
import uvicorn
from openai import OpenAI

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.apps import A2AStarletteApplication
from a2a.server.events import EventQueue
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from a2a.utils import new_agent_text_message

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")
logger = logging.getLogger("primary-agent")

PORT = 11424
OLLAMA_BASE = "http://127.0.0.1:11434/v1"
MODEL = "qwen3.5:0.8b"

# Map tool names to their A2A agent ports
AGENT_TOOLS = {
    "find_food": 11421,
    "find_transport": 11422,
    "find_nearby": 11423,
}

# OpenAI function definitions — each wraps a sub-agent
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "find_food",
            "description": "Find food and restaurant recommendations for a city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The food-related query including city name",
                    },
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "find_transport",
            "description": "Find transport and transit options for a city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The transport-related query including city name",
                    },
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "find_nearby",
            "description": "Find nearby attractions and things to do in a city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The attractions query including city name",
                    },
                },
                "required": ["query"],
            },
        },
    },
]


async def call_sub_agent(tool_name: str, query: str) -> str:
    """Call a sub-agent via A2A and return the text response."""
    port = AGENT_TOOLS[tool_name]
    url = f"http://localhost:{port}/"
    rpc_request = {
        "jsonrpc": "2.0",
        "id": f"tool-{tool_name}",
        "method": "message/send",
        "params": {
            "message": {
                "role": "user",
                "parts": [{"kind": "text", "text": query}],
                "messageId": f"msg-tool-{tool_name}",
            }
        },
    }

    logger.info("Calling sub-agent %s on port %d", tool_name, port)
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


class PrimaryAgent:
    """Uses sub-agents as tools via OpenAI function calling + A2A."""

    def __init__(self) -> None:
        """Initialize the OpenAI client for Ollama."""
        self._client = OpenAI(base_url=OLLAMA_BASE, api_key="unused")

    async def process(self, user_query: str) -> str:
        """Process query using sub-agents as tools."""
        logger.info("Primary agent processing: %s", user_query[:60])

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a trip planning assistant. "
                    "Use the available tools to gather information about "
                    "food, transport, and attractions for the destination. "
                    "Call the tools as needed, then synthesize a concise "
                    "trip plan from the results. Do not invent venues or facts that are "
                    "not returned by the tools. If a tool does not provide enough "
                    "information, say the demo data is limited. "
                    "Use plain text only. No markdown. "
                    "Do NOT wrap your response in <think> tags."
                ),
            },
            {"role": "user", "content": user_query},
        ]

        # Try LLM-driven tool calling first
        tool_results = await self._try_llm_tools(messages)

        if not tool_results:
            # Small models may not produce tool_calls — call all agents
            logger.info("LLM did not call tools, invoking all sub-agents directly")
            tool_results = await self._call_all_agents(user_query)

        # Synthesize results
        return await self._synthesize(user_query, tool_results)

    async def _try_llm_tools(self, messages: list) -> dict:
        """Attempt LLM-driven tool calling. Return tool results or empty dict."""
        collected = {}

        for iteration in range(5):
            logger.info("LLM call iteration %d", iteration + 1)
            response = self._client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=TOOLS,
                extra_body={"reasoning": {"effort": "none"}},
                max_tokens=768,
            )
            choice = response.choices[0]

            if choice.finish_reason == "tool_calls" and choice.message.tool_calls:
                messages.append(choice.message)
                for tool_call in choice.message.tool_calls:
                    fn_name = tool_call.function.name
                    fn_args = json.loads(tool_call.function.arguments)
                    logger.info("LLM requested tool: %s(%s)", fn_name, fn_args)

                    if fn_name in AGENT_TOOLS:
                        result = await call_sub_agent(
                            fn_name, fn_args.get("query", ""),
                        )
                        collected[fn_name] = result
                    else:
                        result = f"Unknown tool: {fn_name}"

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result,
                    })
            else:
                # LLM finished — if it produced tool results, return them
                break

        return collected

    async def _call_all_agents(self, query: str) -> dict:
        """Call all sub-agents directly as a fallback."""
        results = {}
        for tool_name in AGENT_TOOLS:
            logger.info("Direct call to %s", tool_name)
            results[tool_name] = await call_sub_agent(tool_name, query)
        return results

    async def _synthesize(self, query: str, tool_results: dict) -> str:
        """Build a deterministic trip plan from gathered tool results."""
        return _format_trip_plan(query, tool_results)


def _first_detail_line(text: str) -> str:
    """Return the first bullet/detail line from tool output."""
    payload = _parse_tool_payload(text)
    items = payload.get("items", [])
    if items:
        return _format_tool_item(items[0])
    return payload.get("note", "Demo data is limited.")


def _parse_tool_payload(text: str) -> dict:
    """Parse a tool payload, accepting JSON or plain text."""
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        return {"items": [], "note": text or "Demo data is limited."}
    return parsed if isinstance(parsed, dict) else {"items": [], "note": text}


def _format_tool_item(item: dict) -> str:
    """Format one structured tool item."""
    name = item.get("name", "Unknown")
    details = item.get("details", "")
    return f"{name} ({details})" if details else name


def _format_trip_plan(query: str, tool_results: dict) -> str:
    """Create a grounded trip plan from sub-agent results."""
    nearby_payload = _parse_tool_payload(tool_results.get("find_nearby", ""))
    food_payload = _parse_tool_payload(tool_results.get("find_food", ""))
    transport_payload = _parse_tool_payload(tool_results.get("find_transport", ""))

    nearby_items = nearby_payload.get("items", [])
    food_items = food_payload.get("items", [])
    transport_items = transport_payload.get("items", [])

    lines = [f"Trip plan for: {query}", ""]
    lines.append("Morning sights:")
    if nearby_items:
        lines.append(f"- Primary stop: {_format_tool_item(nearby_items[0])}")
        if len(nearby_items) > 1:
            lines.append(
                "- Backups: "
                + "; ".join(_format_tool_item(item) for item in nearby_items[1:])
            )
    else:
        lines.append(f"- {nearby_payload.get('note', 'No attraction data available.')}")

    lines.extend(["", "Food stop:"])
    if food_items:
        lines.append(f"- Primary stop: {_format_tool_item(food_items[0])}")
        if len(food_items) > 1:
            lines.append(
                "- Backups: " + "; ".join(_format_tool_item(item) for item in food_items[1:])
            )
    else:
        lines.append(f"- {food_payload.get('note', 'No food data available.')}")

    lines.extend(["", "Getting around:"])
    if transport_items:
        lines.append(f"- Primary option: {_format_tool_item(transport_items[0])}")
        if len(transport_items) > 1:
            lines.append(
                "- Alternates: "
                + "; ".join(_format_tool_item(item) for item in transport_items[1:])
            )
    else:
        lines.append(f"- {transport_payload.get('note', 'No transport data available.')}")

    lines.extend([
        "",
        "Note: this plan is composed only from structured sub-agent payloads.",
    ])
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# A2A server wiring
# ---------------------------------------------------------------------------

agent_card = AgentCard(
    name="PrimaryAgent",
    description="Trip planner that uses sub-agents as tools for food, transport, and attractions.",
    url=f"http://localhost:{PORT}/",
    version="1.0.0",
    capabilities=AgentCapabilities(streaming=False),
    default_input_modes=["text"],
    default_output_modes=["text"],
    skills=[
        AgentSkill(
            id="agent_as_tool",
            name="Agent-as-Tool Trip Planning",
            description="Plan trips using sub-agents as stateless tool calls.",
            tags=["tool", "composition"],
            examples=["Plan a trip to San Francisco with food, transport, and sights"],
        ),
    ],
)


class PrimaryExecutor(AgentExecutor):
    """A2A executor for the Primary Agent."""

    def __init__(self) -> None:
        """Initialize."""
        self._agent = PrimaryAgent()

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Handle A2A request."""
        user_text = context.get_user_input().strip()
        result = await self._agent.process(user_text)
        await event_queue.enqueue_event(new_agent_text_message(result))

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Handle cancellation."""


def main() -> None:
    """Start the Primary Agent A2A server."""
    logger.info("Starting PrimaryAgent on port %d", PORT)
    handler = DefaultRequestHandler(
        agent_executor=PrimaryExecutor(),
        task_store=InMemoryTaskStore(),
    )
    server = A2AStarletteApplication(agent_card=agent_card, http_handler=handler)
    uvicorn.run(server.build(), host="0.0.0.0", port=PORT, log_level="warning")


if __name__ == "__main__":
    main()
