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
      unit/                   ← Unit tests (one per rule/service module)
      integration/            ← API-level integration tests
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

## Notification Subsystem

The notification subsystem handles user-facing alerts for loan lifecycle events.

### Delivery Pipeline

```
State transition → Mandatory event check → Channel routing → Delivery attempt → Audit log
```

1. **Mandatory events** — defined in `backend/src/rules/mandatory-events.ts`. Certain
   state transitions require specific notification events. Skipping a mandatory event
   is a compliance violation.
2. **Channel routing** — notifications are delivered via `email` or `sms`. The system
   supports SMS → email fallback when the SMS provider is unhealthy.
3. **Preference control** — users set per-event channel preferences via
   `PUT /api/notifications/preferences`. The preference-event-channel validator
   enforces business rules before persistence.

### Event-Channel Validation

The `preference-event-channel-validator.ts` rule module enforces two constraints:

1. **Mandatory event protection** — events that appear in `MANDATORY_EVENTS` must keep
   at least one delivery channel enabled. You cannot disable both email and SMS for a
   mandatory event.
2. **LEGAL-218 (California SMS restriction)** — California decline notifications cannot
   disable SMS unless email remains enabled as a fallback for that event. Because
   preference writes are global (not loan-scoped), the validator defaults to
   California-restricted mode when no loan state context is available.

### Notification Preferences Data Model

```typescript
interface NotificationPreference {
  userId: string;
  event: NotificationEvent; // "approval" | "decline" | "document-request" | "manual-review-escalation"
  channel: NotificationChannel; // "email" | "sms"
  enabled: boolean;
  updatedAt: string;
  updatedBy: string;
}
```

### Route Authorization

- **Read**: underwriter, analyst-manager, compliance-reviewer
- **Write**: underwriter, analyst-manager only
- **Delegated sessions**: read-only — cannot modify preferences

## Three-Layer Separation

Every backend feature follows the same three-layer pattern:

| Layer    | Location        | Responsibility                     | I/O Allowed |
| -------- | --------------- | ---------------------------------- | ----------- |
| Routes   | `src/routes/`   | HTTP handling, param extraction    | Yes         |
| Rules    | `src/rules/`    | Pure business logic, validation    | No          |
| Services | `src/services/` | Persistence, external calls, audit | Yes         |

Request flow: Route → authenticate → authorize → validate → Rule → Service → respond.

## Audit Requirements

Audit events are recorded BEFORE persistence — if logging fails, the write
does NOT proceed (fail-closed semantics). Every mutating route handler must
call the audit service. Audit entries include:

- `action` — what happened
- `actor` — who did it
- `target` — what was affected
- `timestamp` — when it happened
- `details` — additional context (JSON)

## Testing Conventions

- Test framework: Vitest
- Unit tests mirror rule modules: `rules/foo.ts` → `tests/unit/foo.test.ts`
- Integration tests use the full Express app via supertest
- All rule modules must have a matching unit test file
- Tests import from `../src/` — never from compiled output
