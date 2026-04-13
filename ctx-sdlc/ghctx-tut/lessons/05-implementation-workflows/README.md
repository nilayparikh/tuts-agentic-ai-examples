# Lesson 05 — Implementation Workflows

> **App:** Loan Workbench (TypeScript Express API + SQLite)
> **Topic:** Specialized agents for implementation, review, and testing with different tool access and responsibilities.

## Setup

```bash
python util.py --setup
python util.py --run
```

## What This Demonstrates

Three agents with different capabilities form an implementation workflow.

| Agent         | Tools                                   | Role                    |
| ------------- | --------------------------------------- | ----------------------- |
| `implementer` | edit, terminal, code search, problems   | Writes and runs code    |
| `reviewer`    | code search, problems, usages           | Reviews without editing |
| `tester`      | edit, terminal, tests, failure analysis | Writes and runs tests   |

This lesson also includes a TDD skill and prompt files for structured implementation and review.

## Example Goal

This lesson should demonstrate a focused implementation slice, not a sprawling feature branch.

For this example, the intended outcome is:

- add one pure notification-preference write rule with explicit edge-case coverage
- wire the minimal production change into the existing notification route
- add tests that cover a happy path, a false positive, and a hard negative
- leave protected config and database files untouched

## Context Files

| Path                                          | Purpose                                                   |
| --------------------------------------------- | --------------------------------------------------------- |
| `.github/agents/implementer.agent.md`         | Implementation agent definition                           |
| `.github/agents/reviewer.agent.md`            | Review agent definition                                   |
| `.github/agents/tester.agent.md`              | Testing agent definition                                  |
| `.github/prompts/implement-feature.prompt.md` | Feature implementation workflow                           |
| `.github/prompts/review-changes.prompt.md`    | Review workflow                                           |
| `.github/skills/tdd-workflow/SKILL.md`        | TDD skill                                                 |
| `docs/implementation-playbook.md`             | Implementation standards                                  |
| `docs/implementation-workflow-example.md`     | Concrete lesson-05 demo target and assessment constraints |
| `specs/non-functional-requirements.md`        | NFR constraints                                           |

## Copilot CLI Workflow

The CLI cannot switch into custom agents, but it can still provide a baseline implementation prompt.

```bash
copilot -p "Inspect docs/, specs/, and the relevant notification-preference write surfaces you discover in this lesson before editing. Use the playbook and example doc as success criteria, not as a fixed file checklist. Add one focused notification-preference write rule plus matching tests, then wire the minimal production change into the route. Keep delegated-session and role guards, enforce mandatory-event and LEGAL-218 edge cases, keep the scope to the current notification write path, and do not edit protected config or database files. In the final handoff, state which behaviors the tests should fail on before the production change and which should pass after it, and name any intentionally deferred write surfaces that remain out of scope. Do not use SQL or task/todo write tools." --allow-all-tools --deny-tool=sql
```

For review-oriented prompting:

```bash
copilot -p "Review the notification preferences implementation for security issues, missing audit entries, and NFR compliance." --allow-all-tools
```

Expected outcome:

- the CLI makes a focused implementation change in `src/backend/src/` plus matching unit tests
- the change reflects the playbook's rule/service/route boundaries rather than inlining everything in the route
- the run stays constrained to repo file work instead of side-effecting task/todo tools
- the handoff explains the expected test-first red/green behavior even though the CLI run does not execute tests
- the handoff makes the scope boundary explicit by naming any still-deferred preference-write surfaces
- the result is still a baseline approximation, not true multi-agent separation, because the CLI cannot switch agents mid-run

## VS Code Chat Workflow

Implement with `@implementer`:

```text
Implement the notification preferences feature from specs/non-functional-requirements.md. Create the route, business rules, and service layer.
```

Test with `@tester`:

```text
Write tests for the notification preferences feature. Follow TDD and verify they pass.
```

Review with `@reviewer`:

```text
Review the notification preferences implementation. Check for security issues, missing audit entries, and NFR compliance.
```

You can also run the prompt file workflow for feature implementation and review.

For the captured demo run, use `python util.py --demo --model gpt-5.4`.

## Cleanup

```bash
python util.py --clean
```
