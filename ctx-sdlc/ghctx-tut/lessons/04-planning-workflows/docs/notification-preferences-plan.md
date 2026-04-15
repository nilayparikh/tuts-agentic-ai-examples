# Notification Preferences Implementation Plan

**Status:** Planning Phase  
**Owner:** Lending Platform Product (PROJ-412)  
**Target:** 2026 Q2 Pilot  
**Last Updated:** 2026-04-15

---

## Executive Summary

This plan outlines the implementation of user-configurable notification preferences for the Loan Workbench platform. The feature addresses alert fatigue by allowing underwriters and analyst managers to control which notifications they receive (approval, decline, document-request, manual-review-escalation) across email and SMS channels.

**Key Constraints:**
- Mandatory notification events (manual-review-escalation) must always have at least one enabled channel.
- California loans have a temporary SMS restriction for decline notifications (LEGAL-218).
- Delegated analyst-manager sessions are read-only.
- Audit logging must fail-closed (abort saves if audit unavailable).
- Compliance reviewers have read-only access.
- SMS provider failures fall back to email without modifying stored preferences.

**Canonical Source:** Product Specification (specs/product-spec-notification-preferences.md) is the primary authority. NFRs provide constraints and safety rails. Architecture and ADRs guide implementation pattern choices.

---

## Confirmed Requirements with Source References

### Functional Requirements (FR)

| ID  | Requirement                                                  | Source Reference                                            |
| --- | ------------------------------------------------------------ | ----------------------------------------------------------- |
| FR1 | Preference matrix: email/SMS independent per event type      | product-spec-notification-preferences.md § Functional Requirements § FR-1 |
| FR2 | Mandatory event rule: ≥1 channel for manual-review-escalation | product-spec-notification-preferences.md § FR-2 (explicit hard negative pattern) |
| FR3 | Role-based defaults on first access (no migration required)   | product-spec-notification-preferences.md § FR-3 § User-based defaults table |
| FR4 | California SMS restriction for decline (LEGAL-218)          | product-spec-notification-preferences.md § FR-4 (explicit: loan_state based) |
| FR5 | Degraded delivery fallback: SMS→email, no pref modification  | product-spec-notification-preferences.md § FR-5 (explicit false positive pattern) |
| FR6 | Audit all preference changes (actor, timestamp, old/new values) | product-spec-notification-preferences.md § FR-6 (complete audit trail) |

### Special Conditions (SC)

| ID   | Condition                                                    | Source Reference                                           |
| ---- | ------------------------------------------------------------ | ---------------------------------------------------------- |
| SC-1 | Locked applications: prefs change globally, UI clarifies no retroactive effect | product-spec-notification-preferences.md § SC-1 |
| SC-2 | Delegated sessions: read-only (no modify), visually indicated | product-spec-notification-preferences.md § SC-2 (explicit hard negative pattern) |
| SC-3 | Multi-state portfolio: conditional rules, not blanket disable | product-spec-notification-preferences.md § SC-3 |

### Non-Functional Requirements (NFR)

| ID   | Requirement                                                  | Source Reference                                                  |
| ---- | ------------------------------------------------------------ | ------------------------------------------------------------- |
| NFR1 | Performance: ≤150 ms p95 (settings page load), ≤400 ms p95 (save) | non-functional-requirements.md § NFR-1 |
| NFR2 | Availability: audit writes fail-closed (abort on audit unavailable) | non-functional-requirements.md § NFR-2 (explicit hard negative) |
| NFR3 | Security: no SMS phone numbers in logs/analytics; delegated sessions explicit in audit | non-functional-requirements.md § NFR-3 |
| NFR4 | Accessibility: persistent explanatory text for mandatory controls, ARIA live regions | non-functional-requirements.md § NFR-4 |
| NFR5 | Observability: distinct metrics for validation vs provider failures, SMS fallback tracking | non-functional-requirements.md § NFR-5 |
| NFR6 | Feature flag: 404 for non-pilot users (not 403); role-based defaults without migration | non-functional-requirements.md § NFR-6 |
| NFR7 | Compliance: 24-month audit retention; mandatory escalation delivery testable | non-functional-requirements.md § NFR-7 |

### Architectural Patterns

| ID  | Pattern                                                      | Source Reference                                              |
| --- | ------------------------------------------------------------ | ------------------------------------------------------------- |
| AR1 | Central client store for persisted user preferences (not component-local state) | docs/adr/ADR-003-frontend-state.md § Decision |
| AR2 | Pure business rule functions with structured result objects  | src/backend/src/rules/business-rules.ts, role-permissions.ts |
| AR3 | Routes orchestrate; business rules live in src/backend/src/rules/ | docs/architecture.md § System Shape § Key Architectural Rules |
| AR4 | Audit via queue broker OR direct DB write (controlled by `queueAudit` flag) | src/backend/src/config/feature-flags.ts, audit-service.ts |
| AR5 | Message contracts in queue/contracts.ts are breaking-change surface | docs/architecture.md § Key Architectural Rules § #7 |
| AR6 | Feature-flagged endpoints return 404 (not 403) for non-pilot users | non-functional-requirements.md § NFR-6 |

---

## Open Questions with File References

1. **Compliance Reviewer Audit Access**: Should compliance reviewers access preference audit history from the same settings page or a separate audit viewer?
   - **Reference**: product-spec-notification-preferences.md § Open Questions #1
   - **Implication for Plan**: Affects frontend routing and component composition. Current routes/audit.ts exists but may need expansion.

2. **Portfolio View Restriction Display**: Should multi-state portfolio views show restriction summary banner or per-row indicators?
   - **Reference**: product-spec-notification-preferences.md § Open Questions #3
   - **Implication for Plan**: Affects frontend component architecture but does not block core feature (single-state view implementation).

3. **Audit Service Availability Handling**: Does "fail-closed" mean the save endpoint returns 500, or does it retry with exponential backoff?
   - **Reference**: non-functional-requirements.md § NFR-2 (hard negative pattern)
   - **Implication for Plan**: Clarify in error-handling strategy before implementing audit integration.

4. **SMS Fallback Metrics**: Should `notification.sms.fallback` metric increment only on successful email delivery, or on fallback trigger?
   - **Reference**: non-functional-requirements.md § NFR-5
   - **Implication for Plan**: Affects queue handler implementation in queue/handlers/.

---

## Inferred Implementation Choices

### Separated from Confirmed Requirements

The following choices are derived from architecture and NFR context, **not** explicit in functional requirements:

1. **Preference Validation as Pure Function**  
   - **Inference**: Business rule pattern (AR2) + mandatory event hard negative (FR2).
   - **Choice**: Implement `canDisableChannel(loanState, event, channel, userId) => ChannelDisableRule` as pure function in `src/backend/src/rules/notification-channel-rules.ts`.
   - **Why**: Enables AI-safety testing for edge cases (e.g., CA decline SMS, zero-channel scenarios).

2. **Delegated Session Authorization at Route Handler**  
   - **Inference**: SC-2 delegated read-only pattern + existing route structure (notifications.ts).
   - **Choice**: Route handler checks `session.delegatedFor` and returns 403 before accepting PUT (already implemented in notifications.ts lines 59–65, 124–129, 206–211).
   - **Why**: Consistent with existing guard pattern; prevents optimization mistakes.

3. **Role-Based Default Generation at Route Handler (Lazy)**  
   - **Inference**: FR-3 "no migration required" + architecture rule (AR3 "routes orchestrate").
   - **Choice**: GET /api/notifications/preferences/:userId returns defaults if no saved preferences exist (not on login/signup).
   - **Why**: Avoids upfront migration; accepts trade-off of first-access latency.

4. **Central Client Store for Preference State**  
   - **Inference**: ADR-003 decision (AR1) + persisted user preferences cross-screen scenario.
   - **Choice**: Frontend state manager (likely Zustand or simple Redux) stores preference matrix and handles optimistic updates with rollback on API rejection.
   - **Why**: Ensures consistency across navigation, page refresh, and delegated-session detection.

5. **Validation Failure Metric Distinction**  
   - **Inference**: NFR-5 observability requirement + route error handling.
   - **Choice**: Emit `preference.save.failure` with tag distinguishing `validation_error` (hard 400) vs `provider_error` (soft 500).
   - **Why**: Enables alerting on actionable infrastructure failures vs user-input mistakes.

6. **Audit Logging as Separate Middleware Invocation**  
   - **Inference**: NFR-2 fail-closed + audit-service.ts pattern (auditAction queues or writes synchronously).
   - **Choice**: Preference save fails (rollback, return 500) if auditAction emits error or fails synchronously.
   - **Why**: Prevents silent audit loss; complies with fail-closed requirement.

---

## Constraints and Special Conditions

### Critical Constraints

1. **Mandatory Event Hard Negative (FR2)**  
   - Users may not disable all channels for `manual-review-escalation`.
   - **Both UI and API** must enforce this rule.
   - **Test Case**: Attempt to disable email while SMS is already disabled → must fail.
   - **Source**: product-spec-notification-preferences.md § FR-2 § HARD NEGATIVE pattern.

2. **California SMS Restriction (LEGAL-218)**  
   - SMS for `decline` notifications must remain unavailable when `loanState = "CA"`.
   - Applies to **loan jurisdiction**, not borrower address if they differ.
   - **UI Impact**: Show persistent helper text (not tooltip) explaining restriction.
   - **Source**: product-spec-notification-preferences.md § FR-4; non-functional-requirements.md § NFR-6.

3. **Fail-Closed Audit (NFR2)**  
   - If audit service is unavailable, preference save must **fail** (not silently skip audit).
   - **Test Case**: Simulate audit-service outage → API returns 500, preference is NOT saved.
   - **Source**: non-functional-requirements.md § NFR-2 § HARD NEGATIVE pattern.

4. **Delegated Session Read-Only (SC-2)**  
   - Analyst managers in delegated mode may **read** but not **modify** delegate preferences.
   - UI must indicate delegated-session mode visually.
   - **Test Case**: Try to PATCH preferences in delegated session → 403 "Delegated sessions cannot modify...".
   - **Source**: product-spec-notification-preferences.md § SC-2 § HARD NEGATIVE pattern (optimistic UI update without server rejection).

5. **Feature Flag Rollout (NFR6)**  
   - Non-pilot users must see **404** (not 403) for feature-flagged endpoints.
   - Leaking 403 tells users the feature exists but is restricted.
   - **Source**: non-functional-requirements.md § NFR-6.

### False-Positive Patterns (Not Bugs)

1. **SMS Fallback to Email During Outage**  
   - A user receives email instead of SMS during SMS-provider outage.
   - **Not a bug**: Stored preferences are unchanged; delivery logs show fallback.
   - Support must check delivery logs, not preference store.
   - **Source**: product-spec-notification-preferences.md § FR-5 § FALSE POSITIVE pattern.

2. **Disabling SMS While Email Remains Enabled**  
   - User disables SMS for `manual-review-escalation` while email is enabled.
   - **Not a violation**: Constraint is ≥1 channel, not which channel is active.
   - **Source**: product-spec-notification-preferences.md § FR-2 § FALSE POSITIVE pattern.

3. **Role-Based Defaults Without Migration**  
   - New/existing users without saved preferences receive defaults on first API access (no upfront migration).
   - **Not a data-integrity bug**: Lazy default generation is correct per spec.
   - **Source**: non-functional-requirements.md § NFR-6 § FALSE POSITIVE pattern.

4. **Preference Reads During Audit Outage**  
   - User reads preferences while audit service is unavailable.
   - **Not a bug**: Only writes require audit availability.
   - **Source**: non-functional-requirements.md § NFR-2 § FALSE POSITIVE pattern.

---

## Numbered Tasks with Acceptance Criteria and Source References

### Phase 1: Backend Rules and Persistence (Foundation)

#### Task 1.1: Implement Mandatory Event Validation Rule
- **Description**: Create pure function `canDisableChannel()` in `src/backend/src/rules/notification-channel-rules.ts`.
- **Acceptance Criteria**:
  - Function accepts `(loanState, event, channel, mandatoryEvents)` as parameters (no internal imports of loan/user data).
  - Returns `{ allowed: boolean, reason: string }`.
  - Rejects any attempt to disable all channels for events in mandatoryEvents.
  - Rejects SMS disable for decline on CA loans (if `loanState = "CA"` and `event = "decline"` and `channel = "sms"`).
  - Exports function for route and test use.
- **Test Coverage**:
  - Happy path: disable SMS for approval (email enabled) → allowed.
  - Boundary: disable email for escalation when SMS enabled → allowed.
  - Hard negative: disable email for escalation when SMS already disabled → rejected.
  - Hard negative: disable SMS for decline on CA loan → rejected.
  - Hard negative: disable SMS for decline on non-CA loan → allowed.
- **Source Reference**: product-spec-notification-preferences.md § FR-2, FR-4; rules/business-rules.ts pattern.

#### Task 1.2: Extend Preference Repository with Bulk Query
- **Description**: Add function to `src/backend/src/models/preference-repository.ts` to fetch all preferences for a user with defaults applied.
- **Acceptance Criteria**:
  - Function: `getEffectivePreferences(userId: string, role: UserRole) => NotificationPreference[]`.
  - Returns saved preferences or role-based defaults if no saved preferences exist.
  - Defaults match FR-3 table (underwriter/analyst-manager: all events email enabled, escalation-only SMS).
  - No database write occurs (read-only).
- **Test Coverage**:
  - New user (no saved prefs) → returns defaults for role.
  - Partially saved user (some prefs exist) → merges saved + defaults.
  - Full user (all prefs exist) → returns saved only.
- **Source Reference**: product-spec-notification-preferences.md § FR-3; preference-repository.ts pattern.

#### Task 1.3: Extend Notification Routes with Validation Gate
- **Description**: Modify `src/backend/src/routes/notifications.ts` PUT handlers to call `canDisableChannel()` before persisting.
- **Acceptance Criteria**:
  - GET /api/notifications/preferences/:userId returns effective preferences (saved + defaults).
  - PUT /api/notifications/preferences validates change using `canDisableChannel()`.
  - If validation fails, return 400 with structured error: `{ code: "MANDATORY_CHANNEL_REQUIRED", message: "..." }`.
  - If audit fails (fail-closed), return 500 with error details.
  - All PUT operations audit the change (actor, previous value, new value, delegated-for if applicable).
- **Test Coverage**:
  - Valid preference save succeeds, audit entry created.
  - Invalid save (violates mandatory rule) returns 400, no change persisted.
  - Audit outage returns 500, preference NOT saved.
  - Delegated session blocks PUT, returns 403.
- **Source Reference**: product-spec-notification-preferences.md § FR-2, FR-6, SC-2; notifications.ts lines 45–105, 112–188, 195–271; NFR-2.

#### Task 1.4: Implement Degraded-Mode SMS Fallback Handler
- **Description**: Create or extend queue handler in `src/backend/src/queue/handlers/` for SMS fallback on notification delivery failure.
- **Acceptance Criteria**:
  - When notification.requested event is emitted with `preferredChannel: "sms"`, handler attempts SMS delivery.
  - If SMS provider unavailable and email enabled in preferences, fallback to email delivery.
  - Emit `notification.sms.fallback` metric on fallback trigger.
  - **Critical**: Do NOT modify stored preferences during fallback.
  - Log fallback with context (userId, event, reason).
- **Test Coverage**:
  - SMS failure with email enabled → fallback succeeds, metric incremented, prefs unchanged.
  - SMS failure with email disabled → delivery fails, no fallback, metric not incremented.
  - SMS success → no fallback, metric not incremented.
- **Source Reference**: product-spec-notification-preferences.md § FR-5; non-functional-requirements.md § NFR-5.

#### Task 1.5: Feature-Flag Gating and 404 Response
- **Description**: Add feature flag `notificationPreferences` to `src/backend/src/config/feature-flags.ts` and guard routes.
- **Acceptance Criteria**:
  - Add `notificationPreferences` flag to featureFlags object.
  - Update feature-flags.ts documentation.
  - Wrap notification preference routes with flag check that returns 404 (not 403) for non-pilot users.
  - Compliance reviewer reads always allowed (read doesn't leak existence).
- **Test Coverage**:
  - Non-pilot user GET → 404.
  - Non-pilot user PUT → 404.
  - Pilot user GET → 200 (or 404 if user not found, separate error).
- **Source Reference**: non-functional-requirements.md § NFR-6; feature-flags.ts pattern.

---

### Phase 2: Audit and Observability Integration

#### Task 2.1: Extend Audit Logging for Preference Changes
- **Description**: Ensure audit service captures all preference mutations with actor, delegated-for, and complete before/after state.
- **Acceptance Criteria**:
  - Audit entry includes: action ("preference.updated"), actor ID, delegated-for ID (if applicable), previous preference state, new preference state, source ("notification-routes"), timestamp.
  - Audit entry persisted before response sent to client (fail-closed on audit failure).
  - Phone numbers in audit entries must not appear in client logs or analytics exports.
- **Test Coverage**:
  - Preference update → audit entry created with correct fields.
  - Delegated session → audit includes both actor and delegated-for.
  - Audit DB failure → save operation fails (no partial state).
- **Source Reference**: product-spec-notification-preferences.md § FR-6, SC-2; NFR-3 (privacy), NFR-2 (fail-closed); audit-repository.ts and audit-service.ts patterns.

#### Task 2.2: Observability Metrics Setup
- **Description**: Emit metrics from preference save endpoint and SMS fallback handler.
- **Acceptance Criteria**:
  - Histogram `preference.save.latency` on successful saves (p50/p95/p99).
  - Counter `preference.save.failure` with tags: `error_type="validation_error"` (4xx) or `"provider_error"` (5xx).
  - Counter `preference.read.failure` on GET failures.
  - Counter `audit.write.failure` on audit service errors.
  - Counter `notification.sms.fallback` on SMS→email fallback.
  - Logs distinguish validation failures from downstream provider failures.
- **Test Coverage**:
  - Save succeeds → latency metric incremented.
  - Validation fails → `preference.save.failure` with `validation_error` tag.
  - Audit fails → `audit.write.failure` incremented.
  - SMS fallback triggers → fallback counter incremented.
- **Source Reference**: non-functional-requirements.md § NFR-5.

---

### Phase 3: Frontend Implementation (UI and State)

#### Task 3.1: Central Store Setup (Preference State)
- **Description**: Initialize preference state in central client store (Zustand, Redux, etc. per ADR-003).
- **Acceptance Criteria**:
  - Store schema includes:
    - `preferences: NotificationPreference[]` (fetched from API).
    - `defaults: NotificationPreference[]` (applied on first fetch if no saved prefs).
    - `isDelegatedSession: boolean` (read from x-delegated-for context).
    - `isLoading: boolean`, `error?: string` (for async operations).
  - Actions: `setPreferences()`, `updatePreference()`, `rollbackPreference()` (on API rejection).
  - Selectors: `getEffectivePreferences()`, `isChannelMandatory()`, `canDisableChannel()`.
  - Optimistic update with rollback on API 400/500.
- **Test Coverage**:
  - Store initializes with empty preferences.
  - Fetched preferences hydrate store.
  - Optimistic update followed by API success → persisted.
  - Optimistic update followed by API 400 → rolled back to previous state, error shown.
  - Delegated session blocks write actions.
- **Source Reference**: ADR-003 (AR1); product-spec-notification-preferences.md § SC-2.

#### Task 3.2: Preference Settings Page Component
- **Description**: Build preference matrix UI in `src/frontend/src/pages/preferences.ts` (or equivalent).
- **Acceptance Criteria**:
  - Render matrix: rows = events (approval, decline, document-request, manual-review-escalation), columns = channels (email, sms).
  - Each cell is a toggle (on/off).
  - Mandatory events (manual-review-escalation) have **persistent helper text** (not tooltip): "At least one channel must be enabled for escalation notifications."
  - CA decline SMS disabled control with explanation: "SMS for decline notifications is unavailable for California loans (legal review LEGAL-218 in progress)."
  - Delegated sessions show visual indicator: "You are viewing [user] preferences in read-only mode."
  - Finalized loan applications show clarification: "Changes to preferences apply globally. Notifications already queued for completed applications are not affected."
  - Save button submits all changed preferences; success toast on 200; error toast on 4xx/5xx.
  - Optimistic UI update followed by rollback on API rejection (toast: "Failed to save. Your previous settings have been restored.").
- **Test Coverage**:
  - Page renders preference matrix for current user.
  - Toggling a non-mandatory channel updates store optimistically.
  - Toggling all channels off for mandatory event → save fails, toast shows error.
  - Attempting to toggle CA decline SMS → toggle stays disabled, tooltip/helper text shown.
  - Delegated session: toggles disabled, indicator visible.
  - Save latency tracked (should be ≤400 ms p95 per NFR-1).
- **Source Reference**: product-spec-notification-preferences.md § FR-1 through FR-6, SC-1 through SC-3, UX Notes; NFR-4 (accessibility), NFR-6.

#### Task 3.3: Accessibility and Screen Reader Support
- **Description**: Ensure preference controls are keyboard-reachable and ARIA-compliant.
- **Acceptance Criteria**:
  - All toggles reachable via Tab key; focus indicators visible.
  - Helper text associated with toggles via `aria-describedby`.
  - Status messages (save success/failure) in `role="alert"` or `role="status"` with `aria-live="polite"`.
  - Screen reader announces: toggle state, mandatory event constraint, CA restriction reason.
  - No tooltip-only explanations; all critical info in visible text.
- **Test Coverage**:
  - Keyboard navigation reaches all controls.
  - Screen reader reads helper text and status messages.
  - ARIA annotations validate in axe or similar accessibility tool.
- **Source Reference**: non-functional-requirements.md § NFR-4.

#### Task 3.4: Compliance Reviewer Read-Only View
- **Description**: Extend preference UI for compliance-reviewer role (or separate audit-viewer component).
- **Acceptance Criteria**:
  - Compliance reviewer sees preference matrix but all controls disabled.
  - Shows effective preferences (including applied defaults).
  - Optionally displays audit trail of preference changes (user, timestamp, old/new values).
  - Visually distinct from underwriter/analyst-manager edit mode.
- **Test Coverage**:
  - Compliance reviewer loads preference page → all toggles disabled.
  - Audit history visible (if implemented in same page).
  - Save button absent or grayed out.
- **Source Reference**: product-spec-notification-preferences.md § User Roles § Compliance Reviewer, SC-2 (audit trail); non-functional-requirements.md § NFR-7.

---

### Phase 4: Testing and Validation

#### Task 4.1: Unit Tests for Notification Channel Rules
- **Description**: Write comprehensive tests in `src/backend/tests/unit/notification-channel-rules.test.ts`.
- **Acceptance Criteria**:
  - Happy path tests: valid disables (non-mandatory events, multiple channels enabled).
  - Boundary tests: exactly one channel left enabled for mandatory event.
  - False positive tests: disabling one channel while another is enabled (not a violation).
  - Hard negative tests: disabling all channels (rejected), CA decline SMS (rejected).
  - Parameter-driven tests for all event/channel/loanState combinations.
- **Test Coverage**: ≥90% code coverage of canDisableChannel().
- **Source Reference**: product-spec-notification-preferences.md § FR-2 § pattern examples; .github/instructions/testing.instructions.md.

#### Task 4.2: Integration Tests for Preference Routes
- **Description**: Write integration tests in `src/backend/tests/integration/` for preference endpoints.
- **Acceptance Criteria**:
  - Test GET /api/notifications/preferences/:userId (default generation, saved prefs, permission checks).
  - Test PUT /api/notifications/preferences (validation, audit, feature-flag gating, delegated-session blocking).
  - Test degraded-mode scenarios (audit unavailable, SMS fallback).
  - Test role permissions (underwriter/analyst-manager write, compliance-reviewer read-only).
  - Test 404 returns for non-pilot users.
- **Test Coverage**: All happy-path and error paths for each endpoint.
- **Source Reference**: non-functional-requirements.md § NFR-6, NFR-2; product-spec-notification-preferences.md § FR-1–FR-6.

#### Task 4.3: Frontend Integration Tests
- **Description**: Write UI tests for preference component (Vitest + user-event or similar).
- **Acceptance Criteria**:
  - User can toggle preferences and see optimistic updates.
  - Save succeeds → toast, state persisted.
  - Save fails (4xx) → toast, state rolled back.
  - Delegated session mode: UI shows indicator, toggles disabled.
  - Mandatory event rule enforced in UI (prevent save if all channels off).
  - CA restriction: SMS toggle disabled with explanation visible.
  - Keyboard navigation and ARIA labels validated.
- **Test Coverage**: All user workflows and error states.
- **Source Reference**: ADR-003, product-spec-notification-preferences.md § UX Notes, § SC-2.

#### Task 4.4: Performance and Load Testing
- **Description**: Verify preference endpoints meet NFR-1 latency budgets.
- **Acceptance Criteria**:
  - Settings page load (GET preferences + render) ≤150 ms p95 (measured without network latency).
  - Preference save (PUT + audit) ≤400 ms p95.
  - No N+1 queries in preference fetches.
  - Stress test: 100 concurrent saves → no degradation >20%.
- **Test Coverage**: Baseline against main branch; regression detection in CI/CD.
- **Source Reference**: non-functional-requirements.md § NFR-1.

#### Task 4.5: End-to-End Scenarios (Manual + Automated)
- **Description**: Document and execute end-to-end test scenarios covering all hard negatives and false positives.
- **Acceptance Criteria**:
  - **Hard Negative 1**: Attempt to disable all channels for manual-review-escalation → fails with 400, preference unchanged.
  - **Hard Negative 2**: Enable decline SMS on CA loan → fails with 400, preference unchanged.
  - **Hard Negative 3**: Attempt preference update in delegated session → fails with 403, no audit entry created.
  - **Hard Negative 4**: Audit service unavailable during save → 500, preference NOT persisted (fail-closed).
  - **Hard Negative 5**: UI optimistically updates toggle, server rejects → toast and rollback visible.
  - **False Positive 1**: SMS provider outage, user receives email instead → logs show fallback, prefs unchanged, not a bug.
  - **False Positive 2**: New user gets role defaults on first access → expected, no migration bug.
  - **False Positive 3**: Disable SMS while email enabled → allowed (≥1 channel rule satisfied).
  - **False Positive 4**: Read preferences during audit outage → succeeds (only writes require audit).
- **Test Coverage**: All patterns documented with test data and expected outcomes.
- **Source Reference**: product-spec-notification-preferences.md § FR-2 § patterns, § SC-2, § Open Questions; non-functional-requirements.md § NFR-2 § patterns.

---

## Validation Steps

### Before Pilot Rollout

1. **Rule Validation**
   - [ ] canDisableChannel() correctly rejects all hard negatives (task 4.1).
   - [ ] Unit tests cover ≥90% of rule logic.
   - [ ] CA LEGAL-218 restriction verified with legal team.

2. **API Contract Validation**
   - [ ] Audit entry schema matches AuditRequestedEvent contract (queue/contracts.ts).
   - [ ] Preference endpoint responses match frontend API client types.
   - [ ] 404 responses for non-pilot users confirmed (no 403 leakage).

3. **Audit Safety**
   - [ ] Audit writes tested under simulated provider outage (fail-closed verified).
   - [ ] Audit entries retain 24-month history per NFR-7.
   - [ ] Phone numbers excluded from client logs (NFR-3 privacy check).

4. **Frontend State Safety**
   - [ ] Central store rollback tested on API rejection (optimistic update pattern, task 4.3).
   - [ ] Navigating away and back preserves correct state (no stale cache).
   - [ ] Delegated session mode toggle prevents writes at store and route level.

5. **Performance Baselines**
   - [ ] Settings page load ≤150 ms p95 (task 4.4).
   - [ ] Preference save ≤400 ms p95 (task 4.4).
   - [ ] No N+1 queries in preference endpoints.

6. **Observability Readiness**
   - [ ] Metrics dashboard created for preference.save.latency, preference.save.failure, audit.write.failure, notification.sms.fallback.
   - [ ] Alerting configured for audit.write.failure counter (NFR-5, NFR-7).
   - [ ] Log patterns validated (validation_error vs provider_error distinction, task 2.2).

7. **Compliance and Audit**
   - [ ] Audit trail shows actor, timestamp, previous/new values, delegated-for context (task 2.1).
   - [ ] Compliance reviewer read-only view implemented and tested (task 3.4).
   - [ ] 24-month retention policy documented in runbooks.

### Pilot Monitoring (First 2 Weeks)

1. **Metric Thresholds**
   - [ ] `preference.save.failure` <0.1% validation errors (normal user behavior).
   - [ ] `audit.write.failure` = 0 (fail-closed behavior active).
   - [ ] `notification.sms.fallback` within expected range (baseline depends on SMS provider SLA).
   - [ ] `preference.save.latency` p95 ≤400 ms (NFR-1).

2. **Issue Tracking**
   - [ ] No Sev2 incidents from suppressed mandatory escalation alerts.
   - [ ] No Sev2 incidents from preference UI/API errors.
   - [ ] Document and triage any false-positive patterns (task 4.5 scenarios should not generate tickets).

3. **User Feedback**
   - [ ] Pilot cohort confirms delegated-session indicator is visible (SC-2).
   - [ ] CA restriction explanation is understandable (FR-4 UX Notes).
   - [ ] Alert fatigue reduction tracking (product success metric: 30% reduction in document-request mute requests).

---

## Risks and Dependencies

### Technical Risks

| Risk                                    | Severity | Mitigation                                                   |
| --------------------------------------- | -------- | ------------------------------------------------------------ |
| **Audit Service Bottleneck** (NFR-2 fail-closed) | High     | Implement circuit breaker for audit queue; monitor `audit.write.failure` counter during load testing (task 4.4). If audit latency exceeds preference save budget, consider async fallback with retry. |
| **Central Store Desync** (ADR-003 compliance) | Medium   | Implement rollback test in task 4.3; validate store state persists correctly across navigation. Consider time-to-live (TTL) for cached prefs to catch server-side changes. |
| **SMS Fallback Silent Failure** (FR-5 false positive) | Medium   | Log every fallback attempt with user context; set up dashboard alerting if fallback rate exceeds provider SLA. Ensure support runbook references delivery logs, not prefs. |
| **Delegated Session Authorization Bypass** (SC-2 hard negative) | High     | Test delegated-session blocks at both route layer (task 1.3) and store layer (task 3.1); add audit entry validation to catch attempts. |
| **California LEGAL-218 Regulatory Compliance** (FR-4, LEGAL-218) | Critical | Coordinate with legal team before pilot rollout; document LEGAL-218 case number in code and audit trail. Update feature-flag documentation with compliance expiration date (when LEGAL-218 resolves). |

### Dependency Risks

| Dependency                               | Risk                                                         | Mitigation                                                   |
| ---------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **Audit Service Availability** (NFR-2) | Audit service downtime prevents preference saves (fail-closed). | Prioritize audit service redundancy; implement circuit breaker. Set up alerting for `audit.write.failure` spikes. |
| **SMS Provider SLA** (FR-5 degraded-mode) | SMS outages trigger fallback and email volume spike; email provider may throttle. | Monitor email queue depth; implement rate limiting if fallback rate exceeds thresholds. Set up playbook for cascading SMS+email failures. |
| **Feature-Flag Service** (NFR-6)      | Non-pilot users see 404 only if feature-flag service returns correct flag state. | Ensure feature-flag service is highly available; use cache with fallback to "feature disabled" (conservative). |
| **Database Performance** (NFR-1 latency) | Preference queries on large user tables may exceed 150 ms p95 budget. | Index on (user_id, event, channel) composite key; test preference-repository query plans at 1M+ user scale. |

### Schedule Dependencies

1. **Legal Review LEGAL-218 Completion**: California decline SMS restriction tied to external legal milestone. Plan CA restriction removal as separate rollout once LEGAL-218 resolves.
2. **Compliance Audit Retention Setup**: 24-month retention policy (NFR-7) requires database/archival infrastructure in place before pilot.
3. **Feature-Flag Rollout Coordination**: Pilot cohort selection and flag deployment must be coordinated across teams; allow 1 week lead time for infrastructure validation.

---

## Summary of Confirmed vs. Open vs. Inferred

| Aspect                                  | Status     | Details                                                         |
| --------------------------------------- | ---------- | --------------------------------------------------------------- |
| **Preference Matrix (FR-1)**            | Confirmed  | 4 events × 2 channels, per product spec.                        |
| **Mandatory Event Rule (FR-2)**         | Confirmed  | ≥1 channel for manual-review-escalation; hard negatives explicit. |
| **Role Defaults (FR-3)**                | Confirmed  | Underwriter/analyst-manager defaults table; lazy generation OK.  |
| **CA SMS Restriction (FR-4, LEGAL-218)** | Confirmed  | loan_state-based, explicit hard negative.                       |
| **SMS Fallback (FR-5)**                 | Confirmed  | No pref modification; false-positive pattern documented.        |
| **Audit Trail (FR-6)**                  | Confirmed  | Complete trail with actor, timestamp, previous/new values.     |
| **Delegated Session Blocking (SC-2)**   | Confirmed  | Read-only with visual indicator; hard negatives explicit.       |
| **Fail-Closed Audit (NFR-2)**           | Confirmed  | Saves must abort if audit unavailable; hard negative explicit. |
| **Compliance Reviewer Access (Open Q1)** | Open       | Same page or separate audit viewer? Decision affects UI routing. |
| **Portfolio Restriction Display (Open Q3)** | Open   | Banner or per-row indicators? Does not block core implementation. |
| **Validation Rule as Pure Function**    | Inferred   | Derived from AR2 (pure business rules) + FR-2 hard negatives.  |
| **Delegated Session Guard at Route**    | Inferred   | Derived from SC-2 + existing route pattern.                     |
| **Lazy Defaults (No Upfront Migration)** | Inferred   | Derived from FR-3 "no migration required" + route-level orchestration (AR3). |
| **Central Client Store (ADR-003)**      | Inferred   | Mandatory per ADR-003 for persisted cross-screen state.         |
| **Metric Distinction (Validation vs Provider)** | Inferred | Derived from NFR-5 observability + route error handling.       |

---

## Canonical Source Justification

**Primary Authority:** `specs/product-spec-notification-preferences.md`  
**Rationale:**
- Contains all functional requirements (FR-1 through FR-6), special conditions (SC-1 through SC-3), and role-based defaults.
- Explicitly documents hard negative patterns (FR-2 mandatory event, SC-2 delegated sessions) to prevent AI-safety mistakes.
- Explicitly documents false-positive patterns (FR-2, FR-5) to prevent over-constraint.
- Open questions are recorded with answers (e.g., Q2: loan-state vs borrower-state answered as loan-state).

**Secondary Authority:** `specs/non-functional-requirements.md`  
**Rationale:**
- Provides safety rails (fail-closed audit, 404 for non-pilot, accessibility, observability).
- Annotates hard negatives and false positives with AI-mistake warnings.
- Defines observability metrics and performance budgets (NFR-1, NFR-5).

**Tertiary Authority:** `docs/architecture.md` + `docs/adr/ADR-003-frontend-state.md`  
**Rationale:**
- Confirms system shape, rule placement (rules/), and route orchestration (AR3).
- Mandates central client store for persisted preferences (ADR-003).
- Specifies that feature-flagged endpoints return 404 (not 403) per architectural security best practice.

**Implementation Patterns:**
- Existing `src/backend/src/rules/business-rules.ts` and `role-permissions.ts` define the pattern for business rule modules.
- Existing `src/backend/src/routes/notifications.ts` (already partially implemented) shows route-layer delegation blocking and audit calls.
- Existing `src/backend/src/config/feature-flags.ts` and `audit-service.ts` show feature-flag and audit integration patterns.

---

## Glossary

- **LEGAL-218**: Legal review tracking regulatory compliance for decline SMS in California; temporary restriction applies to loans with `loanState = "CA"`.
- **Fail-Closed**: When audit service unavailable, the preference save operation must fail (return 500, no partial state persisted) rather than silently skip audit logging.
- **Delegated Session**: An analyst manager operating on behalf of another user via `x-delegated-for` header; all write operations blocked.
- **Hard Negative**: An incorrect behavior that an AI assistant is likely to generate without explicit spec warning (e.g., allowing all channels to be disabled, or returning 403 instead of 404 for feature-gated endpoints).
- **False Positive**: Correct behavior that might be mistaken for a bug without spec guidance (e.g., SMS fallback to email during outage, or role defaults without migration).
- **Central Client Store**: A single source of truth for application state on the frontend (e.g., Zustand, Redux) that persists across page navigation and refresh, required by ADR-003.
- **Optimistic Update**: UI update that assumes API success, followed by rollback if API rejects the change (required for user experience but must include rollback logic per ADR-003).

---

## Appendix: Feature Flag Readiness Checklist

Before enabling `notificationPreferences` flag for pilot:

- [ ] Feature flag added to config/feature-flags.ts with documentation.
- [ ] All preference routes wrapped with flag check (404 for non-pilot).
- [ ] Audit service fail-closed testing completed (task 4.2).
- [ ] Performance baselines established (task 4.4).
- [ ] Central store rollback tested (task 4.3).
- [ ] Delegated-session authorization verified at route and store layers (task 4.1, 3.1).
- [ ] CA LEGAL-218 restriction confirmed with legal team.
- [ ] Observability dashboard and alerting set up (task 2.2).
- [ ] Runbooks created for SMS fallback and audit failures.
- [ ] Pilot cohort size and timeline agreed with product/leadership.
- [ ] Release notes prepared (feature description, SC-1/SC-2 limitations, delegated-session caveat).

