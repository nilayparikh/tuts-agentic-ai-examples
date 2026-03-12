# Non-Functional Requirements — Implementation Workflows

These NFRs apply during implementation. Each includes the **AI mistake without
context** annotation showing what goes wrong when the AI doesn't have this NFR.

---

## NFR-1: Audit Trail Integrity (Fail-Closed)

**Requirement**: Every mutation that changes user data must write an audit entry
BEFORE persisting the change. If the audit write fails, the mutation MUST fail
with a 503 error. No silent fallback.

**AI mistake without context**: AI implements try-catch around the audit write
and proceeds with the mutation anyway. "Best-effort logging" sounds reasonable
but violates a compliance requirement.

> **HARD NEGATIVE**: The AI generates code that catches audit failures and logs
> a warning instead of aborting. This passes basic tests but fails compliance.

**Test signal**: Any test that mocks audit failure should assert the mutation
did NOT persist AND the response is 503.

---

## NFR-2: Degraded Mode for Non-Critical Services

**Requirement**: Notification delivery failures must fall back to email when SMS
is unavailable. The fallback must NOT modify stored user preferences.

**AI mistake without context**: AI implements the fallback but also updates the
user's stored channel preference from SMS to email "for consistency."

> **FALSE POSITIVE**: AI flags the inconsistency between stored preference (SMS)
> and actual delivery (email) as a bug. It's intentional — delivery degrades
> but preferences don't change.

**Test signal**: After a degraded delivery, GET /preferences should still show
the original SMS preference.

---

## NFR-3: Request Latency Budget

**Requirement**: Preference save operations must complete in <200ms under normal
conditions. Sequential I/O should be minimized.

**AI mistake without context**: AI adds synchronous delivery confirmation after
every preference save, doubling latency. Delivery is async by design.

> **FALSE POSITIVE**: AI suggests adding `await deliverNotification()` to the
> save handler for "consistency." Delivery is fire-and-forget by design.

---

## NFR-4: Role-Scoped Data Access

**Requirement**: Underwriters can only see their own audit entries. Analyst-managers
see entries for their team. Compliance reviewers see all entries.

**AI mistake without context**: AI implements a single `/audit` endpoint that
returns all entries regardless of role, adding a client-side filter. Server-side
scoping is the requirement.

> **HARD NEGATIVE**: The AI returns all audit data and filters in the response
> mapper. This "works" for underwriters viewing their own data but leaks
> everyone else's data in the response payload.

---

## NFR-5: Feature Flag Behavior (404 Not 403)

**Requirement**: Non-pilot users hitting gated endpoints must receive 404 (Not
Found), not 403 (Forbidden). This prevents information leakage about unreleased
features.

**AI mistake without context**: AI uses 403 because "the user isn't authorized
for this feature." The distinction matters — 403 confirms the endpoint exists.

> **HARD NEGATIVE**: AI returns 403 for non-pilot users. Security scanners and
> curious users now know the feature endpoint exists and is gated.

---

## NFR-6: Schema Backward Compatibility

**Requirement**: API schema changes must be additive. Existing clients must not
break when new fields are added. Removed fields must be deprecated with a
minimum two-release notice.

**AI mistake without context**: AI renames a response field from `channels` to
`notificationChannels` for "clarity." All existing clients break.

> **HARD NEGATIVE**: The AI improves naming but breaks every consumer. Additive
> changes (adding `notificationChannels` alongside `channels`) are safe.

---

## NFR-7: Structured Logging and Observability

**Requirement**: All log entries must be structured JSON with `correlationId`,
`userId`, `action`, and `timestamp`. No `console.log()` with string concatenation.

**AI mistake without context**: AI uses `console.log(\`User ${userId} saved preferences\`)`
which is unstructured and not machine-parseable.

> **FALSE POSITIVE**: AI flags existing structured logging as "verbose" and
> simplifies to `console.log()`. The structured format is a requirement.
