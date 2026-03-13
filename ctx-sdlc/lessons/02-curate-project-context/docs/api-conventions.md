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
| Set notification pref | PUT   | `/api/notifications/preferences`         | Owner-only write, delegated sessions blocked |
| Audit log             | GET   | `/api/audit`                             | Append-only, no deletes                     |

## Lesson 02 Example Conventions

For the lesson 02 preference-management example, the existing write endpoints should be aligned around one consistent authorization model:

| Resource                    | Verb | Path                                     | Notes |
| --------------------------- | ---- | ---------------------------------------- | ----- |
| Single preference write     | PUT  | `/api/notifications/preferences`               | Preserve owner-only writes and central error handling |
| Email preference bulk write | PUT  | `/api/notifications/preferences/:userId/email` | Updates all standard email-event preferences for one user |
| SMS preference bulk write   | PUT  | `/api/notifications/preferences/:userId/sms`   | Updates all standard sms-event preferences for one user |

Required constraints for those lesson routes:

- user in path must match the authenticated actor
- delegated sessions cannot write
- compliance reviewers remain read-only
- authorization failures should throw `FORBIDDEN:` errors for the central error handler
- each changed preference must emit audit behavior
- do not introduce new queue contracts or new domain types
- keep the change local to `src/backend/src/routes/notifications.ts` unless a read-only import already exists elsewhere

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
- Owner-only writes still apply even if a route includes `:userId` in the path.
