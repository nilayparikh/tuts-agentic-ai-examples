# Lesson 09 — AI-Assisted SDLC Capstone

> **App:** Loan Workbench (TypeScript Express API + SQLite)
> **Topic:** Full SDLC synthesis combining the context-engineering techniques from Lessons 01-08.

## Setup

```bash
python util.py --setup
python util.py --run
```

## What This Demonstrates

This capstone combines the live context surfaces that are actually present in the lesson into one cross-stack workflow:

- global project instructions
- backend-scoped instructions
- frontend-scoped instructions
- shared architecture documentation
- discovered backend and frontend implementation surfaces

The point of the lesson is not breadth for its own sake. It is to show that a discovery-first workflow can build a credible backend-plus-frontend plan without hardcoding all of the context into the prompt.

## Context Files

| Path | Purpose |
| --- | --- |
| `.github/copilot-instructions.md` | Project-wide conventions |
| `.github/instructions/api.instructions.md` | API-specific patterns |
| `.github/instructions/frontend.instructions.md` | Frontend-specific patterns |
| `docs/architecture.md` | System architecture reference |
| `docs/capstone-example.md` | Concrete lesson-09 demo target and assessment constraints |

## Example Goal

This lesson should demonstrate cross-stack SDLC implementation quality.

For this example, the intended outcome is:

- inspect the capstone's baseline instructions, backend/frontend scoped instructions, architecture doc, and relevant notification-preference code surfaces
- discover the specific backend route, backend supporting surfaces, frontend page, frontend component, and API-client surfaces instead of relying on a hardcoded read list
- implement a notification preference event-channel validator with unit tests
- wire the validator into the existing notification route
- the changes are assessable via actual vs expected file and pattern comparison

## Copilot CLI Workflow

Use the CLI for a discovery-first capstone implementation:

```bash
copilot -p "Inspect the capstone lesson's project instructions, backend and frontend scoped instructions, architecture doc, and the relevant backend/frontend notification-preference surfaces you discover before answering. Do not assume a fixed file list beyond those starting points. Then implement a notification preference event-channel validator as a cross-stack hardening slice: 1. Create a pure validation rule module at backend/src/rules/preference-event-channel-validator.ts that validates event-channel combinations are allowed, enforcing that mandatory events cannot have all channels disabled, and respecting LEGAL-218 California SMS restrictions from existing rules. 2. Create unit tests at backend/tests/unit/preference-event-channel-validator.test.ts covering valid combinations, mandatory-event violations, and LEGAL-218 false positive and hard negative cases. 3. Wire the validator import into the existing notification preference write route in backend/src/routes/notifications.ts. Follow the repository conventions you discover. Apply the changes directly in code. Do not run npm install, npm test, or any shell commands. Do not use SQL." --allow-all-tools --deny-tool=powershell --deny-tool=sql
```

Expected result:

- the CLI creates a validator module and matching tests using discovered conventions
- the validator is wired into the existing route
- mandatory-event and LEGAL-218 constraints are enforced
- `.output/change/demo.patch` contains all file changes
- `.output/change/comparison.md` shows actual vs expected file and pattern match results

## VS Code Chat Workflow

Suggested capstone flow:

1. Start with a planning ask that identifies the backend and frontend surfaces involved.
2. Open backend files where API instructions activate and refine the backend slice.
3. Open frontend files where frontend instructions activate and refine the UX slice.
4. Compare which requirements are globally portable versus scoped to one surface.
5. Reflect on which earlier lesson patterns are being reused in the capstone.

Expected result: learners see how a discovery-first prompt plus scoped instruction activation can produce a practical cross-stack SDLC plan.

For the captured demo run, use `python util.py --demo --model gpt-5.4`.

## Cleanup

```bash
python util.py --clean
```
