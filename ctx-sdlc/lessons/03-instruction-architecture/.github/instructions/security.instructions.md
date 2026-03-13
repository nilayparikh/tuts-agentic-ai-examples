---
applyTo: "src/backend/src/middleware/**"
---

# Security Instructions

Rules for authentication, authorization, and security middleware.

## Authentication

- All requests (except `/health`) must carry an `x-user-id` header.
- Users are resolved from the SQLite database — unknown IDs return 401.
- Never log or expose user credentials, phone numbers, or session tokens in responses.

## Delegated Sessions

- A delegated session is created when `x-delegated-for` is present.
- Only `analyst-manager` role can operate in delegated mode — other roles get 403.
- Delegated sessions allow reads but **block all writes** — enforce via `blockDelegatedWrites` middleware.
- Audit entries for delegated sessions must record both the actor and the delegated-for user.

## Role-Based Access

- Use `requireRole()` middleware — never check roles inline in route handlers.
- `compliance-reviewer` is read-only for ALL notification/preference operations.
- Role checks happen after authentication, before any business logic.

## Error Responses

- 401 for missing or invalid authentication.
- 403 for insufficient role or delegated-session write attempt.
- Never reveal internal role names or permission details in 401/403 error messages to unauthenticated callers.
- Use 404 (not 403) for feature-flagged endpoints to avoid leaking feature existence.

## Sensitive Data

- Phone numbers are sensitive operational data (NFR-3).
- Do not include phone numbers in debug logs, analytics events, or error responses.
- Mask sensitive fields before any logging call.
