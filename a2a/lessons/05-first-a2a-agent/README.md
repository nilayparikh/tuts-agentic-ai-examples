# Lesson 05 — Building Your First A2A Agent

[![Watch: Building Your First A2A Agent](https://img.youtube.com/vi/xD606KkVkoA/maxresdefault.jpg)](https://www.youtube.com/watch?v=xD606KkVkoA)

## Quick Links

- <a href="https://www.youtube.com/watch?v=xD606KkVkoA" target="_blank" rel="noopener noreferrer">Watch the lesson</a>
- <a href="https://tuts.localm.dev/a2a/first-a2a-agent" target="_blank" rel="noopener noreferrer">Companion page</a>
- Previous lesson: <a href="https://tuts.localm.dev/a2a/setup-resources" target="_blank" rel="noopener noreferrer">Setup & Resources</a>
- Next lesson: [Wrapping Agents as A2A Servers](../06-a2a-server/)

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

| Provider                    | Setup                                                                                                                                                                                                                 | Credential                 |
| --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------- |
| **GitHub Models** (default) | No Azure required. <a href="https://github.com/settings/tokens" target="_blank" rel="noopener noreferrer">Create a free PAT</a> — no scopes needed.                                                                   | `GITHUB_TOKEN` in `.env`   |
| **AI Toolkit LocalFoundry** | No token needed. Install <a href="https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio" target="_blank" rel="noopener noreferrer">VS Code AI Toolkit</a>, load a model, run it. | Model running on port 5272 |

Change `PROVIDER` in the notebook setup cell to switch providers.

## Setup

```bash
cd src
pip install openai python-dotenv
```

## Run

Open `qa_agent.ipynb` in Jupyter or VS Code and run all cells.

## Files

| File                            | Description             |
| ------------------------------- | ----------------------- |
| `src/qa_agent.ipynb`            | Self-contained notebook |
| `src/data/insurance_policy.txt` | Sample knowledge base   |

## Key Concepts

- **OpenAI-compatible API** — both GitHub Models and LocalFoundry use the same API; only `base_url` and `api_key` differ
- **PROVIDER pattern** — single variable switches between GitHub Models and LocalFoundry
- **Async pattern** — `async def query()` prepares for A2A server wrapping in Lesson 6
- **Knowledge injection** — System prompt template with domain document
- **Standalone testing** — Always verify agent logic before adding protocol layers

## Next Steps

→ [Lesson 06](../06-a2a-server/) — Wrap this agent as an A2A server
