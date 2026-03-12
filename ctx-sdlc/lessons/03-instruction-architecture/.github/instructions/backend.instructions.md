---
applyTo: "src/backend/src/**/*.ts"
---

# Backend API Instructions

Rules for Express route handlers, services, and domain logic.

## Route Patterns

- Each route module exports a `Router` instance.
- Use `requireRole()` middleware for authorization on every route.
- Use `blockDelegatedWrites` on all mutating preference/decision routes.
- Validate request bodies at the top of each handler — return 400 for missing fields.
- Send appropriate HTTP status codes: 201 for creates, 200 for reads/updates, 204 for deletes, 422 for business rule violations.

## Service Patterns

- Services contain business logic; routes contain HTTP plumbing.
- Services must not import Express types — they receive plain TypeScript arguments.
- The audit service is a hard dependency for writes. Use the queue broker or direct DB write based on the `queueAudit` feature flag.

## State Machine

- All state transitions must go through `canTransition()` in `backend/src/rules/state-machine.ts`.
- Never assign a status directly without checking the transition table.
- `funded` and `closed` are terminal states.

## Feature Flags

- Feature flags are defined in `backend/src/config/feature-flags.ts`.
- Feature-flagged endpoints return 404 (not 403) to hide feature existence from non-pilot users.
