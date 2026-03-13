# Loan Workbench — System Architecture (Capstone)

## Product Scope

Loan Workbench supports intake, underwriting review, document collection, and
final decision workflows for commercial loan applications. This is the same
codebase used throughout Lessons 01–08; the capstone applies all context-
engineering surfaces learned so far.

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
  frontend/
    src/
      api/                    ← Typed HTTP client matching backend routes
      pages/                  ← Dashboard, application detail, preferences
      components/             ← Reusable UI components
    styles/
```

## Key Architectural Rules

1. Loan lifecycle states: `submitted → under_review → approved/denied → funded/closed`.
2. State transitions validated by `app/backend/src/rules/state-machine.ts`.
3. California loans have jurisdiction-specific rules in `app/backend/src/rules/business-rules.ts`.
4. Role-based permissions are defined in `app/backend/src/rules/role-permissions.ts`.
5. Audit logging is mandatory for all writes — either via queue broker or direct DB insert.
6. Notification delivery supports SMS → email fallback based on provider health.
7. Message contracts in `app/backend/src/queue/contracts.ts` are a breaking-change surface.

## API Conventions

- All endpoints under `/api/` prefix.
- Auth: `x-user-id` header identifies caller; `x-delegated-for` enables delegated sessions.
- Error responses: `{ error: string }` body with appropriate HTTP status.
- State transitions not in the valid set are rejected with 422.
