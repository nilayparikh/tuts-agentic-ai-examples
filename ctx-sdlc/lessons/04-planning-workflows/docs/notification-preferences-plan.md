# Notification Preferences Implementation Plan

## 1. Summary

Implement notification preferences as a pilot-gated, source-of-truth-backed feature spanning backend rules/services/routes, frontend state/UI, audit, and observability. The feature must let authorized users manage email/SMS per event type while preserving mandatory escalation delivery, delegated-session read-only behavior, California decline SMS restrictions (`LEGAL-218`), degraded-mode delivery fallback, and fail-closed audit semantics. Relevant architecture surfaces already exist in `src/backend/src/routes/notifications.ts`, `src/backend/src/services/audit-service.ts`, `src/backend/src/queue/handlers/*.ts`, `src/frontend/src/pages/preferences.ts`, and `src/frontend/src/components/notification-toggle.ts` (see `docs/architecture.md:10-32`, `src/backend/src/routes/notifications.ts:33-271`, `src/frontend/src/pages/preferences.ts:10-39`).

### Canonical source hierarchy for this plan

1. **Product spec + NFRs are canonical for feature behavior and quality bars** because this lesson explicitly asks for planning against those sources, and the product spec is the only source with FR/SC identifiers (`docs/planning-workflow-example.md:31-39`, `specs/product-spec-notification-preferences.md:66-193`, `specs/non-functional-requirements.md:9-110`).
2. **ADR-003 is canonical for frontend state ownership and optimistic-save behavior** (`docs/adr/ADR-003-frontend-state.md:14-31`).
3. **Architecture doc is canonical for affected layers and breaking-change surfaces** such as rules/services/routes/queue contracts and pilot-gated rollout expectations (`docs/architecture.md:39-58`).
4. **Existing source is canonical only for the current baseline**, not for desired behavior when it conflicts with the spec/NFRs. Example conflicts:
   - The current audit path is asynchronous or best-effort and does **not** fail closed (`src/backend/src/services/audit-service.ts:18-45`, `src/backend/src/queue/handlers/audit-handler.ts:8-13`, `src/backend/src/middleware/audit-logger.ts:59-64`) but NFR-2 requires writes to abort if audit is unavailable (`specs/non-functional-requirements.md:23-34`).
   - The bug report title says "manual-review escalation SMS toggle" but the body and FR-4 both describe **decline SMS** as the California-restricted case; this plan treats FR-4 and the bug body/expected behavior as canonical (`specs/bug-report.md:5-6`, `specs/bug-report.md:14-26`, `specs/product-spec-notification-preferences.md:105-119`).

## 2. Source-backed confirmed requirements

| ID | Confirmed requirement | Key sources | Current implementation impact |
| --- | --- | --- | --- |
| FR-1 | Support email and SMS preferences for `approval`, `decline`, `document-request`, and `manual-review-escalation`, persisted across sessions/devices. | `specs/product-spec-notification-preferences.md:68-79`, `:30-35`; `specs/feature-request.md:7-10` | Current repository and routes already model these events/channels, but the UI is a flat toggle list rather than a governed preference matrix (`src/backend/src/models/types.ts:37-45`, `src/backend/src/models/preference-repository.ts:31-77`, `src/frontend/src/pages/preferences.ts:19-36`). |
| FR-2 | Manual-review escalation is mandatory: users may change the secondary channel, but at least one channel must remain enabled; UI and API must both enforce this. | `specs/product-spec-notification-preferences.md:81-92` | No current route/rule enforcement exists in `notifications.ts`; current PUT handlers can disable all SMS or all email values blindly (`src/backend/src/routes/notifications.ts:45-271`). Mandatory notification emission already exists for workflow transitions and must remain compatible (`src/backend/src/rules/mandatory-events.ts:17-37`, `src/backend/src/services/loan-service.ts:100-117`). |
| FR-3 | Defaults are role-based and generated on first access without a backfill migration. | `specs/product-spec-notification-preferences.md:94-104`; `specs/non-functional-requirements.md:86-97` | Current preferences page just shows empty state when no rows exist; no effective-default synthesis is present (`src/frontend/src/pages/preferences.ts:29-31`, `src/backend/src/models/preference-repository.ts:31-45`). |
| FR-4 / LEGAL-218 | Decline SMS must remain disabled for California loans; rule keys off `loanState`, not borrower address; mixed portfolio context must explain conditional restrictions rather than blanket-disable all SMS. | `specs/product-spec-notification-preferences.md:105-119`, `:166-170`; `specs/feature-request.md:21-25`; `specs/bug-report.md:22-24`, `:42-45` | Current notification preference API does not accept or validate loan context; current UI has no restriction messaging (`src/backend/src/routes/notifications.ts:49-54`, `:75-100`; `src/frontend/src/components/notification-toggle.ts:15-41`). |
| FR-5 | When SMS provider is unavailable, delivery may fall back to email if email is enabled; stored preferences must not change; fallback must emit a separate metric. | `specs/product-spec-notification-preferences.md:120-130`; `specs/feature-request.md:23-24`; `specs/non-functional-requirements.md:65-74` | Runtime fallback behavior exists in the notification handler, but no metrics surface exists yet (`src/backend/src/queue/handlers/notification-handler.ts:7-12`, `:62-76`). |
| FR-6 | Every preference change must audit actor, timestamp, previous value, new value, source channel, and delegated-for user when applicable. | `specs/product-spec-notification-preferences.md:132-142` | Current route-level audit includes actor/delegatedFor/previous/new/source but timestamp is implicit inside the repository, and writes are not fail-closed (`src/backend/src/services/audit-service.ts:18-45`, `src/backend/src/models/audit-repository.ts:26-61`). |
| SC-1 | In `finalized` state, global preferences can still change, but the UI must explain that already queued notifications for that application are unaffected. | `specs/product-spec-notification-preferences.md:147-152` | Current page has no application-context messaging. Source state names include `finalized`, which aligns with this special condition (`src/backend/src/models/types.ts:10-17`). |
| SC-2 | Delegated sessions may view the delegate's preferences but may not modify them; the UI must indicate delegated mode; audit must record actor and delegated-for; optimistic UI must not show success on rejected delegated writes. | `specs/product-spec-notification-preferences.md:153-165`; `specs/bug-report.md:20-27`, `:47-64`; `docs/adr/ADR-003-frontend-state.md:24-31` | Backend session context already captures `delegatedFor`, and current write routes block delegated writes, but GET scoping and frontend delegated indicators/rollback behavior are incomplete (`src/backend/src/middleware/auth.ts:61-75`, `src/backend/src/routes/notifications.ts:59-65`, `:123-129`, `:206-212`, `src/frontend/src/components/notification-toggle.ts:29-41`). |
| SC-3 | Mixed-portfolio restrictions must be presented as conditional rules rather than blanket disabling controls. | `specs/product-spec-notification-preferences.md:166-170` | No current portfolio-aware UI or API metadata exists (`src/frontend/src/pages/preferences.ts:19-36`, `src/frontend/src/api/client.ts:83-97`). |
| ADR-003 | Persisted preferences belong in the central client store, not component-local state; optimistic updates require store rollback on server rejection. | `docs/adr/ADR-003-frontend-state.md:14-31`, `:33-37`; `specs/product-spec-notification-preferences.md:179-180` | Current UI uses local DOM state per checkbox and direct API calls, not a central store (`src/frontend/src/components/notification-toggle.ts:18-44`). |
| NFR-2 | Reads must tolerate provider degradation, but preference writes must **fail closed** if audit logging is unavailable. | `specs/non-functional-requirements.md:21-34` | Current audit middleware and queue handler tolerate failures instead of rejecting writes, which is explicitly non-compliant (`src/backend/src/middleware/audit-logger.ts:37-65`, `src/backend/src/queue/handlers/audit-handler.ts:8-13`, `:23-52`). |
| NFR-3 | Only authenticated internal users may access preferences; delegated sessions must be explicit in audit logs; sensitive SMS destination data must stay out of logs/analytics. | `specs/non-functional-requirements.md:38-47` | Auth exists and delegated context is propagated, but the plan should keep logs/analytics limited to preference state and identifiers, not phone data (`src/backend/src/middleware/auth.ts:38-75`, `src/backend/src/models/types.ts:51-57`). |
| NFR-4 | Controls must be keyboard-reachable and screen-reader labeled; disabled mandatory/legal controls need persistent text; save status needs ARIA live announcement. | `specs/non-functional-requirements.md:50-60`; `specs/product-spec-notification-preferences.md:176-180` | Current checkbox UI lacks helper text, group semantics, and save-status announcements (`src/frontend/src/components/notification-toggle.ts:18-26`, `src/frontend/src/pages/preferences.ts:19-38`). |
| NFR-5 | Emit metrics for read/save failures, audit write failures, fallback invocations, and save latency; distinguish validation failures from downstream failures. | `specs/non-functional-requirements.md:63-80` | No metrics implementation is present in the current source (`src/backend/src`, search results for metrics were empty). |
| NFR-6 | Ship behind a release flag; non-pilot users must get 404, not 403; defaults on first access are expected and not a data bug. | `specs/non-functional-requirements.md:84-97`; `docs/architecture.md:43-47` | Existing feature flags do not include a notification-preferences pilot flag, and current routes are always mounted (`src/backend/src/config/feature-flags.ts:16-25`, `src/backend/src/app.ts:52-57`). |
| NFR-7 | Retain audit records for 24 months; mandatory escalation delivery rules must be testable and documented; compliance review must show effective preference state including defaults. | `specs/non-functional-requirements.md:101-110` | Audit repository is append-only, which aligns with retention expectations, but the effective-default/read-only reviewer view still needs design and implementation (`src/backend/src/models/audit-repository.ts:1-9`, `src/backend/src/routes/audit.ts:17-34`). |

## 3. Open questions with file references

1. **Should compliance reviewers access audit history from the same settings page or a separate audit viewer?** The product spec leaves this open, while the codebase already has a separate audit route that could be linked instead of embedded.  
   Sources: `specs/product-spec-notification-preferences.md:187-193`, `src/backend/src/routes/audit.ts:17-34`.

2. **Should mixed-portfolio restrictions render as a summary banner, per-row indicators, or both?** The product spec explicitly asks this, and the current frontend has no portfolio-aware model yet.  
   Sources: `specs/product-spec-notification-preferences.md:166-170`, `:187-193`, `src/frontend/src/pages/preferences.ts:19-36`.

3. **What is the authoritative read-scope rule for non-delegated underwriters and analyst managers?** The product spec clearly defines self-edit and delegated inspection, but the current GET endpoint accepts any `userId` for any allowed role.  
   Sources: `specs/product-spec-notification-preferences.md:48-62`, `:153-160`, `src/backend/src/routes/notifications.ts:33-43`.

4. **How should loan context reach the preference API for FR-4/SC-3 validation?** The current save payload contains only `userId`, `event`, `channel`, and `enabled`, yet the California rule depends on `loanState`, and the bug report already calls out this gap as a likely root cause.  
   Sources: `src/backend/src/routes/notifications.ts:49-54`, `:75-100`, `src/frontend/src/api/client.ts:87-97`, `specs/bug-report.md:49-56`, `:60-63`.

5. **How should fail-closed auditability work when `queueAudit` is enabled?** The NFR requires rejecting the save before success is reported, but the current queue model emits after persistence and does not roll the write back on handler failure.  
   Sources: `specs/non-functional-requirements.md:23-34`, `src/backend/src/services/audit-service.ts:34-45`, `src/backend/src/queue/handlers/audit-handler.ts:8-13`.

## 4. Inferred implementation choices (not confirmed requirements)

These are recommended plan assumptions based on source structure and architecture rules, but they are **not** directly mandated by the specs.

1. **Add a dedicated pilot flag for notification preferences** instead of overloading unrelated flags like `smsFallback` or `californiaRules`, because NFR-6 requires release gating and the current feature-flag surface does not model it (`specs/non-functional-requirements.md:84-95`, `src/backend/src/config/feature-flags.ts:16-25`).

2. **Move preference validation into a dedicated rules/service layer** so routes remain orchestration-only, matching the architecture rule that business rules live under `src/backend/src/rules/` and services handle orchestration/I/O (`docs/architecture.md:22-25`, `specs/feature-request.md:31-34`).

3. **Return an "effective preferences" response model** that includes synthesized defaults, disabled reasons, mandatory-event metadata, delegated-session mode, and contextual restriction explanations. This best fits FR-3, FR-4, SC-2, SC-3, and NFR-4 without forcing the frontend to reconstruct business rules (`specs/product-spec-notification-preferences.md:94-119`, `:153-180`).

4. **Use a central client store for the preference matrix and save lifecycle** rather than direct DOM mutation, to comply with ADR-003 and support rollback, ARIA status, and contextual banners (`docs/adr/ADR-003-frontend-state.md:16-31`, `src/frontend/src/components/notification-toggle.ts:18-44`).

5. **Prefer a transactional or preflight audit-write strategy for preference saves** so the main write cannot succeed unless auditability is guaranteed. This is the clearest way to satisfy NFR-2 given the current asynchronous audit path. (`specs/non-functional-requirements.md:23-34`, `src/backend/src/services/audit-service.ts:18-45`).

## 5. Constraints and special conditions

- **Delegated sessions are read-only for writes**: delegated users may inspect but not save another user's preferences, and the UI must make that mode obvious (`specs/product-spec-notification-preferences.md:153-160`, `src/backend/src/middleware/auth.ts:63-72`).

- **`LEGAL-218` applies to California decline SMS, not manual-review escalation SMS**: use `loanState` as the jurisdiction source, show persistent explanation text, and present multi-state restrictions conditionally rather than globally (`specs/product-spec-notification-preferences.md:105-119`, `:166-170`).

- **Mandatory-event delivery must stay intact**: manual-review escalation may not be reduced to zero channels, and existing workflow-triggered mandatory-event emission in `loan-service.ts` / `mandatory-events.ts` must continue to produce deliverable events (`specs/product-spec-notification-preferences.md:81-92`, `src/backend/src/rules/mandatory-events.ts:17-37`, `src/backend/src/services/loan-service.ts:100-117`).

- **Audit must fail closed for writes**: do not treat audit as fire-and-forget for preference saves. A read succeeding during audit trouble is a **false positive** and not a bug; a successful-looking write without an audit trail is a **hard negative** and a real bug (`specs/non-functional-requirements.md:23-34`).

- **Degraded-mode fallback is runtime delivery logic, not preference mutation**: receiving email during SMS outage is a **false positive** for "bad preferences" if stored SMS is still enabled; metrics must capture fallback separately (`specs/product-spec-notification-preferences.md:120-130`, `src/backend/src/queue/handlers/notification-handler.ts:62-76`).

- **Pilot gating must hide the feature with 404 for non-pilot users**: returning 403 would leak feature existence and is a **hard negative** against NFR-6 (`specs/non-functional-requirements.md:84-95`).

- **Accessibility constraints are explicit**: disabled controls need persistent helper text, not just a tooltip, and save outcomes need ARIA live messaging (`specs/non-functional-requirements.md:50-60`, `specs/product-spec-notification-preferences.md:176-180`).

- **Queued-notification caveat for finalized applications**: preference changes remain global, but the UI must say they do not affect notifications already queued for that finalized application (`specs/product-spec-notification-preferences.md:147-152`).

## 6. Numbered tasks with acceptance criteria and source references

1. **Define and gate the feature entry points**
   - Scope: introduce a notification-preferences pilot flag, guard backend endpoints and frontend navigation/page loading, and return 404 for non-pilot users.
   - Acceptance criteria:
     - Non-pilot users receive 404, not 403, for notification-preference routes/pages.
     - Pilot users see the feature without changing unrelated app behavior.
     - Rollout notes include observability and fallback expectations.
   - Sources: NFR-6 (`specs/non-functional-requirements.md:84-97`), architecture rule on pilot-gated features (`docs/architecture.md:43-47`), current flag surface (`src/backend/src/config/feature-flags.ts:16-25`).

2. **Introduce backend preference-domain logic for effective defaults and validation**
   - Scope: add/centralize rules for role-based defaults, mandatory-event zero-channel protection, California decline SMS restriction, delegated-session/owner checks, and compliance reviewer read-only semantics.
   - Acceptance criteria:
     - First access returns effective defaults without requiring seeded rows or migration.
     - Disabling both channels for `manual-review-escalation` is rejected in both granular and bulk-save flows.
     - Decline SMS rejects for California context with an explicit reason tied to `loanState`.
     - Delegated sessions and compliance reviewers cannot write preferences.
   - Sources: FR-2/3/4 (`specs/product-spec-notification-preferences.md:81-119`), SC-2 (`:153-165`), NFR-6 (`specs/non-functional-requirements.md:86-97`), current route gaps (`src/backend/src/routes/notifications.ts:45-271`).

3. **Refactor notification preference API routes/services around the rules layer**
   - Scope: keep routes thin, return effective preferences plus disabled/helper metadata, and ensure GET/PUT semantics reflect the agreed read/write scope.
   - Acceptance criteria:
     - GET returns effective preference state, including defaults and restriction explanations.
     - PUT rejects invalid saves before persistence and returns enough structured error information for UI rollback.
     - API surfaces identify delegated-session mode and restriction reasons without exposing sensitive phone data.
   - Sources: architecture layering (`docs/architecture.md:22-25`, `:53-58`), ADR-003 (`docs/adr/ADR-003-frontend-state.md:24-31`), NFR-3 (`specs/non-functional-requirements.md:38-47`), current route/client shape (`src/backend/src/routes/notifications.ts:33-271`, `src/frontend/src/api/client.ts:83-97`).

4. **Make preference saves fail closed on auditability**
   - Scope: redesign preference-save flow so audit failure prevents a successful mutation response; ensure audit entries capture actor, delegated-for, previous/new values, source, and timestamp.
   - Acceptance criteria:
     - A preference save cannot return success if the audit path is unavailable.
     - Audit records contain actor, delegated-for, previous/new values, source, and timestamp for every successful save.
     - Validation failures remain 4xx and audit/provider failures are distinguishable for logging/metrics.
   - Sources: FR-6 (`specs/product-spec-notification-preferences.md:132-142`), NFR-2/NFR-5/NFR-7 (`specs/non-functional-requirements.md:21-34`, `:63-80`, `:101-107`), current conflicting audit path (`src/backend/src/services/audit-service.ts:18-45`, `src/backend/src/queue/handlers/audit-handler.ts:8-13`, `src/backend/src/middleware/audit-logger.ts:37-65`).

5. **Preserve mandatory-event delivery and degraded-mode fallback behavior**
   - Scope: ensure preference validation and delivery logic work together so mandatory escalation remains deliverable and SMS outages fall back to email without rewriting stored preferences.
   - Acceptance criteria:
     - Workflow transitions that require `manual-review-escalation` continue to emit the event.
     - Preference state never mutates because of runtime SMS fallback.
     - Fallback invocations emit a dedicated metric and are distinguishable from preference-save errors.
   - Sources: FR-2/FR-5 (`specs/product-spec-notification-preferences.md:81-92`, `:120-130`), NFR-5 (`specs/non-functional-requirements.md:63-80`), current mandatory/fallback surfaces (`src/backend/src/rules/mandatory-events.ts:17-37`, `src/backend/src/services/loan-service.ts:100-117`, `src/backend/src/queue/handlers/notification-handler.ts:33-77`).

6. **Rebuild the frontend preferences experience around central state and explicit UX constraints**
   - Scope: replace direct-toggle local mutation with a store-backed matrix page that supports optimistic rollback, delegated banners, persistent helper text, finalized-state messaging, and ARIA live announcements.
   - Acceptance criteria:
     - Persisted preference state lives in the central client store, not component-local state.
     - Delegated mode is visually obvious and save actions are disabled or blocked before request.
     - Mandatory/legal restriction explanations are persistently visible.
     - Save success/failure is announced accessibly, and optimistic changes roll back correctly on server rejection.
     - Finalized application context warns that queued notifications are unaffected.
   - Sources: ADR-003 (`docs/adr/ADR-003-frontend-state.md:16-31`), SC-1/SC-2/SC-3 (`specs/product-spec-notification-preferences.md:147-180`), NFR-4 (`specs/non-functional-requirements.md:50-60`), current simplistic UI (`src/frontend/src/pages/preferences.ts:10-39`, `src/frontend/src/components/notification-toggle.ts:18-44`).

7. **Add compliance/audit viewing behavior for effective preferences**
   - Scope: expose read-only effective preferences for compliance reviewers and resolve whether audit history is embedded or linked.
   - Acceptance criteria:
     - Compliance reviewers can inspect effective preferences including defaults but cannot modify operational settings.
     - The chosen audit-view pattern is documented and consistent with existing audit routes.
     - Audit retention assumptions remain compatible with the append-only repository.
   - Sources: product roles + open question (`specs/product-spec-notification-preferences.md:59-63`, `:187-193`), NFR-7 (`specs/non-functional-requirements.md:101-107`), current audit route/repository (`src/backend/src/routes/audit.ts:17-34`, `src/backend/src/models/audit-repository.ts:1-9`).

8. **Close the testing and observability gaps**
   - Scope: add backend/frontend tests and telemetry for validation, audit failure, rollout gating, delegated behavior, fallback, and accessibility.
   - Acceptance criteria:
     - Unit/integration coverage exists for all hard negatives and false positives listed below.
     - Metrics exist for read/save failure, audit write failure, fallback, and save latency.
     - Logs distinguish validation issues from downstream failures without leaking sensitive SMS destination data.
   - Sources: NFR-3/NFR-5 (`specs/non-functional-requirements.md:38-47`, `:63-80`), lesson expectations (`docs/planning-workflow-example.md:33-39`, `:55-60`), current sparse tests (`src/backend/tests/unit/notification-service.test.ts:10-15`, `src/backend/tests/integration/decisions.test.ts:7-14`).

## 7. Validation steps

1. **Defaults and first access**
   - Verify a pilot underwriter with no stored rows receives FR-3 defaults on first load without migration.
   - Confirm compliance reviewer sees effective read-only state, including defaults.  
   Sources: FR-3, NFR-6, NFR-7 (`specs/product-spec-notification-preferences.md:94-104`, `specs/non-functional-requirements.md:86-107`).

2. **Mandatory-event hard negative / false positive**
   - Hard negative: attempt to disable both channels for `manual-review-escalation`; API and UI must reject it.
   - False positive: disable only SMS while email remains enabled; this must succeed.  
   Sources: FR-2 (`specs/product-spec-notification-preferences.md:81-92`).

3. **Delegated-session hard negative**
   - In delegated mode, verify preferences are viewable but save is blocked and no success toast/state commit survives.
   - Confirm audit records include both actor and delegated-for for allowed reads/surfaced operations.  
   Sources: SC-2, ADR-003, bug report (`specs/product-spec-notification-preferences.md:153-165`, `docs/adr/ADR-003-frontend-state.md:24-31`, `specs/bug-report.md:20-27`).

4. **California restriction / LEGAL-218**
   - Hard negative: attempt to enable decline SMS for a California loan context; control must be disabled or save rejected with persistent explanation.
   - Confirm the rule keys off `loanState`, not borrower address.
   - In mixed-portfolio context, verify restrictions render conditionally rather than blanket-disabling all SMS.  
   Sources: FR-4, SC-3 (`specs/product-spec-notification-preferences.md:105-119`, `:166-170`).

5. **Fail-closed audit behavior**
   - Hard negative: simulate audit unavailability and confirm preference save fails without persisting the new preference.
   - False positive: reads should still succeed during the same outage.  
   Sources: NFR-2 (`specs/non-functional-requirements.md:21-34`).

6. **Degraded-mode fallback**
   - False positive: simulate SMS outage with email enabled and confirm delivery falls back to email without mutating stored preferences.
   - Verify `notification.sms.fallback` metric increments separately.  
   Sources: FR-5, NFR-5 (`specs/product-spec-notification-preferences.md:120-130`, `specs/non-functional-requirements.md:65-74`).

7. **Pilot gating**
   - Hard negative: a non-pilot user must see 404, not 403, for backend endpoints and the UI entry point.  
   Sources: NFR-6 (`specs/non-functional-requirements.md:86-95`).

8. **Accessibility and finalized-state messaging**
   - Validate keyboard navigation, screen-reader labels, persistent helper text, and ARIA live status updates.
   - In finalized context, confirm the UI warns that already queued notifications are unaffected.  
   Sources: SC-1, NFR-4 (`specs/product-spec-notification-preferences.md:147-180`, `specs/non-functional-requirements.md:50-60`).

## 8. Risks and dependencies

- **Audit architecture risk**: the current queue-based audit flow is fundamentally at odds with fail-closed preference saves. Resolving this may require a synchronous write path, a transactional outbox, or another design that guarantees auditability before success is returned (`src/backend/src/services/audit-service.ts:18-45`, `src/backend/src/queue/handlers/audit-handler.ts:8-13`).

- **Frontend state dependency**: the current preferences UI is not built on a central store, so ADR-003 compliance is a non-trivial refactor rather than a small toggle patch (`src/frontend/src/components/notification-toggle.ts:18-44`, `docs/adr/ADR-003-frontend-state.md:16-31`).

- **API contract dependency**: FR-4 and SC-3 need contextual restriction data, but current client/server payloads do not carry loan or portfolio context (`src/frontend/src/api/client.ts:83-97`, `src/backend/src/routes/notifications.ts:49-54`).

- **Telemetry gap**: NFR-5 calls for metrics, but no metrics layer appears in the current source. Implementation may need a new observability abstraction or integration point.

- **Read-scope ambiguity**: the desired read behavior for non-delegated internal roles is not fully specified and should be resolved before implementation to avoid shipping an over-broad read surface.

- **Bug-report wording conflict**: if the team uses the bug title instead of FR-4/body details, they could incorrectly apply `LEGAL-218` to manual-review escalation SMS instead of decline SMS. The plan should keep FR-4 as canonical.
