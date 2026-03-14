# Lesson 02 — Curate Project Context

> **App:** Loan Workbench (TypeScript Express API + SQLite)
> **Topic:** Building the shared context layer: `.github/` for behavior and `docs/` for knowledge.

## Setup

```bash
python util.py --setup
python util.py --run
```

## What This Demonstrates

Context has two complementary halves:

| Layer | Location | Contains | Activation |
| --- | --- | --- | --- |
| Behavior | `.github/` | How the model should behave | Auto-loaded by Copilot |
| Knowledge | `docs/` | What the model should know | Read or searched as needed |

## Context Files

| Path | Purpose |
| --- | --- |
| `.github/copilot-instructions.md` | Project-level behavioral guidance |
| `docs/architecture.md` | System architecture knowledge |
| `docs/api-conventions.md` | API design standards |
| `docs/preference-management-example.md` | The concrete lesson-02 target and constraints |

## Example Goal

This lesson is not trying to show that AI can add any random route.

It is trying to show that curated context helps the CLI make a small backend change that still respects repository standards and constraints.

For this example, the intended change is:

- harden the existing notification preference write routes
- keep the change inside `backend/src/routes/notifications.ts`
- preserve owner-only writes, delegated-session blocking, compliance-reviewer read-only behavior, audit logging, and central error-prefix handling
- prefer a small local refactor that makes the generic route and the email/SMS routes follow the same rules

## Copilot CLI Workflow

Ask for architectural understanding and generation from the lesson root:

```bash
copilot -p "What is the architecture of this project, and what coding conventions should I follow for backend route changes?" --allow-all-tools
```

Then ask for generation:

```bash
copilot -p "First inspect the existing notification-preference write surface in this lesson to discover the current authorization, audit, and error-handling conventions. Then refactor notification preference write handlers so the generic route and the existing email/SMS routes follow the same owner-only, delegated-session, audit, and FORBIDDEN-error conventions." --allow-all-tools
```

The lesson demo helper runs this generation prompt, writes the CLI prompt/session artifacts into `.output/`, and is intended to use GitHub Copilot's Gemini Flash model when that model is exposed by the CLI surface.

Expected outcome:

- behavior guidance comes through strongly from `.github/`
- knowledge from `docs/` is available only if the model chooses to read it
- the generation prompt still requires context discovery instead of assuming route behavior from the prompt alone
- the best output should tighten `notifications.ts`, keep audit behavior, and preserve the repository's write constraints with a small local refactor

## VS Code Chat Workflow

Compare three modes.

Behavior only:

```text
Add a route for preference management. Users save notification channel preferences (email, SMS) per event type.
```

Knowledge only:

- explicitly attach `docs/architecture.md`
- ask the same prompt

Both together:

- keep `.github/copilot-instructions.md` in the workspace
- expose `docs/architecture.md` and `docs/api-conventions.md`
- ask the same prompt again

Expected result: the model becomes both style-consistent and architecturally correct.

## Cleanup

```bash
python util.py --clean
```
