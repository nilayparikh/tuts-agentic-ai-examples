# Non-Functional Requirements

These NFRs constrain the notification preferences feature. Each requirement
is annotated with the kind of mistake an AI assistant is likely to make
when the NFR is missing from context.

---

## NFR-1: Performance

- Settings page initial load must add ≤ 150 ms p95 over the existing settings
  route baseline.
- Preference save API must complete within 400 ms p95 under normal load.

> **AI mistake without context:** An assistant might generate a preference save
> that does multiple sequential DB writes and a synchronous email-validation
> round-trip, exceeding the latency budget.

---

## NFR-2: Availability and Resilience

- Preference reads must tolerate notification-provider degradation (the provider
  is not the source of truth for preferences).
- **If audit logging is unavailable, writes must FAIL CLOSED** rather than
  silently saving preferences without an audit trail.

> **HARD NEGATIVE:** Most services treat logging as fire-and-forget. An AI
> will generate `try { auditLog(...) } catch { /* ignore */ }` unless the NFR
> explicitly overrides that pattern. The correct behavior is to abort the
> enclosing save operation.

> **FALSE POSITIVE:** Preference reads succeeding during an audit-service
> outage is NOT a bug — only writes require audit availability.

---

## NFR-3: Security and Privacy

- Only authenticated internal users can access the preferences endpoint.
- SMS destination values (phone numbers) are **sensitive operational data** and
  must not appear in client logs or analytics events.
- Delegated sessions must be explicitly identified in audit logs.

> **AI mistake without context:** An assistant might log the full preference
> object (including phone number metadata) in a debug statement.

---

## NFR-4: Accessibility

- Preference controls must be keyboard-reachable and screen-reader labeled.
- Disabled mandatory-event controls must have **persistent explanatory text**,
  not just a tooltip that disappears.
- Status messages for save success and failure must be announced via ARIA live
  regions.

> **AI mistake without context:** An assistant will generate a disabled toggle
> with a title attribute (tooltip) instead of visible helper text.

---

## NFR-5: Observability

Emit metrics for:

| Metric                      | Type      | Purpose                                       |
| --------------------------- | --------- | --------------------------------------------- |
| `preference.read.failure`   | Counter   | Store read errors                             |
| `preference.save.failure`   | Counter   | Distinguishes validation from provider errors |
| `audit.write.failure`       | Counter   | Tracks fail-closed rejections                 |
| `notification.sms.fallback` | Counter   | SMS→email fallback invocations                |
| `preference.save.latency`   | Histogram | p50/p95/p99 save duration                     |

Logs must distinguish **validation failures** (4xx, user error) from
**downstream provider failures** (5xx, infrastructure) so alerting routes
correctly.

> **AI mistake without context:** An assistant might use a single generic
> error counter, making it impossible to filter signal from noise in dashboards.

---

## NFR-6: Change Safety

- Feature must ship behind a **release flag** for the initial pilot cohort.
- Non-pilot users must see no change — feature-flagged endpoints should return
  404 (not 403) to avoid leaking feature existence.
- Existing users without saved preferences must receive role-based defaults
  without requiring a data backfill before first load.

> **HARD NEGATIVE:** An assistant generating the feature-flag guard might use
> 403 Forbidden, which tells non-pilot users the feature exists but they lack
> access. The spec requires 404 to completely hide the feature.

> **FALSE POSITIVE:** A pilot user getting role-based defaults on first access
> (even though no migration ran) is correct behavior, not a data-integrity bug.

---

## NFR-7: Compliance

- Audit records for preference changes must be **retained for 24 months**.
- Mandatory escalation delivery rules must be testable and documented in the
  release checklist.
- The compliance reviewer's read-only view must show the effective preference
  state including applied defaults.

> **AI mistake without context:** An assistant might apply a TTL or cleanup
> job to audit records without checking the retention policy.
