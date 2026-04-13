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
    db/                     ← SQLite connection, schema, seed data, migrations
    middleware/             ← Auth, audit logger, error handler, rate limiter
    queue/                  ← In-process pub/sub broker + handlers
    models/                 ← Domain types + repository classes (DB CRUD)
    routes/                 ← HTTP route handlers
    rules/                  ← State machine, business rules, permissions
    services/               ← Orchestration layer (loan, decision, notification, audit)
  tests/                    ← Unit + integration tests
  frontend/
  src/
    api/                    ← Typed HTTP client
    pages/                  ← Dashboard, detail, preferences
    components/             ← UI building blocks
  styles/                   ← CSS
```

## Key Constraints

1. Loan applications follow a strict state machine (`VALID_TRANSITIONS`).
2. California loans have jurisdiction-specific rules (min $50K, max $5M).
3. Approval authority depends on loan amount and user role.
4. Notification preferences support SMS → email fallback.
5. Audit logging is mandatory for all mutating operations.
6. The queue broker uses typed message contracts — changing them is a breaking change.

## Lesson 01 Experiment Notes

This lesson intentionally uses a workflow whose requirements are spread across
multiple files. A model without repository context will often produce code that
looks competent but violates repo rules.

For the canonical experiment, see `docs/manual-review-escalation.md`.
