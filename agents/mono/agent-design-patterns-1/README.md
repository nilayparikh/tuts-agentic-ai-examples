# Agent Design Patterns Part 1 — Foundational Patterns

Runnable examples for the foundational patterns in the AI Agent Design Patterns
mono series.

## Patterns

| #   | Pattern           | Folder                  | Ports       |
| --- | ----------------- | ----------------------- | ----------- |
| 01  | Single Agent      | `01-single-agent/`      | 11100       |
| 02  | Sequential Agents | `02-sequential-agents/` | 11201-11203 |
| 03  | Parallel Agents   | `03-parallel-agents/`   | 11301-11305 |

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
cd _examples/agents/mono/agent-design-patterns-1/01-single-agent
python util.py --start
python client.py
python util.py --stop
```

Each subfolder contains its own `util.py`, `client.py`, and README.
