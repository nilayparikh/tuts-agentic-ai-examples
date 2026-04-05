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

# No environment variables are required.
# These examples default to http://127.0.0.1:11434/v1 and qwen3.5:0.8b.
# Only set overrides if you want different values.
# set OLLAMA_BASE_URL=http://127.0.0.1:11434/v1
# set OLLAMA_MODEL=qwen3.5:0.8b
```

## Running

```bash
cd _examples/agents/mono/agent-design-patterns-1/01-single-agent
python util.py --start   # keep this terminal open
python client.py         # run from another terminal
# press Ctrl+C in the util.py terminal, or run: python util.py --stop
```

Each subfolder contains its own `util.py`, `client.py`, and README.
