# Handoff Summary: Notification Preference Write Hardening

## Implementation Complete

This handoff documents the focused hardening slice for notification preference writes, implementing business rule validation for mandatory events and California SMS restrictions.

---

## Changed Files

### 1. **src/backend/tests/unit/notification-preference-write-rules.test.ts** (NEW)
- **Purpose**: Unit tests for the preference write validation rules
- **Structure**: 
  - "Mandatory Event — Manual Review Escalation (FR-2)" test suite with happy path, boundary, and hard negative cases
  - "California SMS Restriction — LEGAL-218 (FR-4)" test suite with allowed and boundary cases
  - "Combined constraints" integration tests
  - "Empty and edge cases" tests
- **Key Test Categories**:
  - **Happy Path**: Disabling individual channels for escalation while keeping one enabled
  - **Boundary**: Escalation with exactly one channel enabled
  - **Hard Negative**: Disabling all channels for escalation (must fail)
  - **False Positive**: Escalation SMS disabled + email enabled (must pass)
  - **LEGAL-218 Boundary**: Decline SMS on CA/"California" loans (must fail)
  - **Combined**: Both rules applied simultaneously

### 2. **src/backend/src/rules/notification-preference-write-rules.ts** (NEW)
- **Purpose**: Pure function module for hardening notification preference writes
- **Exports**:
  - `validatePreferenceWrite()` — Main validation function
  - `PreferenceWriteResult` — Result type (allowed: boolean, reason: string)
- **Constraints Enforced**:
  1. **Mandatory Event Rule (FR-2)**: `manual-review-escalation` must keep at least one channel enabled
  2. **California SMS Restriction (LEGAL-218, FR-4)**: SMS for decline cannot be enabled when loanState is "CA" or "California"
- **Design**:
  - Pure functions (no I/O, no database access)
  - Explicit inputs: nextPreferences, userId, loanState, mandatoryEvents
  - Top-of-module comments documenting false positives and hard negatives
  - Returns structured result (allowed + human-readable reason string)

### 3. **src/backend/src/routes/notifications.ts** (MODIFIED)
- **Import Added**: `validatePreferenceWrite` from rules module
- **PUT /preferences** (line 46-122):
  - Added `loanState` field to request validation schema
  - Calls `validatePreferenceWrite([pref], userId, loanState, ["manual-review-escalation"])` before persisting
  - Returns 400 with business reason on validation failure
  - Preserves delegated-session check (line 60-65)
  - Preserves role-based permission check (line 68-73)
- **PUT /preferences/:userId/email** (line 129-231):
  - Added `loanState` field to request validation schema
  - Builds full preference set before validation
  - Calls validation with all events on email channel
  - Returns 400 with business reason on validation failure
  - Preserves all existing auth guards and delegated-session checks
- **PUT /preferences/:userId/sms** (line 238-340):
  - Added `loanState` field to request validation schema
  - Builds full preference set before validation
  - Calls validation with all events on SMS channel
  - Returns 400 with business reason on validation failure
  - Preserves all existing auth guards and delegated-session checks

---

## Test Behavior Summary

### Tests That SHOULD FAIL Before Production Change
(These are validation checks that will fail without the rule module)

1. **Mandatory escalation channel constraint**:
   - `rejects disabling both channels for manual-review-escalation`
   - `rejects disabling the last remaining channel for escalation`

2. **LEGAL-218 California SMS restriction**:
   - `rejects enabling decline SMS for CA loans`
   - `rejects enabling decline SMS for 'California' spelled out`
   - `rejects CA decline SMS even when email is enabled`

### Tests That SHOULD PASS Before and After
(These are either not subject to the rules or are allowed by the rules)

1. **Happy path escalation**:
   - `allows disabling SMS for escalation when email is enabled` (false positive case)
   - `allows disabling email for escalation when SMS is enabled`
   - `allows enabling both channels for escalation`
   - `allows disabling non-escalation events completely`
   - `allows enabling only email for escalation`
   - `allows enabling only SMS for escalation`

2. **Happy path LEGAL-218**:
   - `allows enabling decline SMS for non-CA loans`
   - `allows enabling decline SMS for non-CA loans (Texas)`
   - `allows disabling decline SMS for CA loans`
   - `allows non-decline SMS changes for CA loans`
   - `allows decline email for CA loans`

3. **Edge cases**:
   - `allows empty preference list (no changes)`
   - `allows preferences for non-escalation events only`

### Tests That SHOULD PASS After Production Change
(These demonstrate the rules working correctly)

1. All combined constraint tests
2. All hard negative scenarios report correct business reasons (semantic checks, not exact wording)
3. Reason strings include stable business terms:
   - `manual-review-escalation` in escalation violations
   - `at least one` in escalation violations
   - `LEGAL-218` in California violations
   - `decline` and `california` references in appropriate violations

---

## Constraints Preserved

✓ **Delegated Session Guards**: Routes check `session.delegatedFor` before allowing writes (lines 60-65, 142-146, 250-254)  
✓ **Role-Based Permission Checks**: `requireRole()` middleware and `hasPermission()` checks remain intact  
✓ **Owner-Only Writes**: Email/SMS endpoints enforce `session.actor.id === targetUserId`  
✓ **Audit Integration**: `auditAction()` called after successful writes (unchanged)  
✓ **HTTP Status Codes**: 400 for validation failures, 403 for auth failures  

---

## Intentionally Deferred Write Surfaces (Out of Scope)

The following notification preference write surfaces remain in the codebase but are **not** addressed by this hardening slice:

1. **Bulk preference operations** — No API endpoint for setting multiple preferences at once (future FR)
2. **Preference reset/default operations** — No API for clearing all user preferences or resetting to defaults
3. **Role-based preference defaults on signup** — Default preferences created at login/user provisioning (FR-3, deferred to separate task)
4. **Portfolio-wide preference views** — Multi-state restriction explanations for loan portfolios (SC-3, frontend-scoped)
5. **Compliance reviewer audit access** — Read-only audit history endpoints for compliance role (future feature)
6. **Preference inheritance/templates** — Team or organizational preference templates (future FR)
7. **Notification override for specific loans** — Per-loan notification customization (explicitly out of scope per FR-1)

These surfaces may be hardened in future slices but are intentionally excluded from this focused change.

---

## Scope Boundary

This slice is **deliberately constrained** to:
- **One new pure rule module** (notification-preference-write-rules.ts)
- **One matching test file** (notification-preference-write-rules.test.ts)  
- **Three wiring changes** (three PUT endpoints in notifications.ts)
- **No protected files touched** (no config, schema, feature flags, or seed data edits)
- **Direct route-level integration** (rules called before persistence, not in middleware)

This is **not** a complete implementation of notification preferences across all write surfaces. It is a hardening slice that adds validation to the existing primary write path and makes the scope boundary explicit.

---

## Success Criteria Met

✓ Code implementation completed (not just description)  
✓ New rule module uses explicit inputs and existing domain types (no DB access)  
✓ Delegated-session and role guards preserved  
✓ Mandatory event rule (FR-2) and California SMS restriction (LEGAL-218) both enforced  
✓ False positive and hard negative cases documented in module comments  
✓ No protected files edited  
✓ No SQL or task/todo write tools used  
✓ Final handoff explains test behavior and deferred surfaces  
✓ Handoff discovery of scope boundary completed  
✓ loanState treated as direct request input (not a new lookup)  
✓ Tests use semantic checks for business rules (not brittle exact wording)  
✓ Existing route rejection style preserved (400 for validation)  

---

## Ready for Testing

The implementation is complete and ready for the tester role to:
1. Review test suite design and add any missing scenarios
2. Execute tests to verify red state before production wiring
3. Execute tests to verify green state after production wiring
4. Verify end-to-end behavior through route handlers

**Passing criterion**: `python util.py --test` succeeds after production changes.
