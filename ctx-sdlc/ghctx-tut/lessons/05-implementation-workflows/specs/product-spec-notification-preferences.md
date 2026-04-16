# Product Specification: Notification Preferences

## Document Status

| Field    | Value                             |
| -------- | --------------------------------- |
| Owner    | Lending Platform Product          |
| Status   | Draft for implementation planning |
| Target   | 2026 Q2 pilot                     |
| Tracking | PROJ-412                          |

## Problem Statement

Underwriters and analyst managers need finer control over operational
notifications. The current Loan Workbench sends a fixed set of email alerts
with no user-level preferences. Teams report alert fatigue for routine document
requests and missed high-severity escalation events when all notifications are
treated the same.

## Goal

Allow authorized users to configure notification preferences by channel and
event type without breaking auditability, workflow SLAs, or regulatory
communications that must always be delivered.

---

## In Scope

- Settings UI for notification preferences in `apps/web/`
- API support in `services/api/` for reading and updating preferences
- Persistence across sessions and devices
- Role-aware defaults for underwriters and analyst managers
- Event-specific preferences for: approval, decline, document-request,
  manual-review-escalation

## Out of Scope

- SMS provider migration
- Push notifications
- Per-loan notification overrides
- Customer-facing borrower communications

---

## User Roles

### Underwriter

- Can edit their own notification preferences
- **Cannot suppress mandatory manual-review-escalation notifications**

### Analyst Manager

- Can edit their own notification preferences
- Receives additional portfolio-level digest notifications (later release)
- Can operate in **delegated mode** on behalf of another user

### Compliance Reviewer

- **Read-only** access to effective preference configuration for audit review
- Cannot change operational preferences from the UI

---

## Functional Requirements

### FR-1: Preference Matrix

Users can configure email and SMS independently for these event types:

| Event                    | Email        | SMS            |
| ------------------------ | ------------ | -------------- |
| Approval decision issued | configurable | configurable   |
| Decline decision issued  | configurable | configurable\* |
| Document request created | configurable | configurable   |
| Manual-review escalation | configurable | configurable   |

\*Subject to state-specific restrictions — see FR-4.

### FR-2: Mandatory Event Rules

Manual-review escalation is a **mandatory notification**. Users may change the
secondary channel, but **at least one channel must remain enabled**.

> **HARD NEGATIVE pattern:** Without this rule, an AI generating the preference
> update handler will produce code that allows disabling all channels. The UI
> and API must both enforce this constraint.

> **FALSE POSITIVE pattern:** A user disabling SMS for escalation while email
> remains enabled is NOT a violation. The constraint is about having zero
> channels, not about which specific channel is active.

### FR-3: Role-Based Defaults

| Role                | Email default                            | SMS default     |
| ------------------- | ---------------------------------------- | --------------- |
| Underwriter         | All events enabled                       | Escalation only |
| Analyst Manager     | All events enabled                       | Escalation only |
| Compliance Reviewer | No operational defaults (read-only role) | N/A             |

New users without saved preferences must receive these defaults on first access
**without requiring a data backfill migration**.

### FR-4: Temporary SMS Restriction — California

SMS for decline decisions must remain **disabled for California loans** until
the legal review tracked in `LEGAL-218` is complete.

- The UI must explain why the option is unavailable when the active loan context
  is California.
- The restriction is based on loan jurisdiction (`loanState`), not borrower
  address, when the two differ.
- From a **multi-state portfolio view**, state-specific restrictions should be
  shown as conditional rules rather than blanket-disabling all SMS controls.

> **HARD NEGATIVE pattern:** Enabling decline SMS on a CA loan looks like normal
> toggle behavior in code. The restriction is invisible without this spec.

### FR-5: Degraded Delivery Fallback

If the SMS provider is unavailable:

1. Delivery falls back to email when email is enabled for that event.
2. **Stored preferences must NOT be modified by the fallback.**
3. Fallback invocations must be logged with a separate metric.

> **FALSE POSITIVE pattern:** A user receiving an email instead of SMS during
> an outage is NOT a preference bug. Support agents must check delivery logs,
> not the preference store, to diagnose delivery complaints.

### FR-6: Auditability

Every preference change must record:

- Actor identity
- Timestamp
- Previous value
- New value
- Source channel
- Delegated-for user (if applicable)

---

## Special Conditions

### SC-1: Locked (Finalized) Applications

When a loan application is in `finalized` state, users can still update their
preferences globally, but the settings screen must clarify that changes **do not
affect notifications already queued** for that application.

### SC-2: Delegated Sessions

If an analyst manager is operating in delegated mode:

- They may **view** the delegate's notification preferences.
- They may **not modify** the delegate's preferences.
- The UI must visually indicate delegated-session mode.
- Audit entries must record both the actor and the delegated-for user.

> **HARD NEGATIVE pattern:** A delegated save that shows a "success" toast but
> reverts on refresh indicates the UI is optimistically updating local state
> without checking the server rejection. This is a real bug already reported.

### SC-3: Mixed Portfolio Context

When the settings screen is opened from a portfolio view containing loans
across multiple states, state-specific restrictions should be explained as
conditional rules rather than blanket-disabling controls.

---

## UX Notes

- Show channel controls in a matrix grid by event type.
- Mandatory events should be **visually marked** and explained inline.
- Disabled controls must include persistent helper text, not just tooltips.
- Saving should be optimistic **only if rollback is supported by the store**.

## Success Metrics

- 30% reduction in document-request alert-mute requests within 60 days
- < 1% failed preference saves during pilot
- Zero Sev2 incidents caused by suppressed mandatory escalation alerts

## Open Questions

1. Should compliance reviewers access audit history from the same settings page
   or a separate audit viewer?
2. Is the California decline SMS restriction loan-state based or borrower-state
   based when they differ? **Answer: loan-state** (per legal review 2026-02).
3. Should portfolio-view restrictions show a summary banner or per-row indicators?
