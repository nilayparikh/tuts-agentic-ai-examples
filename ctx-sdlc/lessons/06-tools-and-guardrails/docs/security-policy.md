# Security Policy — Loan Workbench

This document defines the security controls enforced by hooks and instructions.
It is the source of truth for what is allowed and what is blocked.

## Protected Files

The following files are protected by the file-protection hook and cannot be
edited by AI assistance:

| File                                      | Reason                                                                  | Change Process                                         |
| ----------------------------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------ |
| `.env` / `.env.*`                         | Contains database paths, API keys, feature flag overrides               | Manual edit by an authorized engineer. Reviewed in PR. |
| `app/backend/src/config/feature-flags.ts` | Controls pilot gating. Incorrect changes expose unreleased features.    | Product owner approval + manual edit.                  |
| `app/backend/src/db/schema.sql`           | Database DDL. Modifications can break migrations and the test baseline. | Coordinated change with migration update.              |
| `app/backend/src/db/seed.ts`              | Contains seeded test data. Modifications can break the test baseline.   | Coordinated change with test update.                   |

### Why AI Cannot Edit These Files

These files are not dangerous because of what they contain syntactically — they
are dangerous because of the **decisions** they encode. Feature flags determine
who sees unreleased features. Environment variables contain secrets. Test data
establishes the baseline that all tests rely on.

An AI assistant might "helpfully" add a feature flag for a feature it's building,
or seed test data that makes its tests pass but breaks others, or modify the
database schema without a migration. The file-protection hook prevents this.

## Audit Requirements

### Fail-Closed Semantics

All data mutations must write an audit entry BEFORE persisting the change.
If the audit service is unavailable, the mutation MUST fail with HTTP 503.

This is enforced by:

1. **Code design**: Audit events are emitted via the queue broker (or direct DB
   write) before persisting in every route handler.
2. **Tests**: Edge-case tests verify that audit failure blocks persistence.
3. **Hooks**: Pre-commit validation ensures tests pass before code is committed.

### What Gets Audited

| Action                       | Audit Fields                               | Retention |
| ---------------------------- | ------------------------------------------ | --------- |
| Preference save              | userId, changes, timestamp, sessionType    | 90 days   |
| Application state transition | applicationId, fromState, toState, userId  | Permanent |
| Decision recording           | applicationId, decision, userId, timestamp | Permanent |
| Failed mutation              | userId, action, reason, timestamp          | 30 days   |

## Session Security

### Delegated Sessions

A delegated session is when user A acts on behalf of user B. The `x-delegated-for`
header indicates delegation.

**Rule**: Delegated sessions are read-only for sensitive operations. The
`blockDelegatedWrites` middleware enforces this on:

- `PUT /notifications/preferences`
- `POST /decisions`
- `PATCH /applications/:id/status`

### Why This Matters for AI

An AI assistant might not distinguish between "I'm helping user A" and "user A
is acting as user B." Without the delegated session context, the AI would
happily mutate data on behalf of a delegated principal — which violates the
security model.

## Error Response Safety

Error responses must not leak:

- Stack traces
- Internal file paths
- Database connection strings
- User IDs of other users
- Feature flag names or values

The central error handler in `app/backend/src/middleware/error-handler.ts` enforces this.
For 4xx errors, a brief message is returned. For 5xx errors, only a generic
"Internal server error" with a correlation ID is returned.

## Incident Response

If a security control is bypassed:

1. Check the audit log for the affected time period.
2. Verify hook configurations have not been modified.
3. Review MCP server access logs (if write-capable servers are configured).
4. Document the incident and update this policy if needed.
