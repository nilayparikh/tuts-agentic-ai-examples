"""
Submit all eight test applicants through the loan approval pipeline.

Sends each application from the shared ``_common/src/loan_data.py`` fixtures
to the MasterOrchestrator and prints the results with a summary table.

Usage:
    python submit_test_batch.py
"""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

# Add _common/src to path for loan_data
_SRC = Path(__file__).parent.resolve()
_COMMON = (_SRC / "../../_common/src").resolve()
_LESSON_COMMON = (_SRC / "../../../_common/src").resolve()
sys.path.insert(0, str(_SRC))
sys.path.insert(0, str(_COMMON))
sys.path.insert(0, str(_LESSON_COMMON))

import httpx  # noqa: E402
from dotenv import find_dotenv, load_dotenv  # noqa: E402

load_dotenv(find_dotenv(raise_error_if_not_found=False))

# Import loan data from _common
try:
    from loan_data import APPLICANTS  # noqa: E402
except ImportError:
    print(
        "ERROR: Could not import loan_data. Make sure _common/src/loan_data.py exists."
    )
    sys.exit(1)

ORCHESTRATOR_URL = "http://localhost:10100/"

DECISION_SYMBOLS = {
    "APPROVED": "✅",
    "DECLINED": "❌",
    "PENDING_REVIEW": "👤",
    "REJECTED": "⛔",
}


async def submit_application(client: httpx.AsyncClient, app_dict: dict) -> dict:
    """Submit one application to the orchestrator via A2A JSON-RPC."""
    rpc_request = {
        "jsonrpc": "2.0",
        "id": f"batch-{app_dict['applicant_id']}",
        "method": "message/send",
        "params": {
            "message": {
                "role": "user",
                "parts": [{"kind": "text", "text": json.dumps(app_dict)}],
                "messageId": f"msg-{app_dict['applicant_id']}",
            }
        },
    }

    resp = await client.post(ORCHESTRATOR_URL, json=rpc_request, timeout=300.0)
    resp.raise_for_status()
    rpc_response = resp.json()

    # Extract text result — handle direct Message and Task responses
    result = rpc_response.get("result", {})

    # Direct Message response
    if result.get("kind") == "message":
        parts = result.get("parts", [])
        if parts:
            return json.loads(parts[0].get("text", "{}"))

    # Task response with artifacts
    artifacts = result.get("artifacts", [])
    if artifacts:
        parts = artifacts[0].get("parts", [])
        if parts:
            return json.loads(parts[0].get("text", "{}"))

    # Task response with status message
    status = result.get("status", {})
    message = status.get("message", {})
    parts = message.get("parts", [])
    if parts:
        return json.loads(parts[0].get("text", "{}"))

    return {"error": "No response from orchestrator"}


async def main() -> None:
    """Submit all test applicants and display results."""
    print("=" * 70)
    print("Multi-Agent Loan Approval Pipeline — Test Batch Submission")
    print("=" * 70)
    print()

    results: list[tuple[str, str, str, int | str]] = []

    async with httpx.AsyncClient() as client:
        for applicant in APPLICANTS:
            app_dict = applicant.to_dict()
            app_id = applicant.applicant_id
            name = applicant.full_name

            print(f"Submitting {name} ({app_id})…", end=" ", flush=True)

            try:
                result = await submit_application(client, app_dict)
                decision = result.get("decision", "UNKNOWN")
                score = result.get("score", "N/A")
                symbol = DECISION_SYMBOLS.get(decision, "❓")
                print(f"{symbol} {decision} (score: {score})")
                results.append((app_id, name, decision, score))
            except Exception as exc:  # pylint: disable=broad-except
                print(f"❗ Error: {exc}")
                results.append((app_id, name, "ERROR", "N/A"))

    # Summary table
    print()
    print("=" * 70)
    print(f"{'ID':<15} {'Name':<20} {'Decision':<18} {'Score':<6}")
    print("-" * 70)
    for app_id, name, decision, score in results:
        symbol = DECISION_SYMBOLS.get(decision, "❓")
        print(f"{app_id:<15} {name:<20} {symbol} {decision:<15} {score}")
    print("=" * 70)

    # Statistics
    total = len(results)
    approved = sum(1 for _, _, d, _ in results if d == "APPROVED")
    declined = sum(1 for _, _, d, _ in results if d == "DECLINED")
    escalated = sum(1 for _, _, d, _ in results if d == "PENDING_REVIEW")
    rejected = sum(1 for _, _, d, _ in results if d == "REJECTED")
    errors = sum(1 for _, _, d, _ in results if d == "ERROR")

    print()
    print(f"Total: {total}")
    print(f"  Auto-Approved  : {approved} ({approved/total*100:.0f}%)")
    print(f"  Auto-Declined  : {declined} ({declined/total*100:.0f}%)")
    print(f"  Escalated      : {escalated} ({escalated/total*100:.0f}%)")
    if rejected:
        print(f"  Rejected       : {rejected}")
    if errors:
        print(f"  Errors         : {errors}")


if __name__ == "__main__":
    asyncio.run(main())
