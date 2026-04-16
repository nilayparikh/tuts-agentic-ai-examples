# Lesson 05 — Implementation Workflows

> **App:** Loan Workbench (TypeScript Express API + SQLite)
> **Topic:** Specialized agents for implementation, review, and testing with different tool access and responsibilities.

## Prerequisite — Lesson 04 Plan

This lesson continues from the plan produced in
[Lesson 04 — Planning Workflows](../04-planning-workflows). That lesson
investigates the notification-preferences feature request, inspects the
architecture, product spec, ADR, and NFRs, then writes a structured
implementation plan to `docs/notification-preferences-plan.md`.

Lesson 05 picks up that plan and executes one focused implementation slice:
hardening the notification-preference write path with a pure rule module,
matching tests, and minimal route wiring.

## Setup

```bash
python util.py --setup
python util.py --run
```

## Validation

After running `--demo` or making manual changes, validate that everything works:

```bash
python util.py --test
```

This runs:

1. **Backend tests** — `vitest run` for all backend unit and integration tests
2. **UI tests** — Playwright Python tests that verify API rule enforcement and frontend rendering

Prerequisites: `pip install playwright pytest` and `python -m playwright install chromium`.

Verified on 2026-04-16:

- `python util.py --demo --model gpt-5.4` completed and wrote the captured artifacts under `.output/`
- `.output/change/comparison.md` reported `Files match: True` and `Patterns match: True`
- the captured change set matched the intended three-file implementation slice
- `python util.py --test` passed on the checked-in workspace with 29 backend tests and 13 UI tests

This is the key lesson: patch-shape comparison is useful, but it is not enough on its
own. The real gate is the validator. In the current checked-in example, both the patch
comparison and the end-to-end test suite agree.

## What This Demonstrates

Three agents with different capabilities form an implementation workflow.

| Agent         | Tools                                 | Role                    |
| ------------- | ------------------------------------- | ----------------------- |
| `implementer` | edit, terminal, code search, problems | Writes focused code     |
| `reviewer`    | code search, problems, usages         | Reviews without editing |
| `tester`      | edit, terminal, tests                 | Writes and runs tests   |

This lesson also includes a TDD skill and prompt files for structured implementation and review.

## Example Goal

This lesson should demonstrate a focused implementation slice, not a sprawling feature branch.

For this example, the intended outcome is:

- add one pure notification-preference write rule with explicit edge-case coverage
- wire the minimal production change into the existing single-write notification route
- add tests that cover a happy path, a false positive, and a hard negative
- leave protected config and database files untouched

## Context Files

| Path                                             | Purpose                                                   |
| ------------------------------------------------ | --------------------------------------------------------- |
| `docs/notification-preferences-plan.md`          | Implementation plan produced by Lesson 04 planner agent   |
| `docs/architecture.md`                           | System architecture and rule-placement conventions        |
| `docs/implementation-playbook.md`                | Implementation standards and role boundaries              |
| `docs/implementation-workflow-example.md`        | Concrete lesson-05 demo target and assessment constraints |
| `specs/product-spec-notification-preferences.md` | Product specification (FR-1–FR-6, SC-1–SC-3)              |
| `specs/non-functional-requirements.md`           | NFR constraints                                           |
| `.github/agents/implementer.agent.md`            | Implementation agent definition                           |
| `.github/agents/reviewer.agent.md`               | Review agent definition                                   |
| `.github/agents/tester.agent.md`                 | Testing agent definition                                  |
| `.github/prompts/implement-feature.prompt.md`    | Feature implementation workflow                           |
| `.github/prompts/review-changes.prompt.md`       | Review workflow                                           |
| `.github/skills/tdd-workflow/SKILL.md`           | TDD skill                                                 |

## Copilot CLI Workflow

The CLI cannot switch into custom agents, but it can still provide a baseline implementation prompt.

```bash
copilot -p "Read docs/notification-preferences-plan.md first — this is the implementation plan from the planning workflow. Then inspect docs/, specs/, and the relevant notification-preference write surfaces you discover in this lesson before editing. Use the playbook and example doc as success criteria, not as a fixed file checklist. Add one focused notification-preference write rule plus matching tests, then wire the minimal production change into the route. Keep delegated-session and role guards, enforce mandatory-event and LEGAL-218 edge cases, keep the scope to the current notification write path, and do not edit protected config or database files. In the final handoff, state which behaviors the tests should fail on before the production change and which should pass after it, and name any intentionally deferred write surfaces that remain out of scope. Do not use SQL or task/todo write tools." --allow-all-tools --deny-tool=sql
```

For review-oriented prompting:

```bash
copilot -p "Review the notification preferences implementation for security issues, missing audit entries, and NFR compliance." --allow-all-tools
```

Expected outcome:

- the CLI reads the plan from Lesson 04 and uses it to scope the implementation slice
- the CLI makes a focused implementation change in `src/backend/src/` plus matching unit tests
- the change reflects the playbook's rule/service/route boundaries rather than inlining everything in the route
- the run stays constrained to repo file work instead of side-effecting task/todo tools
- the handoff explains the expected test-first red/green behavior even though the CLI run does not execute tests
- the handoff makes the scope boundary explicit by naming any still-deferred preference-write surfaces
- the result is still a baseline approximation, not true multi-agent separation, because the CLI cannot switch agents mid-run

## VS Code Chat Workflow

Start by reviewing the plan from Lesson 04:

```text
Read docs/notification-preferences-plan.md and summarize the implementation tasks relevant to hardening the notification-preference write path.
```

Implement with `@implementer`:

```text
Implement the notification preference write hardening from the plan. Create the rule, wire the route, and follow the playbook conventions.
```

Test with `@tester`:

```text
Write tests for the notification preference write rules. Follow TDD and verify they pass.
```

Review with `@reviewer`:

```text
Review the notification preferences implementation against the plan, product spec, and NFRs. Check for security issues, missing audit entries, and edge-case coverage.
```

You can also run the prompt file workflow for feature implementation and review.

For the captured demo run, use `python util.py --demo --model gpt-5.4`.

After any demo or manual implementation, validate with `python util.py --test`.

If the Copilot CLI is slow to export `session.md` on your machine, you can tune the
demo window without editing code:

```bash
$env:CTX_SDLC_DEMO_TIMEOUT = "600"
$env:CTX_SDLC_DEMO_IDLE_TIMEOUT = "180"
python util.py --demo
```

## Cleanup

```bash
python util.py --clean
```

---

## Series Navigation

| #   | Lesson                    | Video                                                                                                     | Example Code                                                    |
| --- | ------------------------- | --------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| 01  | Why Context Engineering   | <a href="https://www.youtube.com/watch?v=YBXo_hxr9k4" target="_blank" rel="noopener noreferrer">Watch</a> | [01-why-context-engineering](../01-why-context-engineering)     |
| 02  | Curate Project Context    | <a href="https://www.youtube.com/watch?v=1B90MkDnmhs" target="_blank" rel="noopener noreferrer">Watch</a> | [02-curate-project-context](../02-curate-project-context)       |
| 03  | Instruction Architecture  | <a href="https://www.youtube.com/watch?v=BS2NbFnyYJY" target="_blank" rel="noopener noreferrer">Watch</a> | [03-instruction-architecture](../03-instruction-architecture)   |
| 04  | Planning Workflows        | <a href="https://www.youtube.com/watch?v=KuLgT8Wck_E" target="_blank" rel="noopener noreferrer">Watch</a> | [04-planning-workflows](../04-planning-workflows)               |
| 05  | Implementation Workflows  | _Coming soon_                                                                                             | [05-implementation-workflows](../05-implementation-workflows)   |
| 06  | Tools and Guardrails      | _Coming soon_                                                                                             | [06-tools-and-guardrails](../06-tools-and-guardrails)           |
| 07  | Surface Strategy          | _Coming soon_                                                                                             | [07-surface-strategy](../07-surface-strategy)                   |
| 08  | Operating Model           | _Coming soon_                                                                                             | [08-operating-model](../08-operating-model)                     |
| 09  | AI-Assisted SDLC Capstone | _Coming soon_                                                                                             | [09-ai-assisted-sdlc-capstone](../09-ai-assisted-sdlc-capstone) |

Full Course: <a href="https://tuts.localm.dev/ctx-sdlc" target="_blank" rel="noopener noreferrer">Context Engineering for GitHub Copilot</a>
