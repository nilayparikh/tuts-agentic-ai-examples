# Lesson 06 — Wrapping Agents as A2A Servers

Transform the standalone QAAgent from Lesson 5 into a fully **A2A-compliant server**.

## What You'll Build

An A2A server that:

- Wraps `QAAgent` with the `AgentExecutor` interface
- Serves an Agent Card at `/.well-known/agent.json`
- Handles JSON-RPC requests via `A2AStarletteApplication`
- Runs on `localhost:10001`

## Prerequisites

1. Complete [Lesson 05](../05-first-a2a-agent/) (QAAgent)
2. Install the A2A SDK:
   ```bash
   pip install "a2a-sdk[http-server]"
   ```
3. `GITHUB_TOKEN` environment variable set

## Setup

```bash
cd src
pip install "a2a-sdk[http-server]" openai python-dotenv
```

## Run

**Start the server:**

```bash
cd src
python server.py
# Server running at http://localhost:10001
# Agent Card at http://localhost:10001/.well-known/agent.json
```

**Test with curl:**

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

**Notebook:** Open `a2a_server.ipynb` for an interactive walkthrough of each component.

## Files

| File                            | Description                                  |
| ------------------------------- | -------------------------------------------- |
| `src/a2a_server.ipynb`          | Interactive notebook walkthrough             |
| `src/server.py`                 | Runnable server script (start with `python`) |
| `src/agent_executor.py`         | AgentExecutor wrapping QAAgent               |
| `src/data/insurance_policy.txt` | Knowledge base (copied from Lesson 5)        |

## Key Concepts

- **AgentExecutor** — A2A SDK's abstract interface between protocol and agent logic
- **Agent Card** — JSON manifest describing agent skills and capabilities
- **EventQueue** — Bridges agent output to A2A protocol events
- **`new_agent_text_message()`** — Helper that creates properly formatted text responses
- **A2AStarletteApplication** — Pre-built ASGI server from the A2A SDK

## A2A SDK Imports Reference

```python
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
```

## Next Steps

→ [Lesson 07](../07-a2a-client/) — Build a client that discovers and calls this server

> **Keep the server running** — you'll need it for Lesson 7!
