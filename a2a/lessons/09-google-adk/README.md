# Lesson 09 — Google ADK: Threat-Intelligence Research Agent

## Overview

Build a **ThreatBriefing** A2A agent using Google Agent Development Kit (ADK)
and expose it with the `to_a2a()` one-liner — the simplest A2A server
integration of any framework.

The agent searches a curated cybersecurity vulnerability knowledge base
(synthetic CVE data), retrieves detailed records, and synthesises structured
threat briefings using Kimi-K2 via Azure AI Foundry.

## Architecture

```
┌─────────────────────────────────┐
│  knowledge_base.py              │
│  (CVE data + search functions)  │
└────────────┬────────────────────┘
             │ imported
┌────────────▼────────────────────┐
│  research_agent.py              │
│  LlmAgent + FunctionTool ×2    │
│  (LiteLlm → Azure Kimi-K2)     │
└────────────┬────────────────────┘
             │ to_a2a()
┌────────────▼────────────────────┐
│  server.py  (port 10002)        │
│  A2A protocol ─ Agent Card,     │
│  JSON-RPC, task management      │
└────────────┬────────────────────┘
             │ A2A
┌────────────▼────────────────────┐
│  client.py                      │
│  Discover agent → send query → │
│  display threat briefing        │
└─────────────────────────────────┘
```

## Source Files

| File                    | Purpose                                                                     |
| ----------------------- | --------------------------------------------------------------------------- |
| `src/knowledge_base.py` | Synthetic CVE / threat data + search and lookup tools                       |
| `src/research_agent.py` | ADK `LlmAgent` with `FunctionTool` wrappers + `LiteLlm` Azure config        |
| `src/server.py`         | `to_a2a()` one-liner → A2A Starlette server on port 10002                   |
| `src/client.py`         | A2A client — discovers agent, sends query, displays briefing                |
| `src/server.ipynb`      | Simplified ADK server demo — GitHub Phi-4 / LocalFoundry, no Azure required |
| `src/client.ipynb`      | Simplified A2A client demo                                                  |

## Notebooks (Simple)

The two notebooks demonstrate the **Google ADK `to_a2a()` pattern** with
your choice of **free** model provider — no Azure account required.

| Notebook           | Port  | What it shows                                          |
| ------------------ | ----- | ------------------------------------------------------ |
| `src/server.ipynb` | 10091 | Build an ADK LlmAgent + `to_a2a()` server step-by-step |
| `src/client.ipynb` | —     | Discover and query the ADK A2A server                  |

Open both notebooks and run `server.ipynb` first, then `client.ipynb`.

### Provider options

| Provider                    | Set `PROVIDER =` | Credential                                     |
| --------------------------- | ---------------- | ---------------------------------------------- |
| **GitHub Models** (default) | `"github"`       | `GITHUB_TOKEN` in `.env`                       |
| **AI Toolkit LocalFoundry** | `"localfoundry"` | VS Code AI Toolkit + model loaded on port 5272 |

Change `PROVIDER` in cell 2 of `server.ipynb` before running.

> **Jupyter note:** All async calls in the notebooks use `await` directly rather
> than `asyncio.run()`. Jupyter already runs inside a live event loop, so
> `asyncio.run()` raises `RuntimeError: cannot be called from a running event loop`.
> Top-level `await` in cells works correctly with IPython ≥ 7.

## Running the Example

### Prerequisites

```bash
cd _examples/a2a
# Activate virtual environment
.venv\Scripts\Activate.ps1        # Windows
# source .venv/bin/activate       # macOS / Linux

pip install -r requirements.txt
```

Ensure `.env` has:

```
AZURE_OPENAI_ENDPOINT=https://<resource>.openai.azure.com
AZURE_AI_API_KEY=<your-key>
AZURE_AI_MODEL_DEPLOYMENT_NAME=Kimi-K2
```

### Start the Server

```bash
cd lessons/09-google-adk/src
python server.py
```

Expected output:

```
Starting ThreatBriefingAgent A2A server on port 10002 ...
  Agent Card : http://localhost:10002/.well-known/agent-card.json
  JSON-RPC   : POST http://localhost:10002/
```

### Run the Client

In a separate terminal (with the venv activated):

```bash
cd lessons/09-google-adk/src

# Default query (XZ backdoor)
python client.py

# Custom query
python client.py "ssh vulnerabilities"
python client.py "CVE-2024-38063 windows ipv6"
python client.py "fortinet vpn"
```

### Run via Lesson Script

The interactive lesson script starts the server automatically:

```bash
cd _examples/a2a
python scripts/lesson_09.py
```

## Key Concepts Demonstrated

1. **ADK `to_a2a()` One-Liner** — compare the 3-line server setup to
   lesson 08's manual `A2AStarletteApplication` wiring
2. **LiteLlm Model Adapter** — run Azure-hosted Kimi-K2 without any
   Google Cloud / Vertex AI dependency
3. **FunctionTool** — wrap plain Python functions as agent tools with
   automatic parameter discovery from type hints and docstrings
4. **Full A2A Round-Trip** — Agent Card discovery → JSON-RPC query →
   structured response extraction
5. **Cross-Framework Interoperability** — any A2A client (from any
   framework) can call this server using the standard protocol

## Sample CVE Data

The knowledge base includes five synthetic entries:

| CVE            | Title                      | Severity        |
| -------------- | -------------------------- | --------------- |
| CVE-2024-3094  | XZ Utils Backdoor          | CRITICAL (10.0) |
| CVE-2024-4577  | PHP CGI Argument Injection | CRITICAL (9.8)  |
| CVE-2024-21762 | Fortinet FortiOS OOB Write | CRITICAL (9.6)  |
| CVE-2024-6387  | OpenSSH regreSSHion        | HIGH (8.1)      |
| CVE-2024-38063 | Windows TCP/IP IPv6 RCE    | CRITICAL (9.8)  |
