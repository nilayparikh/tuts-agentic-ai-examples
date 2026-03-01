"""
MasterOrchestrator A2A Server — port 10100.

Wraps MasterOrchestrator as a standards-compliant A2A server. Accepts
loan application JSON and routes through the full agent pipeline.
After each run it pushes a summary record to the Escalation REST API
so the React dashboard can display all processed loans.

Usage:
    python orchestrator_server.py
"""

# pylint: disable=wrong-import-position,wrong-import-order

import json
import logging
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]

_SRC = Path(__file__).parent.resolve()
sys.path.insert(0, str(_SRC))

import httpx  # noqa: E402
import uvicorn  # noqa: E402
from dotenv import find_dotenv, load_dotenv  # noqa: E402

load_dotenv(find_dotenv(raise_error_if_not_found=False))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)-18s %(levelname)-7s %(message)s",
    datefmt="%H:%M:%S",
)

from a2a.server.agent_execution import AgentExecutor, RequestContext  # noqa: E402
from a2a.server.apps import A2AStarletteApplication  # noqa: E402
from a2a.server.events import EventQueue  # noqa: E402
from a2a.server.request_handlers import DefaultRequestHandler  # noqa: E402
from a2a.server.tasks import InMemoryTaskStore  # noqa: E402
from a2a.types import AgentCapabilities, AgentCard, AgentSkill  # noqa: E402
from a2a.utils import new_agent_text_message  # noqa: E402

from orchestrator import MasterOrchestrator  # noqa: E402

SERVER_PORT = 10100


REST_API_URL = "http://localhost:8080/api/loans"
logger = logging.getLogger("orchestrator_server")


class OrchestratorExecutor(AgentExecutor):
    """Bridge A2A protocol to MasterOrchestrator.process_application()."""

    def __init__(self) -> None:
        self._orchestrator = MasterOrchestrator()
        self._discovered = False

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """Handle an incoming A2A task — process a loan application."""
        # Lazy discovery on first request
        if not self._discovered:
            await self._orchestrator.discover_agents()
            self._discovered = True

        user_text = context.get_user_input().strip()

        try:
            application = json.loads(user_text)
        except json.JSONDecodeError:
            await event_queue.enqueue_event(
                new_agent_text_message(
                    '{"error": "Invalid JSON. Send a loan application object."}'
                )
            )
            return

        result = await self._orchestrator.process_application(application)

        # Push processed loan to dashboard REST API (best-effort, non-blocking)
        await _push_loan_record(application, result)

        await event_queue.enqueue_event(
            new_agent_text_message(json.dumps(result, indent=2))
        )

    async def cancel(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """Cancellation is not supported."""
        raise NotImplementedError("cancel not supported")


async def _push_loan_record(application: dict, result: dict) -> None:
    """Best-effort POST of pipeline result to the Escalation REST API."""
    escalation_info = result.get("escalation", {})
    payload = {
        "applicant_id": result.get("applicant_id", application.get("applicant_id", "")),
        "full_name": application.get("full_name", "Unknown"),
        "decision": result.get("decision", "UNKNOWN"),
        "action": result.get("action", "UNKNOWN"),
        "reason": result.get("reason", ""),
        "score": result.get("score", 0),
        "compliant": result.get("compliant", True),
        "risk_factors": result.get("risk_factors", []),
        "compensating_factors": result.get("compensating_factors", []),
        "flags": result.get("flags", []),
        "conditions": result.get("conditions", []),
        "reasoning": result.get("reasoning", ""),
        "application_data": application,
        "thresholds": result.get("thresholds", {}),
        "escalation_id": escalation_info.get("escalation_id"),
        "decided_at": result.get("decided_at"),
    }
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(REST_API_URL, json=payload)
            if resp.status_code not in (200, 201):
                logger.warning("Loan history push failed: HTTP %d", resp.status_code)
    except Exception as exc:  # pylint: disable=broad-except
        logger.warning("Loan history push error (REST API may not be ready): %s", exc)


agent_card = AgentCard(
    name="LoanApprovalOrchestrator",
    description=(
        "Multi-agent loan approval pipeline. Routes applications through "
        "intake, risk scoring, compliance, decisioning, and optional "
        "human-in-the-loop escalation."
    ),
    url=f"http://localhost:{SERVER_PORT}/",
    version="1.0.0",
    capabilities=AgentCapabilities(streaming=False),
    default_input_modes=["text"],
    default_output_modes=["text"],
    skills=[
        AgentSkill(
            id="process_loan",
            name="Process Loan Application",
            description=(
                "Run a loan application through the full multi-agent pipeline: "
                "intake → risk scoring → compliance → decision → escalation."
            ),
            tags=["loan", "approval", "orchestration", "multi-agent"],
            examples=["Process this loan application JSON"],
        )
    ],
)

request_handler = DefaultRequestHandler(
    agent_executor=OrchestratorExecutor(),
    task_store=InMemoryTaskStore(),
)

server = A2AStarletteApplication(
    agent_card=agent_card,
    http_handler=request_handler,
)

if __name__ == "__main__":
    print(f"Starting LoanApprovalOrchestrator A2A server on port {SERVER_PORT} …")
    print(f"  Agent Card : http://localhost:{SERVER_PORT}/.well-known/agent.json")
    print()
    print("Pipeline agents expected on:")
    print("  IntakeAgent       : http://localhost:10101/")
    print("  RiskScorerAgent   : http://localhost:10102/")
    print("  ComplianceAgent   : http://localhost:10103/")
    print("  DecisionAgent     : http://localhost:10104/")
    print("  EscalationAgent   : http://localhost:10105/")
    print()
    uvicorn.run(server.build(), host="0.0.0.0", port=SERVER_PORT)
