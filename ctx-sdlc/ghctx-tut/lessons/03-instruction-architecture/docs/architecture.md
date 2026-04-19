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
