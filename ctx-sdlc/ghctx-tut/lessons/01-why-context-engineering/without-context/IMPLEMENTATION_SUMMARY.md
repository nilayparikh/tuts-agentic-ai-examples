# Manual Review Escalation Workflow Implementation

## Summary
Implemented a complete manual review escalation workflow for the Loan Workbench platform. This allows underwriters and analysts to escalate loan applications for higher-level review when needed.

## Files Changed

### 1. New Files Created

#### `backend/src/models/escalation-repository.ts`
- Database operations for escalations
- Functions: `findEscalationById`, `findEscalationsByApplication`, `findEscalationsByStatus`, `findEscalationsByRecipient`, `createEscalation`, `updateEscalationStatus`
- Follows same pattern as loan-repository and decision repository

#### `backend/src/services/escalation-service.ts`
- High-level API for escalation business logic
- Functions:
  - `escalateReview()` - Create escalation with validation
  - `resolveEscalation()` - Close/resolve escalation
  - `getEscalationsForApplication()` - Retrieve escalations for a loan
  - `getPendingEscalationsForUser()` - Get pending escalations assigned to user
- Validates application state, recipient, and reason
- Emits audit, notification, and escalation events via message broker
- Enforces that only escalation recipient can resolve it

#### `backend/src/routes/escalation.ts`
- Express route handlers for escalation endpoints:
  - `GET /api/escalations/application/:applicationId` - Get escalations for application
  - `GET /api/escalations/pending` - Get pending escalations for current user
  - `POST /api/escalations` - Create new escalation
  - `PATCH /api/escalations/:id/resolve` - Resolve escalation
- Role-based access control via `requireRole` middleware

#### `backend/src/queue/handlers/escalation-handler.ts`
- Processes `escalation.requested` events from message queue
- Logs escalation events for tracking
- Extensible for future workflows (metrics, external systems, etc.)

### 2. Modified Files

#### `backend/src/models/types.ts`
- Added `Escalation` interface:
  ```typescript
  interface Escalation {
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

#### `backend/src/queue/contracts.ts`
- Added `EscalationRequestedEvent` interface for message broker contract
- Updated `BrokerEvent` union type to include `EscalationRequestedEvent`
- Payload includes: escalationId, applicationId, escalatedBy, escalatedTo, reason

#### `backend/src/db/schema.sql`
- Added `escalations` table with columns:
  - id (TEXT PRIMARY KEY)
  - application_id (FOREIGN KEY to loan_applications)
  - escalated_by (FOREIGN KEY to users)
  - escalated_to (FOREIGN KEY to users)
  - reason (TEXT NOT NULL)
  - status (TEXT with CHECK for 'pending', 'resolved', 'cancelled')
  - created_at, updated_at (timestamps)
- Added three indexes for efficient querying:
  - idx_escalations_application
  - idx_escalations_status
  - idx_escalations_recipient

#### `backend/src/db/seed.ts`
- Added `insertEscalation` prepared statement
- Added seed data with two example escalations:
  - esc-1: app-1 escalated from u-1 to u-2 (underwriter to manager)
  - esc-2: app-3 escalated from u-2 to u-3 (manager to compliance-reviewer)

#### `backend/src/app.ts`
- Imported `escalationRoutes` from routes/escalation.js
- Imported `registerEscalationHandler` from queue/handlers/escalation-handler.js
- Registered escalation handler in queue initialization
- Mounted escalation routes at `/api/escalations`

#### `backend/src/rules/role-permissions.ts`
- Added permission types: `escalation:create`, `escalation:read`, `escalation:resolve`
- Assigned permissions to roles:
  - Underwriters: all escalation permissions + existing permissions
  - Analyst-managers: all escalation permissions + existing permissions
  - Compliance-reviewers: read + resolve (no create) + existing permissions

## Architecture Decisions

1. **State Transitions**: Escalations can only be created for applications in "underwriting" or "decision" states, preventing premature escalations

2. **Permission Model**: 
   - Underwriters and analysts can CREATE escalations
   - All roles can READ escalations
   - All roles can RESOLVE escalations (recipient authorization enforced in service)

3. **Event-Driven**: Uses message broker for consistency with existing patterns:
   - Audit events for trail
   - Notification events for user alerts
   - Escalation events for extensibility

4. **Recipient Authorization**: Only the escalation recipient can resolve it, enforced at service layer

5. **Mandatory Escalation Event**: Already defined in mandatory-events.ts for "underwriting→decision" transition, now fully integrated

## API Endpoints

### Create Escalation
```
POST /api/escalations
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
Returns: Escalation[] 
```

### Get Pending Escalations for User
```
GET /api/escalations/pending
Returns: Escalation[] (filtered by status='pending' and escalated_to=user)
```

### Resolve Escalation
```
PATCH /api/escalations/:id/resolve
Returns: Updated Escalation object with status='resolved'
```

## Testing Scenarios

The seed data includes:
- Two sample users escalating to higher-level roles
- Applications in different states (underwriting, decision)
- Demonstrating escalation workflow with realistic use cases

## Compliance Notes

- All escalations are audited via AuditRequestedEvent
- Notifications are sent to escalation recipients
- Only authorized roles can create escalations
- Only escalation recipients can resolve them
- Status transitions are validated (pending → resolved/cancelled only)
