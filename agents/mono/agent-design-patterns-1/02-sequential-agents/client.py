"""Client for the Sequential Agents pattern.

Sends a trip-planning query to the orchestrator, which chains
FoodFinder -> Transport to produce a combined itinerary.

Usage:
    python client.py
"""

import asyncio
import json
import uuid

import httpx

ORCHESTRATOR_URL = "http://127.0.0.1:11203"


def _print_json_block(label: str, payload: dict) -> None:
    """Print a formatted JSON payload for request/response tracing."""
    print(label)
    print(json.dumps(payload, indent=2))
    print()


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


async def discover_agent(base_url: str) -> dict:
    """Fetch the agent card from the well-known endpoint."""
    url = f"{base_url}/.well-known/agent.json"
    print(f"[discovery] GET {url}")
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        card = resp.json()
    print(f"[discovery] HTTP {resp.status_code}")
    print(f"[discovery] Agent: {card.get('name', 'unknown')}")
    print(f"[discovery] Description: {card.get('description', 'N/A')}")
    return card


async def send_query(base_url: str, query: str) -> dict:
    """Send a message via A2A JSON-RPC to the orchestrator."""
    msg_id = str(uuid.uuid4())
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "message/send",
        "params": {
            "message": {
                "role": "user",
                "parts": [{"kind": "text", "text": query}],
                "messageId": msg_id,
            }
        },
    }

    print(f"\n{'=' * 60}")
    print(f"  Query: {query}")
    print(f"{'=' * 60}")
    print(f"[client] POST {base_url}")
    print(f"[client] RPC method: {payload['method']}")
    print(f"[client] RPC id: {payload['id']}")
    print(f"[client] Message id: {payload['params']['message']['messageId']}")
    _print_json_block("[client] Request payload:", payload)

    async with httpx.AsyncClient(timeout=120.0) as client:
        resp = await client.post(base_url, json=payload)
        resp.raise_for_status()
        result = resp.json()
    print(f"[client] HTTP {resp.status_code}")
    _print_json_block("[client] Raw RPC response:", result)

    # Extract text from response
    rpc_result = result.get("result", {})
    text = _extract_text(rpc_result)

    if text:
        print("\n--- Response ---")
        print(text)
    else:
        print(f"[client] Raw response: {json.dumps(result, indent=2)}")

    return result


async def main() -> None:
    """Run the sequential agent client demo."""
    print("=" * 60)
    print("  Sequential Agents Pattern - Client Demo")
    print("  Pipeline: FoodFinder -> Transport")
    print("=" * 60)

    # Discover the orchestrator
    await discover_agent(ORCHESTRATOR_URL)

    # Demo query
    queries = [
        "I'm visiting Tokyo for 2 days. Find great food spots and plan transport.",
        "Plan a food tour in Paris with transport between restaurants.",
    ]

    for query in queries:
        await send_query(ORCHESTRATOR_URL, query)
        print()

    print("=" * 60)
    print("  Demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
