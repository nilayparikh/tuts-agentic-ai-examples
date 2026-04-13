# GitHub Copilot CLI — Configuration Guide

This guide shows how to use the standalone GitHub Copilot CLI in the terminal
alongside the VS Code context already set up for the Loan Workbench.

## Installation

```bash
# Install the GitHub Copilot CLI (standalone)
npm install -g @githubnext/github-copilot-cli

# Verify installation
copilot --version
```

## Basic Commands

```bash
# Get a code suggestion (non-interactive, auto-approve)
copilot -p "add a delete route for loan applications" --allow-all

# Explain existing code
copilot -p "explain app/backend/src/middleware/auth.ts" --allow-all

# Suggest a git command
copilot -p "undo last commit but keep changes" --allow-all

# Suggest a shell command
copilot -p "find all TypeScript files with console.log" --allow-all

# Save output to a markdown file
copilot -p "add a delete route" --allow-all --share=output.md

# Use a specific model
copilot -p "explain this code" --allow-all --model gpt-5.4

# Silent mode (no spinner)
copilot -p "explain this code" --allow-all -s

# Skip custom instructions
copilot -p "explain this code" --allow-all --no-custom-instructions
```

## How Context Loads in CLI

| Context Artifact                         | Loaded in CLI? | Notes                              |
| ---------------------------------------- | -------------- | ---------------------------------- |
| `.github/copilot-instructions.md`        | ✅ Yes         | Auto-loaded from repo root         |
| `.github/instructions/*.instructions.md` | ❌ No          | VS Code only (applyTo scoping)     |
| `.github/agents/*.agent.md`              | ❌ No          | VS Code Chat only                  |
| `.github/skills/*/SKILL.md`              | ❌ No          | VS Code Chat only                  |
| `.github/prompts/*.prompt.md`            | ❌ No          | VS Code Chat only (slash commands) |
| `.github/hooks/*`                        | ❌ No          | VS Code only                       |
| `.github/mcp.json`                       | ❌ No          | VS Code only                       |
| `docs/*.md` (via #file: attachment)      | ❌ No          | VS Code Chat only                  |
| `docs/*.md` (via semantic search)        | ✅ Partial     | If the repo is indexed             |

**Key insight**: `.github/copilot-instructions.md` is the ONLY context file
that is guaranteed to load across all surfaces. This is why Lesson 02 puts
the most critical context there.

## Shell Aliases (Optional)

Add these to your shell profile (`~/.bashrc`, `~/.zshrc`, or PowerShell
`$PROFILE`) for faster workflows:

```bash
# Bash/Zsh aliases
alias cq='copilot -p'            # quick prompt
alias cqa='copilot -p --allow-all' # auto-approve
```

```powershell
# PowerShell aliases
function cq  { copilot -p @args }
function cqa { copilot -p @args --allow-all }
```

## Workflow Examples

### Generating a New Route (CLI)

```bash
# Navigate to the project root (where .github/ lives)
cd /path/to/loan-workbench

# The CLI auto-loads .github/copilot-instructions.md
copilot -p "write an Express route handler for GET /api/v1/applications/:id
that follows the three-layer architecture (route → rules → service),
uses ESM imports, and returns structured JSON errors" --allow-all
```

The suggestion will follow the conventions from `copilot-instructions.md`:
ESM imports, `const`, `async` handler, structured error responses.

But it will NOT know about the detailed architecture (state machine, fail-closed
audit) because `docs/architecture.md` is not auto-loaded in CLI.

### Explaining Code (CLI)

```bash
copilot -p "explain app/backend/src/rules/smsRestriction.ts" --allow-all
```

The CLI will explain the code using whatever it can infer from the file content
plus the instructions in `.github/copilot-instructions.md`. It will know this
is an Express/TypeScript project with specific conventions.

### Git Workflow (CLI)

```bash
# Suggest the right git command
copilot -p "create a branch for adding delete functionality" --allow-all

# Suggest shell commands for project tasks
copilot -p "run only the tests in the rules directory" --allow-all
```

## Designing for CLI Parity

When adding new context to the Loan Workbench, follow this decision tree:

```
Is this critical for ALL surfaces (VS Code, CLI, coding agent, review)?
├── YES → Put it in .github/copilot-instructions.md
│         (keep it brief — summary + references)
└── NO  → Does it need path-scoped activation?
    ├── YES → Use .github/instructions/*.instructions.md
    │         (VS Code + coding agent only)
    └── NO  → Does it define a role or workflow?
        ├── YES → Use .github/agents/*.agent.md
        │         (VS Code Chat only)
        └── NO  → Put it in docs/*.md as referenceable knowledge
                  (VS Code via #file:, CLI via semantic search)
```

**Rule of thumb**: If you can only put context in ONE place, put it in
`.github/copilot-instructions.md`. Everything else is a surface-specific
enhancement that improves the experience on surfaces that support it.

## Limitations of CLI

- Single prompt → single response (use `-p` for non-interactive)
- No file attachment (`#file:` is VS Code Chat only)
- No agent invocation (`@agent` is VS Code Chat only)
- No prompt files (`/prompt` is VS Code Chat only)
- No custom instructions with path scoping
- No MCP tool access
- No pre/post-edit hooks

The CLI is best for:

- Quick code suggestions when you're already in the terminal
- Explaining unfamiliar code files
- Generating git or shell commands
- Verifying that your portable context (instructions) works without VS Code
