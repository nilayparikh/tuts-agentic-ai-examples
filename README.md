# A2A Examples

Code examples for the A2A tutorial course. Each example demonstrates a concept
from the structured lessons using the course's model provider stack.

## Example Index

| Example                    | Lesson | Concept                                | Model                      |
| -------------------------- | ------ | -------------------------------------- | -------------------------- |
| `01-qa-agent/`             | 05     | Standalone agent class                 | Phi-4 (GitHub Models)      |
| `02-a2a-server/`           | 06     | AgentExecutor + Agent Card             | Phi-4 (GitHub Models)      |
| `03-a2a-client/`           | 07     | A2ACardResolver + send/stream          | Phi-4 (GitHub Models)      |
| `04-msft-agent-framework/` | 08     | A2AAgent proxy + OrchestratorAgent     | Kimi-K2-Thinking (Foundry) |
| `05-google-adk/`           | 09     | LlmAgent + to_a2a() + RemoteA2aAgent   | Kimi-K2 (Foundry)          |
| `06-langgraph-mcp/`        | 10     | FastMCP + create_react_agent + bridge  | Qwen2.5 Coder (Local)      |
| `07-crewai/`               | 11     | Agent/Task/Crew + CrewAIExecutor       | Kimi-K2-Thinking (Foundry) |
| `08-openai-agents-sdk/`    | 12     | @tool + Agent + Runner + handoffs      | Phi-4 (GitHub Models)      |
| `09-claude-agent-sdk/`     | 13     | Structured tools + conversation memory | Kimi-K2 (Foundry)          |
| `10-github-copilot-sdk/`   | 14     | GitHub API + PR analysis + dual-token  | Phi-4 (GitHub Models)      |
| `11-multi-agent-system/`   | 15     | MasterOrchestrator + 8-agent startup   | All models                 |

## Port Assignments

All examples use a consistent port scheme:

| Port  | Agent             | Example                         |
| ----- | ----------------- | ------------------------------- |
| 10001 | QAAgent           | `01-qa-agent` → `02-a2a-server` |
| 10002 | ResearchAgent     | `05-google-adk`                 |
| 10003 | CodeAgent         | `06-langgraph-mcp`              |
| 10004 | PlannerAgent      | `07-crewai`                     |
| 10005 | TaskAgent         | `08-openai-agents-sdk`          |
| 10006 | AssistantAgent    | `09-claude-agent-sdk`           |
| 10007 | CopilotAgent      | `10-github-copilot-sdk`         |
| 10008 | OrchestratorAgent | `04-msft-agent-framework`       |

## Setup (Lessons 05–07)

```powershell
# Windows — run from a2a/ directory
cd a2a
.\scripts\setup.ps1       # one-time: creates .venv, installs deps, registers kernel
.\scripts\run_all.ps1     # full run: lesson 05 → server → client
```

```bash
# Linux / macOS — run from a2a/ directory
cd a2a
bash scripts/setup.sh
bash scripts/run_all.sh
```

### Environment Variables

Copy `.env.example` → `.env` and fill in your token:

```bash
cp .env.example .env
# edit .env and set:
GITHUB_TOKEN=ghp_your_token_here   # https://github.com/settings/tokens
```

The `.env` file is **git-ignored**. Never commit real tokens.

| Variable               | Required for          | Where to get                                                     |
| ---------------------- | --------------------- | ---------------------------------------------------------------- |
| `GITHUB_TOKEN`         | Lessons 05–07 (Phi-4) | [github.com/settings/tokens](https://github.com/settings/tokens) |
| `AZURE_AI_FOUNDRY_URL` | Lessons 08+           | Azure AI Foundry portal                                          |
| `AZURE_AI_FOUNDRY_KEY` | Lessons 08+           | Azure AI Foundry portal                                          |

### Scripts

All automation is in [a2a/scripts/](a2a/scripts/). See [a2a/scripts/README.md](a2a/scripts/README.md).

> **Note**: Example folders listed above beyond lesson 07 are planned. They will be created
> as lesson content is finalized and video-recorded.

## License

[Mozilla Public License 2.0](LICENSE)
