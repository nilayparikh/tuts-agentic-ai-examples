# Notification Preferences Implementation Plan

## Document Summary

This plan outlines the implementation of per-user notification preferences for the Loan Workbench. The feature allows underwriters and analyst managers to configure email and SMS delivery for four event types (approval, decline, document-request, manual-review-escalation) subject to regulatory restrictions, role-based access controls, delegated-session read-only semantics, and fail-closed audit behavior.

**Canonical Source**: `specs/product-spec-notification-preferences.md` (PROJ-412, Q2 2026 pilot) is the authoritative product specification. `specs/non-functional-requirements.md` refines constraints on audit, performance, security, and observability. `docs/adr/ADR-003-frontend-state.md` governs frontend state ownership. `specs/bug-report.md` demonstrates overlapping rule layers that commonly cause AI-generated code to fail.

---

## Confirmed Requirements (Source-Backed)

### Functional Requirements

| Requirement | Identifier | Description |
|---|---|---|
| Preference matrix | FR-1 | Users configure email and SMS independently for approval, decline, document-request, manual-review-escalation. |
| Mandatory escalation | FR-2 | Manual-review-escalation must have at least one enabled channel; users cannot disable all channels. |
| Role-based defaults | FR-3 | New users without saved preferences receive underwriter/analyst-manager defaults on first access without migration. |
| California SMS restriction | FR-4 / LEGAL-218 | SMS for decline decisions must remain disabled for CA loans until legal review completes. Restriction is loan-state based (not borrower-state). UI must show conditional explanation. |
| Degraded SMS fallback | FR-5 | If SMS provider unavailable, delivery falls back to email when enabled. **Stored preferences must NOT change.** Fallback must be logged separately. |
| Auditability | FR-6 | Every preference change records actor, timestamp, previous value, new value, source channel, and delegated-for user. |

### Special Conditions

| Condition | Identifier | Description |
|---|---|---|
| Locked applications | SC-1 | Settings screen allows preference changes globally; clarify that changes don't affect notifications already queued for a finalized application. |
| Delegated sessions | SC-2 | Analyst managers in delegated mode may **view** delegate's preferences but **cannot modify**. UI must indicate delegated-session mode. Audit entries must record both actor and delegated-for user. |
| Mixed portfolio | SC-3 | When settings opened from multi-state portfolio, show state-specific restrictions as conditional rules rather than blanket-disabling controls. |

### Non-Functional Requirements

| Requirement | Identifier | Key Constraint |
|---|---|---|
| Performance | NFR-1 | Settings load ≤150ms p95 over baseline; save ≤400ms p95. |
| Availability | NFR-2 | **FAIL-CLOSED**: If audit logging unavailable, writes ABORT (not silent save without trail). Reads tolerate provider degradation. |
| Security | NFR-3 | SMS destination values (phone numbers) are sensitive; exclude from client logs/analytics. Delegated sessions explicitly identified in audit. |
| Accessibility | NFR-4 | Keyboard-reachable controls, screen-reader labeled, persistent explanatory text for disabled mandatory events (not tooltips), ARIA live regions for save status. |
| Observability | NFR-5 | Emit counters: `preference.read.failure`, `preference.save.failure`, `audit.write.failure`, `notification.sms.fallback`; histogram `preference.save.latency`. Distinguish validation (4xx) from provider failures (5xx). |
| Change safety | NFR-6 | Feature shipped behind **release flag** (`notificationPreferences`). Non-pilot users see 404 (not 403) to hide feature existence. Role-based defaults on first access (no pre-migration required). |
| Compliance | NFR-7 | Audit records retained 24 months. Mandatory escalation delivery testable and in release checklist. Compliance reviewer's read-only view shows effective preference state including applied defaults. |

### Architecture & Patterns

| Pattern | Identifier | Implication |
|---|---|---|
| Central client store | ADR-003 | Frontend notification preferences must use central store (not component-local state). Optimistic updates must support rollback on API rejection. |
| Message contracts | Design rule | Changes to `src/backend/src/queue/contracts.ts` are breaking changes; all producers and consumers must be updated. |
| Pure business rules | Design pattern | Rule modules in `src/backend/src/rules/` accept parameters (not internal imports); return structured results with `allowed` + `reason` (not bare booleans). |
| Authorization patterns | `middleware/auth.ts` | Delegated-session detection via `x-delegated-for` header. `blockDelegatedWrites` checks before write routes. Feature-flag 404 guards use `notificationPreferences` flag. |

---

## Open Questions & Assumptions

| Question | Details | Resolution |
|---|---|---|
| **Compliance reviewer audit access** | Should audit history be accessed from the same settings page or separate audit viewer? | **Assumption**: Separate audit viewer (follows existing pattern for compliance workflows). If inline audit required, frontend will need two panels and backend will need new audit query endpoint. |
| **Loan-state vs borrower-state for CA restriction** | When loan jurisdiction differs from borrower address, which determines SMS restriction? | **RESOLVED** (per spec answer): Loan-state (`loanState` field on `LoanApplication`). Must be passed to preference save request to enforce at API level. |
| **Portfolio view restriction display** | Summary banner or per-row indicators for state-specific rules in multi-state context? | **Assumption**: Summary banner (lower complexity, clearer UX). Per-row indicators may be added in future polish. |
| **Role-based default generation timing** | Should defaults be generated on first settings page load, or on first preference read (e.g., GET /api/notifications/preferences/:userId)? | **Assumption**: Generate on first read (GET endpoint); preference repository returns generated defaults if no row exists. Simplifies frontend logic. |
| **Feature flag interaction** | If `notificationPreferences` flag is false, should GET also return 404, or 200 with empty array? | **Assumption**: GET returns 200 with empty array (read is allowed for compliance reviewers). Only write endpoints return 404 if flag false. |

---

## Inferred Implementation Choices

These choices derive from the confirmed requirements but are NOT explicit in specs; they guide implementation decisions and should be validated in code review.

### Database Schema Additions

1. **notification_preferences table**: Composite PK (user_id, event, channel). Fields: enabled (bool), updated_at (ISO), updated_by (user_id). Schema already exists in codebase.
2. **audit table**: Expanded to capture `delegated_for` user when applicable. Retention policy: 24 months (NFR-7). Schema already exists in codebase.

### Backend Surfaces

1. **Preference Rules Module** (`src/backend/src/rules/notification-channel-rules.ts`): New pure function `canDisableChannel(event, channel, loanState, mandatoryEvents)` returning `{ allowed: bool, reason: string }`. Enforces:
   - FR-2: Manual-review-escalation cannot have all channels disabled.
   - FR-4: SMS for decline on CA loans cannot be enabled.
   - Rule parameters passed explicitly (not internal imports).

2. **Preference Service** (`src/backend/src/services/preference-service.ts`): New service orchestrating preference updates:
   - Validate preferences against rules before persisting.
   - Apply fail-closed audit semantics (reject write if audit unavailable).
   - Emit preference.updated events to broker for audit handlers.
   - Handle role-based default generation for first-time users.

3. **Notification Routes** (`src/backend/src/routes/notifications.ts`): Additions and modifications:
   - Existing routes already include delegated-session blocks (observed in code).
   - **New**: POST /api/notifications/preferences/defaults/:userId — generate role-based defaults on first access (not exposed, internal use).
   - **Modify**: PUT /api/notifications/preferences — add loanState parameter validation, call canDisableChannel rule, enforce fail-closed audit.
   - **Add feature flag guard**: Return 404 if notificationPreferences flag false AND user not pilot.

4. **Audit Integration**: 
   - Preference updates queued as audit.requested events (if queueAudit flag true) or direct DB writes (if false).
   - NFR-2 fail-closed: If audit handler rejects (error thrown or timeout), the preference save must NOT complete. Route returns 500 with "audit write failed" message.

5. **Observability Metrics**:
   - Counter `preference.read.failure` — preference repository read errors.
   - Counter `preference.save.failure` — splits into `preference.save.validation_failure` (4xx) vs `preference.save.provider_failure` (5xx).
   - Counter `audit.write.failure` — fail-closed rejections.
   - Counter `notification.sms.fallback` — SMS→email fallback invocations (in notification-handler).
   - Histogram `preference.save.latency` — p50/p95/p99.

### Frontend Surfaces

1. **Notification Preferences Page**: New page at `/settings/notifications`:
   - Matrix layout: rows = event types, columns = channels (email, SMS).
   - Role-based visibility: underwriter/analyst-manager see full controls; compliance-reviewer sees read-only view.
   - **Delegated-session indicator**: Banner or badge showing "viewing [delegate name]'s preferences (read-only)".
   - **California restriction indicator**: When CA loan active, show "SMS for decline unavailable (legal review LEGAL-218 pending)" with disabled toggle.
   - **Mandatory escalation indicator**: Badge or helper text on manual-review-escalation row: "At least one channel must remain enabled."

2. **Central Store Updates** (per ADR-003):
   - New store slice: `notificationPreferences` with state:
     ```typescript
     {
       byUserId: Record<string, NotificationPreference[]>,
       loading: boolean,
       error: string | null,
       delegatedFor: User | null,  // if delegated session
       loanState: string | null,   // for state-based restrictions
     }
     ```
   - Actions: `setPreferences`, `updatePreference`, `rollbackPreference`, `setDelegatedSession`, `clearError`.
   - Optimistic update: on local state change, emit update action. On 403/400 response, emit rollback action (restores previous value from store history).

3. **API Client** (`src/frontend/src/api/notifications.ts`):
   - `getPreferences(userId: string): Promise<NotificationPreference[]>`
   - `updatePreference(userId, event, channel, enabled, loanState): Promise<NotificationPreference>`
   - `getDefaults(role: string): Promise<NotificationPreference[]>` — for first-load defaults generation.

4. **UX Affordances**:
   - Disabled controls (CA decline SMS, all-channels-disabled states) use `<fieldset disabled>` with persistent `<legend>` help text (not tooltip).
   - Success toast: "Preferences saved" with automatic dismiss. Error toast: specific message from 4xx rejection or generic "Save failed. Please try again."
   - Save button disabled while `loading === true`.
   - Form state reflects ARIA live region on mount for screen readers.

### Release & Observability

1. **Feature Flag**: `notificationPreferences` (boolean, default false for non-pilot). Controls:
   - GET /api/notifications/preferences returns 200 (always allowed for audit).
   - PUT endpoints return 404 if flag false AND actor not explicitly pilot-tagged.
   - Frontend page /settings/notifications returns 404 if flag false (link hidden in nav).

2. **Pilot Rollout**: 
   - Initial cohort defined in config/feature-flags.ts as whitelist or role-based.
   - Gradual rollout can extend whitelist without code change (env var).
   - Success metrics (30% reduction in mute requests, <1% failed saves) tracked via observability metrics above.

3. **Release Checklist Items**:
   - [ ] Mandatory escalation delivery rule tested for all state transitions.
   - [ ] CA decline SMS restriction tested on CA loans (loanState = "CA") and non-CA.
   - [ ] Fail-closed audit semantics tested (preference write rejects if audit service unavailable).
   - [ ] Delegated-session write block tested (401/403 on delegated PUT).
   - [ ] Role-based defaults generated for first-access scenario.
   - [ ] SMS fallback metrics emitted and dashboards created.
   - [ ] Compliance reviewer read-only access verified (no write permissions).

---

## Constraints & Special Conditions

### Regulatory & Compliance

1. **LEGAL-218 (California Decline SMS)**:
   - SMS for decline decisions disabled for CA loans until legal review completes.
   - Restriction is on the **loan**, not the user (different users may have different restrictions based on which loan they're working on).
   - Implication: `loanState` must be sent to API with each update; rule evaluation is loan-contextual, not user-global.

2. **Mandatory Escalation Delivery**:
   - Manual-review-escalation is a **hard requirement**; cannot be fully suppressed.
   - FR-2: At least one channel (email or SMS) must remain enabled.
   - Implication: Save must validate all escalation channels before persisting. If user tries to disable SMS while email is already disabled, reject with helpful message.

3. **Delegated Sessions (Read-Only)**:
   - Analyst manager with `x-delegated-for` header can GET delegate's preferences but cannot PUT.
   - UI must indicate delegation; user cannot accidentally think they're editing their own prefs.
   - Audit entries must record both actor (analyst manager) and delegatedFor (underwriter).

4. **Fail-Closed Audit Semantics**:
   - If audit handler fails (error thrown, timeout, or unavailable), the preference write is **rejected** (not silently saved).
   - NFR-2 explicitly calls this out as a hard negative pattern.
   - Route handler must check audit completion before returning 200. If audit failed, return 500 with `audit.write.failure` metric.

### Technical Constraints

1. **Frontend State Ownership** (ADR-003):
   - Notification preferences must live in central store, not component-local state.
   - Optimistic updates must support rollback. When API rejects (4xx/5xx), store rollback action reverts local changes.

2. **Message Contract Changes**:
   - No new message types needed. Existing `audit.requested` and `notification.requested` contracts cover preference changes and fallback notifications.
   - If future requirement mandates new preference change event type, update `src/backend/src/queue/contracts.ts` and all consuming handlers.

3. **Preference UPSERT Behavior**:
   - `setPreference` in preference-repository uses INSERT OR REPLACE on composite PK (user_id, event, channel).
   - **No partial updates**: Entire row is replaced, including updated_at and updated_by. This is correct (tracks who last changed it) but easy to miss in code review.

4. **Phone Number Sensitivity**:
   - SMS destination values (phone numbers) must not appear in client logs, analytics, or debug output.
   - Safe to store in DB and return in API response (backend only).
   - Frontend must avoid logging preferences to console or analytics (NFR-3).

### Release & Rollout

1. **Feature Flag (notificationPreferences)**:
   - Non-pilot users calling GET see 200 (read allowed); calling PUT see 404 (write hidden).
   - Prevents leaking feature existence to non-pilot users.
   - Pilot users explicitly whitelisted in config (by user ID, role, or team).

2. **No Migration Required**:
   - Existing users without saved preferences receive role-based defaults on first access.
   - No backfill job needed; defaults are computed on-read by preference service.

3. **Degraded Mode (SMS Fallback)**:
   - If SMS provider unavailable, notification handler falls back to email (if enabled).
   - **Critical**: Stored preference model unchanged. Next request sees original SMS enabled state.
   - Separate metric `notification.sms.fallback` tracks fallback invocations (not a bug or error, expected during provider outage).
   - False positive: User receiving email during SMS outage is NOT a preference data problem.

---

## False Positive & Hard Negative Patterns

### False Positive Example (Correctly Allowed)

**Scenario**: User disables SMS for manual-review-escalation while email remains enabled.

**Naive concern**: "The user disabled a channel for a mandatory event!"

**Reality**: FR-2 requires at least one channel enabled for mandatory events. **This is correct and allowed.** The hard constraint is having zero channels, not which specific channel is active. The system should save this preference without error.

**Implications for code review**:
- Validation logic must check `atLeastOneChannelEnabled(event)` for mandatory events, not individual channel states.
- Tests must include case: escalation SMS disabled, email enabled → should succeed.

### Hard Negative Example (Must Reject)

**Scenario**: User attempts to disable both email and SMS for manual-review-escalation.

**Naive implementation**: Accepts the save, updates preferences table. User later complains they never got escalation alerts.

**Required behavior**: Reject the save (400 status) with message: "Manual-review-escalation requires at least one enabled channel."

**Root cause**: Validation rule missing from preference service.

**Implications for code review**:
- `canDisableChannel(event, channel, ...)` must return `{ allowed: false, reason: "..." }` before save.
- Route handler must check rule result before calling `prefRepo.setPreference()`.
- Tests must include case: escalation SMS disabled AND email disabled → should reject with 400.

---

## Implementation Tasks

### Task 1: Create Notification Channel Rules Module
**Acceptance Criteria**:
- [ ] New file `src/backend/src/rules/notification-channel-rules.ts` exports `canDisableChannel(event, channel, loanState, mandatoryEvents)` returning `{ allowed: bool, reason: string }`.
- [ ] Enforces FR-2: manual-review-escalation cannot have all channels disabled.
- [ ] Enforces FR-4: SMS for decline on CA loans cannot be enabled.
- [ ] Accepts parameters explicitly (no internal imports); is pure function.
- [ ] Includes JSDoc with examples of false-positive and hard-negative cases.
- [ ] Unit tests cover: happy path, boundary (exactly one channel enabled), CA restriction, non-CA bypass.
- [ ] Tests labeled with test category comments (Happy path, Boundary, Hard negative).

**Source References**: FR-2, FR-4 / LEGAL-218, design pattern in `src/backend/src/rules/business-rules.ts`.

---

### Task 2: Create Preference Service
**Acceptance Criteria**:
- [ ] New file `src/backend/src/services/preference-service.ts` exports:
  - `applyRoleDefaults(userId, role): NotificationPreference[]` — generates role-based defaults (all email enabled, SMS escalation only for underwriter/analyst-manager).
  - `updatePreference(session, userId, event, channel, enabled, loanState, mandatoryEvents): Promise<NotificationPreference>` — validates, persists, audits.
  - `getEffectivePreferences(userId): NotificationPreference[]` — returns stored preferences or defaults if no rows exist.
- [ ] Validation calls `canDisableChannel` before persistence; rejects invalid changes with structured error.
- [ ] Audit semantics: emit audit event via broker (if queueAudit flag) or direct write (if false).
- [ ] **Fail-closed**: If audit fails, the preference write is rejected. Service throws error; route catches and returns 500.
- [ ] Returns metrics-ready structured result (includes reason on failure for distinct 4xx vs 5xx counter).
- [ ] Handles delegated-session context (audit includes delegatedFor user).

**Source References**: FR-3, FR-6, NFR-2 (fail-closed), NFR-5 (metrics), SC-2 (delegated audit), design patterns in `src/backend/src/services/audit-service.ts` and `src/backend/src/services/loan-service.ts`.

---

### Task 3: Extend Notification Routes
**Acceptance Criteria**:
- [ ] Existing PUT /api/notifications/preferences route modified to:
  - Accept `loanState` parameter (required for CA restriction check).
  - Call preference-service `updatePreference()` instead of direct repo write.
  - Return 400 with rule reason on validation failure.
  - Return 500 with "audit write failed" on fail-closed audit rejection.
  - Emit `preference.save.latency` metric before returning.
- [ ] Verify delegated-session write block is present on line ~60 (already in codebase; confirm not removed).
- [ ] New route handler for GET /api/notifications/preferences/:userId modified to:
  - Call preference-service `getEffectivePreferences()` to apply defaults.
  - Return applied defaults to compliance reviewers without creating stored rows.
  - Emit `preference.read.failure` metric on error.
- [ ] Feature flag guard: If `notificationPreferences` flag false AND actor not pilot, return 404 on PUT (not 403).
- [ ] On GET: Always return 200 (read allowed for audit and compliance).

**Source References**: FR-1, FR-3, SC-2, NFR-1 (performance), NFR-2 (fail-closed), NFR-5 (metrics), NFR-6 (404 for non-pilot).

---

### Task 4: Update Frontend Central Store (ADR-003)
**Acceptance Criteria**:
- [ ] New Vuex/Pinia store slice (or equivalent central store) with state:
  ```
  notificationPreferences: {
    byUserId: Record<string, NotificationPreference[]>,
    loading: boolean,
    error: string | null,
    delegatedFor: User | null,
    loanState: string | null,
    lastSuccess: timestamp | null,
  }
  ```
- [ ] Actions:
  - `fetchPreferences(userId)` — GET endpoint, applies defaults on empty, updates byUserId.
  - `updatePreference(userId, event, channel, enabled, loanState)` — optimistic update: modifies local state immediately, emits PUT request.
  - `rollbackPreference(userId, event, channel)` — reverts local state on API rejection (hard negative pattern).
  - `setDelegatedSession(user)` — sets delegatedFor, disables write actions.
  - `clearError()` — clears error message.
- [ ] Rollback logic: store maintains previous-value history; on 400/403/500 response, fetch reverts to last known-good state.
- [ ] No phone numbers logged to console or sent to analytics (NFR-3 security).

**Source References**: ADR-003 (central store), SC-2 (delegated mode indication), design patterns in existing store modules.

---

### Task 5: Create Notification Preferences Page Component
**Acceptance Criteria**:
- [ ] New Vue/React component at `src/frontend/src/pages/NotificationPreferences.vue` (or .tsx):
  - Matrix layout: rows = event types, columns = email/SMS.
  - Per-cell toggle: click updates store immediately (optimistic).
  - Role-gated visibility: underwriter/analyst-manager see controls; compliance-reviewer sees read-only labels.
  - Delegated-session banner: "You are viewing [name]'s preferences (read-only)."
  - Mandatory escalation label: "At least one channel required."
  - California restriction explanation (if loanState = "CA"): "SMS for decline is unavailable pending legal review (LEGAL-218)."
  - Disabled controls use `<fieldset disabled>` + visible legend (not tooltip), for NFR-4 accessibility.
  - Save button calls `updatePreference` action for each changed cell.
  - Success toast: "Preferences saved." Error toast: show reason from 4xx response, or "Save failed. Refreshing...".
  - ARIA live region announces save result (NFR-4).
- [ ] Props: userId (string), delegatedFor (User | null), loanState (string | null from active loan context or portfolio filter).
- [ ] No phone numbers rendered or logged (NFR-3 security).
- [ ] Keyboard navigation: Tab between cells, Enter/Space to toggle, Tab to Save button.

**Source References**: FR-1, FR-3, FR-4, SC-1, SC-2, NFR-4 (accessibility), design patterns in existing settings components.

---

### Task 6: Add Feature Flag Support & Observability Metrics
**Acceptance Criteria**:
- [ ] Feature flag `notificationPreferences` added to `src/backend/src/config/feature-flags.ts` (default false).
- [ ] GET /api/notifications/preferences returns 200 regardless of flag (read always allowed).
- [ ] PUT /api/notifications/preferences returns 404 if flag false AND actor not pilot-whitelisted.
- [ ] Frontend page /settings/notifications returns 404 if flag false; nav link hidden.
- [ ] Observability metrics emitted:
  - `preference.read.failure` counter on read errors.
  - `preference.save.failure` split into `validation` and `provider` labels for 4xx vs 5xx.
  - `audit.write.failure` counter on fail-closed rejections.
  - `notification.sms.fallback` counter in notification-handler when fallback triggered.
  - `preference.save.latency` histogram in route handler before response.
- [ ] Metrics initialized in service/route modules with labels for event type, channel, loanState (if applicable).

**Source References**: NFR-5 (observability), NFR-6 (feature flag), design patterns in existing middleware/routes.

---

### Task 7: Add Default Role Permissions & Compliance Reviewer Read-Only
**Acceptance Criteria**:
- [ ] Confirm `src/backend/src/rules/role-permissions.ts` already grants:
  - `notification-pref:read` to all roles (underwriter, analyst-manager, compliance-reviewer).
  - `notification-pref:write` to underwriter and analyst-manager only (NOT compliance-reviewer).
- [ ] Confirm routes check `hasPermission(role, "notification-pref:write")` before PUT.
- [ ] Compliance reviewer GET /api/notifications/preferences/:userId returns effective preferences (including applied defaults) with read-only indicator.
- [ ] Compliance reviewer PUT returns 403 with message: "Compliance reviewers cannot modify notification preferences."

**Source References**: FR-3, role-permissions pattern in `src/backend/src/rules/role-permissions.ts`.

---

### Task 8: Update Audit & Message Contracts (if needed)
**Acceptance Criteria**:
- [ ] Confirm `AuditRequestedEvent` contract (queue/contracts.ts) already includes `delegatedFor` field.
- [ ] Confirm `NotificationRequestedEvent` contract already includes `preferredChannel` field (used for fallback).
- [ ] No new message types added (existing contracts sufficient).
- [ ] Audit entries record preference change action: `"preference.updated"` with previous/new values.
- [ ] Test: update preference, confirm audit entry includes `delegatedFor` if delegated session, null otherwise.

**Source References**: Design rule (message contracts), `src/backend/src/queue/contracts.ts`.

---

### Task 9: Add Unit Tests for Business Rules (False Positive & Hard Negative)
**Acceptance Criteria**:
- [ ] Unit tests in `src/backend/tests/unit/notification-channel-rules.test.ts`:
  - **Happy path**: Disable SMS for approval (non-mandatory) → allowed.
  - **Happy path**: Disable SMS for escalation while email enabled → allowed (false positive safeguard).
  - **Boundary**: Enable SMS for decline on CA loan → rejected (FR-4).
  - **Hard negative**: Disable all channels for escalation → rejected with clear reason.
  - **Hard negative**: Disable email for escalation, SMS already disabled → rejected.
  - **CA bypass**: SMS for decline on non-CA loan → allowed.
  - Tests labeled with category comments (Happy path, Boundary, Hard negative).
- [ ] Unit tests in `src/backend/tests/unit/preference-service.test.ts`:
  - Role-based defaults generated correctly (all email, SMS escalation only).
  - Fail-closed audit: if audit handler throws, updatePreference rejects.
  - Delegated session: audit entries record both actor and delegatedFor.
  - Optimistic update rejection: store receives rollback on 400 response.

**Source References**: Testing pattern in `src/backend/tests/unit/business-rules.test.ts`, false-positive and hard-negative examples in specs.

---

### Task 10: Add Integration Test for Full Workflow
**Acceptance Criteria**:
- [ ] Integration test in `src/backend/tests/integration/notification-preferences.test.ts`:
  - POST /api/notifications/preferences with valid change → success, audit logged, metrics emitted.
  - POST /api/notifications/preferences with escalation all-channels-disabled → 400, no audit, validation metric emitted.
  - PUT /api/notifications/preferences in delegated session → 403, audit logged with actor/delegatedFor.
  - PUT with CA decline SMS on CA loan → 400, audit not logged (validation failure).
  - Audit write fails (mocked error) → preference write rejected with 500, `audit.write.failure` metric.
- [ ] Test loan context: create loan with loanState="CA", attempt decline SMS → rejected; same for loanState="TX" → allowed.

**Source References**: Integration pattern in `src/backend/tests/integration/applications.test.ts`, fail-closed pattern in NFR-2.

---

### Task 11: Add Frontend Component Tests & Rollback Scenario
**Acceptance Criteria**:
- [ ] Component test for NotificationPreferences:
  - Render matrix with toggles for underwriter role → all enabled (writable).
  - Render matrix for compliance-reviewer role → all disabled (read-only).
  - Click escalation SMS toggle (enabled → disabled) → local state updates immediately (optimistic).
  - Backend responds with 400 (rule violation) → rollback action restores previous value.
  - Toast shows error reason: "Manual-review-escalation requires at least one enabled channel."
  - Delegated session: render "viewing [name]'s preferences" banner, click toggle → no state change (disabled button).
  - CA restriction: loanState="CA", escalation SMS toggle disabled, show explanation text (not tooltip).

**Source References**: ADR-003 (optimistic updates and rollback), SC-2 (delegated read-only), NFR-4 (accessibility).

---

### Task 12: Update Release Checklist & Observability Dashboard
**Acceptance Criteria**:
- [ ] Release checklist includes:
  - [ ] Mandatory escalation delivery rule tested for all state transitions (using existing MANDATORY_EVENTS).
  - [ ] CA decline SMS restriction tested on CA loans (loanState="CA") and non-CA.
  - [ ] Fail-closed audit semantics tested (preference write rejects if audit unavailable).
  - [ ] Delegated-session write block tested (403/401 on delegated PUT).
  - [ ] Role-based defaults generated for first-access scenario.
  - [ ] SMS fallback metrics emitted during provider outage simulation.
  - [ ] Compliance reviewer read-only access verified (no write permissions).
  - [ ] Feature flag `notificationPreferences=false` returns 404 for PUT (non-pilot).
- [ ] Dashboard created for metrics: preference.save.latency histogram, preference.save.failure by type (validation vs provider), sms.fallback counter.
- [ ] Success metrics tracked: <1% failed saves (NFR-6), 30% reduction in mute requests within 60 days.

**Source References**: NFR-6 (change safety), NFR-7 (compliance), design patterns in existing release docs.

---

## Validation Steps

### Functional Validation

1. **Preference Matrix**:
   - User opens settings, sees matrix of events × channels.
   - User disables email for document-request, saves → preference persisted, audit logged.
   - User loads settings in new browser tab → preference shown as disabled (not just local state).

2. **Mandatory Escalation Constraint** (Hard Negative):
   - User disables SMS for manual-review-escalation while email enabled → saves successfully.
   - User disables email for manual-review-escalation → SMS already disabled → attempts save → 400 with reason.
   - User reenables email → saves successfully.

3. **California SMS Restriction** (Hard Negative):
   - User views settings for CA loan (loanState="CA") → decline SMS toggle disabled, explanation visible.
   - User views settings for TX loan → decline SMS toggle enabled.
   - User attempts PUT with decline SMS enabled and loanState="CA" → 400 with "California restriction" reason.

4. **Delegated Session** (Read-Only):
   - Analyst manager opens settings with `x-delegated-for: underwriter-1` header.
   - UI shows "You are viewing [underwriter name]'s preferences (read-only)."
   - Toggles appear disabled or non-interactive.
   - Audit log shows both actor (analyst) and delegatedFor (underwriter).
   - Attempting PUT in delegated session → 403.

5. **Fail-Closed Audit**:
   - Audit service intentionally made unavailable (mocked error or network block).
   - User attempts preference save → 500 response with "audit write failed" message.
   - Preference NOT persisted in database.
   - Metric `audit.write.failure` incremented.
   - Audit service restored → preference save succeeds.

6. **SMS Fallback** (Not a Bug):
   - SMS provider made unavailable.
   - Preference set: email enabled, SMS enabled for approval.
   - Transition triggers approval notification → handler attempts SMS, fails, falls back to email.
   - User receives email (not SMS) → check logs, see fallback metric emitted.
   - Preference still shows SMS enabled (not changed).
   - SMS provider restored → next notification uses SMS.

7. **Role-Based Defaults**:
   - New underwriter user, no preferences stored.
   - GET /api/notifications/preferences/new-user-id → returns defaults (all email enabled, SMS escalation only).
   - No rows created in database.
   - User enables email for document-request, saves → now a row exists.
   - GET returns mix of stored + default values.

8. **Compliance Reviewer Access**:
   - Compliance reviewer opens settings → sees matrix, all toggles disabled (read-only).
   - GET request succeeds (returns 200, shows effective preferences including defaults).
   - PUT request → 403 with "compliance reviewers cannot modify" message.

### Performance Validation

1. **Settings Load**: Measure p95 latency of GET /api/notifications/preferences/:userId; confirm ≤150ms p95 over baseline (NFR-1).
2. **Save Latency**: Measure p95 latency of PUT /api/notifications/preferences; confirm ≤400ms p95 (NFR-1). Includes audit write if synchronous.

### Security & Observability Validation

1. **No Phone Numbers in Logs**: Review log output from preference service; confirm no SMS destination values present.
2. **Metrics Cardinality**: Verify metrics tags (event, channel, loanState) don't explode cardinality; cap loanState to top N states if needed.
3. **Distinguish 4xx vs 5xx**: Confirm `preference.save.failure` split by `type: "validation"` (user error) vs `type: "provider"` (infrastructure).

### Rollout Validation

1. **Feature Flag**: Set `notificationPreferences=false` in staging, verify non-pilot GET returns 200, PUT returns 404, UI link hidden.
2. **Pilot Whitelist**: Add single user to pilot, verify they see settings; remove, verify 404 on PUT.
3. **Success Metrics**: After initial pilot, confirm <1% failed saves and 30% reduction in mute requests.

---

## Risks & Dependencies

### Risks

1. **Delegated-Session Write Block Bypass**: If auth middleware check is skipped or route-level check removed, analyst managers can modify delegate's preferences. **Mitigation**: Code review must verify `session.delegatedFor` check on line ~60 of notifications.ts and every write route. Test with delegated session.

2. **Fail-Closed Audit Not Enforced**: Service may silently swallow audit errors (try-catch with no re-throw). **Mitigation**: NFR-2 explicitly calls this a hard negative. Code review must verify error propagates; route handler catches and returns 500. Add test: mock audit error, confirm preference not persisted.

3. **California Restriction Bypassed**: If loanState not passed to API, rule check cannot evaluate. **Mitigation**: Require loanState parameter in PUT request body. Validate non-null. Test with missing loanState.

4. **Frontend Optimistic Update Not Rolled Back**: UI updates local state but doesn't revert on API rejection. **Mitigation**: ADR-003 requires rollback logic. Test: click toggle (local update), trigger 400 response, verify toggle reverts.

5. **Role-Based Defaults Not Generated**: New users without stored preferences see empty preference list instead of defaults. **Mitigation**: preference-service `getEffectivePreferences()` must return computed defaults if no rows exist. Test: first access by new user, verify defaults returned and not persisted.

6. **SMS Fallback Changes Stored Preference**: If fallback logic calls `setPreference()`, stored state is modified (hard negative). **Mitigation**: Fallback must emit notification on email channel only; must not update preference store. Confirm notification-handler does not call setPreference. Metric `notification.sms.fallback` is count, not a preference change.

7. **Performance Regression**: Permission check, rule evaluation, and audit write add latency. **Mitigation**: NFR-1 performance budgets must be met. Use batch queries where possible; cache role permissions. Profile before/after in staging.

8. **Message Contract Breaking Change**: If preference change event structure added without updating all consumers, handlers fail silently. **Mitigation**: Design rule: all contract changes must update producers AND consumers simultaneously. No new message types needed for this feature (audit.requested already works).

### Dependencies

1. **Audit Service Availability**: Feature requires audit writes to succeed (fail-closed). Depends on audit-handler and broker reliability.
2. **Feature Flag Infrastructure**: Depends on config/feature-flags.ts and env.ts for pilot rollout control.
3. **Central Store Pattern** (ADR-003): Frontend implementation depends on existing central store architecture (Vuex/Pinia/Redux).
4. **Database Schema**: notification_preferences and audit tables must exist (already present in codebase).
5. **Notification Provider**: Degraded-mode fallback depends on notification-handler SMS attempt + email fallback logic (existing, must be verified).

---

## Summary Table: What Changes Where

| Layer | Surface | Change Type | Key File(s) |
|---|---|---|---|
| **Rules** | Notification channel rules | New module | `src/backend/src/rules/notification-channel-rules.ts` |
| **Business Logic** | Preference service | New module | `src/backend/src/services/preference-service.ts` |
| **Routes** | Notification preferences API | Extend + modify | `src/backend/src/routes/notifications.ts` |
| **Config** | Feature flags | Extend | `src/backend/src/config/feature-flags.ts` |
| **Store** | Central client state | New slice | `src/frontend/src/store/notificationPreferences.ts` |
| **Components** | Settings UI | New page | `src/frontend/src/pages/NotificationPreferences.vue` |
| **API Client** | HTTP client | New methods | `src/frontend/src/api/notifications.ts` |
| **Tests** | Business rules & integration | New tests | `src/backend/tests/unit/notification-channel-rules.test.ts`, `src/backend/tests/integration/notification-preferences.test.ts` |
| **Observability** | Metrics & dashboards | New metrics | Service/route modules emit counters & histogram |

---

## Conclusion

This plan separates confirmed requirements (from product spec, NFRs, and ADRs) from inferred implementation choices. It surfaces the four overlapping constraint layers (authorization, business rule, UI pattern, audit) that the bug report demonstrates. It explicitly calls out delegated sessions, LEGAL-218, mandatory-event delivery, fail-closed audit behavior, degraded-mode fallback, and both false-positive and hard-negative patterns. It provides numbered tasks with acceptance criteria and source references, validation steps covering functional/performance/security dimensions, and identified risks and dependencies for the implementation team.
