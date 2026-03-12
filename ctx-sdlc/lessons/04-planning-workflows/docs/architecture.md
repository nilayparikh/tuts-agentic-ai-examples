# Loan Workbench Architecture

## Product Scope

Loan Workbench supports intake, underwriting review, document collection, and
final decision workflows for commercial loan applications.

## System Shape

```
backend/
  src/
    app.ts                  ← Express entry point, middleware chain
    config/                 ← Environment config, feature flags
    db/                     ← SQLite connection, schema, seed, migrations
    middleware/             ← Auth, audit logger, error handler, rate limiter
    queue/                  ← In-process event broker + handlers
      contracts.ts          ← Typed message contracts (breaking-change surface)
      broker.ts             ← Pub/sub: on(), emit(), flush()
      handlers/             ← Notification + audit event consumers
    models/                 ← Domain types + DB repository classes
    routes/                 ← HTTP route handlers
    rules/                  ← State machine, business rules, role permissions
    services/               ← Business logic orchestration
  tests/
frontend/
  src/
    api/                    ← Typed HTTP client matching backend routes
    pages/                  ← Dashboard, application detail, preferences
    components/             ← UI building blocks
  styles/
```

- `docs/` stores architecture documentation.
- `docs/adr/` stores design decisions that guide planning.
- `specs/` stores product specs and NFRs that constrain implementation.

## Key Architectural Rules

1. Backend API and frontend SPA communicate via typed HTTP client.
2. Underwriting decisions require API support and audit coverage.
3. Features affecting workflow states must specify migration and validation steps.
4. Pilot-gated features must call out rollout, observability, and fallback behavior.
5. Product rules may vary by role, loan jurisdiction, and delegated-session mode.
6. Audit is mandatory for all writes — via queue broker or direct DB write.
7. Message contracts in `backend/src/queue/contracts.ts` are a breaking-change surface.

## State Machine

Loan applications follow a strict lifecycle:

```
submitted → under_review → approved → funded
                         → denied   → closed
```

`funded` and `closed` are terminal — no transitions are allowed after them.
