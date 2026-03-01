"""
Start all agents for the multi-agent loan approval pipeline.

Launch all five specialized agents and the orchestrator as
separate subprocesses, then wait for them to be ready.

Usage:
    python start_all.py
"""

from __future__ import annotations

import asyncio
import os
import subprocess
import sys
import time
from pathlib import Path

import httpx
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(raise_error_if_not_found=False))

# ── Agent configuration ──────────────────────────────────────────────────────

_SRC = Path(__file__).parent.resolve()

AGENTS = [
    {"name": "IntakeAgent", "script": "intake_server.py", "port": 10101},
    {"name": "RiskScorerAgent", "script": "risk_scorer_server.py", "port": 10102},
    {"name": "ComplianceAgent", "script": "compliance_server.py", "port": 10103},
    {"name": "DecisionAgent", "script": "decision_server.py", "port": 10104},
    {"name": "EscalationAgent", "script": "escalation_server.py", "port": 10105},
    {"name": "Orchestrator", "script": "orchestrator_server.py", "port": 10100},
]


async def _wait_for_agent(name: str, port: int, timeout: float = 30.0) -> bool:
    """Poll an agent's Agent Card endpoint until it responds."""
    url = f"http://localhost:{port}/.well-known/agent.json"
    deadline = time.monotonic() + timeout
    async with httpx.AsyncClient() as client:
        while time.monotonic() < deadline:
            try:
                resp = await client.get(url, timeout=2.0)
                if resp.status_code == 200:
                    print(f"  ✅ {name} ready on port {port}")
                    return True
            except (httpx.ConnectError, httpx.ReadTimeout):
                pass
            await asyncio.sleep(0.5)
    print(f"  ❌ {name} failed to start on port {port}")
    return False


async def main() -> None:
    """Launch all agents and wait for readiness."""
    provider = os.getenv("PROVIDER", "github").lower()
    provider_labels = {
        "github": "GitHub Models (gpt-4o-mini)",
        "gh": "GitHub Models (gpt-4o-mini)",
        "microsoftfoundry": "Azure AI Foundry (Kimi-K2)",
        "azure": "Azure AI Foundry (Kimi-K2)",
        "microsoft": "Azure AI Foundry (Kimi-K2)",
        "localfoundry": "LocalFoundry / AI Toolkit",
        "local": "LocalFoundry / AI Toolkit",
        "ollama": "LocalFoundry / AI Toolkit",
    }
    provider_display = provider_labels.get(provider, f"Unknown ({provider})")

    print("=" * 60)
    print("Multi-Agent Loan Approval Pipeline — Startup")
    print("=" * 60)
    print()
    print(f"  LLM Provider : {provider_display}")
    print(f"  PROVIDER env : {provider}")
    print()

    # Logs directory — each agent writes to its own log file
    _LOGS = _SRC.parent / "logs"
    _LOGS.mkdir(exist_ok=True)

    procs: list[subprocess.Popen] = []

    for agent in AGENTS:
        script_path = _SRC / agent["script"]
        log_path = _LOGS / f"{agent['name'].lower()}.log"
        log_file = open(
            log_path, "w", encoding="utf-8"
        )  # pylint: disable=consider-using-with
        print(f"Starting {agent['name']} ({agent['script']}) on port {agent['port']}…")
        print(f"  Log: {log_path}")
        proc = subprocess.Popen(  # pylint: disable=consider-using-with
            [sys.executable, str(script_path)],
            cwd=str(_SRC),
            stdout=log_file,
            stderr=subprocess.STDOUT,
        )
        procs.append(proc)

    print()
    print("Waiting for agents to become ready…")
    print()

    results = await asyncio.gather(
        *[_wait_for_agent(a["name"], a["port"]) for a in AGENTS]
    )

    ready = sum(results)
    total = len(AGENTS)
    print()
    print(f"{ready}/{total} agents ready.")

    if ready < total:
        print(f"⚠️  Some agents failed to start. Check logs in: {_LOGS}")
    else:
        print()
        print("🚀 All agents running! Pipeline is ready.")
        print()
        print("  Orchestrator : http://localhost:10100/")
        print("  REST API     : http://localhost:8080/api/escalations/pending")
        print()
        print(f"  Agent logs   : {_LOGS}")
        print()
        print("Submit applications with:")
        print("  python submit_test_batch.py")
        print()

    print("Press Ctrl+C to stop all agents.")
    try:
        while True:
            await asyncio.sleep(1)
            # Check if any process has died
            for i, proc in enumerate(procs):
                if proc.poll() is not None:
                    print(f"⚠️  {AGENTS[i]['name']} exited with code {proc.returncode}")
    except KeyboardInterrupt:
        print()
        print("Shutting down all agents…")
        for proc in procs:
            proc.terminate()
        for proc in procs:
            proc.wait(timeout=5)
        print("All agents stopped.")


if __name__ == "__main__":
    asyncio.run(main())
