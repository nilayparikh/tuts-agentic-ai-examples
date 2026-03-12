# TaskFlow — GitHub Copilot CLI Integration (Mature Stage)

> **Stage 5**: At maturity, the CLI is a primary productivity surface for
> terminal-native developers. This guide shows the CLI workflow alongside
> the VS Code workflow.

## Setup

```bash
# Verify Copilot CLI installation
copilot --version
```

## What Works in CLI (from TaskFlow context)

| Artifact                          | CLI Support | Notes                      |
| --------------------------------- | :---------: | -------------------------- |
| `copilot-instructions.md`         |     ✅      | Auto-loaded from repo root |
| Path-scoped `.instructions.md`    |     ❌      | VS Code only               |
| Planner / Implementer agents      |     ❌      | VS Code Chat only          |
| TDD workflow skill                |     ❌      | VS Code Chat only          |
| Prompt files (/add-feature, etc.) |     ❌      | VS Code Chat only          |
| MCP servers                       |     ❌      | VS Code only               |
| Hooks                             |     ❌      | VS Code only               |

## CLI Task Workflows

### Quick Code Generation

```bash
# The CLI picks up copilot-instructions.md automatically
copilot -p "add a Zustand store for project settings with actions to update name and toggle visibility" --allow-all

# Git operations
copilot -p "create a git command to make a feature branch for task-comments" --allow-all

# Shell operations
copilot -p "run Prisma migration for adding comments table" --allow-all
```

### Code Explanation

```bash
# Explain a complex file
copilot -p "explain packages/api/src/services/taskService.ts" --allow-all

# Explain a specific function
copilot -p "explain the authenticate middleware in packages/api/src/middleware/auth.ts" --allow-all
```

### Shell Aliases

```bash
# Add to ~/.bashrc, ~/.zshrc, or PowerShell $PROFILE
alias cop='copilot -p'

# PowerShell equivalent
function cop { copilot -p $args --allow-all }
```

### Saving Output

```bash
# Save session as markdown for documentation
copilot -p "explain the data model" --allow-all --share=output/data-model.md

# Silent mode for scripting
copilot -p "list all API routes" --allow-all -s
```
