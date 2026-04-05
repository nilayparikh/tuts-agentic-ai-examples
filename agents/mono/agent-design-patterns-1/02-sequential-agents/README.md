# Sequential Agents Pattern

Fixed pipeline of A2A agents executing in deterministic order.

## Architecture

```mermaid
graph LR
    U[User] -->|trip query| O[Orchestrator]
    O -->|Step 1| F[Food Finder Agent]
    F -->|food results| O
    O -->|Step 2 + food context| T[Transport Agent]
    T -->|transport plan| O
    O -->|combined plan| U
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
ollama pull gemma4:e2b
```

## Running

```bash
# Terminal 1 -- start all servers
cd _examples/agents/mono/agent-design-patterns-1/02-sequential-agents
python util.py --start

# Terminal 2 -- run client
python client.py

# Stop all servers from Terminal 1 with Ctrl+C,
# or from any terminal with:
python util.py --stop
```

## Port Assignments

| Port  | Service                 |
| ----- | ----------------------- |
| 11201 | Food Finder Agent       |
| 11202 | Transport Agent         |
| 11203 | Sequential Orchestrator |
