# Lesson 04 — Planning Workflows

[![Watch: Mastering GitHub Copilot Plan Mode](https://img.youtube.com/vi/KuLgT8Wck_E/maxresdefault.jpg)](https://www.youtube.com/watch?v=KuLgT8Wck_E)

> <strong>Watch the video:</strong> <a href="https://www.youtube.com/watch?v=KuLgT8Wck_E" target="_blank" rel="noopener noreferrer">Mastering GitHub Copilot Plan Mode</a>
> <strong>Website:</strong> <a href="https://tuts.localm.dev/" target="_blank" rel="noopener noreferrer">LocalM Tuts</a>

> **App:** Loan Workbench (TypeScript Express API + SQLite)
> **Topic:** Read-only planning, investigation, and triage workflows using custom agents and prompt files.

## Setup

```bash
python util.py --setup
python util.py --run
```

## What This Demonstrates

Planning workflows use read-only agents and prompt files that combine docs,
specs, and codebase context to produce structured plans without editing code.

| File                                        | Type   | Purpose                    |
| ------------------------------------------- | ------ | -------------------------- |
| `.github/agents/planner.agent.md`           | Agent  | Read-only investigator     |
| `.github/prompts/investigate-bug.prompt.md` | Prompt | Bug investigation workflow |
| `.github/prompts/plan-feature.prompt.md`    | Prompt | Feature planning workflow  |
| `.github/prompts/triage-incident.prompt.md` | Prompt | Incident triage workflow   |

## Context Files

| Path                                             | Purpose                                                 |
| ------------------------------------------------ | ------------------------------------------------------- |
| `docs/architecture.md`                           | System architecture reference                           |
| `docs/adr/ADR-003-frontend-state.md`             | Architecture decision record                            |
| `specs/product-spec-notification-preferences.md` | Product specification                                   |
| `specs/non-functional-requirements.md`           | NFR constraints                                         |
| `specs/bug-report.md`                            | Sample bug report                                       |
| `specs/feature-request.md`                       | Sample feature request                                  |
| `docs/planning-workflow-example.md`              | Concrete lesson-04 demo target and planning constraints |

## Example Goal

This lesson should demonstrate planning quality through a written plan artifact.

For this example, the intended outcome is:

- investigate the notification preferences feature request
- inspect the relevant lesson docs, specs, and code surfaces first instead of relying on a hardcoded file checklist
- synthesize architecture, ADR, product spec, and NFR constraints into a structured implementation plan
- explicitly separate product requirements from inferred implementation choices
- write the plan to `docs/notification-preferences-plan.md` so the output is assessable as a code change
- the plan must explicitly call out delegated sessions, LEGAL-218, mandatory-event delivery, fail-closed audit behavior, degraded-mode fallback, at least one false positive, and at least one hard negative

## Copilot CLI Workflow

Plan a feature:

```bash
copilot -p "Inspect the relevant docs/, specs/, and existing source surfaces for notification preferences in this lesson before answering. Discover the architecture, ADR, product, and NFR context you need rather than assuming a fixed file list. Produce a structured implementation plan and save it to docs/notification-preferences-plan.md. The plan must include: summary, source-backed confirmed requirements with references to FR/SC/ADR/NFR identifiers, open questions with file references, inferred implementation choices separated from confirmed requirements, constraints and special conditions, numbered tasks with acceptance criteria and source references, validation steps, and risks/dependencies. Explicitly call out delegated sessions, LEGAL-218, mandatory-event delivery, fail-closed audit behavior, degraded-mode fallback, at least one false positive, and at least one hard negative. If the sources overlap or conflict, identify the canonical source for the plan and explain why. Do not run shell commands and do not use SQL." --allow-all-tools --deny-tool=powershell --deny-tool=sql
```

Expected outcome:

- the CLI writes a structured plan to `docs/notification-preferences-plan.md`
- the plan cites FR, SC, ADR, and NFR sources instead of giving a shallow task list
- the plan explains which source should be treated as canonical if multiple lesson artifacts overlap or conflict
- the plan surfaces hidden complexity such as delegated sessions, LEGAL-218, fail-closed audit behavior, and degraded-mode fallback
- `.output/change/demo.patch` contains the plan file addition
- `.output/change/comparison.md` shows actual vs expected file and pattern match results

## VS Code Chat Workflow

Use the `@planner` agent for read-only investigation.

Suggested prompts:

```text
Investigate the bug described in specs/bug-report.md. Trace the data flow from the frontend save action through the API to the database and identify where stale data could be served.
```

```text
Plan the implementation of notification preferences per specs/product-spec-notification-preferences.md and specs/non-functional-requirements.md.
```

```text
Users report 500 errors on the notification preferences page during peak hours. Triage the incident and produce a root-cause hypothesis.
```

Expected result: the planner agent searches the codebase and specs, then returns a structured plan without editing files.

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
| 04  | Planning Workflows        | [Watch](https://www.youtube.com/watch?v=KuLgT8Wck_E) | [04-planning-workflows](../04-planning-workflows)               |
| 05  | Implementation Workflows  | _Coming soon_                                        | [05-implementation-workflows](../05-implementation-workflows)   |
| 06  | Tools and Guardrails      | _Coming soon_                                        | [06-tools-and-guardrails](../06-tools-and-guardrails)           |
| 07  | Surface Strategy          | _Coming soon_                                        | [07-surface-strategy](../07-surface-strategy)                   |
| 08  | Operating Model           | _Coming soon_                                        | [08-operating-model](../08-operating-model)                     |
| 09  | AI-Assisted SDLC Capstone | _Coming soon_                                        | [09-ai-assisted-sdlc-capstone](../09-ai-assisted-sdlc-capstone) |

Full Course: <https://tuts.localm.dev/ctx-sdlc>
