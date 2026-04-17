# Loan Workbench API Reference

## Authentication

All API routes require authentication via `authMiddleware`.
Role-based access is enforced by `requireRole(role)`.

## Endpoints

### Applications

| Method | Path                    | Role      | Description             |
| ------ | ----------------------- | --------- | ----------------------- |
| GET    | `/api/applications`     | viewer    | List all applications   |
| POST   | `/api/applications`     | submitter | Create new application  |
| GET    | `/api/applications/:id` | viewer    | Get application details |
| PUT    | `/api/applications/:id` | submitter | Update application      |

### Decisions

| Method | Path                            | Role     | Description                   |
| ------ | ------------------------------- | -------- | ----------------------------- |
| POST   | `/api/decisions`                | approver | Submit a decision             |
| GET    | `/api/decisions/:applicationId` | viewer   | Get decisions for application |

### Notifications

| Method | Path                      | Role     | Description               |
| ------ | ------------------------- | -------- | ------------------------- |
| GET    | `/api/notifications`      | viewer   | List notification history |
| POST   | `/api/notifications/send` | notifier | Trigger notification      |

### Audit

| Method | Path                   | Role    | Description          |
| ------ | ---------------------- | ------- | -------------------- |
| GET    | `/api/audit`           | auditor | Query audit trail    |
| GET    | `/api/audit/:entityId` | auditor | Get audit for entity |

### Queue Status

| Method | Path                | Role  | Description            |
| ------ | ------------------- | ----- | ---------------------- |
| GET    | `/api/queue-status` | admin | Queue health and stats |

## Error Responses

All errors follow this shape:

```json
{ "error": "Human-readable error message" }
```

The centralized error handler maps error message prefixes to HTTP status codes:

| Prefix           | Status |
| ---------------- | ------ |
| `VALIDATION:`    | 400    |
| `NOT_FOUND:`     | 404    |
| `FORBIDDEN:`     | 403    |
| `INVALID_STATE:` | 409    |
| (unmatched)      | 500    |
