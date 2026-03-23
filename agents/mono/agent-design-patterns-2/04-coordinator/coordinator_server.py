"""Coordinator A2A server — LLM-driven dynamic routing.

Uses an LLM to classify the user query and route it to the
best-fit specialist agent. The routing decision is dynamic,
not hardcoded — the LLM reads agent descriptions and decides.

Available specialists:
  - FoodAgent (port 11411): food, dining, restaurants
  - TransportAgent (port 11412): transit, getting around
  - CostAgent (port 11413): budget, pricing, costs

Requires:
    - All specialist agents running (ports 11411-11413)
    - Ollama running at http://127.0.0.1:11434 with qwen3.5:0.8b pulled

Port: 11414
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
logger = logging.getLogger("coordinator")

PORT = 11414
OLLAMA_BASE = "http://127.0.0.1:11434/v1"
MODEL = "qwen3.5:0.8b"

SPECIALIST_AGENTS = [
    {
        "name": "FoodAgent",
        "port": 11411,
        "description": "Handles food, dining, and restaurant queries.",
    },
    {
        "name": "TransportAgent",
        "port": 11412,
        "description": "Handles transport, transit, and getting-around queries.",
    },
    {
        "name": "CostAgent",
        "port": 11413,
        "description": "Handles budget, pricing, and cost estimate queries.",
    },
]


async def call_agent(name: str, port: int, payload: str) -> str:
    """Send a message to an A2A agent and return the text response."""
    url = f"http://localhost:{port}/"
    rpc_request = {
        "jsonrpc": "2.0",
        "id": f"coord-{name}",
        "method": "message/send",
        "params": {
            "message": {
                "role": "user",
                "parts": [{"kind": "text", "text": payload}],
                "messageId": f"msg-coord-{name}",
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


KEYWORD_RULES = [
    {
        "agent": "TransportAgent",
        "keywords": [
            "transport", "transit", "subway", "metro", "bus", "train",
            "get around", "getting around", "commute", "taxi", "uber",
        ],
    },
    {
        "agent": "CostAgent",
        "keywords": [
            "cost", "budget", "price", "expensive", "cheap", "afford",
            "how much", "spend", "money", "dollar", "euro", "yen",
        ],
    },
    {
        "agent": "FoodAgent",
        "keywords": [
            "food", "restaurant", "eat", "dining", "cuisine", "meal",
            "lunch", "dinner", "breakfast", "cafe", "bar",
        ],
    },
]


class CoordinatorRouter:
    """Uses LLM to classify and route queries to specialist agents."""

    def __init__(self) -> None:
        """Initialize the OpenAI client for Ollama."""
        self._client = OpenAI(base_url=OLLAMA_BASE, api_key="unused")

    def _classify_query(self, query: str) -> str:
        """Use LLM to classify which agent should handle the query."""
        # Try keyword-based classification first for reliability
        keyword_result = self._keyword_classify(query)
        if keyword_result:
            logger.info("Keyword classifier matched: %s", keyword_result)
            return keyword_result

        # Fall back to LLM classification
        agent_descriptions = "\n".join(
            f"- {a['name']}: {a['description']}" for a in SPECIALIST_AGENTS
        )

        response = self._client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a query router. Given a user query and a list "
                        "of available specialist agents, respond with ONLY the "
                        "name of the agent that best handles the query. "
                        "Respond with exactly one agent name, nothing else. "
                        "Do NOT wrap your response in <think> tags.\n\n"
                        f"Available agents:\n{agent_descriptions}"
                    ),
                },
                {"role": "user", "content": query},
            ],
            extra_body={"reasoning": {"effort": "none"}},
            max_tokens=32,
        )
        answer = response.choices[0].message.content or ""
        if "<think>" in answer:
            parts = answer.split("</think>")
            answer = parts[-1].strip() if len(parts) > 1 else answer
        return answer.strip()

    def _keyword_classify(self, query: str) -> str:
        """Classify query using keyword matching. Returns agent name or empty."""
        q_lower = query.lower()
        for rule in KEYWORD_RULES:
            for kw in rule["keywords"]:
                if kw in q_lower:
                    return rule["agent"]
        return ""

    async def process(self, user_query: str) -> str:
        """Classify and route the query to the appropriate agent."""
        logger.info("Coordinator routing: %s", user_query[:60])

        # Step 1: Classify the query (keyword first, then LLM fallback)
        chosen = self._classify_query(user_query)
        logger.info("Classification result: %s", chosen)

        # Step 2: Find the matching agent
        target = None
        for agent in SPECIALIST_AGENTS:
            if agent["name"].lower() in chosen.lower():
                target = agent
                break

        if not target:
            # Fallback: default to FoodAgent
            logger.info("No match for '%s', defaulting to FoodAgent", chosen)
            target = SPECIALIST_AGENTS[0]

        # Step 3: Route to the chosen agent
        logger.info("Routing to %s on port %d", target["name"], target["port"])
        result = await call_agent(target["name"], target["port"], user_query)
        payload = _parse_specialist_payload(result)

        return _format_routing_result(user_query, target["name"], payload)


def _parse_specialist_payload(result: str) -> dict:
    """Parse a structured specialist payload."""
    try:
        parsed = json.loads(result)
    except json.JSONDecodeError:
        return {"items": [], "note": result or "Specialist returned unstructured text."}
    return parsed if isinstance(parsed, dict) else {"items": [], "note": result}


def _format_choice(item: dict) -> str:
    """Format a non-cost specialist item."""
    name = item.get("name", "Unknown")
    details = item.get("details", "")
    return f"{name} ({details})" if details else name


def _format_cost_item(item: dict) -> str:
    """Format a cost specialist item."""
    return f"{item.get('label', 'Unknown')}: {item.get('value', 'Unknown')}"


def _format_payload_block(agent_name: str, payload: dict) -> list[str]:
    """Render one structured specialist payload into human-readable lines."""
    items = payload.get("items", [])
    note = payload.get("note", "")
    city = str(payload.get("city", "unknown")).title()

    if agent_name == "CostAgent":
        lines = [f"Budget snapshot for {city}:"]
        if items:
            for item in items:
                lines.append(f"- {_format_cost_item(item)}")
        else:
            lines.append(f"- {note or 'Budget data unavailable.'}")
        if note and items:
            lines.append(f"Note: {note}")
        return lines

    topic = "Food" if agent_name == "FoodAgent" else "Transport"
    lines = [f"{topic} options for {city}:"]
    if items:
        lines.append(f"- Primary: {_format_choice(items[0])}")
        if len(items) > 1:
            alternates = "; ".join(_format_choice(item) for item in items[1:])
            lines.append(f"- Alternates: {alternates}")
        if note:
            lines.append(f"Note: {note}")
    else:
        lines.append(f"- {note or 'No data available.'}")
    return lines


def _format_routing_result(user_query: str, agent_name: str, payload: dict) -> str:
    """Render the coordinator result from a structured specialist payload."""
    lines = [
        "COORDINATOR ROUTING RESULT",
        "=" * 40,
        f"Original query: {user_query}",
        f"Query classified as: {agent_name}",
        "",
    ]
    lines.extend(_format_payload_block(agent_name, payload))
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# A2A server wiring
# ---------------------------------------------------------------------------

agent_card = AgentCard(
    name="Coordinator",
    description="Routes queries dynamically to specialist agents using LLM classification.",
    url=f"http://localhost:{PORT}/",
    version="1.0.0",
    capabilities=AgentCapabilities(streaming=False),
    default_input_modes=["text"],
    default_output_modes=["text"],
    skills=[
        AgentSkill(
            id="dynamic_routing",
            name="Dynamic Routing",
            description="Route travel queries to the best specialist agent.",
            tags=["routing", "coordinator"],
            examples=[
                "Best restaurants in Paris",
                "How to get around Tokyo",
                "Budget for a weekend in New York",
            ],
        ),
    ],
)


class CoordinatorExecutor(AgentExecutor):
    """A2A executor for the Coordinator."""

    def __init__(self) -> None:
        """Initialize."""
        self._router = CoordinatorRouter()

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Handle A2A request."""
        user_text = context.get_user_input().strip()
        result = await self._router.process(user_text)
        await event_queue.enqueue_event(new_agent_text_message(result))

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Handle cancellation."""


def main() -> None:
    """Start the Coordinator A2A server."""
    logger.info("Starting Coordinator on port %d", PORT)
    handler = DefaultRequestHandler(
        agent_executor=CoordinatorExecutor(),
        task_store=InMemoryTaskStore(),
    )
    server = A2AStarletteApplication(agent_card=agent_card, http_handler=handler)
    uvicorn.run(server.build(), host="0.0.0.0", port=PORT, log_level="warning")


if __name__ == "__main__":
    main()
