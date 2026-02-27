# Scripts

Interactive scenario scripts — one per lesson.
**Cross-platform** — works on Windows, macOS, and Linux with Python 3.10+.
Run everything from the `a2a/` directory (one level above this folder).

## Quick Reference

| Script         | Lesson | What It Does                                  |
| -------------- | ------ | --------------------------------------------- |
| `lesson_05.py` | 05     | Standalone QA agent — runs demo, then prompts |
| `lesson_06.py` | 06     | A2A server — walks through components, starts |
| `lesson_07.py` | 07     | A2A client — discovery, blocking, streaming, prompts |

## Requirements

- Python 3.10+ in the `.venv` (`uv venv .venv --python 3.11`)
- Dependencies installed (`uv pip install -r requirements.txt`)
- `_examples/.env` with `GITHUB_TOKEN=ghp_your_token_here`
  ([get a free PAT](https://github.com/settings/tokens) — no special scopes)

## Usage

```bash
# All three commands use the same syntax on Windows / macOS / Linux
# Run from _examples/a2a/

python scripts/lesson_05.py   # Standalone QA agent (no server needed)

# In terminal 1:
python scripts/lesson_06.py   # Start A2A server on :10001

# In terminal 2 (while server is running):
python scripts/lesson_07.py   # Connect, query, stream, interact
```

## Lesson Scenarios

### Lesson 05 — Standalone QA Agent

No server required. Verifies GitHub Models connectivity and the QAAgent class.

```
━━━  Lesson 05 — Building Your First A2A Agent  ━━━
     Standalone QA Agent · GitHub Phi-4

Step 1 — Environment
  ✅ GITHUB_TOKEN set (github_p...)

Step 2 — Configuring GitHub Models client (Phi-4)
  ✅ Client ready → https://models.inference.ai.azure.com

Step 3 — Loading domain knowledge
  ✅ Loaded 1,763 chars from insurance_policy.txt

Step 4 — Creating QAAgent
  ✅ QAAgent ready

Step 5 — Running demo questions
  ❓ What is the deductible for the Standard plan?
     The deductible for the Standard plan is $500 per incident ...

Step 6 — Interactive mode
  ❓ Your question: _
```

---

### Lesson 06 — A2A Server

Walks through the server components, then starts the server on port 10001.
Keep this terminal open while running Lesson 07.

```
━━━  Lesson 06 — A2A Server  ━━━
     QAAgent wrapped as a fully A2A-compliant API

Step 1 — Environment        ✅ GITHUB_TOKEN set
Step 2 — Agent Card         (explains discovery endpoint)
Step 3 — AgentExecutor      (explains QAAgent →  A2A bridge)
Step 4 — Server Stack       (explains uvicorn / ASGI stack)
Step 5 — Starting Server

  🚀 QAAgent A2A Server
     Listening on:  http://localhost:10001
     Agent Card:    http://localhost:10001/.well-known/agent.json
     Press Ctrl+C to stop.
```

---

### Lesson 07 — A2A Client

Connects to the running server, walks through discovery, blocking calls,
streaming, error handling, then enters an interactive Q&A loop.

```
━━━  Lesson 07 — A2A Client Fundamentals  ━━━
     Discover · Request · Stream · Handle Errors

Step 1 — Discover the Agent Card
  ✅ Agent Card received
     Name:    QAAgent  |  Streaming: True

Step 2 — Blocking request (message/send)
  ❓ What is the annual deductible?
     The annual deductible is $500 ...

Step 3 — Multiple blocking questions   (4 demo questions)
Step 4 — Streaming request             (SSE events printed live)
Step 5 — Error handling                (JSON-RPC + connection)

Step 6 — Interactive mode
  ❓ Your question: _
```

---

## Environment Setup

```dotenv
# _examples/.env
GITHUB_TOKEN=ghp_your_token_here
```

All scripts auto-load `.env` from `_examples/` — no manual export needed.

## Port Reference

| Port  | Agent   | Started by     |
| ----- | ------- | -------------- |
| 10001 | QAAgent | `lesson_06.py` |

## Troubleshooting

| Problem                       | Fix                                                         |
| ----------------------------- | ----------------------------------------------------------- |
| `GITHUB_TOKEN not set`        | Edit `_examples/.env`                                       |
| `Cannot reach localhost:10001` | Start the server first: `python scripts/lesson_06.py`      |
| `ModuleNotFoundError`         | Activate the venv or install deps: `uv pip install -r requirements.txt` |
| `kernel not found`            | Register kernel: `.venv/bin/python -m ipykernel install --user --name a2a-examples` |
