# A2A Tutorial Examples

Working code examples for the [A2A — Agent-to-Agent Protocol](https://a2a-protocol.org/) tutorial course.

## Structure

```
a2a/
  .venv/                        # uv-managed Python 3.11 venv (git-ignored)
  pyproject.toml                # uv project config
  requirements.txt              # pip-installable deps list
  scripts/                      # automation scripts (setup, run, test)
  lessons/
    05-first-a2a-agent/         # Lesson 5: Build a standalone QA agent
    06-a2a-server/              # Lesson 6: Wrap agent as A2A server
    07-a2a-client/              # Lesson 7: Build an A2A client
```

## Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) — fast Python package manager (`pip install uv`)
- GitHub account with a [Personal Access Token](https://github.com/settings/tokens) (no special scopes)

## Quick Start

### 1. Set up your token

```bash
# From _examples/ directory
cp .env.example .env
# Edit .env and set GITHUB_TOKEN=ghp_your_token_here
```

### 2. Create the venv and install dependencies

```powershell
# Windows PowerShell — from a2a/ directory
cd a2a
.\scripts\setup.ps1
```

```bash
# Linux / macOS — from a2a/ directory
cd a2a
bash scripts/setup.sh
```

This creates `.venv/`, installs all deps via uv, and registers the `a2a-examples` Jupyter kernel.

### 3. Run

```powershell
.\scripts\run_all.ps1        # full end-to-end scenario
.\scripts\run_lesson05.ps1   # lesson 05 only (standalone agent)
.\scripts\run_server.ps1     # start A2A server (port 10001)
.\scripts\run_client.ps1     # test running server
```

See [scripts/README.md](../scripts/README.md) for all workflows.

### 4. Open notebooks

Select kernel **"A2A Examples (Python 3.11)"** in VS Code or Jupyter.

## Model Provider

All examples use **GitHub Models** with **Phi-4** — free, no billing required.

| Setting  | Value                                                                        |
| -------- | ---------------------------------------------------------------------------- |
| Endpoint | `https://models.inference.ai.azure.com`                                      |
| Model    | `Phi-4`                                                                      |
| Auth     | `GITHUB_TOKEN` (PAT, no special scopes)                                      |
| SDK      | `openai` (OpenAI-compatible API)                                             |
| Docs     | [docs.github.com/en/github-models](https://docs.github.com/en/github-models) |

## License

[Mozilla Public License 2.0](../../LICENSE)
