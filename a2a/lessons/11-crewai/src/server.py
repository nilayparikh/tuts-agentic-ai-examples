"""
Lesson 11 — A2A Server wrapping the CrewAI OrchestratorAgent.

Usage:
    python server.py          # starts on http://localhost:10004

Reuses ``loan_data.py`` and ``validation_rules.py`` from ``_common/src``.

Environment variables required (loaded from ``_examples/.env``):
    AZURE_OPENAI_ENDPOINT
    AZURE_AI_API_KEY
    AZURE_AI_MODEL_DEPLOYMENT_NAME
"""

from __future__ import annotations

import asyncio
import os
import re
import sys
from pathlib import Path
from uuid import uuid4

# ─── path setup: reuse _common shared data & rules ──────────────────────────
_COMMON = str(Path(__file__).resolve().parents[2] / "_common" / "src")
if _COMMON not in sys.path:
    sys.path.insert(0, _COMMON)

_THIS_SRC = str(Path(__file__).resolve().parent)
if _THIS_SRC not in sys.path:
    sys.path.insert(0, _THIS_SRC)

# ─── load .env ────────────────────────────────────────────────────────────────
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[3] / ".env")

# ─── imports ──────────────────────────────────────────────────────────────────
from a2a.server.agent_execution import AgentExecutor
from a2a.server.events import EventQueue
from a2a.server.request_handler import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCard,
    AgentSkill,
    Artifact,
    Message,
    Part,
    TaskState,
    TextPart,
)
from starlette.applications import Starlette
from starlette.routing import Route
from a2a.server.apps import A2AStarletteApplication

from loan_data import APPLICANT_INDEX
from orchestrator import OrchestratorAgent

# ─── constants ────────────────────────────────────────────────────────────────
SERVER_HOST = "localhost"
SERVER_PORT = 10004

# ─── AgentExecutor ────────────────────────────────────────────────────────────


class LoanValidatorExecutor(AgentExecutor):
    """Bridges A2A request → CrewAI OrchestratorAgent → A2A response."""

    def __init__(self) -> None:
        self._orchestrator = OrchestratorAgent()

    async def execute(self, context, event_queue: EventQueue) -> None:
        user_text = ""
        if context.message and context.message.parts:
            for part in context.message.parts:
                if part.root and hasattr(part.root, "text"):
                    user_text += part.root.text + " "
        user_text = user_text.strip()

        # Extract applicant ID
        match = re.search(r"(APP-\d+)", user_text, re.IGNORECASE)
        applicant_id = match.group(1).upper() if match else None

        if not applicant_id or applicant_id not in APPLICANT_INDEX:
            available = ", ".join(sorted(APPLICANT_INDEX.keys()))
            error_text = (
                f"Unknown applicant ID '{applicant_id or '(none)'}'. "
                f"Available IDs: {available}"
            )
            event_queue.enqueue_event(
                event_queue.build_result(
                    state=TaskState.completed,
                    message=Message(
                        role="agent",
                        parts=[Part(root=TextPart(text=error_text))],
                        messageId=uuid4().hex,
                    ),
                )
            )
            return

        application = APPLICANT_INDEX[applicant_id]
        report = await self._orchestrator.validate(application)
        result_text = str(report)

        event_queue.enqueue_event(
            event_queue.build_result(
                state=TaskState.completed,
                message=Message(
                    role="agent",
                    parts=[Part(root=TextPart(text=result_text))],
                    messageId=uuid4().hex,
                ),
            )
        )

    def cancel(self, context, event_queue: EventQueue) -> None:
        event_queue.enqueue_event(
            event_queue.build_result(
                state=TaskState.canceled,
                message=Message(
                    role="agent",
                    parts=[Part(root=TextPart(text="Validation cancelled."))],
                    messageId=uuid4().hex,
                ),
            )
        )


# ─── Agent Card ───────────────────────────────────────────────────────────────

SKILL = AgentSkill(
    id="loan-validation",
    name="Loan Application Pre-Screening",
    description="Run hard-fail and advisory rule checks on a mortgage application, then generate a structured validation report.",
    tags=["loan", "validation", "mortgage", "crewai"],
    examples=[
        "Validate loan application APP-1001",
        "Run pre-screening for APP-1002",
    ],
)

AGENT_CARD = AgentCard(
    name="LoanValidatorCrewAI",
    description="Mortgage application pre-screening agent powered by CrewAI and Kimi-K2.",
    url=f"http://{SERVER_HOST}:{SERVER_PORT}",
    version="1.0.0",
    skills=[SKILL],
    defaultInputModes=["text"],
    defaultOutputModes=["text"],
)


# ─── main ─────────────────────────────────────────────────────────────────────


def main() -> None:
    executor = LoanValidatorExecutor()
    request_handler = DefaultRequestHandler(
        agent_executor=executor,
        task_store=InMemoryTaskStore(),
    )

    a2a_app = A2AStarletteApplication(
        agent_card=AGENT_CARD,
        http_handler=request_handler,
    )

    import uvicorn

    print(f"🚀 CrewAI Loan Validator A2A server on http://{SERVER_HOST}:{SERVER_PORT}")
    uvicorn.run(a2a_app.build(), host=SERVER_HOST, port=SERVER_PORT)


if __name__ == "__main__":
    main()
