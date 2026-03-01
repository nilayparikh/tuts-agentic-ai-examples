# Lessons — A2A Protocol Examples

Progressive lessons building from a standalone LLM agent to a
multi-framework A2A deployment. Each lesson compiles and runs
independently. Lessons 08–13 all solve the **same loan validation
problem** using different agent frameworks — shared data and rules
live in `_common/src/`. Lesson 14 is a capstone that builds a full
multi-agent loan approval pipeline with a React dashboard.

---

## Lesson Progression

```mermaid
graph LR
    L05["<b>Lesson 05</b><br/>QA Agent<br/><i>Standalone · Phi-4</i>"]
    L06["<b>Lesson 06</b><br/>A2A Server<br/><i>AgentExecutor · port 10001</i>"]
    L07["<b>Lesson 07</b><br/>A2A Client<br/><i>Discover · Query · Stream</i>"]
    L08["<b>Lesson 08</b><br/>Microsoft Agent Framework<br/><i>Orchestration · port 10008</i>"]
    L09["<b>Lesson 09</b><br/>Google ADK<br/><i>to_a2a() one-liner · port 10002</i>"]

    L05 -->|"wrapped by"| L06
    L06 -->|"called by"| L07
    L05 -.->|"same pattern"| L08
    L05 -.->|"same pattern"| L09

    style L05 fill:#dbeafe,stroke:#3b82f6
    style L06 fill:#dcfce7,stroke:#22c55e
    style L07 fill:#dcfce7,stroke:#22c55e
    style L08 fill:#fef3c7,stroke:#f59e0b
    style L09 fill:#fce7f3,stroke:#ec4899
```

---

## Full System Architecture

```mermaid
graph TD
    subgraph "Lesson 05 — Standalone Agent"
        QA["QAAgent\n+ Phi-4 (GitHub Models)"]
    end

    subgraph "Lesson 06 — A2A Server (port 10001)"
        EX06["QAAgentExecutor\n(AgentExecutor)"]
        SRV06["A2AStarletteApplication\nAgent Card · JSON-RPC"]
        EX06 --> QA
        SRV06 --> EX06
    end

    subgraph "Lesson 07 — A2A Client"
        RES["ClientFactory\nDiscover Agent Card"]
        CLI07["Client\nsend_message()"]
        RES --> SRV06
        CLI07 --> SRV06
    end

    subgraph "Lesson 08 — MS Agent Framework (port 10008)"
        ORCH["OrchestratorAgent\n(MS AF + Kimi-K2-Thinking)"]
        EX08["LoanValidatorExecutor\n(AgentExecutor)"]
        SRV08["A2AStarletteApplication\nAgent Card · JSON-RPC"]
        EX08 --> ORCH
        SRV08 --> EX08
        CLI08["A2A Client\n(same protocol as L07)"]
        CLI08 --> SRV08
    end

    subgraph "Lesson 09 — Google ADK (port 10002)"
        LLMA["LlmAgent + FunctionTools\n(ADK + Kimi-K2)"]
        SRV09["to_a2a()\nAgent Card · JSON-RPC"]
        SRV09 --> LLMA
        CLI09["A2A Client\n(same protocol as L07)"]
        CLI09 --> SRV09
    end

    style QA fill:#dbeafe,stroke:#3b82f6
    style SRV06 fill:#dcfce7,stroke:#22c55e
    style SRV08 fill:#fef3c7,stroke:#f59e0b
    style SRV09 fill:#fce7f3,stroke:#ec4899
```

---

## Lessons at a Glance

| Lesson | Folder                          | What It Builds                                    | Port            | Model                  |
| ------ | ------------------------------- | ------------------------------------------------- | --------------- | ---------------------- |
| **05** | `05-first-a2a-agent/`           | Standalone QA agent — insurance policy Q&A        | —               | GitHub Phi-4           |
| **06** | `06-a2a-server/`                | A2A server wrapping the QA agent                  | **10001**       | GitHub Phi-4           |
| **07** | `07-a2a-client/`                | A2A client — discover, query, stream              | —               | _(client only)_        |
| **08** | `08-microsoft-agent-framework/` | Loan validator via MS Agent Framework             | **10008**       | Azure Kimi-K2-Thinking |
| **09** | `09-google-adk/`                | Loan validator via Google ADK `to_a2a()`          | **10002**       | Azure Kimi-K2-Thinking |
| **10** | `10-langgraph/`                 | Loan validator via LangGraph ReAct agent          | **10003**       | Azure Kimi-K2-Thinking |
| **11** | `11-crewai/`                    | Loan validator via CrewAI role-based crew         | **10004**       | Azure Kimi-K2-Thinking |
| **12** | `12-openai-agents-sdk/`         | Loan validator via OpenAI Agents SDK              | **10005**       | Azure Kimi-K2-Thinking |
| **13** | `13-claude-agent-sdk/`          | Loan validator via Claude-style agent patterns    | **10006**       | Azure Kimi-K2-Thinking |
| **14** | `14-multi-agent-deep-dive/`     | Full loan approval pipeline — 6 agents + React UI | **10100–10105** | GitHub gpt-4o-mini     |

---

## A2A Protocol Round-Trip

```mermaid
sequenceDiagram
    participant C as A2A Client
    participant S as A2A Server
    participant E as AgentExecutor
    participant A as Agent (LLM)

    C->>S: GET /.well-known/agent-card.json
    S-->>C: AgentCard (name, skills, capabilities)

    C->>S: POST / (JSON-RPC message/send)
    S->>E: execute(context, event_queue)
    E->>A: query / run / validate
    A-->>E: LLM response
    E-->>S: enqueue_agent_message()
    S-->>C: Task + Message (JSON-RPC response)
```

The **same client pattern** (Lesson 07) calls all three servers (Lessons 06, 08, 09).
The framework used to build the server is invisible to the client — that is A2A interoperability.

---

## Port Reference

| Port    | Lesson | Agent                     | Notes                                         |
| ------- | ------ | ------------------------- | --------------------------------------------- |
| `10001` | 06     | QAAgent                   | Insurance policy Q&A, GitHub Phi-4            |
| `10002` | 09     | LoanValidatorADK          | Google ADK, Azure Kimi-K2-Thinking            |
| `10003` | 10     | LoanValidatorLangGraph    | LangGraph ReAct, Azure Kimi-K2-Thinking       |
| `10004` | 11     | LoanValidatorCrewAI       | CrewAI crew, Azure Kimi-K2-Thinking           |
| `10005` | 12     | LoanValidatorOpenAIAgents | OpenAI Agents SDK, Azure Kimi-K2-Thinking     |
| `10006` | 13     | LoanValidatorClaudeStyle  | Claude-style patterns, Azure Kimi-K2-Thinking |
| `10008` | 08     | LoanValidatorOrchestrator | MS Agent Framework, Azure Kimi-K2-Thinking    |
| `10100` | 14     | LoanApprovalOrchestrator  | Capstone orchestrator, GitHub gpt-4o-mini     |
| `10101` | 14     | IntakeAgent               | Capstone — loan intake parsing                |
| `10102` | 14     | RiskScorerAgent           | Capstone — risk scoring                       |
| `10103` | 14     | ComplianceAgent           | Capstone — compliance checks                  |
| `10104` | 14     | DecisionAgent             | Capstone — approval/decline routing           |
| `10105` | 14     | EscalationAgent           | Capstone — human escalation + REST (8080)     |
| `3000`  | 14     | React UI                  | Capstone — approval dashboard                 |

---

## Model Providers

| Lessons                    | Provider                              | Model                                           | Auth                                     |
| -------------------------- | ------------------------------------- | ----------------------------------------------- | ---------------------------------------- |
| 05, 06, 07 + all notebooks | **GitHub Models** or **LocalFoundry** | `Phi-4` / `qwen2.5-0.5b-instruct-generic-gpu:4` | `GITHUB_TOKEN` **or** VS Code AI Toolkit |
| 08–13 _(full scripts)_     | **Azure AI Foundry**                  | `Kimi-K2-Thinking`                              | `AZURE_AI_API_KEY`                       |
| 14 _(capstone)_            | **GitHub Models**                     | `gpt-4o-mini`                                   | `GITHUB_TOKEN`                           |

---

## Quick Start

### Prerequisites

```bash
# From the a2a/ directory
uv venv .venv && uv pip install -r requirements.txt
# or: pip install -r requirements.txt
```

### Environment

```bash
cp .env.example .env   # then fill in values
```

Minimum for Lessons 05–07 and notebooks:

```dotenv
GITHUB_TOKEN=ghp_your_token_here
```

Additional for Lessons 08–13 scripts:

```dotenv
AZURE_OPENAI_ENDPOINT=https://<name>.openai.azure.com
AZURE_AI_API_KEY=<your-key>
AZURE_AI_MODEL_DEPLOYMENT_NAME=Kimi-K2-Thinking
```

### Interactive lesson scripts

```bash
# From a2a/scripts/
python lesson_05.py   # QA agent walkthrough
python lesson_06.py   # A2A server walkthrough
python lesson_07.py   # A2A client walkthrough
python lesson_08.py   # MAF orchestrator + live A2A demo
python lesson_09.py   # ADK one-liner + live A2A demo
```

### Notebooks (GitHub Models or LocalFoundry — no Azure needed)

Open in VS Code or Jupyter. Change `PROVIDER` in the setup cell to switch between
**GitHub Models** (`"github"`, default) and **AI Toolkit LocalFoundry** (`"localfoundry"`).

| Notebook                                | What it shows                             |
| --------------------------------------- | ----------------------------------------- |
| `05-first-a2a-agent/src/qa_agent.ipynb` | Build and test a standalone agent         |
| `06-a2a-server/src/a2a_server.ipynb`    | Wrap an agent as an A2A server            |
| `07-a2a-client/src/a2a_client.ipynb`    | Discover, query, and stream from a server |

---

## Framework Comparison (Lessons 08 vs 09)

```mermaid
graph LR
    subgraph "Lesson 08 — Microsoft Agent Framework"
        direction TB
        B1["1. Define tools\n(@tool decorator)"]
        B2["2. Create Agent\nAgent(tools=[...])"]
        B3["3. Implement AgentExecutor\n(30 lines)"]
        B4["4. Wire A2AStarletteApplication\n(20 lines)"]
        B1 --> B2 --> B3 --> B4
    end

    subgraph "Lesson 09 — Google ADK"
        direction TB
        A1["1. Define tools\n(plain functions)"]
        A2["2. Create LlmAgent\nLlmAgent(tools=[...])"]
        A3["3. One-liner server\nto_a2a(agent, port=X)"]
        A1 --> A2 --> A3
    end
```

| Aspect         | MS Agent Framework (L08)                           | Google ADK (L09)            |
| -------------- | -------------------------------------------------- | --------------------------- |
| Agent type     | `Agent(tools, client)`                             | `LlmAgent(tools, model)`    |
| LLM adapter    | `AzureOpenAIChatClient`                            | `LiteLlm` (any provider)    |
| A2A wiring     | Manual `AgentExecutor` + `A2AStarletteApplication` | `to_a2a(agent)`             |
| Lines to serve | ~50                                                | ~5                          |
| Control        | High — full executor control                       | Low — framework handles all |
| Best for       | Complex orchestration                              | Rapid prototyping           |

---

## File Map

```
lessons/
  README.md                                         ← This file
  _common/
    src/
      loan_data.py                                  ← LoanApplication + 8 test fixtures
      validation_rules.py                           ← Hard/soft check tools + policy lookup
  05-first-a2a-agent/
    README.md
    src/
      qa_agent.ipynb                                ← Self-contained agent notebook
      data/insurance_policy.txt
  06-a2a-server/
    README.md
    src/
      a2a_server.ipynb                              ← Self-contained server notebook (port 10001)
      data/insurance_policy.txt
  07-a2a-client/
    README.md
    src/
      a2a_client.ipynb                              ← Discover + query + stream
  08-microsoft-agent-framework/
    README.md
    src/
      server.py                                     ← A2A server (port 10008)
      client.py                                     ← A2A client
      orchestrator.py                               ← OrchestratorAgent (MS AF)
  09-google-adk/
    README.md
    src/
      server.py                                     ← A2A server (port 10002)
      client.py                                     ← A2A client
      orchestrator.py                               ← OrchestratorAgent (ADK LlmAgent)
  10-langgraph/
    README.md
    src/
      server.py                                     ← A2A server (port 10003)
      client.py                                     ← A2A client
      orchestrator.py                               ← OrchestratorAgent (LangGraph ReAct)
  11-crewai/
    README.md
    src/
      server.py                                     ← A2A server (port 10004)
      client.py                                     ← A2A client
      orchestrator.py                               ← OrchestratorAgent (CrewAI crew)
  12-openai-agents-sdk/
    README.md
    src/
      server.py                                     ← A2A server (port 10005)
      client.py                                     ← A2A client
      orchestrator.py                               ← OrchestratorAgent (OpenAI Agents)
  13-claude-agent-sdk/
    README.md
    src/
      server.py                                     ← A2A server (port 10006)
      client.py                                     ← A2A client
      orchestrator.py                               ← OrchestratorAgent (Claude-style)
  14-multi-agent-deep-dive/
    README.md
    WALKTHROUGH.md
    agents/
      src/
        model_provider.py                           ← Unified LLM provider abstraction
        telemetry.py                                ← OpenTelemetry setup
        intake_agent.py + intake_server.py          ← IntakeAgent (port 10101)
        risk_scorer.py + risk_scorer_server.py      ← RiskScorerAgent (port 10102)
        compliance_agent.py + compliance_server.py  ← ComplianceAgent (port 10103)
        decision_agent.py + decision_server.py      ← DecisionAgent (port 10104)
        escalation_agent.py + escalation_server.py  ← EscalationAgent (port 10105 + REST 8080)
        orchestrator.py + orchestrator_server.py    ← MasterOrchestrator (port 10100)
        start_all.py                                ← Launch all agents
        submit_test_batch.py                        ← Submit 8 test applications
    ui/
      src/                                          ← React approval dashboard (port 3000)
```

---

## License

[Mozilla Public License 2.0](../../LICENSE)
