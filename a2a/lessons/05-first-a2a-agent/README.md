# Lesson 05 — Building Your First A2A Agent

Build a standalone QA agent powered by **GitHub Phi-4** that answers questions about insurance policies.

## What You'll Build

A `QAAgent` class that:

- Loads domain knowledge (insurance policy document)
- Injects knowledge into a system prompt
- Queries GitHub Phi-4 via the OpenAI-compatible API
- Returns grounded, factual answers

## Prerequisites

**Python 3.10+** with a virtual environment.

Choose a model provider:

| Provider                    | Setup                                                                                                                                                            | Credential                 |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------- |
| **GitHub Models** (default) | No Azure required. [Create a free PAT](https://github.com/settings/tokens) — no scopes needed.                                                                   | `GITHUB_TOKEN` in `.env`   |
| **AI Toolkit LocalFoundry** | No token needed. Install [VS Code AI Toolkit](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio), load a model, run it. | Model running on port 5272 |

Change `PROVIDER` in the notebook setup cell (or top of `qa_agent.py`) to switch providers.

## Setup

```bash
cd src
pip install openai python-dotenv
```

## Run

Open `qa_agent.ipynb` in Jupyter or VS Code and run all cells.

Or run the standalone module:

```bash
python qa_agent.py
```

## Files

| File                            | Description                      |
| ------------------------------- | -------------------------------- |
| `src/qa_agent.ipynb`            | Interactive notebook walkthrough |
| `src/qa_agent.py`               | Importable agent module          |
| `src/data/insurance_policy.txt` | Sample knowledge base            |

## Key Concepts

- **OpenAI-compatible API** — both GitHub Models and LocalFoundry use the same API; only `base_url` and `api_key` differ
- **PROVIDER pattern** — single variable switches between GitHub Models and LocalFoundry
- **Async pattern** — `async def query()` prepares for A2A server wrapping in Lesson 6
- **Knowledge injection** — System prompt template with domain document
- **Standalone testing** — Always verify agent logic before adding protocol layers

## Next Steps

→ [Lesson 06](../06-a2a-server/) — Wrap this agent as an A2A server
