# Loan Workbench Architecture

## Product Scope

Loan Workbench supports intake, underwriting review, document collection, and
final decision workflows for commercial loan applications.

## System Shape

```
src/
  backend/
    src/
      app.ts                ← Express entry point, middleware chain
      config/               ← Environment config, feature flags
      db/                   ← SQLite connection, schema, seed, migrations
      middleware/           ← Auth, audit logger, error handler, rate limiter
      queue/                ← In-process event broker + handlers
      models/               ← Domain types + DB repository classes
      routes/               ← HTTP route handlers
      rules/                ← State machine, business rules, role permissions
      services/             ← Business logic orchestration
    tests/
      unit/                 ← Pure function and rule tests
      integration/          ← Route + service tests
  frontend/
    src/
      api/                  ← Typed HTTP client
      pages/                ← Dashboard, detail, preferences
      components/           ← UI building blocks
    styles/
```

## Instruction Scoping

Instructions are scoped to match the source structure:

| Instruction File                 | `applyTo`                       | Covers                     |
| -------------------------------- | ------------------------------- | -------------------------- |
| `copilot-instructions.md`        | all files                       | Global conventions         |
| `backend.instructions.md`        | `src/backend/src/**/*.ts`       | Route and service patterns |
| `business-rules.instructions.md` | `src/backend/src/rules/**`      | Rule authoring standards   |
| `security.instructions.md`       | `src/backend/src/middleware/**` | Auth and security patterns |
| `testing.instructions.md`        | `src/backend/tests/**`          | Test conventions           |

This layering means editing a file in `src/backend/src/rules/` activates three
instruction files simultaneously: global, backend, and business-rules.

## Lesson 03 Example Target

The lesson demo should deliberately cross instruction boundaries.

The preferred change is:

- add a pure rule module in `src/backend/src/rules/notification-channel-rules.ts`
- add matching tests in `src/backend/tests/unit/notification-channel-rules.test.ts`
- keep the rule pure and side-effect free
- keep the tests explicit and behavior-oriented

That combination lets the model pick up repository-wide rules, backend conventions, business-rule conventions, and test conventions in one task.
*** Add File: Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\lessons\03-instruction-architecture\docs\instruction-layering-example.md
# Lesson 03 — Instruction Layering Example

This document defines the concrete example used in Lesson 03.

## Objective

Show that layered instruction files improve both where GitHub Copilot CLI edits and how it structures the generated code.

The example should touch two scoped surfaces:

- `src/backend/src/rules/notification-channel-rules.ts`
- `src/backend/tests/unit/notification-channel-rules.test.ts`

## Expected Change Shape

The preferred implementation for this lesson is:

- create a new pure business-rule module for notification channel changes
- create matching unit tests that mirror the source path
- keep the change local to the rule and its tests

## Required Constraints

These constraints are part of the example and must be preserved by the generated code:

1. The rule module must stay pure: no Express imports, no database access, no audit writes, no queue usage.
2. The rule module must return structured results rather than a bare boolean.
3. California-specific restriction text must include `LEGAL-218` in both the rule metadata and the human-readable reason.
4. The module header comments must document one false positive and one hard negative scenario.
5. The tests must cover happy path, boundary case, false positive, and hard negative scenarios.
6. The tests must use explicit assertions rather than snapshots.
7. Do not modify `src/backend/src/models/types.ts` for this lesson.
8. Do not run shell commands during the assessment run.

## Concrete Scenario

For this lesson, the rule should validate notification channel changes for mandatory events.

The intended hard case is:

- on California loans, decline notifications must not end up with every channel disabled
- disabling SMS is acceptable when email remains enabled
- disabling the last enabled channel for a California decline notification should fail with a structured `LEGAL-218` reason

Good output usually introduces a function like `validateNotificationChannelChange(...)` with a narrow input shape and a structured result object.

## What Good Output Looks Like

Good output will usually:

- add one rule file and one matching test file
- keep all business logic inside the rule module
- keep tests close to the instruction language: false positive, hard negative, and boundary cases should be visible in test names or comments
- avoid inventing services, repositories, or new global domain types
