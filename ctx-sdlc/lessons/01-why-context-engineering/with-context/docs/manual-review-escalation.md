# Manual Review Escalation — Hidden Workflow Spec

This file is the source of truth for Lesson 01's comparison task.

The task prompt intentionally does **not** include the requirements below.
A model only sees them when repository context is available.

## Goal

Implement the repository's **manual review escalation workflow** for an existing
loan application.

## Required Behavior

1. Add a new endpoint: `POST /api/applications/:id/manual-review`
2. Put the route in `app/backend/src/routes/applications.ts`
3. Put orchestration logic in `app/backend/src/services/loan-service.ts`
4. Do **not** place business logic directly in the route handler
5. Only users with role `analyst-manager` may trigger this workflow
6. Delegated sessions must be rejected for this mutating operation
7. The workflow does **not** change the loan's lifecycle status
8. The workflow must emit the existing `notification.requested` broker event
9. The notification event must use `event: "manual-review-escalation"`
10. Do **not** add or modify queue contract types for this task
11. Audit the operation using the repo's existing audit pattern
12. Use action name `loan.manual-review-requested`
13. The response payload should be:

```json
{
  "ok": true,
  "applicationId": "app-123",
  "notificationEventId": "uuid"
}
```

## California High-Risk Rule

If all of the following are true:

- `featureFlags.californiaRules === true`
- `loan.loanState === "CA"`
- `loan.amount >= 1000000`

Then prefix the notification subject with:

```text
[CA-HighRisk]
```

## Non-Goals

The implementation must **not**:

- delete loan applications
- transition the loan to another lifecycle state
- create a brand-new queue event contract
- bypass the service layer
- ignore delegated-session restrictions

## Why This Works As A Demo

A model without repo context often produces one or more of these errors:

- invents a new route path or file location
- puts orchestration directly in the route
- allows the wrong role
- changes `status` when no transition is required
- invents a new event type instead of reusing `notification.requested`
- misses the California subject-prefix rule
