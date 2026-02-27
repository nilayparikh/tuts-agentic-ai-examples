# Lesson 05 — Building Your First A2A Agent

Build a standalone QA agent powered by **GitHub Phi-4** that answers questions about insurance policies.

## What You'll Build

A `QAAgent` class that:

- Loads domain knowledge (insurance policy document)
- Injects knowledge into a system prompt
- Queries GitHub Phi-4 via the OpenAI-compatible API
- Returns grounded, factual answers

## Prerequisites

1. **GitHub Account** with a Personal Access Token (PAT)
   - Go to [github.com/settings/tokens](https://github.com/settings/tokens)
   - Create a PAT (classic) — no special scopes required
   - See [GitHub Models docs](https://docs.github.com/en/github-models) for details

2. **Python 3.10+** with a virtual environment

3. **Environment variable:**
   ```bash
   export GITHUB_TOKEN=ghp_your_token_here
   ```

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

- **OpenAI-compatible API** — GitHub Models uses the same API as OpenAI, just a different base URL
- **Async pattern** — `async def query()` prepares for A2A server wrapping in Lesson 6
- **Knowledge injection** — System prompt template with domain document
- **Standalone testing** — Always verify agent logic before adding protocol layers

## Next Steps

→ [Lesson 06](../06-a2a-server/) — Wrap this agent as an A2A server
