# Lesson 07 — Surface Strategy

[![Watch: Context Engineering the Multi-Agent Era: Copilot, Claude, and Codex](https://img.youtube.com/vi/XvUSBlrXZoA/maxresdefault.jpg)](https://www.youtube.com/watch?v=XvUSBlrXZoA)

> <strong>Watch the video:</strong> <a href="https://www.youtube.com/watch?v=XvUSBlrXZoA" target="_blank" rel="noopener noreferrer">Context Engineering the Multi-Agent Era: Copilot, Claude, and Codex</a>
> <strong>Website:</strong> <a href="https://tuts.localm.dev/" target="_blank" rel="noopener noreferrer">LocalM Tuts</a>

> **App shape:** Loan Workbench (TypeScript + Express + SQLite)
> **Teaching goal:** Show how reusable application context feeds multiple
> coding agents through a clean data/format separation.

## Important Framing

This lesson is not here to run the app.

It is here to show and walk through the context architecture itself — how
application knowledge lives in one place and gets projected into tool-native
formats for GitHub Copilot, Claude Code, and Codex.

## What This Demonstrates

| Artifact                                                    | Role                             | Why it matters                                                      |
| ----------------------------------------------------------- | -------------------------------- | ------------------------------------------------------------------- |
| `.code.agent/context/*.md`                                  | Reusable application context     | All app knowledge lives here — written once, never duplicated       |
| `.code.agent/templates/*.tpl`                               | Pure format shells               | Agent-specific structure with zero application content              |
| `.code.agent/graph.json`                                    | Context-to-output mapping        | Declares which context feeds which template to produce which output |
| `transform.py`                                              | Generation engine                | Reads context, applies templates, writes outputs                    |
| `AGENTS.md`                                                 | Shared projection (Codex/humans) | Generated from `app-identity.md` context                            |
| `CLAUDE.md`                                                 | Claude bridge                    | Imports `@AGENTS.md` — no content duplication                       |
| `.github/copilot-instructions.md`                           | Copilot bridge                   | Generated from `app-identity.md` context                            |
| `.github/instructions/*.instructions.md`                    | Copilot scoped rules             | Generated from backend/frontend/testing/api context                 |
| `.claude/rules/*.md`                                        | Claude scoped rules              | Same context as Copilot, different format                           |
| `.github/agents/reviewer.agent.md`                          | Reviewer agent                   | Generated from reviewer checklist context                           |
| `.github/skills/loan-workbench-delivery/SKILL.md`           | Delivery skill                   | Generated from delivery workflow context                            |
| `.github/prompts/implement-loan-workbench-change.prompt.md` | Planning prompt                  | Generated from change planning context                              |
| `.github/hooks/context-guard.json`                          | Context guard hook               | Generated from hook configuration context                           |
| `docs/*.md`                                                 | Application documentation        | Documents the `src/` app — architecture, API, features, data model  |

## No Setup Required

There is nothing to install for the lesson story.

You can optionally run `python util.py --summary` to print the walkthrough map,
but the lesson works by reading files, not by starting services.

If you change the context or templates, run `python transform.py --write` to
refresh the generated outputs.

## Context Pack Layout

```text
07-surface-strategy/
  .code.agent/
    graph.json
    context/
      app-identity.md
      backend.md
      frontend.md
      testing.md
      api-routes.md
      delivery-workflow.md
      change-planning.md
      reviewer-checklist.md
      context-guard.md
    templates/
      agents.md.tpl
      claude-bridge.md.tpl
      copilot-bridge.md.tpl
      copilot-instruction.md.tpl
      claude-rule.md.tpl
      copilot-agent.md.tpl
      copilot-skill.md.tpl
      copilot-prompt.md.tpl
      hook.json.tpl
  AGENTS.md                          ← generated
  CLAUDE.md                          ← generated
  .github/
    copilot-instructions.md          ← generated
    instructions/
      backend.instructions.md        ← generated
      frontend.instructions.md       ← generated
      tests.instructions.md          ← generated
      api.instructions.md            ← generated
    agents/
      reviewer.agent.md              ← generated
    skills/
      loan-workbench-delivery/
        SKILL.md                     ← generated
    prompts/
      implement-loan-workbench-change.prompt.md  ← generated
    hooks/
      context-guard.json             ← generated
  .claude/
    rules/
      backend.md                     ← generated
      frontend.md                    ← generated
      tests.md                       ← generated
      api.md                         ← generated
  docs/
    architecture.md
    api-reference.md
    feature-map.md
    data-model.md
  transform.py
```

## Key Design Principle

Context is DATA — it holds application knowledge in `.code.agent/context/`.
Templates are FORMAT — they hold agent-specific structural wrappers in
`.code.agent/templates/`. The two never cross. Templates contain zero
application knowledge. Context contains zero agent-specific formatting.
`transform.py` maps one to the other through `graph.json`. 5. Let Claude import that projection through `CLAUDE.md`. 6. Let Copilot use `.github/copilot-instructions.md` as its bridge. 7. Generate skills, prompts, hooks, and scoped rules from the same model. 8. Keep scoped rules tool-native, but semantically aligned.

That is the practical portability lesson. Shared intent matters more than file
name uniformity.

## Walkthrough Order

Use this order when presenting the example:

1. Start with `AGENTS.md` and explain the shared base.
2. Open `docs/context-graph.md` and show the graph.
3. Open `.code.agent/graph.json` and `.code.agent/templates/`.
4. Open `transform.py` and explain the projection step.
5. Open `CLAUDE.md` and show the import pattern.
6. Open `.github/copilot-instructions.md` and explain the Copilot bridge.
7. Compare `.github/instructions/api.instructions.md` with `.claude/rules/api.md`.
8. Finish with `docs/portability-matrix.md` and
   `docs/surface-portability-notes.md`.

## What You Should Say Out Loud

- "This repo is a context specimen, not a runnable app demo."
- "AGENTS.md is the shared story."
- "Claude imports the shared story. Copilot needs its own bridge."
- "Scoped rules stay native to each tool, but the semantics match."
- "Docs carry the explanation so the entry files stay small."

## Series Navigation

| #   | Lesson                                                                    | Video                                       | Example                                                        |
| --- | ------------------------------------------------------------------------- | ------------------------------------------- | -------------------------------------------------------------- |
| 01  | Context Engineering for GitHub Copilot [Course Intro] \| Lesson 01        | https://www.youtube.com/watch?v=YBXo_hxr9k4 | [01-why-context-engineering](../01-why-context-engineering/)   |
| 02  | GitHub Copilot: Mastering .github/ and /docs/ \| Lesson 02 of 09          | https://www.youtube.com/watch?v=1B90MkDnmhs | [02-curate-project-context](../02-curate-project-context/)     |
| 03  | The 3-Axis Model: Precision Context for GitHub Copilot \| Lesson 03 of 09 | https://www.youtube.com/watch?v=BS2NbFnyYJY | [03-instruction-architecture](../03-instruction-architecture/) |
| 04  | Mastering GitHub Copilot Plan Mode                                        | https://www.youtube.com/watch?v=KuLgT8Wck_E | [04-planning-workflows](../04-planning-workflows/)             |
| 05  | How to Build an AI "Dev Team" in GitHub Copilot \| Lesson 05 of 09        | https://www.youtube.com/watch?v=ZvclU2Jyx5o | [05-implementation-workflows](../05-implementation-workflows/) |
| 06  | Stop AI Mistakes with GitHub Copilot Hooks & Guardrails                   | https://www.youtube.com/watch?v=MBHvkVrEgRk | [06-tools-and-guardrails](../06-tools-and-guardrails/)         |
| 07  | Context Engineering the Multi-Agent Era: Copilot, Claude, and Codex       | https://www.youtube.com/watch?v=XvUSBlrXZoA | [07-surface-strategy](./)                                      |
