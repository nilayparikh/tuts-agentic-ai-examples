# Multi-Agent Loan Approval System — Detailed Walkthrough

This document walks through every component of the capstone multi-agent loan
approval system. Read this alongside the source code to understand the
architecture, data flow, and key implementation patterns.

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Pipeline Flow](#2-pipeline-flow)
3. [Agent Deep Dive](#3-agent-deep-dive)
   - [IntakeAgent](#31-intakeagent-port-10101)
   - [RiskScorerAgent](#32-riskscoragent-port-10102)
   - [ComplianceAgent](#33-complianceagent-port-10103)
   - [DecisionAgent](#34-decisionagent-port-10104)
   - [EscalationAgent](#35-escalationagent-port-10105--8080)
4. [MasterOrchestrator](#4-masterorchestrator-port-10100)
5. [A2A Server Pattern](#5-a2a-server-pattern)
6. [OpenTelemetry Instrumentation](#6-opentelemetry-instrumentation)
7. [React UI](#7-react-ui)
   - [Approval Queue](#71-approval-queue)
   - [Telemetry Dashboard](#72-telemetry-dashboard)
8. [Data Model](#8-data-model)
9. [Configuration Reference](#9-configuration-reference)
10. [Extending the System](#10-extending-the-system)

---

## 1. System Overview

The loan approval system demonstrates how five specialized AI agents cooperate
via the A2A (Agent-to-Agent) protocol to process mortgage loan applications.
The system is designed around a key insight: **most decisions can be automated,
but edge cases need human judgment**.

### Design Principles

- **Pipeline architecture** — each agent performs one step, passing structured
  data to the next
- **80/20 split** — ~80% of applications resolved by AI, ~20% escalated
- **Full observability** — every agent call is traced with OpenTelemetry
- **A2A-native** — agents discover each other via Agent Cards and communicate
  using the A2A JSON-RPC protocol

### Technology Stack

| Layer         | Technology                          |
| ------------- | ----------------------------------- |
| Agent runtime | Python 3.10+, A2A SDK 0.3.24+       |
| LLM provider  | Azure AI Foundry (Kimi-K2-Thinking) |
| Tracing       | OpenTelemetry (OTLP + Console)      |
| REST API      | FastAPI + Uvicorn                   |
| Frontend      | React 19, Vite 6, Recharts          |
| Transport     | HTTP (A2A JSON-RPC, REST)           |

---

## 2. Pipeline Flow

When a loan application is submitted, it flows through five agents in sequence:

```
Application JSON
       │
       ▼
┌──────────────┐
│ IntakeAgent  │  Validates required fields, normalizes data,
│   (10101)    │  computes DTI and LTV ratios
└──────┬───────┘
       │  Validated & enriched application
       ▼
┌──────────────┐
│ RiskScorer   │  40% deterministic rules + 60% LLM reasoning
│   (10102)    │  → composite risk score (0–100)
└──────┬───────┘
       │  Score + reasoning + risk/compensating factors
       ▼
┌──────────────┐
│ Compliance   │  FHA / VA / Conventional regulatory checks
│   (10103)    │  → flags (hard/soft) + conditions
└──────┬───────┘
       │  Compliance report
       ▼
┌──────────────┐
│ Decision     │  Routes based on risk score thresholds:
│   (10104)    │  ≤40 → approve, ≥80 → decline, else escalate
└──────┬───────┘
       │ APPROVED / DECLINED / PENDING_REVIEW
       ▼
┌──────────────┐
│ Escalation   │  Stores escalated cases, serves REST API
│   (10105)    │  for the human review React UI
└──────────────┘
```

### Data Shape Through the Pipeline

Each agent adds structured data. By the time the Decision Agent acts,
the payload contains:

```json
{
  "intake": {
    "valid": true,
    "application": { "...normalized fields..." },
    "dti_ratio": 0.35,
    "ltv_ratio": 0.85
  },
  "risk": {
    "score": 62,
    "category": "ESCALATE",
    "reasoning": "Mixed signals: strong income but high LTV...",
    "risk_factors": ["LTV ratio above 80%"],
    "compensating_factors": ["Stable employment > 5 years"]
  },
  "compliance": {
    "loan_type": "conventional",
    "passed": true,
    "flags": [{"rule": "LTV_LIMIT", "severity": "soft", "message": "..."}],
    "conditions": ["PMI required for LTV > 80%"]
  },
  "decision": "PENDING_REVIEW"
}
```

---

## 3. Agent Deep Dive

### 3.1 IntakeAgent (Port 10101)

**File:** `agents/src/intake_agent.py`

The intake agent is the gatekeeper. It validates required fields exist and
fall within reasonable ranges, then computes two key derived values:

- **DTI (Debt-to-Income)** = `monthly_debt / (annual_income / 12)`
- **LTV (Loan-to-Value)** = `loan_amount / property_value`

**Validation rules:**

- All required fields must be present (`full_name`, `annual_income`,
  `loan_amount`, `property_value`, `credit_score`, `monthly_debt`,
  `employment_years`, `loan_type`)
- `annual_income` > 0
- `credit_score` between 300–850
- `loan_amount` > 0, `property_value` > 0

**On failure:** Returns `{ "valid": false, "errors": [...] }` — the orchestrator
short-circuits and reports the validation errors.

**On success:** Returns the normalized application with DTI and LTV appended.

### 3.2 RiskScorerAgent (Port 10102)

**File:** `agents/src/risk_scorer.py`

This is the most complex agent. It combines deterministic scoring with LLM
reasoning for a composite risk score.

#### Deterministic Score (40% weight)

Five rules with fixed point allocations:

| Rule             | Low Risk (0 pts)  | Medium (10 pts)   | High (20 pts) |
| ---------------- | ----------------- | ----------------- | ------------- |
| Credit Score     | ≥ 740             | 670–739           | < 670         |
| DTI Ratio        | ≤ 0.36            | 0.36–0.43         | > 0.43        |
| LTV Ratio        | ≤ 0.80            | 0.80–0.95         | > 0.95        |
| Employment Years | ≥ 3               | 1–3               | < 1           |
| Income vs. Loan  | income ≥ loan×0.3 | income ≥ loan×0.2 | otherwise     |

The deterministic score is the sum of the five rule scores (0–100 scale).

#### LLM Assessment (60% weight)

The agent calls Azure AI Foundry (Kimi-K2-Thinking) with a structured prompt
containing the full application data and asks for:

- A risk score (0–100)
- Plain-English reasoning
- Risk factors (list)
- Compensating factors (list)

The LLM response is parsed from JSON and used for the 60% component.

#### Composite Score

```
composite = (deterministic × 0.4) + (llm_score × 0.6)
```

#### Categorization

| Score Range | Category     |
| ----------- | ------------ |
| ≤ 40        | AUTO_APPROVE |
| 41–80       | ESCALATE     |
| ≥ 80        | AUTO_DECLINE |

### 3.3 ComplianceAgent (Port 10103)

**File:** `agents/src/compliance_agent.py`

Performs regulatory compliance checks based on the loan type. Each loan type
has different rules enforced by FHA, VA, or conventional lending standards.

#### FHA Checks

- DTI limit: 0.43 (hard) — exceeding blocks the loan
- LTV limit: 0.965 (soft) — flags but doesn't block
- Minimum credit score: 580 (hard)
- Condition: MIP (Mortgage Insurance Premium) required

#### VA Checks

- DTI limit: 0.41 (hard)
- No LTV limit (VA loans allow 100% financing)
- Condition: Certificate of Eligibility required

#### Conventional Checks

- DTI limit: 0.45 (hard)
- LTV limit: 0.97 (soft)
- Minimum credit score: 620 (hard)
- Condition: PMI required if LTV > 80%

**Severity levels:**

- `hard` — typically blocks approval or requires exception
- `soft` — flagged for review, may have conditions attached

### 3.4 DecisionAgent (Port 10104)

**File:** `agents/src/decision_agent.py`

The simplest agent — it applies threshold-based routing using the risk score:

```python
if score <= approve_threshold:  # default 40
    return "APPROVED"
elif score >= decline_threshold:  # default 80
    return "DECLINED"
else:
    return "PENDING_REVIEW"
```

Thresholds are configurable via environment variables (`AUTO_APPROVE_THRESHOLD`,
`AUTO_DECLINE_THRESHOLD`), allowing business rules to be tuned without
code changes.

### 3.5 EscalationAgent (Port 10105 + 8080)

**File:** `agents/src/escalation_agent.py`

Dual-role agent:

1. **A2A Agent (port 10105)** — receives escalated applications from the
   orchestrator via A2A protocol, stores them in an in-memory queue
2. **REST API (port 8080)** — serves the React UI with:
   - `GET /api/escalations/pending` — pending applications
   - `GET /api/escalations` — all applications (any status)
   - `GET /api/escalations/{id}` — single application
   - `POST /api/escalations/{id}/decide` — submit human decision
   - `GET /api/stats` — aggregate counts

The `EscalationStore` is a simple in-memory dict. In production you would
back this with a database (PostgreSQL, Redis, etc.).

Each `EscalationRecord` includes:

- Full application context (from intake)
- Risk score and reasoning (from risk scorer)
- Compliance flags and conditions (from compliance)
- Status tracking (PENDING → APPROVED/DECLINED/INFO_REQUESTED)
- Audit trail (decided_by, decided_at, decision_notes)

---

## 4. MasterOrchestrator (Port 10100)

**File:** `agents/src/orchestrator.py`

The orchestrator is the system's control plane. It manages the full pipeline:

### Agent Discovery

On startup, the orchestrator fetches Agent Cards from each agent's
`/.well-known/agent.json` endpoint. This is a core A2A capability —
agents are discovered dynamically, not hardcoded.

```python
async def discover_agents(self):
    for name, url in self.agent_urls.items():
        card_url = f"{url}/.well-known/agent.json"
        resp = await self._client.get(card_url)
        self.agents[name] = resp.json()
```

### Pipeline Execution

For each application:

1. Call IntakeAgent → validate & normalize
2. If invalid → return errors
3. Call RiskScorerAgent → get risk score
4. Call ComplianceAgent → get compliance report
5. Call DecisionAgent → get routing decision
6. If PENDING_REVIEW → call EscalationAgent
7. Return final result with full context

### A2A JSON-RPC Communication

Each agent call uses the A2A `message/send` method:

```python
async def _call_agent(self, agent_url, payload, headers=None):
    body = {
        "jsonrpc": "2.0",
        "id": str(uuid4()),
        "method": "message/send",
        "params": {
            "message": {
                "role": "user",
                "parts": [{"kind": "text", "text": json.dumps(payload)}]
            }
        }
    }
    resp = await self._client.post(agent_url, json=body, headers=headers)
    return resp.json()
```

### Trace Context Propagation

The orchestrator injects W3C Trace Context headers on every outbound call,
allowing the full pipeline to appear as a single distributed trace in
tools like Jaeger or Grafana Tempo.

---

## 5. A2A Server Pattern

Every agent follows the same A2A server pattern from the SDK:

```python
# 1. Define AgentCard (metadata)
agent_card = AgentCard(
    name="IntakeAgent",
    description="Validates and normalizes loan applications",
    url=f"http://localhost:{PORT}",
    version="1.0.0",
    capabilities=AgentCapabilities(streaming=False),
    skills=[AgentSkill(id="validate", name="Validate Application", ...)]
)

# 2. Implement AgentExecutor
class IntakeExecutor(AgentExecutor):
    async def execute(self, context, event_queue):
        # Parse input from A2A message
        data = json.loads(context.get_user_message())
        # Run agent logic
        result = await IntakeAgent().validate(data)
        # Return via event_queue
        event_queue.enqueue(
            SendTaskResponse(result=TaskResult(
                status=TaskStatus(state=TaskState.completed),
                artifacts=[...]
            ))
        )

# 3. Wire up and run
handler = DefaultRequestHandler(agent_card, IntakeExecutor())
app = A2AStarletteApplication(agent_card, handler)
uvicorn.run(app.build(), host="0.0.0.0", port=PORT)
```

This pattern repeats identically for all five agents and the orchestrator.

---

## 6. OpenTelemetry Instrumentation

**File:** `agents/src/telemetry.py`

### Setup

```python
def setup_telemetry(service_name: str) -> TracerProvider:
    resource = Resource.create({"service.name": service_name})
    provider = TracerProvider(resource=resource)

    # Export to OTLP collector (Jaeger, Grafana Tempo, etc.)
    otlp = OTLPSpanExporter(endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "..."))
    provider.add_span_processor(BatchSpanProcessor(otlp))

    # Also log to console for development
    provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))

    trace.set_tracer_provider(provider)
    return provider
```

### Trace Context Propagation

When the orchestrator calls downstream agents, it injects W3C trace context:

```python
def inject_trace_context() -> dict[str, str]:
    headers: dict[str, str] = {}
    inject(headers)  # W3C TraceContext propagation
    return headers
```

Each downstream agent extracts the context to continue the trace:

```python
def extract_trace_context(headers: dict[str, str]) -> Context:
    return extract(headers)
```

This creates a distributed trace that spans all five agents:

```
MasterOrchestrator
  ├── IntakeAgent.validate (65ms)
  ├── RiskScorerAgent.score (380ms)
  │     └── LLM call to Azure AI Foundry (320ms)
  ├── ComplianceAgent.check (95ms)
  ├── DecisionAgent.decide (35ms)
  └── EscalationAgent.escalate (55ms)  ← only for PENDING_REVIEW
```

---

## 7. React UI

The React application provides two main views:

### 7.1 Approval Queue

**File:** `ui/src/components/ApprovalQueue.tsx`

Polls `GET /api/escalations/pending` every 3 seconds and renders one
`ApplicationCard` per pending application.

Each card shows:

- Applicant name, ID, escalation timestamp
- Risk score (color-coded: green ≤40, amber 40–80, red ≥80)
- AI reasoning (plain-English explanation from the LLM)
- Risk factors and compensating factors side-by-side
- Compliance flags with severity badges
- Required conditions
- Full application data grid
- Action buttons: **Approve**, **Decline**, **Request Info**

When a reviewer clicks an action, the UI sends:

```
POST /api/escalations/{id}/decide
{ "decision": "APPROVED", "decided_by": "Reviewer", "notes": "..." }
```

### 7.2 Telemetry Dashboard

**File:** `ui/src/components/TelemetryDashboard.tsx`

Polls `/api/stats` and `/api/escalations` every 5 seconds.

Contains:

- **KPI cards** — Total, Pending, Approved, Declined, Info Requested
- **Decision Distribution** (pie chart) — Visual breakdown via Recharts
- **Agent Pipeline Latency** (horizontal bar chart) — Average latency
  per agent showing where time is spent
- **Pipeline Trace Waterfall** — Visual timeline of recent application
  processing showing each agent's execution as a colored bar

The Vite dev server proxies `/api/*` requests to `localhost:8080` (the
Escalation Agent's REST API), so no CORS issues during development.

---

## 8. Data Model

### Test Applicants

Eight test applicants are defined in `_common/src/loan_data.py` and shared
across lessons. They cover a range of risk profiles:

| Applicant         | Credit | Income   | Loan     | Expected Outcome |
| ----------------- | ------ | -------- | -------- | ---------------- |
| Sarah Chen        | 780    | $125,000 | $350,000 | Auto-Approve     |
| Marcus Williams   | 680    | $75,000  | $280,000 | Escalate         |
| Emily Johnson     | 580    | $45,000  | $200,000 | Auto-Decline     |
| David Kim         | 720    | $95,000  | $400,000 | Escalate         |
| Jennifer Martinez | 810    | $200,000 | $500,000 | Auto-Approve     |
| Robert Taylor     | 640    | $55,000  | $180,000 | Escalate         |
| Amanda Foster     | 750    | $110,000 | $320,000 | Auto-Approve     |
| James Cooper      | 590    | $40,000  | $150,000 | Auto-Decline     |

### EscalationRecord

```python
class EscalationRecord(BaseModel):
    id: str                          # UUID
    applicant_id: str                # From application data
    full_name: str                   # From application data
    application_data: dict           # Full normalized application
    risk_score: float                # Composite score (0–100)
    reasoning: str                   # LLM explanation
    risk_factors: list[str]          # From risk scorer
    compensating_factors: list[str]  # From risk scorer
    compliance_flags: list[dict]     # From compliance agent
    compliance_conditions: list[str] # From compliance agent
    status: str                      # PENDING / APPROVED / DECLINED / INFO_REQUESTED
    escalated_at: str                # ISO timestamp
    decided_at: str | None           # ISO timestamp (after review)
    decided_by: str | None           # Reviewer name
    decision_notes: str | None       # Reviewer notes
```

---

## 9. Configuration Reference

All configuration is via environment variables (see `.env.example`):

| Variable                      | Default                           | Description                     |
| ----------------------------- | --------------------------------- | ------------------------------- |
| `GITHUB_TOKEN`                | (required)                        | GitHub Models API key for Phi-4 |
| `AZURE_AI_FOUNDRY_ENDPOINT`   | (required)                        | Azure AI Foundry base URL       |
| `AZURE_AI_FOUNDRY_KEY`        | (required)                        | Azure AI Foundry API key        |
| `AZURE_AI_FOUNDRY_MODEL`      | `Kimi-K2-Thinking`                | Model for risk scoring LLM      |
| `AUTO_APPROVE_THRESHOLD`      | `40`                              | Score ≤ this → auto-approve     |
| `AUTO_DECLINE_THRESHOLD`      | `80`                              | Score ≥ this → auto-decline     |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `http://localhost:4318/v1/traces` | OTLP HTTP endpoint              |
| `ESCALATION_API_PORT`         | `8080`                            | REST API port for React UI      |

---

## 10. Extending the System

### Add a New Agent

1. Create `new_agent.py` with your agent logic class
2. Create `new_agent_server.py` following the A2A server pattern (Section 5)
3. Choose an unused port (e.g., 10106)
4. Add the agent URL to `orchestrator.py`'s `AGENT_URLS` dict
5. Update `start_all.py` to include the new server

### Add a Database Backend

Replace `EscalationStore` in `escalation_agent.py` with a database-backed
implementation. The store interface is simple:

```python
class EscalationStore:
    async def add(self, record: EscalationRecord) -> None: ...
    async def get(self, id: str) -> EscalationRecord | None: ...
    async def list_pending(self) -> list[EscalationRecord]: ...
    async def list_all(self) -> list[EscalationRecord]: ...
    async def update_decision(self, id, decision, by, notes) -> None: ...
    def stats(self) -> dict: ...
```

### Connect a Real OTLP Collector

1. Run Jaeger: `docker run -p 4318:4318 -p 16686:16686 jaegertracing/jaeger:latest`
2. Set `OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318/v1/traces`
3. Open Jaeger UI at `http://localhost:16686`
4. Filter by service name (e.g., `loan-intake-agent`)

### Adjust Decision Thresholds

Change `AUTO_APPROVE_THRESHOLD` and `AUTO_DECLINE_THRESHOLD` in `.env`:

```bash
# More conservative: escalate more to humans
AUTO_APPROVE_THRESHOLD=30
AUTO_DECLINE_THRESHOLD=70

# More aggressive: let AI decide more
AUTO_APPROVE_THRESHOLD=50
AUTO_DECLINE_THRESHOLD=90
```

---

## Appendix: A2A Protocol Quick Reference

| Concept     | Description                                                 |
| ----------- | ----------------------------------------------------------- |
| Agent Card  | JSON metadata at `/.well-known/agent.json` describing agent |
| JSON-RPC    | Transport protocol — `message/send` to invoke agents        |
| Task        | A unit of work tracked by the A2A runtime                   |
| Artifact    | Structured data returned by an agent (text, file, etc.)     |
| Skill       | A capability advertised in the Agent Card                   |
| Event Queue | Async queue for streaming agent responses                   |
