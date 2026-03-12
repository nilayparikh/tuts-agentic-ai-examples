# Loan Workbench API Conventions

## Endpoint Patterns

| Resource              | Verb  | Path                                     | Notes                                       |
| --------------------- | ----- | ---------------------------------------- | ------------------------------------------- |
| Loan applications     | GET   | `/api/applications`                      | Filterable by status, role                  |
| Single application    | GET   | `/api/applications/:id`                  | 404 if not found                            |
| Create application    | POST  | `/api/applications`                      | Requires `applicantName`, `amount`, `state` |
| Transition status     | PATCH | `/api/applications/:id/status`           | Validates state machine                     |
| Decisions             | GET   | `/api/decisions/:appId`                  | Decisions for an application                |
| Record decision       | POST  | `/api/decisions`                         | Role + amount guard                         |
| Notification prefs    | GET   | `/api/notifications/preferences/:userId` | Auth required                               |
| Set notification pref | PUT   | `/api/notifications/preferences`         | Owner or delegated session                  |
| Audit log             | GET   | `/api/audit`                             | Append-only, no deletes                     |

## Error Handling

Errors use descriptive prefixes that the central error handler maps to HTTP status codes:

| Error Prefix     | HTTP Status |
| ---------------- | ----------- |
| `FORBIDDEN:`     | 403         |
| `VALIDATION:`    | 400         |
| `INVALID_STATE:` | 422         |
| `NOT_FOUND:`     | 404         |

## Auth Model

- Primary auth: `x-user-id` header (required on all requests except `/health`).
- Delegated sessions: `x-delegated-for` header allows acting on behalf of another user.
- Compliance reviewers have read-only access to notification preferences (can read, cannot write).
