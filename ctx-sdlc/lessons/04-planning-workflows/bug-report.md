# Bug Report: Delegated Session + California SMS Toggle

## Title

Manual-review escalation SMS toggle appears enabled for California loans in
delegated sessions; save succeeds visually but reverts on refresh.

## Reported Behavior

An analyst manager opened notification settings while acting on behalf of an
underwriter (`x-delegated-for: u-1`) for a California loan (`app-100`). They
observed:

1. The SMS toggle for decline notifications was **enabled and editable** even
   though California loans restrict decline SMS (LEGAL-218).
2. They were able to click the SMS toggle and press Save.
3. A success toast appeared.
4. On page refresh, the value had reverted to the previous state.

## Expected Behavior

- **Delegated sessions should be read-only** for another user's preferences (SC-2).
- **California loan restrictions** should disable the decline SMS toggle and show
  an explanation (FR-4).
- A save **should not appear successful** if the backend rejects it (ADR-003
  optimistic-update rollback).

## Environment

- Web app build: `2026.03.1-rc2`
- Reported by: Pilot cohort underwriter ops team
- Frequency: 3 of 8 attempts in staging

## Why This Is Nuanced

This bug report is deliberately designed to demonstrate overlapping constraints.
The visible symptom looks like a simple UI toggle issue, but the actual problem
touches **four** independent rules:

| Layer         | Rule                                                      | Source           |
| ------------- | --------------------------------------------------------- | ---------------- |
| Authorization | Delegated sessions are read-only                          | SC-2             |
| Business rule | CA decline SMS is restricted                              | FR-4 / LEGAL-218 |
| UI pattern    | Optimistic update must support rollback                   | ADR-003          |
| Audit         | If audit write failed, the save should have been rejected | NFR-2            |

### Possible Root Causes (ranked by likelihood)

1. **Delegated-session write guard** is not applied to the preference save route.
   The `blockDelegatedWrites` middleware may be missing from the PUT handler.
2. **State restriction check** is not being called during save because `loanState`
   is not passed in the request body.
3. **Optimistic store update** fires on HTTP 200 without checking the response body
   for partial rejections (207 status).
4. **Audit service outage** may have caused the save to fail closed, but the error
   was swallowed by the frontend error boundary.

### Investigation Inputs

- Compare UI behavior against `specs/product-spec-notification-preferences.md` sections SC-2 and FR-4.
- Check `src/routes/notifications.ts` for the `blockDelegatedWrites` middleware attachment.
- Check whether the preference save sends `loanState` to the API.
- Verify that the audit service was healthy at the time of the report.
- Check `src/middleware/auth.ts` for delegated-session detection logic.
