# Sequential Agents Pattern

[![Watch: The Sequential AI Agent Blueprint](https://img.youtube.com/vi/XaiCXeeyNzQ/maxresdefault.jpg)](https://www.youtube.com/watch?v=XaiCXeeyNzQ)

> **Watch the video:** [The Sequential AI Agent Blueprint](https://www.youtube.com/watch?v=XaiCXeeyNzQ)
> **Website:** [LocalM Tuts](https://tuts.localm.dev/)

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
ollama pull qwen3.5:0.8b
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

## Series Navigation

| # | Pattern | Video | Example |
|---|---------|-------|---------|
| 01 | Single Agent | [Watch](https://www.youtube.com/watch?v=j98Csy8DbPo) | [Code](../01-single-agent/) |
| **02** | **Sequential Agents** (this) | [Watch](https://www.youtube.com/watch?v=XaiCXeeyNzQ) | — |
| 03 | Parallel Agents | [Watch](https://www.youtube.com/watch?v=trrAd7zXVqI) | [Code](../03-parallel-agents/) |
| 04 | Coordinator | [Watch](https://www.youtube.com/watch?v=N05AycfgBPc) | [Code](../../agent-design-patterns-2/04-coordinator/) |
| 05 | Agent-as-Tool | [Watch](https://www.youtube.com/watch?v=fG-0_nCm3K8) | [Code](../../agent-design-patterns-2/05-agent-as-tool/) |
| 06 | Loop & Critique | [Watch](https://www.youtube.com/watch?v=SSJ_c77bJSY) | [Code](../../agent-design-patterns-2/06-loop-and-critique/) |
