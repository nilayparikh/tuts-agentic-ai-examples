# Loan Workbench — Domain Vocabulary

Canonical terminology for the Loan Workbench codebase. Use these exact terms
in code, comments, documentation, and AI conversations. Do not use synonyms.

## Lifecycle Terms

| Term               | Definition                                                          | Do NOT Use              |
| ------------------ | ------------------------------------------------------------------- | ----------------------- |
| Application State  | One of: `intake`, `review`, `underwriting`, `decision`, `finalized` | status, phase, stage    |
| State Transition   | A valid move from one application state to another                  | status change, update   |
| Finalized          | Terminal state — no further transitions allowed                     | completed, closed, done |
| Cooling-off Period | Mandatory 3-day wait between review → underwriting (CA only)        | delay, hold, pause      |

## Notification Terms

| Term                    | Definition                                                                    | Do NOT Use               |
| ----------------------- | ----------------------------------------------------------------------------- | ------------------------ |
| Mandatory Event         | A notification event that must fire for a state transition                    | required notification    |
| Notification Channel    | Delivery method: `email` or `sms`                                             | transport, medium        |
| Notification Event      | One of: `approval`, `decline`, `document-request`, `manual-review-escalation` | alert type, message type |
| Notification Preference | User's per-event, per-channel opt-in/opt-out setting                          | subscription, setting    |
| Event-Channel Validator | Rule module that checks preference updates against business rules             | preference validator     |
| Delivery Fallback       | SMS → email fallback when SMS provider is unhealthy                           | backup, retry            |

## Regulatory Terms

| Term                          | Definition                                                                       | Do NOT Use                          |
| ----------------------------- | -------------------------------------------------------------------------------- | ----------------------------------- |
| LEGAL-218                     | California decline notifications cannot disable SMS unless email remains enabled | CA SMS rule, California restriction |
| California Restricted Context | Validator defaults to CA-safe mode when no loan state is available               | California mode, CA flag            |
| Mandatory Event Channel       | At least one channel must stay enabled for mandatory events                      | required channel                    |

## Role Terms

| Term                | Definition                                                       | Do NOT Use           |
| ------------------- | ---------------------------------------------------------------- | -------------------- |
| Underwriter         | Primary loan reviewer — can read/write preferences               | reviewer, agent      |
| Analyst-Manager     | Senior reviewer — can read/write preferences, approve high-value | manager, admin       |
| Compliance-Reviewer | Regulatory auditor — read-only access to preferences             | auditor, inspector   |
| Delegated Session   | Acting on behalf of another user — read-only for preferences     | proxy, impersonation |

## Architecture Terms

| Term                   | Definition                                                           | Do NOT Use             |
| ---------------------- | -------------------------------------------------------------------- | ---------------------- |
| Three-Layer Separation | Route → Rule → Service pattern                                       | MVC, layers            |
| Pure Rule              | Business logic module with no I/O — located in `src/rules/`          | helper, utility        |
| Fail-Closed Audit      | Audit log must succeed before persistence — write fails if log fails | logging, tracking      |
| Queue Broker           | In-process event bus in `src/queue/`                                 | message queue, pub/sub |
