---
applyTo: "**"
---

# Loan Workbench — Project Context

TypeScript Express API with embedded message broker and SQLite persistence
for loan application workflow management.

## Stack

- TypeScript 5.7 strict mode, ESM imports
- Express 4.21, better-sqlite3 for persistence
- In-process event broker for async side-effects (notifications, audit)
- Vitest for tests
- Vanilla TypeScript frontend SPA

## Architecture Rules

- Backend code in `src/backend/src/`, frontend in `src/frontend/src/`
- Routes orchestrate; business rules live in `src/backend/src/rules/`
- Services handle I/O; rules are pure functions
- Audit via queue broker or direct DB write (based on `queueAudit` feature flag)
- State machine guards required for all application transitions
- Feature flags return 404 for non-pilot users (not 403)
- Delegated sessions (analyst-manager acting for another user) are read-only
- Message contracts in `src/backend/src/queue/contracts.ts` are a breaking-change surface
- Lesson 04 planning workflows are read-only. Plans should not propose direct edits until ambiguity is resolved.

## Domain

- Loan applications follow a state machine: submitted → under_review → approved/denied → funded/closed
- Notification preferences are configurable per user, per event type, per channel
- California loans have jurisdiction-specific rules (min $50K, max $5M)
- SMS → email fallback when provider is unhealthy
- Mandatory events must have at least one notification channel enabled
- Role defaults are generated on first access (no migration needed)

## Specs and Docs

- `specs/product-spec-notification-preferences.md` — functional requirements
- `specs/non-functional-requirements.md` — NFR constraints
- `docs/architecture.md` — system shape and key decisions
- `docs/adr/` — architecture decision records
