# Portability Matrix — Context Artifacts × Surfaces

Use this matrix to decide where to place context based on which surfaces
your team uses.

## Feature × Surface Support

| Context Artifact                  | VS Code Chat | VS Code Inline | GitHub CLI | Coding Agent | Code Review |
| --------------------------------- | :----------: | :------------: | :--------: | :----------: | :---------: |
| `.github/copilot-instructions.md` |      ✅      |       ✅       |     ✅     |      ✅      |     ✅      |
| `.instructions.md` (path-scoped)  |      ✅      |       ✅       |     ❌     |      ✅      |     ❌      |
| `.agent.md` (agents)              |      ✅      |       ❌       |     ❌     |      ✅      |     ❌      |
| `SKILL.md` (skills)               |      ✅      |       ❌       |     ❌     |      ❌      |     ❌      |
| `.prompt.md` (prompt files)       |      ✅      |       ❌       |     ❌     |      ✅      |     ❌      |
| `mcp.json` (tool servers)         |      ✅      |       ❌       |     ❌     |      ✅      |     ❌      |
| Copilot Hooks                     |      ✅      |       ❌       |     ❌     |      ❌      |     ❌      |
| `#file:` attachment               |      ✅      |       ❌       |     ❌     |      ✅      |     ❌      |
| `@workspace` indexing             |      ✅      |       ❌       |     ❌     |      ✅      |     ❌      |
| `docs/*.md` (semantic search)     |      ✅      |    Partial     |  Partial   |      ✅      |   Partial   |

## The Portability Pyramid

```
                    ┌─────────────┐
                    │    Hooks    │ ← VS Code only
                   ─┤   Skills   │ ← VS Code Chat only
                  ──┤   Agents   │ ← VS Code Chat + Coding Agent
                 ───┤  Prompts   │ ← VS Code Chat + Coding Agent
                ────┤    MCP     │ ← VS Code + Coding Agent
               ─────┤ .instructions.md │ ← VS Code + Coding Agent
              ──────┤ docs/*.md  │ ← all (via search / #file:)
             ───────┤ copilot-instructions.md │ ← ALL SURFACES
             ───────┴────────────────────────┘
```

**Foundation-first design**: Start at the base (most portable) and layer
upward. Each layer adds power but reduces portability.

## Decision Framework

### Choosing the Right Layer

**Question 1**: Does this context need to work for CLI users?

- YES → Must be in `.github/copilot-instructions.md` or `docs/`
- NO → Can use any layer

**Question 2**: Does this context need path activation?

- YES → Use `.instructions.md` (accepts `applyTo` globs)
- NO → Use `.github/copilot-instructions.md` for rules, `docs/` for knowledge

**Question 3**: Does this context define a role with specific tools?

- YES → Use `.agent.md` (with tool restrictions)
- NO → Use instructions or prompts

**Question 4**: Is this a repeatable multi-step workflow?

- YES → Use `.prompt.md` (with variables)
- NO → Put it in instructions

**Question 5**: Does this need automated enforcement (no human trigger)?

- YES → Use hooks (pre-commit, post-edit)
- NO → Use any appropriate layer

### Example Decisions

| Context Need                         | Correct Layer             | Why                                      |
| ------------------------------------ | ------------------------- | ---------------------------------------- |
| "Use ESM imports"                    | `copilot-instructions.md` | Universal rule, all surfaces need it     |
| "Route handlers follow this pattern" | `api.instructions.md`     | Path-scoped to `src/routes/`             |
| "Review code against checklist"      | `reviewer.agent.md`       | Role + tool restrictions                 |
| "Plan a new feature"                 | `add-feature.prompt.md`   | Repeatable workflow with variables       |
| "Block commits with TODO"            | `pre-commit-guard` hook   | Automated enforcement                    |
| "System architecture"                | `docs/architecture.md`    | Deep knowledge, not a rule               |
| "Why Express over Fastify"           | `docs/adr/ADR-001.md`     | Decision record, referenceable knowledge |

## Portability Testing Protocol

When adding or changing context, verify it works on your team's active surfaces:

### 1. VS Code Chat Test

```
Open Chat → ask about the topic → verify context is applied
```

### 2. VS Code Inline Test

```
Start typing in a relevant file → verify completions follow conventions
```

### 3. CLI Test

```bash
cd /project/root
copilot -p "relevant prompt about the topic" --allow-all
# Verify output follows conventions from copilot-instructions.md
```

### 4. Coding Agent Test

```
Open Copilot Coding Agent → describe task → verify it picks up
instructions.md, agents, and prompts
```

### 5. Code Review Test

```
Open a PR → check Copilot review suggestions → verify they reference
copilot-instructions.md conventions
```

**If it only needs to work in VS Code Chat**: any layer is fine.
**If it needs to work everywhere**: `.github/copilot-instructions.md` only.
