# Manual Review Escalation Workflow — Implementation Summary

## Overview
Implemented a complete manual review escalation workflow for the Loan Workbench platform. This allows underwriters and analysts to escalate loan applications for higher-level review when needed.

## Files Changed

### New Files Created

#### 1. `backend/src/models/escalation-repository.ts`
- **Purpose**: Database operations for escalations
- **Key Functions**:
  - `findEscalationById(id)` - Retrieve escalation by ID
  - `findEscalationsByApplication(applicationId)` - Get all escalations for a loan
  - `findEscalationsByStatus(status)` - Filter by status (pending/resolved/cancelled)
  - `findEscalationsByRecipient(userId)` - Get pending escalations for a user
  - `createEscalation(data)` - Create new escalation
  - `updateEscalationStatus(id, status)` - Update escalation status
- **Architecture**: Follows same pattern as loan-repository and other repositories

#### 2. `backend/src/services/escalation-service.ts`
- **Purpose**: High-level API for escalation business logic
- **Key Functions**:
  - `escalateReview(session, applicationId, escalatedToUserId, reason)` - Create escalation with validation
    - Validates: delegated sessions rejected, application exists and in valid state (underwriting/decision), recipient exists, reason not empty
    - Emits: audit event, notification event, escalation event
  - `resolveEscalation(session, escalationId)` - Close/resolve escalation
    - Validates: escalation exists, only recipient can resolve, status is pending
    - Emits: audit event
  - `getEscalationsForApplication(applicationId)` - Retrieve escalations for a loan
  - `getPendingEscalationsForUser(userId)` - Get pending escalations assigned to user
- **Architecture**: Delegates to repository for persistence, broker for event emission

#### 3. `backend/src/routes/escalation.ts`
- **Purpose**: Express route handlers for escalation endpoints
- **Endpoints**:
  - `GET /api/escalations/application/:applicationId` - Get escalations for application
  - `GET /api/escalations/pending` - Get pending escalations for current user
  - `POST /api/escalations` - Create new escalation
    - Request body: `{ applicationId, escalatedToUserId, reason }`
  - `PATCH /api/escalations/:id/resolve` - Resolve escalation
- **Authorization**: Role-based access control via `requireRole` middleware
  - Create: underwriter, analyst-manager only
  - Read/Resolve: all roles

#### 4. `backend/src/queue/handlers/escalation-handler.ts`
- **Purpose**: Processes escalation.requested events from message queue
- **Function**: Logs escalation events for tracking
- **Extensibility**: Prepared for future workflows (metrics, external systems)

### Modified Files

#### 1. `backend/src/models/types.ts`
- **Change**: Added `Escalation` interface
  ```typescript
  export interface Escalation {
    id: string;
    applicationId: string;
    escalatedBy: string;
    escalatedTo: string;
    reason: string;
    status: "pending" | "resolved" | "cancelled";
    createdAt: string;
    updatedAt: string;
  }
  ```

#### 2. `backend/src/queue/contracts.ts`
- **Change**: Added `EscalationRequestedEvent` interface and updated `BrokerEvent` union type
  ```typescript
  export interface EscalationRequestedEvent extends BaseEvent {
    type: "escalation.requested";
    payload: {
      escalationId: string;
      applicationId: string;
      escalatedBy: string;
      escalatedTo: string;
      reason: string;
    };
  }
  ```
- **Impact**: Event broker now handles escalation events

#### 3. `backend/src/db/schema.sql`
- **Change**: Added `escalations` table with structure:
  ```sql
  CREATE TABLE IF NOT EXISTS escalations (
      id              TEXT PRIMARY KEY,
      application_id  TEXT NOT NULL REFERENCES loan_applications(id),
      escalated_by    TEXT NOT NULL REFERENCES users(id),
      escalated_to    TEXT NOT NULL REFERENCES users(id),
      reason          TEXT NOT NULL,
      status          TEXT NOT NULL DEFAULT 'pending'
                      CHECK (status IN ('pending', 'resolved', 'cancelled')),
      created_at      TEXT NOT NULL DEFAULT (datetime('now')),
      updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
  );
  ```
- **Indexes**: Three indexes for efficient querying:
  - `idx_escalations_application` - Find escalations by application
  - `idx_escalations_status` - Filter by status
  - `idx_escalations_recipient` - Find pending escalations for a user

#### 4. `backend/src/db/seed.ts`
- **Change**: Added `insertEscalation` prepared statement and seed data
- **Seed Data**: Two example escalations:
  - esc-1: app-1 escalated from u-1 (underwriter) to u-2 (analyst-manager)
  - esc-2: app-3 escalated from u-2 (analyst-manager) to u-3 (compliance-reviewer)

#### 5. `backend/src/app.ts`
- **Changes**:
  - Import `escalationRoutes` from routes/escalation
  - Import `registerEscalationHandler` from queue/handlers/escalation-handler
  - Register escalation handler in queue initialization
  - Mount escalation routes at `/api/escalations`

#### 6. `backend/src/rules/role-permissions.ts`
- **Changes**: Added escalation permissions and assigned to roles
  - New permissions: `escalation:create`, `escalation:read`, `escalation:resolve`
  - Underwriters: all escalation permissions
  - Analyst-managers: all escalation permissions
  - Compliance-reviewers: read + resolve (no create)

## Architecture Decisions

### 1. State Constraints
- Escalations can only be created for applications in "underwriting" or "decision" states
- Prevents escalating applications that haven't reached the appropriate review stage

### 2. Recipient Authorization
- Only the escalation recipient can resolve it
- Enforced at service layer to maintain separation of concerns

### 3. Event-Driven Design
- Leverages existing message broker pattern consistent with other workflows:
  - **Audit events** for compliance trail
  - **Notification events** for user alerts
  - **Escalation events** for extensibility (metrics, integrations, etc.)

### 4. Permission Model
- Granular permissions following existing pattern
- Underwriters and analysts can CREATE escalations
- All roles can READ and RESOLVE escalations
- Recipient-based authorization ensures proper workflow

### 5. Database Design
- Escalations table uses text status with CHECK constraint (matches application state pattern)
- Foreign keys reference users and loan_applications
- Indexes optimize common queries

## API Endpoints

### Create Escalation
```
POST /api/escalations
Authorization: underwriter, analyst-manager
Body: {
  applicationId: string,
  escalatedToUserId: string,
  reason: string
}
Returns: Escalation object
```

### Get Escalations for Application
```
GET /api/escalations/application/:applicationId
Authorization: underwriter, analyst-manager, compliance-reviewer
Returns: Escalation[]
```

### Get Pending Escalations for User
```
GET /api/escalations/pending
Authorization: underwriter, analyst-manager, compliance-reviewer
Returns: Escalation[] (filtered by status='pending' and escalated_to=user)
```

### Resolve Escalation
```
PATCH /api/escalations/:id/resolve
Authorization: underwriter, analyst-manager, compliance-reviewer
Returns: Updated Escalation object with status='resolved'
```

## Validation Rules

### Create Escalation
- ✓ Application must exist
- ✓ Application must be in "underwriting" or "decision" state
- ✓ Escalated-to user must exist
- ✓ Reason must not be empty
- ✓ Delegated sessions cannot create escalations

### Resolve Escalation
- ✓ Escalation must exist
- ✓ Escalation must be in "pending" status
- ✓ Only the recipient can resolve it

## Audit & Compliance

- **Escalation created** - Audited with full context (who escalated, to whom, reason)
- **Escalation resolved** - Audited with resolution details
- **Notifications** - Escalation recipients are notified via email/SMS based on preferences
- **Event logging** - All escalations logged for metrics and extensibility

## Testing Scenarios

The seed data provides realistic test cases:
1. **Underwriter to Analyst-Manager escalation** (esc-1): Handles unusual loan structure
2. **Analyst-Manager to Compliance escalation** (esc-2): High-value loan sign-off

Both escalations are in "pending" status, ready for resolution workflow testing.

## Integration with Existing Systems

### Message Broker
- Uses existing `broker.emit()` pattern for events
- Compatible with existing notification and audit handlers
- Extensible for future event consumers

### Role-Based Access Control
- Integrated with existing `requireRole` middleware
- Respects existing role definitions
- Follows permission matrix pattern

### Database
- Uses same connection pattern as other repositories
- Leverages prepared statements for security
- Follows transaction pattern from seed script

## Summary

This implementation provides a complete, production-ready escalation workflow that:
- Follows all existing repository patterns and conventions
- Integrates seamlessly with the event-driven architecture
- Enforces proper authorization and validation
- Maintains audit trail for compliance
- Enables notifications to escalation recipients
- Is extensible for future enhancements
