# Lesson 06 — Wrapping Agents as A2A Servers

Transform the standalone QAAgent from Lesson 5 into a fully **A2A-compliant server**.

## What You'll Build

An A2A server that:

- Wraps `QAAgent` with the `AgentExecutor` interface
- Serves an Agent Card at `/.well-known/agent-card.json`
- Handles JSON-RPC requests via `A2AStarletteApplication`
- Runs on `localhost:10001`

## Prerequisites

1. Complete [Lesson 05](../05-first-a2a-agent/) (QAAgent)
2. Install the A2A SDK:
   ```bash
   pip install "a2a-sdk[http-server]"
   ```
3. Choose a model provider:

| Provider                    | Credential                                   |
| --------------------------- | -------------------------------------------- |
| **GitHub Models** (default) | `GITHUB_TOKEN` in `.env`                     |
| **AI Toolkit LocalFoundry** | Model running on port 5272 — no token needed |

Change `PROVIDER` in the notebook setup cell to switch providers.

## Setup

```bash
cd src
pip install "a2a-sdk[http-server]" openai python-dotenv
```

## Run

Open `a2a_server.ipynb` in Jupyter or VS Code and **run all cells** through the
server cell. The server starts on `localhost:10001` inside the notebook kernel.

**Test with curl** (while the server is running):

```bash
# Fetch Agent Card
curl http://localhost:10001/.well-known/agent.json | python -m json.tool

# Send a question
curl -X POST http://localhost:10001 \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "test-1",
    "method": "message/send",
    "params": {
      "message": {
        "role": "user",
        "parts": [{"kind": "text", "text": "What is the deductible?"}],
        "messageId": "msg-001"
      }
    }
  }'
```

## Files

| File                            | Description                           |
| ------------------------------- | ------------------------------------- |
| `src/a2a_server.ipynb`          | Self-contained server notebook        |
| `src/data/insurance_policy.txt` | Knowledge base (copied from Lesson 5) |

## Key Concepts

- **AgentExecutor** — A2A SDK's abstract interface between protocol and agent logic
- **Agent Card** — JSON manifest describing agent skills and capabilities
- **EventQueue** — Bridges agent output to A2A protocol events
- **TaskStatusUpdateEvent** — Emits state transitions (working, completed, input_required)
- **A2AStarletteApplication** — Pre-built ASGI server from the A2A SDK

## A2A SDK Imports Reference

```python
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
```

## Next Steps

→ [Lesson 07](../07-a2a-client/) — Build a client that discovers and calls this server

> **Keep the server running** — you'll need it for Lesson 7!
