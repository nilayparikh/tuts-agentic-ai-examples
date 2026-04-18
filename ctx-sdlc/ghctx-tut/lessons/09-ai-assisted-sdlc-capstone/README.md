# Lesson 09 — AI-Assisted SDLC Capstone

> <strong>Website:</strong> <a href="https://tuts.localm.dev/" target="_blank" rel="noopener noreferrer">LocalM Tuts</a>
> <strong>Course Page:</strong> <a href="https://tuts.localm.dev/ctx-sdlc" target="_blank" rel="noopener noreferrer">Context Engineering for GitHub Copilot</a>

> **App:** Loan Workbench (TypeScript Express API + SQLite)
> **Topic:** Hands-on capstone applying context-engineering techniques from Lessons 01–08.

## Setup

```bash
python util.py --setup
```

If a generic lesson template shows `Run: python util.py --run`, ignore it for this example. This lesson uses `util.py --setup` only.

## Overview

This capstone has four exercises. Each targets a different layer of the
context-engineering delivery loop. You'll configure context, plan with
agents, implement with role separation, and validate with guardrails —
all on the same Loan Workbench codebase.

## Prerequisites

- Complete Lessons 01–08 of Context Engineering for GitHub Copilot
- VS Code with GitHub Copilot extension
- Node.js 20+ and npm

## Setup

```bash
cd src
npm install
```

## Exercises

| Exercise | Focus                         | Guide                                                                                                  | Estimated Time |
| -------- | ----------------------------- | ------------------------------------------------------------------------------------------------------ | -------------- |
| 1        | Context Foundation            | [exercise-01-context-foundation.md](exercises/exercise-01-context-foundation.md)                       | 30–45 min      |
| 2        | Planning Workflow             | [exercise-02-planning-workflow.md](exercises/exercise-02-planning-workflow.md)                         | 30–45 min      |
| 3        | Role-Separated Implementation | [exercise-03-role-separated-implementation.md](exercises/exercise-03-role-separated-implementation.md) | 45–60 min      |
| 4        | Guardrails & Validation       | [exercise-04-guardrails-and-validation.md](exercises/exercise-04-guardrails-and-validation.md)         | 30–45 min      |

## Exercise Flow

Each exercise builds on the previous one:

```
Exercise 1: Context Foundation
  └─ Update docs, create vocabulary
      └─ Exercise 2: Planning Workflow
          └─ Create prompt file, test planning
              └─ Exercise 3: Role Separation
                  └─ Create agents, implement with TDD
                      └─ Exercise 4: Guardrails
                          └─ Create hooks, build context inventory
```

## Context Files (Starting Point)

| Path                                            | Purpose                         |
| ----------------------------------------------- | ------------------------------- |
| `.github/copilot-instructions.md`               | Project-wide conventions        |
| `.github/instructions/api.instructions.md`      | Backend API patterns            |
| `.github/instructions/frontend.instructions.md` | Frontend SPA patterns           |
| `docs/architecture.md`                          | System architecture reference   |
| `docs/VOCAB.md`                                 | Domain vocabulary               |
| `docs/capstone-example.md`                      | Capstone exercise constraints   |
| `docs/CONTEXT_MAP.md`                           | Full context map of the project |

## What You'll Create

By the end of all four exercises:

- **Updated docs:** Enhanced architecture.md + VOCAB.md (Exercise 1)
- **Prompt file:** `.github/prompts/feature-plan.prompt.md` (Exercise 2)
- **Agent files:** `.github/agents/planner.agent.md`, `.github/agents/tester.agent.md` (Exercise 3)
- **Hook configs:** `.github/hooks/audit-check.json`, `.github/hooks/test-coverage.json` (Exercise 4)
- **Context inventory:** `docs/CONTEXT_INVENTORY.md` (Exercise 4)

## Codebase Structure

```
src/
  backend/
    src/
      app.ts                  ← Express entry point
      config/                 ← Environment config, feature flags
      db/                     ← SQLite connection, schema, seed
      middleware/             ← Auth, audit logger, error handler, rate limiter
      models/                 ← Domain types + repositories
      queue/                  ← In-process event broker + handlers
      routes/                 ← HTTP route handlers
      rules/                  ← Business rules (pure logic, no I/O)
      services/               ← Business logic orchestration
    tests/
      unit/                   ← Unit tests for rules and services
      integration/            ← API integration tests
  frontend/
    src/
      api/                    ← Typed HTTP client
      pages/                  ← SPA pages
      components/             ← Reusable UI components
```

## Key Source Files

These files are central to the exercises:

| File                                                      | Relevant To                |
| --------------------------------------------------------- | -------------------------- |
| `backend/src/rules/preference-event-channel-validator.ts` | Exercise 1 (understanding) |
| `backend/src/rules/mandatory-events.ts`                   | Exercise 1 (documentation) |
| `backend/src/routes/notifications.ts`                     | Exercise 2, 3, 4           |
| `backend/src/services/audit-service.ts`                   | Exercise 3, 4              |
| `backend/src/middleware/rate-limiter.ts`                  | Exercise 2 (planning)      |
| `backend/src/models/types.ts`                             | All exercises              |

```

```
