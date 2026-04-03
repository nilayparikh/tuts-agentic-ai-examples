"""Client for the Agent-as-Tool pattern demo.

Sends a trip planning query to the Primary Agent which uses
sub-agents as tools to gather food, transport, and attraction data.

Usage:
    python client.py
"""

import json
import sys

import httpx

AGENT_URL = "http://127.0.0.1:11424/"
AGENT_CARD_URL = "http://127.0.0.1:11424/.well-known/agent-card.json"

QUERIES = [
    "Plan a day trip to San Francisco. I need food, transport, and things to see.",
]


def _print_json_block(label: str, payload: dict) -> None:
    """Print a formatted JSON payload for request/response tracing."""
    print(label)
    print(json.dumps(payload, indent=2))
    print()


def discover_agent() -> dict:
    """Fetch and display the agent card."""
    print("=" * 60)
    print("  Agent-as-Tool Pattern - Client")
    print("=" * 60)
    print()
    print("-- Discovering agent...")
    print(f"   GET {AGENT_CARD_URL}")

    resp = httpx.get(AGENT_CARD_URL, timeout=10.0)
    if resp.status_code != 200:
        print(f"ERROR: Agent card fetch failed (status {resp.status_code})")
        sys.exit(1)

    card = resp.json()
    print(f"   HTTP {resp.status_code}")
    print(f"   Agent: {card.get('name', 'Unknown')}")
    print(f"   Description: {card.get('description', '')}")
    skills = card.get("skills", [])
    for skill in skills:
        print(f"   Skill: {skill.get('name', '')} - {skill.get('description', '')}")
    print()
    return card


def send_query(query: str, query_num: int) -> str:
    """Send a query via A2A JSON-RPC and return the response text."""
    print(f"-- Query {query_num}: {query}")
    print()
    print("   (Agent may call multiple sub-agents as tools - please wait...)")
    print()

    rpc_request = {
        "jsonrpc": "2.0",
        "id": f"tool-client-{query_num}",
        "method": "message/send",
        "params": {
            "message": {
                "role": "user",
                "parts": [{"kind": "text", "text": query}],
                "messageId": f"msg-tool-{query_num}",
            }
        },
    }

    print(f"   POST {AGENT_URL}")
    print(f"   RPC method: {rpc_request['method']}")
    print(f"   RPC id: {rpc_request['id']}")
    print(f"   Message id: {rpc_request['params']['message']['messageId']}")
    _print_json_block("-- Request Payload:", rpc_request)

    resp = httpx.post(AGENT_URL, json=rpc_request, timeout=300.0)
    print(f"   HTTP {resp.status_code}")
    rpc_response = resp.json()
    _print_json_block("-- Raw RPC Response:", rpc_response)

    result = rpc_response.get("result", {})
    text = ""
    if isinstance(result, dict):
        if result.get("kind") == "message":
            parts = result.get("parts", [])
            text = parts[0].get("text", "") if parts else ""
        artifacts = result.get("artifacts", [])
        if artifacts and not text:
            parts = artifacts[0].get("parts", [])
            text = parts[0].get("text", "") if parts else ""
        status = result.get("status", {})
        if not text:
            msg = status.get("message", {})
            if isinstance(msg, dict):
                parts = msg.get("parts", [])
                text = parts[0].get("text", "") if parts else ""

    if not text:
        text = json.dumps(result, indent=2)

    print("-- Response:")
    for line in text.split("\n"):
        print(f"   {line}")
    print()
    return text


def main() -> None:
    """Run the agent-as-tool client demo."""
    discover_agent()

    for i, query in enumerate(QUERIES, 1):
        print("-" * 60)
        send_query(query, i)

    print("=" * 60)
    print("  Agent-as-Tool Pattern demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
