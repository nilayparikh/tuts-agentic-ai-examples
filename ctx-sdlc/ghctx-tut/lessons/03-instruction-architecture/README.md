# Lesson 03 — Instruction Architecture

[![Watch: The 3-Axis Model: Precision Context for GitHub Copilot | Lesson 03 of 09](https://img.youtube.com/vi/BS2NbFnyYJY/maxresdefault.jpg)](https://www.youtube.com/watch?v=BS2NbFnyYJY)

> <strong>Watch the video:</strong> <a href="https://www.youtube.com/watch?v=BS2NbFnyYJY" target="_blank" rel="noopener noreferrer">The 3-Axis Model: Precision Context for GitHub Copilot | Lesson 03 of 09</a>
> <strong>Website:</strong> <a href="https://tuts.localm.dev/" target="_blank" rel="noopener noreferrer">LocalM Tuts</a>
> <strong>Course Page:</strong> <a href="https://tuts.localm.dev/ctx-sdlc" target="_blank" rel="noopener noreferrer">Context Engineering for GitHub Copilot</a>

> **App:** Loan Workbench (TypeScript Express API + SQLite)
> **Topic:** Layered custom instructions scoped by file path, concern, and implementation surface.

## Setup

```bash
python util.py --setup
python util.py --run
```

## What This Demonstrates

A single global instruction file is not enough. This lesson shows layered
`.instructions.md` files that activate based on the file being edited.

| Editing                              | Active Instructions                                                                      |
| ------------------------------------ | ---------------------------------------------------------------------------------------- |
| `src/backend/src/routes/*.ts`        | `copilot-instructions.md` + `backend.instructions.md`                                    |
| `src/backend/src/rules/*.ts`         | `copilot-instructions.md` + `backend.instructions.md` + `business-rules.instructions.md` |
| `src/backend/src/middleware/auth.ts` | `copilot-instructions.md` + `backend.instructions.md` + `security.instructions.md`       |
| `src/backend/tests/*.test.ts`        | `copilot-instructions.md` + `testing.instructions.md`                                    |

## Context Files

| Path                                                  | `applyTo`                       | Purpose                                        |
| ----------------------------------------------------- | ------------------------------- | ---------------------------------------------- |
| `.github/copilot-instructions.md`                     | all files                       | Project-wide conventions                       |
| `.github/instructions/backend.instructions.md`        | `src/backend/src/**/*.ts`       | Express API patterns                           |
| `.github/instructions/business-rules.instructions.md` | `src/backend/src/rules/**`      | Business-rule authoring conventions            |
| `.github/instructions/security.instructions.md`       | `src/backend/src/middleware/**` | Auth and security patterns                     |
| `.github/instructions/testing.instructions.md`        | `src/backend/tests/**`          | Test conventions and anti-patterns             |
| `docs/architecture.md`                                | —                               | Referenced by instructions                     |
| `docs/instruction-layering-example.md`                | —                               | Concrete lesson-03 demo target and constraints |

## Example Goal

This lesson should demonstrate scoped instruction layering, not just a random backend change.

For this example, the intended change is:

- create a pure rule module at `src/backend/src/rules/notification-channel-rules.ts`
- add matching tests at `src/backend/tests/unit/notification-channel-rules.test.ts`
- make the rule and tests reflect the scoped instruction files for `rules/` and `tests/`
- preserve the repository's expectations around structured rule results, LEGAL-218 references, and explicit test categories
- reuse existing mandatory-event knowledge instead of creating a second hardcoded mandatory-event list

## Copilot CLI Workflow

Use the installed CLI from the lesson root:

```bash
copilot -p "Create a pure business-rule module at src/backend/src/rules/notification-channel-rules.ts and matching tests at src/backend/tests/unit/notification-channel-rules.test.ts. First inspect the existing backend rule and test surfaces to discover the current notification-channel conventions and the existing mandatory-event source of truth. Then implement the rule for mandatory-event channel changes, including the California decline LEGAL-218 restriction. Reuse the discovered mandatory-event source or explicit function inputs; do not assume its file path and do not create a second hardcoded mandatory-events list or helper. Follow the repository conventions you discover." --allow-all-tools
```

Expected outcome:

- the CLI can still discover repository-wide rules and scoped instruction files when it edits both `src/backend/src/rules/` and `src/backend/tests/`
- the generated rule module should stay pure, use structured results, and include LEGAL-218 in the California restriction
- the generated rule should derive mandatory-event behavior from the discovered source of truth or explicit inputs, not a duplicate in-file list or an assumed hardcoded source path
- the generated tests should mirror the new source file and cover happy path, boundary, false positive, and hard negative scenarios

The editor remains the clearest place to observe file-scoped activation, but this CLI demo is now strong enough to assess whether layered instructions were applied.

## VS Code Chat Workflow

Rules layer:

- open `src/backend/src/rules/notification-channel-rules.ts`
- ask for a pure validation rule for notification channel changes

Test layer:

- open `src/backend/tests/unit/notification-channel-rules.test.ts`
- ask for tests covering false positives and hard negatives

Security layer:

- open `src/backend/src/middleware/auth.ts`
- ask for auth or rate-limiting changes

Expected result: each location activates a different instruction stack automatically.

## Cleanup

```bash
python util.py --clean
```

---

## Series Navigation

| #   | Lesson                    | Video                                                | Example Code                                                    |
| --- | ------------------------- | ---------------------------------------------------- | --------------------------------------------------------------- |
| 01  | Why Context Engineering   | [Watch](https://www.youtube.com/watch?v=YBXo_hxr9k4) | [01-why-context-engineering](../01-why-context-engineering)     |
| 02  | Curate Project Context    | [Watch](https://www.youtube.com/watch?v=1B90MkDnmhs) | [02-curate-project-context](../02-curate-project-context)       |
| 03  | Instruction Architecture  | [Watch](https://www.youtube.com/watch?v=BS2NbFnyYJY) | [03-instruction-architecture](../03-instruction-architecture)   |
| 04  | Planning Workflows        | _Coming soon_                                        | [04-planning-workflows](../04-planning-workflows)               |
| 05  | Implementation Workflows  | _Coming soon_                                        | [05-implementation-workflows](../05-implementation-workflows)   |
| 06  | Tools and Guardrails      | _Coming soon_                                        | [06-tools-and-guardrails](../06-tools-and-guardrails)           |
| 07  | Surface Strategy          | _Coming soon_                                        | [07-surface-strategy](../07-surface-strategy)                   |
| 08  | Operating Model           | _Coming soon_                                        | [08-operating-model](../08-operating-model)                     |
| 09  | AI-Assisted SDLC Capstone | _Coming soon_                                        | [09-ai-assisted-sdlc-capstone](../09-ai-assisted-sdlc-capstone) |

Full Course: <https://tuts.localm.dev/ctx-sdlc>
