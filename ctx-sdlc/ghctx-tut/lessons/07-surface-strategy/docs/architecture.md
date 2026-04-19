# Loan Workbench Architecture

## System Overview

Loan Workbench is a commercial loan processing system. It manages the full
lifecycle from application submission through decisioning, notification, and
audit.

## Backend

The Express 4 backend follows a strict layering model:

```
HTTP Request
  → express.json()
  → rateLimiterMiddleware
  → authMiddleware
  → auditLoggerMiddleware
  → Route Handler
    → requireRole / validateBody
    → Business Rule
    → Service
    → Response
  → errorHandler (on failure)
```

### Routes

Each route file handles one domain surface:

| Route file | Domain |
| --- | --- |
| `applications.ts` | Loan application CRUD and state transitions |
| `decisions.ts` | Approval and rejection workflows |
| `notifications.ts` | Notification delivery and status |
| `audit.ts` | Audit log queries |
| `queue-status.ts` | Async queue monitoring |

### Services

| Service | Responsibility |
| --- | --- |
| `loanService` | Loan lifecycle management |
| `decision-service` | Approval/rejection orchestration |
| `notification-service` | Async notification dispatch via queue |
| `audit-service` | Audit trail recording |

### Rules

Business rules in `src/backend/src/rules/` are pure domain logic with no I/O.
They handle state transitions and validation for loan processing.

## Frontend

The frontend is a plain TypeScript SPA served by Vite:

- Hash-based routing initialized in `main.ts`
- `renderAppShell` creates the application shell
- Pages render into a container element
- API client in `src/frontend/src/api/` handles all backend communication

### Pages

| Page | Purpose |
| --- | --- |
| Dashboard | Overview of loan applications and status |
| Queue Monitor | Async queue health and delivery status |
| Preferences | User settings |
| API Explorer | Interactive API documentation |

## Storage

SQLite via `better-sqlite3`. Database initialization happens in
`src/backend/src/db/`.

## Testing

Vitest-based test suite:

- `src/backend/tests/unit/` — domain rule tests
- `src/backend/tests/integration/` — API contract tests
