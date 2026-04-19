# Single Agent Pattern

[![Watch: Single AI Agent Pattern](https://img.youtube.com/vi/j98Csy8DbPo/maxresdefault.jpg)](https://www.youtube.com/watch?v=j98Csy8DbPo)

## Quick Links

- <a href="https://www.youtube.com/watch?v=j98Csy8DbPo" target="_blank" rel="noopener noreferrer">Watch the video</a>
- [Part 1 overview](../README.md)
- <a href="https://tuts.localm.dev/" target="_blank" rel="noopener noreferrer">Series website</a>

One LLM agent with tools that dynamically decides execution order.

## Architecture

```mermaid
graph LR
    U[User] -->|trip query| A[Trip Planner Agent]
    A -->|calls| T1[search_attractions]
    A -->|calls| T2[search_restaurants]
    A -->|calls| T3[get_weather]
    A -->|response| U
```

## Setup

```bash
cd _examples/agents/mono/agent-design-patterns-1
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt
ollama pull qwen3.5:0.8b
```

## Running

```bash
# Terminal 1 — start agent server
cd _examples/agents/mono/agent-design-patterns-1/01-single-agent
python util.py --start

# Terminal 2 — run client
python client.py

# Stop server from Terminal 1 with Ctrl+C,
# or from any terminal with:
python util.py --stop
```

## Port Assignment

| Port  | Service                |
| ----- | ---------------------- |
| 11100 | Trip Planner A2A Agent |

## Series Links

- Current pattern: Single Agent
- Next pattern: [Sequential Agents](../02-sequential-agents/)
- Full series: [Part 1 overview](../README.md) and [Part 2 overview](../../agent-design-patterns-2/README.md)
