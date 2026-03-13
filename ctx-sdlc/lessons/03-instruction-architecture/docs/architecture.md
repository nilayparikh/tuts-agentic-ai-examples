# Loan Workbench Architecture

## Product Scope

Loan Workbench supports intake, underwriting review, document collection, and
final decision workflows for commercial loan applications.

## System Shape

```
app/
  backend/
    src/
    app.ts                  ← Express entry point, middleware chain
    config/                 ← Environment config, feature flags
    db/                     ← SQLite connection, schema, seed, migrations
    middleware/             ← Auth, audit logger, error handler, rate limiter
    queue/                  ← In-process event broker + handlers
    models/                 ← Domain types + DB repository classes
    routes/                 ← HTTP route handlers
    rules/                  ← State machine, business rules, role permissions
    services/               ← Business logic orchestration
  tests/
    unit/                   ← Pure function and rule tests
    integration/            ← Route + service tests
  frontend/
  src/
    api/                    ← Typed HTTP client
    pages/                  ← Dashboard, detail, preferences
    components/             ← UI building blocks
  styles/
```

## Instruction Scoping

Instructions are scoped to match the source structure:

| Instruction File                 | `applyTo`                       | Covers                     |
| -------------------------------- | ------------------------------- | -------------------------- |
| `copilot-instructions.md`        | all files                       | Global conventions         |
| `backend.instructions.md`        | `app/backend/src/**/*.ts`       | Route and service patterns |
| `business-rules.instructions.md` | `app/backend/src/rules/**`      | Rule authoring standards   |
| `security.instructions.md`       | `app/backend/src/middleware/**` | Auth and security patterns |
| `testing.instructions.md`        | `app/backend/tests/**`          | Test conventions           |

This layering means editing a file in `app/backend/src/rules/` activates three
instruction files simultaneously: global, backend, and business-rules.
