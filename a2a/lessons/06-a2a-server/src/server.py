"""A2A Server — Serves QAAgent as a fully A2A-compliant endpoint.

Run:
    python server.py

Endpoints:
    GET  /.well-known/agent.json  — Agent Card (discovery)
    POST /                        — JSON-RPC message handling
"""

# pylint: disable=wrong-import-position,wrong-import-order

import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]

import uvicorn  # noqa: E402
from dotenv import find_dotenv, load_dotenv  # noqa: E402

# Load .env from nearest parent directory (searches up to _examples/.env)
load_dotenv(find_dotenv(raise_error_if_not_found=False))

from a2a.server.apps import A2AStarletteApplication  # noqa: E402
from a2a.server.request_handlers import DefaultRequestHandler  # noqa: E402
from a2a.server.tasks import InMemoryTaskStore  # noqa: E402
from a2a.types import AgentCapabilities, AgentCard, AgentSkill  # noqa: E402

from agent_executor import QAAgentExecutor  # noqa: E402

# ---------------------------------------------------------------------------
# Agent Card — describes what this agent can do
# ---------------------------------------------------------------------------

agent_card = AgentCard(
    name="QAAgent",
    description="Answers questions about insurance policies using GitHub Phi-4",
    url="http://localhost:10001/",
    version="1.0.0",
    capabilities=AgentCapabilities(streaming=True),
    default_input_modes=["text"],
    default_output_modes=["text"],
    skills=[
        AgentSkill(
            id="policy-qa",
            name="Policy Question Answering",
            description="Answer questions about insurance policy documents",
            tags=["qa", "insurance", "policy"],
            examples=[
                "What is the deductible for the Standard plan?",
                "Are cosmetic procedures covered?",
                "How do I file a claim?",
            ],
        )
    ],
)

# ---------------------------------------------------------------------------
# Wire up: Executor → Handler → Application
# ---------------------------------------------------------------------------

request_handler = DefaultRequestHandler(
    agent_executor=QAAgentExecutor(),
    task_store=InMemoryTaskStore(),
)

server = A2AStarletteApplication(
    agent_card=agent_card,
    http_handler=request_handler,
)

# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("🚀 Starting QAAgent A2A Server on http://localhost:10001")
    print("📋 Agent Card: http://localhost:10001/.well-known/agent.json")
    uvicorn.run(server.build(), host="0.0.0.0", port=10001)
