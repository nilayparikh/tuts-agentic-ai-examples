"""
MasterOrchestrator — Discover and route loan applications through the pipeline.

Discovers all five specialized agents via A2ACardResolver, then routes
each loan application sequentially through intake → risk scoring →
compliance → decision → (optional) escalation.

Environment variables
---------------------
  Uses same model/API keys as child agents for any direct LLM calls.
"""

from __future__ import annotations

import json
import logging
import time

import httpx

from telemetry import tracer, inject_trace_context

logger = logging.getLogger("orchestrator")


# ── Agent port map ────────────────────────────────────────────────────────────

AGENT_PORTS = {
    "intake": 10101,
    "risk_scorer": 10102,
    "compliance": 10103,
    "decision": 10104,
    "escalation": 10105,
}


class MasterOrchestrator:
    """Discover agents via A2A and route loan applications through the pipeline."""

    def __init__(self) -> None:
        self._agent_cards: dict[str, dict] = {}

    async def discover_agents(self) -> dict[str, dict]:
        """Fetch Agent Cards from all pipeline agents."""
        with tracer.start_as_current_span("discover_agents") as span:
            logger.info("Discovering pipeline agents…")
            async with httpx.AsyncClient(timeout=10.0) as client:
                for name, port in AGENT_PORTS.items():
                    try:
                        url = f"http://localhost:{port}/.well-known/agent.json"
                        resp = await client.get(url)
                        resp.raise_for_status()
                        self._agent_cards[name] = resp.json()
                        span.set_attribute(f"agent.{name}.discovered", True)
                        logger.info(
                            "  ✅ %s discovered on port %d",
                            name,
                            port,
                        )
                    except Exception as exc:  # pylint: disable=broad-except
                        span.set_attribute(f"agent.{name}.discovered", False)
                        span.set_attribute(f"agent.{name}.error", str(exc))
                        logger.error(
                            "  ❌ %s failed on port %d: %s",
                            name,
                            port,
                            exc,
                        )

            span.set_attribute("agents_discovered", len(self._agent_cards))
            logger.info(
                "Discovery complete: %d/%d agents found",
                len(self._agent_cards),
                len(AGENT_PORTS),
            )
            return self._agent_cards

    async def process_application(self, application: dict) -> dict:
        """Run a loan application through the full agent pipeline.

        Returns the final decision result including any escalation info.
        """
        with tracer.start_as_current_span("process_application") as span:
            app_id = application.get("applicant_id", "unknown")
            span.set_attribute("applicant_id", app_id)
            pipeline_start = time.perf_counter()

            logger.info("")
            logger.info("=" * 70)
            logger.info(
                "[%s] PIPELINE START — %s",
                app_id,
                application.get("full_name", "Unknown"),
            )
            logger.info("=" * 70)

            # Step 1: Intake validation
            step_start = time.perf_counter()
            logger.info("[%s] Step 1/5: IntakeAgent ─ validating…", app_id)
            intake_result = await self._call_agent("intake", json.dumps(application))
            intake_data = json.loads(intake_result)
            step_ms = (time.perf_counter() - step_start) * 1000
            logger.info("[%s] Step 1/5: IntakeAgent done (%.0fms)", app_id, step_ms)

            if not intake_data.get("valid", False):
                span.set_attribute("outcome", "REJECTED_INTAKE")
                logger.warning(
                    "[%s] PIPELINE ABORTED — intake validation failed: %s",
                    app_id,
                    intake_data.get("errors", []),
                )
                return {
                    "applicant_id": app_id,
                    "decision": "REJECTED",
                    "action": "INTAKE_REJECTED",
                    "reason": "Application failed intake validation",
                    "errors": intake_data.get("errors", []),
                }

            normalized_app = intake_data.get("application", application)

            # Step 2: Risk scoring
            step_start = time.perf_counter()
            logger.info("[%s] Step 2/5: RiskScorerAgent ─ scoring…", app_id)
            risk_result = await self._call_agent(
                "risk_scorer", json.dumps(normalized_app)
            )
            risk_data = json.loads(risk_result)
            step_ms = (time.perf_counter() - step_start) * 1000
            span.set_attribute("risk_score", risk_data.get("score", -1))
            logger.info(
                "[%s] Step 2/5: RiskScorerAgent done (%.0fms) — score=%s, category=%s",
                app_id,
                step_ms,
                risk_data.get("score"),
                risk_data.get("category"),
            )

            # Step 3: Compliance check
            step_start = time.perf_counter()
            logger.info("[%s] Step 3/5: ComplianceAgent ─ checking…", app_id)
            compliance_result = await self._call_agent(
                "compliance", json.dumps(normalized_app)
            )
            compliance_data = json.loads(compliance_result)
            step_ms = (time.perf_counter() - step_start) * 1000
            logger.info(
                "[%s] Step 3/5: ComplianceAgent done (%.0fms) — compliant=%s, flags=%d",
                app_id,
                step_ms,
                compliance_data.get("compliant"),
                len(compliance_data.get("flags", [])),
            )

            # Step 4: Decision
            step_start = time.perf_counter()
            logger.info("[%s] Step 4/5: DecisionAgent ─ routing…", app_id)
            decision_input = {
                "applicant_id": app_id,
                "application": normalized_app,
                **risk_data,
                "compliant": compliance_data.get("compliant", True),
                "flags": compliance_data.get("flags", []),
                "conditions": compliance_data.get("conditions", []),
                "exceptions": compliance_data.get("exceptions", []),
            }
            decision_result = await self._call_agent(
                "decision", json.dumps(decision_input)
            )
            decision_data = json.loads(decision_result)
            step_ms = (time.perf_counter() - step_start) * 1000
            span.set_attribute("decision", decision_data.get("decision", "UNKNOWN"))
            logger.info(
                "[%s] Step 4/5: DecisionAgent done (%.0fms) — decision=%s, action=%s",
                app_id,
                step_ms,
                decision_data.get("decision"),
                decision_data.get("action"),
            )

            # Step 5: Escalation if needed
            if decision_data.get("action") == "ESCALATE":
                step_start = time.perf_counter()
                logger.info(
                    "[%s] Step 5/5: EscalationAgent ─ queuing for review…", app_id
                )
                escalation_input = {
                    **decision_data,
                    "application": normalized_app,
                }
                escalation_result = await self._call_agent(
                    "escalation", json.dumps(escalation_input)
                )
                escalation_data = json.loads(escalation_result)
                decision_data["escalation"] = escalation_data
                span.set_attribute("escalated", True)
                step_ms = (time.perf_counter() - step_start) * 1000
                logger.info(
                    "[%s] Step 5/5: EscalationAgent done (%.0fms) — escalation_id=%s",
                    app_id,
                    step_ms,
                    escalation_data.get("escalation_id"),
                )
            else:
                span.set_attribute("escalated", False)
                logger.info("[%s] Step 5/5: Escalation skipped (auto-decided)", app_id)

            total_ms = (time.perf_counter() - pipeline_start) * 1000
            logger.info("")
            logger.info(
                "[%s] PIPELINE COMPLETE — %s in %.0fms",
                app_id,
                decision_data.get("decision", "UNKNOWN"),
                total_ms,
            )
            logger.info("=" * 70)

            return decision_data

    async def _call_agent(self, agent_name: str, payload: str) -> str:
        """Send a task to an A2A agent and return the text response."""
        port = AGENT_PORTS[agent_name]
        url = f"http://localhost:{port}/"
        headers = {
            "Content-Type": "application/json",
            **inject_trace_context(),
        }

        # JSON-RPC request for message/send
        rpc_request = {
            "jsonrpc": "2.0",
            "id": f"{agent_name}-task",
            "method": "message/send",
            "params": {
                "message": {
                    "role": "user",
                    "parts": [{"kind": "text", "text": payload}],
                    "messageId": f"msg-{agent_name}",
                }
            },
        }

        with tracer.start_as_current_span(f"call_{agent_name}") as span:
            span.set_attribute("agent.name", agent_name)
            span.set_attribute("agent.port", port)
            logger.debug("  → calling %s on :%d …", agent_name, port)
            call_start = time.perf_counter()

            try:
                async with httpx.AsyncClient(timeout=90.0) as client:
                    resp = await client.post(url, json=rpc_request, headers=headers)
                    resp.raise_for_status()
                    rpc_response = resp.json()
            except Exception:
                logger.exception("  ✗ %s call FAILED (:%d)", agent_name, port)
                raise

            call_ms = (time.perf_counter() - call_start) * 1000
            logger.debug(
                "  ← %s responded in %.0fms (HTTP %d)",
                agent_name,
                call_ms,
                resp.status_code,
            )

            # Extract text from the A2A response
            result = rpc_response.get("result", {})

            # Direct Message response: result.kind == "message" with result.parts
            if result.get("kind") == "message":
                parts = result.get("parts", [])
                if parts:
                    return parts[0].get("text", "{}")

            # Task response with artifacts
            artifacts = result.get("artifacts", [])
            if artifacts:
                parts = artifacts[0].get("parts", [])
                if parts:
                    return parts[0].get("text", "{}")

            # Task response with status message
            status = result.get("status", {})
            message = status.get("message", {})
            parts = message.get("parts", [])
            if parts:
                return parts[0].get("text", "{}")

            logger.warning("  ⚠ %s returned empty payload", agent_name)
            return "{}"
