# Loan Workbench Data Model

## Domain Entities

### Application

A loan application submitted for review.

| Field | Type | Description |
| --- | --- | --- |
| id | string (UUID) | Unique identifier |
| applicant | string | Applicant name |
| amount | number | Loan amount requested |
| status | string | Current state (draft, submitted, under_review, approved, rejected) |
| createdAt | string (ISO 8601) | Creation timestamp |
| updatedAt | string (ISO 8601) | Last update timestamp |

### Decision

An approval or rejection decision on an application.

| Field | Type | Description |
| --- | --- | --- |
| id | string (UUID) | Unique identifier |
| applicationId | string (UUID) | Related application |
| decision | string | approved or rejected |
| reason | string | Decision rationale |
| decidedBy | string | Role or user who decided |
| createdAt | string (ISO 8601) | Decision timestamp |

### Notification

A notification dispatched through the async queue.

| Field | Type | Description |
| --- | --- | --- |
| id | string (UUID) | Unique identifier |
| applicationId | string (UUID) | Related application |
| type | string | Notification type |
| status | string | pending, sent, failed |
| createdAt | string (ISO 8601) | Creation timestamp |

### AuditEntry

An immutable audit trail record.

| Field | Type | Description |
| --- | --- | --- |
| id | string (UUID) | Unique identifier |
| entityId | string (UUID) | Related entity |
| action | string | Action performed |
| actor | string | Who performed the action |
| details | object | Action-specific data |
| createdAt | string (ISO 8601) | Timestamp |

## Storage

All entities are stored in SQLite via `better-sqlite3`.
Database schema and migrations are managed in `src/backend/src/db/`.
