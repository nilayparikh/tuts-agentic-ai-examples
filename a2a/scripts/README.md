# Scripts

Automation scripts for running A2A example lessons.
All scripts run from the `a2a/` directory (one level above this folder).

## Quick Reference

| Script                     | OS         | Purpose                                              |
| -------------------------- | ---------- | ---------------------------------------------------- |
| `setup.ps1` / `setup.sh`   | Win / Unix | One-time: create venv, install deps, register kernel |
| `run_lesson05.ps1` / `.sh` | Win / Unix | Run Lesson 05 standalone agent                       |
| `run_server.ps1` / `.sh`   | Win / Unix | Start A2A server (blocks until Ctrl+C)               |
| `run_client.ps1` / `.sh`   | Win / Unix | Test running server with 4 questions                 |
| `run_notebooks.ps1`        | Win        | Execute all notebooks via nbconvert                  |
| `run_all.ps1` / `.sh`      | Win / Unix | Full end-to-end: 05 → start server → 07 client       |

## Usage

```powershell
# Windows PowerShell — run from a2a/ directory
cd Y:\.sources\localm-tuts\a2a\_examples\a2a

.\scripts\setup.ps1           # First time only
.\scripts\run_lesson05.ps1    # Lesson 05 standalone
.\scripts\run_server.ps1      # Start server (keep this terminal open)
.\scripts\run_client.ps1      # In a NEW terminal — test the server
.\scripts\run_all.ps1         # Full automated run
```

```bash
# Linux / macOS — run from a2a/ directory
cd /path/to/_examples/a2a

bash scripts/setup.sh
bash scripts/run_lesson05.sh
bash scripts/run_server.sh     # keep terminal open
bash scripts/run_client.sh     # in a new terminal
bash scripts/run_all.sh
```

## Workflows

### Workflow 1 — Quick Smoke Test (Lesson 05 only)

No server needed. Just verifies GitHub Models connectivity and the QAAgent class.

```powershell
.\scripts\run_lesson05.ps1
```

Expected output: 3 questions answered from the insurance policy document.

---

### Workflow 2 — Interactive Server + Manual Client

Best for learning — you see server logs in one terminal and client output in another.

**Terminal 1** (server):

```powershell
.\scripts\run_server.ps1
```

**Terminal 2** (client):

```powershell
.\scripts\run_client.ps1
```

Or test manually with curl:

```bash
# Fetch Agent Card
curl http://localhost:10001/.well-known/agent.json | python -m json.tool

# Ask a question
curl -X POST http://localhost:10001 \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "message/send",
    "params": {
      "message": {
        "role": "user",
        "parts": [{"kind": "text", "text": "What is the deductible?"}],
        "messageId": "msg-001"
      }
    }
  }'
```

---

### Workflow 3 — Full Automated Run (CI-friendly)

Starts the server as a background process, runs all client tests, then stops the server.

```powershell
.\scripts\run_all.ps1
```

Expected output:

```
✅ Lesson 05 complete
✅ Server ready at http://localhost:10001
Q: What is the annual deductible?
A: The annual deductible for the ACME Standard Plan is $500...
...
Passed: 5 / 5
✅ Server stopped
```

---

### Workflow 4 — Notebook Execution

Execute all notebook cells headlessly and save outputs:

```powershell
.\scripts\run_notebooks.ps1           # all notebooks
.\scripts\run_notebooks.ps1 -Lesson 05  # single lesson
```

> **Note:** Lesson 07 notebook requires the server running.
> Start it with `run_server.ps1` before running notebooks for lesson 07.

---

## Environment Setup

All scripts load `.env` from `_examples/.env` automatically.
The `.env` file must contain:

```dotenv
GITHUB_TOKEN=ghp_your_token_here
```

Get a GitHub PAT (no special scopes needed) at:
https://github.com/settings/tokens

## Port Reference

| Port  | Agent   | Script           |
| ----- | ------- | ---------------- |
| 10001 | QAAgent | `run_server.ps1` |

## Troubleshooting

| Problem                 | Fix                                                           |
| ----------------------- | ------------------------------------------------------------- |
| `GITHUB_TOKEN not set`  | Edit `_examples/.env`                                         |
| `Server not reachable`  | Run `run_server.ps1` in a separate terminal first             |
| `ModuleNotFoundError`   | Run `setup.ps1` to install deps                               |
| `kernel not found`      | Run `setup.ps1` to register the `a2a-examples` kernel         |
| `uv: command not found` | Install uv: `pip install uv` or `winget install astral-sh.uv` |
