# A2A Protocol — Code Examples

Working code examples for the **Agent-to-Agent (A2A) Protocol** tutorial series.
Ten progressive lessons build from a standalone LLM agent to a multi-framework
A2A deployment, culminating in a full loan approval pipeline with six agents
and a React dashboard.

## Lesson Map

```mermaid
graph LR
    L05["Lesson 05\nQA Agent\nStandalone · Phi-4"]
    L06["Lesson 06\nA2A Server\nAgentExecutor · port 10001"]
    L07["Lesson 07\nA2A Client\nDiscover · Query · Stream"]
    L08["Lesson 08\nMS Agent Framework\nOrchestration · port 10008"]
    L09["Lesson 09\nGoogle ADK\nto_a2a() · port 10002"]
    L10["Lesson 10\nLangGraph\nReAct · port 10003"]
    L11["Lesson 11\nCrewAI\nCrew · port 10004"]
    L12["Lesson 12\nOpenAI Agents\nSDK · port 10005"]
    L13["Lesson 13\nClaude Agent\nStyle · port 10006"]
    L14["Lesson 14\nCapstone\n6 agents · React UI"]

    L05 -->|wrapped by| L06
    L06 -->|called by| L07
    L05 -.->|same pattern| L08
    L05 -.->|same pattern| L09
    L08 -.->|same problem| L10 & L11 & L12 & L13
    L10 & L11 & L12 & L13 -.->|capstone| L14

    style L05 fill:#dbeafe,stroke:#3b82f6
    style L06 fill:#dcfce7,stroke:#22c55e
    style L07 fill:#dcfce7,stroke:#22c55e
    style L08 fill:#fef3c7,stroke:#f59e0b
    style L09 fill:#fce7f3,stroke:#ec4899
    style L10 fill:#ede9fe,stroke:#8b5cf6
    style L11 fill:#ede9fe,stroke:#8b5cf6
    style L12 fill:#ede9fe,stroke:#8b5cf6
    style L13 fill:#ede9fe,stroke:#8b5cf6
    style L14 fill:#fef9c3,stroke:#eab308
```

| Lesson | Folder                                  | What you build                                    | Port        |
| ------ | --------------------------------------- | ------------------------------------------------- | ----------- |
| 05     | `lessons/05-first-a2a-agent/`           | Standalone `QAAgent` class with Phi-4             | —           |
| 06     | `lessons/06-a2a-server/`                | `AgentExecutor` + Agent Card + A2A server         | 10001       |
| 07     | `lessons/07-a2a-client/`                | `ClientFactory` discover + send + stream          | —           |
| 08     | `lessons/08-microsoft-agent-framework/` | `OrchestratorAgent` (MAF + Kimi-K2)               | 10008       |
| 09     | `lessons/09-google-adk/`                | `LlmAgent` + `to_a2a()` one-liner (ADK)           | 10002       |
| 10     | `lessons/10-langgraph/`                 | LangGraph ReAct agent as A2A server               | 10003       |
| 11     | `lessons/11-crewai/`                    | CrewAI role-based crew as A2A server              | 10004       |
| 12     | `lessons/12-openai-agents-sdk/`         | OpenAI Agents SDK agent as A2A server             | 10005       |
| 13     | `lessons/13-claude-agent-sdk/`          | Claude-style agent patterns as A2A server         | 10006       |
| 14     | `lessons/14-multi-agent-deep-dive/`     | Full loan approval pipeline — 6 agents + React UI | 10100–10105 |

---

## Model Provider Options

All notebooks and the lesson scripts support two providers. No Azure or Google Cloud
account is required if you use either of these free options.

```mermaid
graph TD
    NB["Notebook / Script"]
    NB -->|"PROVIDER = 'github'"| GH["GitHub Models\nhttps://models.inference.ai.azure.com\nRequires: GITHUB_TOKEN"]
    NB -->|"PROVIDER = 'localfoundry'"| LF["AI Toolkit LocalFoundry\nhttp://localhost:5272/v1/\nRequires: VS Code AI Toolkit + loaded model"]
```

### GitHub Models (default)

1. Go to [github.com/settings/tokens](https://github.com/settings/tokens) → **Generate new token (classic)**
2. No scopes required — a token with no permissions works
3. Copy the token to `_examples/.env`:
   ```dotenv
   GITHUB_TOKEN=ghp_your_token_here
   ```

### AI Toolkit LocalFoundry

1. Install the [VS Code AI Toolkit extension](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio)
2. Open AI Toolkit → **Models** → choose a model (e.g. `qwen2.5-0.5b-instruct-generic-gpu:4`) → **Load**
3. The server starts on `http://localhost:5272/v1/` — no token needed
4. In the notebook, change `PROVIDER = "localfoundry"` in cell 2

```python
# AI Toolkit LocalFoundry — OpenAI-compatible local server
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:5272/v1/",
    api_key="unused",   # required by the client but ignored by LocalFoundry
)
```

---

## Quick Start — Full Lesson Scripts

```powershell
# Windows — from _examples/a2a/
cd _examples/a2a
.\.venv\Scripts\Activate.ps1

python scripts/lesson_05.py   # standalone agent
python scripts/lesson_06.py   # starts server + smoke-tests agent card
python scripts/lesson_07.py   # client discover + send + stream demo
python scripts/lesson_08.py   # MAF orchestrator + A2A demo
python scripts/lesson_09.py   # ADK to_a2a() + A2A demo
```

```bash
# macOS / Linux
cd _examples/a2a
source .venv/bin/activate

python scripts/lesson_05.py
python scripts/lesson_06.py
python scripts/lesson_07.py
python scripts/lesson_08.py
python scripts/lesson_09.py
```

---

## Setup

### 1. Prerequisites

- Python 3.11+
- `uv` (recommended) or `pip`

### 2. Create the virtual environment

```powershell
# Windows
cd _examples/a2a
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

```bash
# macOS / Linux
cd _examples/a2a
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Or with `uv`:

```bash
cd _examples/a2a
uv venv
uv pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
cp ../.env.example ../.env
# edit ../.env
```

| Variable                         | Required for                                                   | Where to get                                                     |
| -------------------------------- | -------------------------------------------------------------- | ---------------------------------------------------------------- |
| `GITHUB_TOKEN`                   | Lessons 05–09 notebooks + scripts, Lesson 14 (GitHub provider) | [github.com/settings/tokens](https://github.com/settings/tokens) |
| `AZURE_AI_PROJECT_ENDPOINT`      | Lesson 08 full script (Kimi-K2-Thinking)                       | Azure AI Foundry portal                                          |
| `AZURE_AI_API_KEY`               | Lessons 08–13 full scripts                                     | Azure AI Foundry portal                                          |
| `AZURE_AI_MODEL_DEPLOYMENT_NAME` | Lessons 08–13 full scripts                                     | Azure AI Foundry portal                                          |
| `AZURE_OPENAI_ENDPOINT`          | Lessons 09–13 full scripts (Kimi-K2)                           | Azure AI Foundry portal                                          |

The `.env` file is **git-ignored** — never commit real credentials.

---

## Port Reference

| Port      | Agent                      | Lesson           |
| --------- | -------------------------- | ---------------- |
| 10001     | QAAgent                    | 06 · 07          |
| 10002     | LoanValidatorADK           | 09 (full script) |
| 10003     | LoanValidatorLangGraph     | 10 (full script) |
| 10004     | LoanValidatorCrewAI        | 11 (full script) |
| 10005     | LoanValidatorOpenAIAgents  | 12 (full script) |
| 10006     | LoanValidatorClaudeStyle   | 13 (full script) |
| 10008     | LoanValidatorOrchestrator  | 08 (full script) |
| 10100     | LoanApprovalOrchestrator   | 14 (capstone)    |
| 10101–105 | Capstone specialist agents | 14 (capstone)    |
| 8080      | Escalation REST API        | 14 (capstone)    |
| 3000      | React approval dashboard   | 14 (capstone)    |

---

## Repository Structure

```
a2a/
  lessons/
    README.md                           ← per-lesson overview + system diagrams
    _common/src/                        ← shared loan data + validation rules
    05-first-a2a-agent/src/             ← QAAgent class
    06-a2a-server/src/                  ← AgentExecutor + server
    07-a2a-client/src/                  ← ClientFactory + client
    08-microsoft-agent-framework/src/   ← OrchestratorAgent + server/client scripts
    09-google-adk/src/                  ← LlmAgent + to_a2a() + server/client scripts
    10-langgraph/src/                   ← LangGraph ReAct agent + server/client
    11-crewai/src/                      ← CrewAI crew + server/client
    12-openai-agents-sdk/src/           ← OpenAI Agents SDK + server/client
    13-claude-agent-sdk/src/            ← Claude-style patterns + server/client
    14-multi-agent-deep-dive/           ← Full loan pipeline: agents/ + ui/
  scripts/
    lesson_05.py … lesson_09.py        ← interactive lesson runner scripts
    README.md
  requirements.txt
  pyproject.toml
```

See [`lessons/README.md`](lessons/README.md) for detailed diagrams of the full system
architecture and the A2A round-trip sequence.
