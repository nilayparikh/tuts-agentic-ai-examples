# Agent Design Patterns — Runnable Examples

Runnable Python examples for the **AI Agent Design Patterns** mono video series.

## Series

- [Part 1 overview](mono/agent-design-patterns-1/README.md)
- [Part 2 overview](mono/agent-design-patterns-2/README.md)
- <a href="https://tuts.localm.dev/" target="_blank" rel="noopener noreferrer">Series website</a>

## Setup

```bash
cd _examples/agents
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

## Prerequisites

- **Ollama** running locally at `http://127.0.0.1:11434`
- Model pulled: `ollama pull qwen3.5:0.8b`

## Examples

### Part 1 — Foundational Patterns

| Pattern           | Folder                                               | Description                                 | Video |
| ----------------- | ---------------------------------------------------- | ------------------------------------------- | ----- |
| Single Agent      | `mono/agent-design-patterns-1/01-single-agent/`      | One LLM agent with tools, dynamic execution | <a href="https://www.youtube.com/watch?v=j98Csy8DbPo" target="_blank" rel="noopener noreferrer">Watch</a> |
| Sequential Agents | `mono/agent-design-patterns-1/02-sequential-agents/` | Fixed pipeline of chained A2A agents        | <a href="https://www.youtube.com/watch?v=XaiCXeeyNzQ" target="_blank" rel="noopener noreferrer">Watch</a> |
| Parallel Agents   | `mono/agent-design-patterns-1/03-parallel-agents/`   | Concurrent A2A agents with aggregation      | <a href="https://www.youtube.com/watch?v=trrAd7zXVqI" target="_blank" rel="noopener noreferrer">Watch</a> |

### Part 2 — Advanced Patterns

| Pattern             | Folder                                               | Description                               | Video |
| ------------------- | ---------------------------------------------------- | ----------------------------------------- | ----- |
| Coordinator Routing | `mono/agent-design-patterns-2/04-coordinator/`       | LLM-driven dynamic routing to specialists | <a href="https://www.youtube.com/watch?v=N05AycfgBPc" target="_blank" rel="noopener noreferrer">Watch</a> |
| Agent-as-Tool       | `mono/agent-design-patterns-2/05-agent-as-tool/`     | Sub-agents as stateless tool calls        | <a href="https://www.youtube.com/watch?v=fG-0_nCm3K8" target="_blank" rel="noopener noreferrer">Watch</a> |
| Loop & Critique     | `mono/agent-design-patterns-2/06-loop-and-critique/` | Iterative refinement with quality gate    | <a href="https://www.youtube.com/watch?v=SSJ_c77bJSY" target="_blank" rel="noopener noreferrer">Watch</a> |

## Port Assignments

| Port  | Agent                   | Pattern              |
| ----- | ----------------------- | -------------------- |
| 11100 | Single agent server     | 01-single-agent      |
| 11201 | Food finder agent       | 02-sequential-agents |
| 11202 | Transport agent         | 02-sequential-agents |
| 11203 | Sequential orchestrator | 02-sequential-agents |
| 11301 | Museum finder agent     | 03-parallel-agents   |
| 11302 | Concert finder agent    | 03-parallel-agents   |
| 11303 | Restaurant finder agent | 03-parallel-agents   |
| 11304 | Synthesizer agent       | 03-parallel-agents   |
| 11305 | Parallel orchestrator   | 03-parallel-agents   |
| 11401 | Generator agent         | 06-loop-and-critique |
| 11402 | Critic agent            | 06-loop-and-critique |
| 11403 | Loop orchestrator       | 06-loop-and-critique |
| 11411 | Food agent              | 04-coordinator       |
| 11412 | Transport agent         | 04-coordinator       |
| 11413 | Cost agent              | 04-coordinator       |
| 11414 | Coordinator             | 04-coordinator       |
| 11421 | Food finder tool        | 05-agent-as-tool     |
| 11422 | Transport finder tool   | 05-agent-as-tool     |
| 11423 | Nearby finder tool      | 05-agent-as-tool     |
| 11424 | Primary agent           | 05-agent-as-tool     |

## Running Each Example

Each example has a `util.py` with `--start` and `--stop` commands:

```bash
# Set up the shared example environment once
cd _examples/agents
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt
ollama pull qwen3.5:0.8b

# Start all agents for the example
python util.py --start

# In another terminal, run the client
python client.py

# Stop all agents
python util.py --stop
```
