IMPLEMENTATION VERIFICATION CHECKLIST
=====================================

✅ REQUIREMENT: Test-first approach
   - Tests written in src/backend/tests/unit/notification-preference-write-rules.test.ts before rule implementation
   - 40+ test cases covering happy path, boundaries, hard negatives, false positives
   - Uses vitest describe/it pattern consistent with existing tests

✅ REQUIREMENT: Pure rule module with explicit inputs
   - Module: src/backend/src/rules/notification-preference-write-rules.ts
   - No database access (no prefRepo, loanRepo imports)
   - No side effects (no HTTP responses, no audit writes)
   - Accepts explicit parameters: event, channel, enabled, loanState, nextPreference, existingPreferences
   - Returns structured result: PreferenceWriteRule with allowed: boolean and reason: string

✅ REQUIREMENT: Hardening the notification-preference write path
   - Target route: PUT /api/notifications/preferences (single preference writes)
   - Modified notifications.ts to call canWriteNotificationPreference() before persisting
   - Returns 422 Unprocessable Entity on validation failure
   - Preserves existing delegated-session check (line 62-66)
   - Preserves existing role permission check (line 70-75)

✅ REQUIREMENT: Mandatory event rule - manual-review-escalation
   - Rule prevents disabling all channels for manual-review-escalation
   - Tracks existing preferences and applies new write to determine future state
   - Returns clear rejection reason mentioning "manual-review-escalation" and "at least one channel"
   - Allows mixed states (SMS disabled, email enabled or vice versa)

✅ REQUIREMENT: LEGAL-218 California decline SMS restriction
   - Rule checks event === "decline" && channel === "sms" && enabled && isCaliforniaLoan
   - Supports both "CA" and "California" loanState values
   - Reason includes "LEGAL-218" identifier in error message
   - False positive: Other events (approval, escalation) SMS is allowed on CA loans

✅ REQUIREMENT: loanState as direct request input
   - Added loanState to required fields in PUT request body validation (line 55)
   - No loan repository lookups; no loanId parameter
   - Passed directly from request body to rule function (line 88)

✅ REQUIREMENT: False-positive pattern documented and tested
   - Module comment (lines 17-20) explains false positive: disabling escalation SMS with email enabled is allowed
   - Test case at line 90-108: "allows disabling escalation SMS when escalation email is enabled"
   - Test case at line 109-128: "allows disabling escalation email when escalation SMS is enabled"
   - Must remain allowed - tests verify this behavior

✅ REQUIREMENT: Hard-negative pattern documented and tested
   - Module comment (lines 22-25) explains hard negative: all escalation channels disabled
   - Test case at line 145-165: "rejects bulk SMS disable when disabling last escalation channel"
   - Test case at line 167-190: "rejects both escalation channels ending up disabled"
   - Must be rejected - tests verify this behavior

✅ REQUIREMENT: Top-of-module false-positive and hard-negative comments
   - Located in notification-preference-write-rules.ts lines 17-25
   - FALSE POSITIVE section: Explains SMS disable with email enabled is NOT a violation
   - HARD NEGATIVE section: Explains all channels disabled IS a violation

✅ REQUIREMENT: Preserve delegated-session and role guards
   - Delegated session check: lines 62-66 (unchanged from original)
   - Role permission check: lines 70-75 (unchanged from original)
   - Same guards as original route; only added business rule validation before persistence

✅ REQUIREMENT: Minimal route changes
   - Import added (line 20): 1 line
   - Validation extended (line 55): 1 field added to existing validateBody
   - Validation logic inserted (lines 82-98): 17 lines
   - Total: ~20 lines added; no deletion of existing logic; full preservation of guards

✅ REQUIREMENT: Current notification write path discovery
   - Identified 3 write surfaces:
     1. PUT /api/notifications/preferences (HARDENED - in scope)
     2. PUT /api/notifications/preferences/:userId/email (unmodified - out of scope)
     3. PUT /api/notifications/preferences/:userId/sms (unmodified - out of scope)
   - Documented scope boundary in HANDOFF.md § Intentionally Deferred Write Surfaces

✅ REQUIREMENT: Explicit scope boundary in handoff
   - HANDOFF.md lists deferred surfaces:
     • Bulk email toggle endpoint
     • Bulk SMS toggle endpoint
     • Feature flag gating (NFR-6)
     • Audit failure hardening (NFR-2)
     • SMS fallback degradation (FR-5)
     • Role-based default generation (FR-3)

✅ REQUIREMENT: No protected config/database files edited
   - No changes to: feature-flags.ts, schema files, seed data, migrations
   - No changes to: env config, database connection
   - All changes in src/backend/src/rules/, src/backend/src/routes/, src/backend/tests/

✅ REQUIREMENT: No npm install, npm test, vitest, or shell commands
   - Zero shell command executions
   - Zero npm operations
   - File inspection and editing only

✅ REQUIREMENT: No SQL or task/todo write tools
   - No SQL queries executed
   - No task/todo state tracking used
   - Memory and file creation only

✅ REQUIREMENT: Handoff explains test expectations
   - HANDOFF.md § Test Behavior Summary explains:
     - Tests that FAIL before production change
     - Tests that PASS after production change
     - Which assertions prove which behaviors

✅ REQUIREMENT: Aligned with playbook and example doc
   - Playbook (docs/implementation-playbook.md) § Coding Conventions § Business Rules - followed
   - Example (docs/implementation-workflow-example.md) § Expected Change Shape - matched
   - Use of pure rule module, unit test file, minimal route wiring, preserved guards

✅ REQUIREMENT: Uses existing domain types
   - Imports from models/types.ts: NotificationEvent, NotificationChannel, NotificationPreference, SessionContext
   - No new types created (except PreferenceWriteRule and PreferenceWriteInput for rule contract)
   - Consistent with existing codebase patterns

FILES CREATED:
- src/backend/tests/unit/notification-preference-write-rules.test.ts (NEW)
- src/backend/src/rules/notification-preference-write-rules.ts (NEW)
- HANDOFF.md (NEW - documentation)

FILES MODIFIED:
- src/backend/src/routes/notifications.ts
  - Line 20: Import statement added
  - Line 55: loanState validation field added
  - Lines 77-98: Rule validation logic added

ALL REQUIREMENTS SATISFIED ✅
