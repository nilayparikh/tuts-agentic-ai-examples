# Lesson 07 — Surface Strategy — Walkthrough Script

This lesson is a static walkthrough. The goal is to explain the context
architecture, not to execute a CLI session.

## Suggested Walkthrough

### 1. Set the frame

Say this first:

"This example shows how application knowledge lives in one place and gets
projected into tool-native formats for Copilot, Claude, and Codex. Context is
data. Templates are format. The two never cross."

### 2. Open the context layer

Open `.code.agent/context/app-identity.md`.

Explain that all reusable application knowledge lives in `.code.agent/context/`
as markdown files. Each file covers one concern:

- `app-identity.md` — what the app is, stack, source map, shared rules
- `backend.md` — backend architecture, layering, middleware, error handling
- `frontend.md` — frontend stack, routing, rendering, API boundary
- `testing.md` — test stack, intent, change rules
- `api-routes.md` — route handler patterns, middleware chain, error shapes

### 3. Open the template layer

Open `.code.agent/templates/copilot-instruction.md.tpl`.

Point out that the template contains ONLY structural format:

- YAML frontmatter with `applyTo` scope
- A generated notice
- A `{{CONTENT}}` placeholder

Zero application knowledge. The template does not know what "Loan Workbench" is.

### 4. Show the graph

Open `.code.agent/graph.json`.

Explain that the graph maps context files through templates to outputs. Each
output entry declares:

- which context files to concatenate (`content`)
- which template to apply (`template`)
- which structural variables to fill (`vars`)

### 5. Show the generated outputs

Open `AGENTS.md` and `.github/copilot-instructions.md` side by side.

Both are generated from the same `app-identity.md` context but use different
templates — `agents.md.tpl` vs `copilot-bridge.md.tpl`.

### 6. Show Claude bridge

Open `CLAUDE.md`.

Point out that it imports `@AGENTS.md` instead of duplicating content. Claude
inherits the full context through the import.

### 7. Compare scoped parity

Open these two files side by side:

- `.github/instructions/backend.instructions.md`
- `.claude/rules/backend.md`

Same application content from `backend.md`. Different structural format.
Copilot gets `applyTo` frontmatter. Claude gets `paths` frontmatter.

### 8. Show the generation workflow

Run `python transform.py --write` to show how outputs are generated.
Run `python transform.py --check` to verify everything is in sync.

### 9. Application docs

Open `docs/architecture.md` and `docs/api-reference.md`.

These are standalone application documentation for `src/` — not context
engineering docs.

## What This Lesson Proves

1. Context (data) and templates (format) are separate concerns.
2. The same application knowledge serves Copilot, Claude, and Codex without duplication.
3. Templates contain zero application knowledge — they are pure structural shells.
4. Scoped rules stay aligned across tools because they share the same context source.
5. `docs/` documents the real application, not the context architecture.
