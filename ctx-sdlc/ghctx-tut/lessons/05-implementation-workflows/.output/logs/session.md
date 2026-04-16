# 🤖 Copilot CLI Session

> [!NOTE]
> - **Session ID:** `377dfefc-8ead-414c-bf9d-13331963e788`  
> - **Started:** 16/04/2026, 13:56:09  
> - **Duration:** 5m 58s  
> - **Exported:** 16/04/2026, 14:02:08  

---

<sub>⏱️ 7s</sub>

### 👤 User

Inspect docs/, specs/, and the relevant notification-preference write surfaces you discover in this lesson before editing. Use the playbook and example doc as success criteria, not as a fixed file checklist. Implement a focused notification-preference write hardening slice. Write tests first at src/backend/tests/unit/notification-preference-write-rules.test.ts, then add a pure rule module at src/backend/src/rules/notification-preference-write-rules.ts, and wire the minimal production changes into src/backend/src/routes/notifications.ts. In the final handoff, state which behaviors the tests should fail on before the production change and which should pass after it, and name any intentionally deferred write surfaces that remain out of scope. The rule must use explicit inputs plus existing types, not direct DB access. Enforce these cases: manual-review-escalation must keep at least one channel enabled; decline SMS cannot be enabled when loanState is CA or California under LEGAL-218; treat loanState as the direct request input for this route instead of introducing a new loanId lookup or any repository fetch; the false positive where escalation SMS is disabled but escalation email stays enabled must remain allowed. When tests assert business-rule rejections, prefer semantic checks over brittle exact wording, and preserve the current route rejection style when practical; if the route returns 400 or 422 for these rule violations, the payload must still clearly express the business invariant. Preserve delegated-session and role guards, keep changes minimal, keep the scope to the current notification write path, include top-of-module false-positive and hard-negative comments in the new rule file, and do not edit protected config or database files. Do not run npm install, npm test, npx vitest, or any shell commands. Do not use SQL or task/todo write tools. Inspect and edit files only. Return a short handoff summary naming changed files and which tests should pass.

---

<sub>⏱️ 20s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs

```
architecture.md
implementation-playbook.md
implementation-workflow-example.md
notification-preferences-plan.md
```


---

<sub>⏱️ 20s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\specs.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\specs

```
non-functional-requirements.md
product-spec-notification-preferences.md
```


---

<sub>⏱️ 20s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "notification-preference|notification preference|LEGAL-218|manual-review-escalation|decline",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\ghctx-tut\\lessons\\05-implementation-workflows\\docs",
  "output_mode": "content",
  "-n": true,
  "head_limit": 200
}
```

</details>

<details>
<summary>70 lines</summary>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:12:This plan outlines the implementation of user-configurable notification preferences for the Loan Workbench platform. The feature addresses alert fatigue by allowing underwriters and analyst managers to control which notifications they receive (approval, decline, document-request, manual-review-escalation) across email and SMS channels.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:15:- Mandatory notification events (manual-review-escalation) must always have at least one enabled channel.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:16:- California loans have a temporary SMS restriction for decline notifications (LEGAL-218).
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:22:**Canonical Source:** Product Specification (specs/product-spec-notification-preferences.md) is the primary authority. NFRs provide constraints and safety rails. Architecture and ADRs guide implementation pattern choices.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:32:| FR1 | Preference matrix: email/SMS independent per event type      | product-spec-notification-preferences.md § Functional Requirements § FR-1 |
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:33:| FR2 | Mandatory event rule: ≥1 channel for manual-review-escalation | product-spec-notification-preferences.md § FR-2 (explicit hard negative pattern) |
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:34:| FR3 | Role-based defaults on first access (no migration required)   | product-spec-notification-preferences.md § FR-3 § User-based defaults table |
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:35:| FR4 | California SMS restriction for decline (LEGAL-218)          | product-spec-notification-preferences.md § FR-4 (explicit: loan_state based) |
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:36:| FR5 | Degraded delivery fallback: SMS→email, no pref modification  | product-spec-notification-preferences.md § FR-5 (explicit false positive pattern) |
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:37:| FR6 | Audit all preference changes (actor, timestamp, old/new values) | product-spec-notification-preferences.md § FR-6 (complete audit trail) |
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:43:| SC-1 | Locked applications: prefs change globally, UI clarifies no retroactive effect | product-spec-notification-preferences.md § SC-1 |
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:44:| SC-2 | Delegated sessions: read-only (no modify), visually indicated | product-spec-notification-preferences.md § SC-2 (explicit hard negative pattern) |
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:45:| SC-3 | Multi-state portfolio: conditional rules, not blanket disable | product-spec-notification-preferences.md § SC-3 |
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:75:   - **Reference**: product-spec-notification-preferences.md § Open Questions #1
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:79:   - **Reference**: product-spec-notification-preferences.md § Open Questions #3
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:101:   - **Why**: Enables AI-safety testing for edge cases (e.g., CA decline SMS, zero-channel scenarios).
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:135:   - Users may not disable all channels for `manual-review-escalation`.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:138:   - **Source**: product-spec-notification-preferences.md § FR-2 § HARD NEGATIVE pattern.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:140:2. **California SMS Restriction (LEGAL-218)**  
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:141:   - SMS for `decline` notifications must remain unavailable when `loanState = "CA"`.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:144:   - **Source**: product-spec-notification-preferences.md § FR-4; non-functional-requirements.md § NFR-6.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:155:   - **Source**: product-spec-notification-preferences.md § SC-2 § HARD NEGATIVE pattern (optimistic UI update without server rejection).
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:168:   - **Source**: product-spec-notification-preferences.md § FR-5 § FALSE POSITIVE pattern.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:171:   - User disables SMS for `manual-review-escalation` while email is enabled.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:173:   - **Source**: product-spec-notification-preferences.md § FR-2 § FALSE POSITIVE pattern.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:197:  - Rejects SMS disable for decline on CA loans (if `loanState = "CA"` and `event = "decline"` and `channel = "sms"`).
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:203:  - Hard negative: disable SMS for decline on CA loan → rejected.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:204:  - Hard negative: disable SMS for decline on non-CA loan → allowed.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:205:- **Source Reference**: product-spec-notification-preferences.md § FR-2, FR-4; rules/business-rules.ts pattern.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:218:- **Source Reference**: product-spec-notification-preferences.md § FR-3; preference-repository.ts pattern.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:233:- **Source Reference**: product-spec-notification-preferences.md § FR-2, FR-6, SC-2; notifications.ts lines 45–105, 112–188, 195–271; NFR-2.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:247:- **Source Reference**: product-spec-notification-preferences.md § FR-5; non-functional-requirements.md § NFR-5.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:254:  - Wrap notification preference routes with flag check that returns 404 (not 403) for non-pilot users.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:276:- **Source Reference**: product-spec-notification-preferences.md § FR-6, SC-2; NFR-3 (privacy), NFR-2 (fail-closed); audit-repository.ts and audit-service.ts patterns.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:315:- **Source Reference**: ADR-003 (AR1); product-spec-notification-preferences.md § SC-2.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:320:  - Render matrix: rows = events (approval, decline, document-request, manual-review-escalation), columns = channels (email, sms).
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:322:  - Mandatory events (manual-review-escalation) have **persistent helper text** (not tooltip): "At least one channel must be enabled for escalation notifications."
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:323:  - CA decline SMS disabled control with explanation: "SMS for decline notifications is unavailable for California loans (legal review LEGAL-218 in progress)."
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:332:  - Attempting to toggle CA decline SMS → toggle stays disabled, tooltip/helper text shown.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:335:- **Source Reference**: product-spec-notification-preferences.md § FR-1 through FR-6, SC-1 through SC-3, UX Notes; NFR-4 (accessibility), NFR-6.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:362:- **Source Reference**: product-spec-notification-preferences.md § User Roles § Compliance Reviewer, SC-2 (audit trail); non-functional-requirements.md § NFR-7.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:374:  - Hard negative tests: disabling all channels (rejected), CA decline SMS (rejected).
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:377:- **Source Reference**: product-spec-notification-preferences.md § FR-2 § pattern examples; .github/instructions/testing.instructions.md.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:388:- **Source Reference**: non-functional-requirements.md § NFR-6, NFR-2; product-spec-notification-preferences.md § FR-1–FR-6.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:401:- **Source Reference**: ADR-003, product-spec-notification-preferences.md § UX Notes, § SC-2.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:416:  - **Hard Negative 1**: Attempt to disable all channels for manual-review-escalation → fails with 400, preference unchanged.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:417:  - **Hard Negative 2**: Enable decline SMS on CA loan → fails with 400, preference unchanged.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:426:- **Source Reference**: product-spec-notification-preferences.md § FR-2 § patterns, § SC-2, § Open Questions; non-functional-requirements.md § NFR-2 § patterns.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:437:   - [ ] CA LEGAL-218 restriction verified with legal team.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:499:| **California LEGAL-218 Regulatory Compliance** (FR-4, LEGAL-218) | Critical | Coordinate with legal team before pilot rollout; document LEGAL-218 case number in code and audit trail. Update feature-flag documentation with compliance expiration date (when LEGAL-218 resolves). |
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:512:1. **Legal Review LEGAL-218 Completion**: California decline SMS restriction tied to external legal milestone. Plan CA restriction removal as separate rollout once LEGAL-218 resolves.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:523:| **Mandatory Event Rule (FR-2)**         | Confirmed  | ≥1 channel for manual-review-escalation; hard negatives explicit. |
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:525:| **CA SMS Restriction (FR-4, LEGAL-218)** | Confirmed  | loan_state-based, explicit hard negative.                       |
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:542:**Primary Authority:** `specs/product-spec-notification-preferences.md`  
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:570:- **LEGAL-218**: Legal review tracking regulatory compliance for decline SMS in California; temporary restriction applies to loans with `loanState = "CA"`.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\notification-preferences-plan.md:590:- [ ] CA LEGAL-218 restriction confirmed with legal team.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\implementation-workflow-example.md:7:This lesson consumes `docs/notification-preferences-plan.md`, the structured
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\implementation-workflow-example.md:10:notification-preferences feature. Lesson 05 implements only **one focused slice**
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\implementation-workflow-example.md:11:of that plan — hardening the notification-preference write path.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\implementation-workflow-example.md:15:Show that a constrained implementation workflow can make a focused production change with matching tests instead of attempting the entire notification-preferences feature at once.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\implementation-workflow-example.md:31:4. The implementation must cover a mandatory-event rule and the California `LEGAL-218` restriction.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\implementation-workflow-example.md:37:10. The workflow should discover the current notification-preference write surfaces before editing and make the chosen slice boundary explicit.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\implementation-workflow-example.md:43:Harden notification preference writes so the existing route cannot:
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\implementation-workflow-example.md:45:- disable the last available channel for `manual-review-escalation`
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\implementation-workflow-example.md:46:- enable decline SMS for California loan context
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\implementation-workflow-example.md:52:Good output should explicitly name the deferred write surfaces in the handoff instead of silently implying that the whole notification-preferences domain is now complete.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\implementation-workflow-example.md:78:- prefer checking stable business terms like `manual-review-escalation`,
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\implementation-workflow-example.md:79:  `at least one`, or `LEGAL-218`
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\implementation-workflow-example.md:87:The `LEGAL-218` checks may assert the literal token `LEGAL-218`, because that
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\implementation-playbook.md:37:3. Document the legal or business source in a comment (e.g., `// LEGAL-218`).
```

</details>


---

<sub>⏱️ 20s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\specs**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "notification-preference|notification preference|LEGAL-218|manual-review-escalation|decline",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\ghctx-tut\\lessons\\05-implementation-workflows\\specs",
  "output_mode": "content",
  "-n": true,
  "head_limit": 200
}
```

</details>

<details>
<summary>12 lines</summary>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\specs\product-spec-notification-preferences.md:22:Allow authorized users to configure notification preferences by channel and
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\specs\product-spec-notification-preferences.md:30:- Settings UI for notification preferences in `apps/web/`
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\specs\product-spec-notification-preferences.md:34:- Event-specific preferences for: approval, decline, document-request,
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\specs\product-spec-notification-preferences.md:35:  manual-review-escalation
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\specs\product-spec-notification-preferences.md:50:- Can edit their own notification preferences
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\specs\product-spec-notification-preferences.md:51:- **Cannot suppress mandatory manual-review-escalation notifications**
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\specs\product-spec-notification-preferences.md:55:- Can edit their own notification preferences
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\specs\product-spec-notification-preferences.md:107:SMS for decline decisions must remain **disabled for California loans** until
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\specs\product-spec-notification-preferences.md:108:the legal review tracked in `LEGAL-218` is complete.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\specs\product-spec-notification-preferences.md:117:> **HARD NEGATIVE pattern:** Enabling decline SMS on a CA loan looks like normal
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\specs\product-spec-notification-preferences.md:157:- They may **view** the delegate's notification preferences.
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\specs\product-spec-notification-preferences.md:191:2. Is the California decline SMS restriction loan-state based or borrower-state
```

</details>


---

<sub>⏱️ 20s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "notification.*preference|preferences|LEGAL-218|manual-review-escalation|decline",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\ghctx-tut\\lessons\\05-implementation-workflows\\src",
  "output_mode": "content",
  "glob": "**/*.{ts,tsx}",
  "-n": true,
  "head_limit": 300
}
```

</details>

```
No matches found.
```


---

<sub>⏱️ 20s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\tests**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "notification.*preference|preferences|LEGAL-218|manual-review-escalation|decline",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\ghctx-tut\\lessons\\05-implementation-workflows\\tests",
  "output_mode": "content",
  "glob": "**/*.{ts,tsx}",
  "-n": true,
  "head_limit": 300
}
```

</details>

```
No matches found.
```


---

<sub>⏱️ 34s</sub>

### 💬 Copilot

I found the lesson guidance and the current write path. Next I’m reading the spec/playbook plus the existing notification route and rule/test patterns so the change stays narrow and consistent.

---

<sub>⏱️ 35s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\implementation-playbook.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\implementation-playbook.md (lines 1-220)

<details>
<summary>115 lines</summary>

````
1. # Implementation Playbook
2. 
3. This document defines role boundaries, coding conventions, and handoff protocols
4. for the Loan Workbench implementation workflow.
5. 
6. ## Role Boundaries
7. 
8. | Role        | Can Read                | Can Write                                   | Can Execute            |
9. | ----------- | ----------------------- | ------------------------------------------- | ---------------------- |
10. | Implementer | All source, specs, docs | `src/backend/src/**`, `src/frontend/src/**` | Terminal (build, lint) |
11. | Tester      | All source, specs, docs | `src/backend/tests/**` only                 | Terminal + test runner |
12. | Reviewer    | All source, specs, docs | Nothing                                     | Nothing                |
13. 
14. ### Why These Boundaries Exist
15. 
16. - **Implementer cannot run tests**: Forces explicit handoff to the tester.
17.   Prevents "I'll just fix the test to match my code" shortcuts.
18. - **Reviewer cannot write**: Maintains independence. A reviewer who can "just
19.   fix it" is no longer reviewing — they're co-implementing.
20. - **Tester owns the test runner**: Only the tester decides when tests pass.
21.   The implementer provides code; the tester validates it.
22. 
23. ## Coding Conventions
24. 
25. ### Route Handlers (`src/backend/src/routes/`)
26. 
27. 1. Extract business logic to `src/backend/src/rules/` or `src/backend/src/services/` — routes should
28.    orchestrate, not decide.
29. 2. Use `requireRole()` middleware for role checks.
30. 3. Use `blockDelegatedWrites` middleware for mutation endpoints.
31. 4. Audit events via the queue broker or direct DB write before persisting changes.
32. 
33. ### Business Rules (`src/backend/src/rules/`)
34. 
35. 1. Pure functions that take data and return decisions.
36. 2. No side effects (no I/O, no audit writes, no HTTP responses).
37. 3. Document the legal or business source in a comment (e.g., `// LEGAL-218`).
38. 4. Annotate edge cases with `// FALSE POSITIVE` or `// HARD NEGATIVE`.
39. 
40. ### Services (`src/backend/src/services/`)
41. 
42. 1. Handle I/O and external integrations.
43. 2. Fail-closed for security-critical operations (audit).
44. 3. Degrade gracefully for non-critical operations (notification delivery).
45. 4. Never modify stored user preferences as a side effect of delivery.
46. 
47. ### Middleware (`src/backend/src/middleware/`)
48. 
49. 1. Thin and composable — one concern per middleware.
50. 2. Auth middleware sets `req.session`, nothing else.
51. 3. Guard middleware (like `blockDelegatedWrites`) returns 403 on violation.
52. 4. Error handler masks internal details — no stack traces in production.
53. 
54. ### Tests (`src/backend/tests/`)
55. 
56. 1. Use `describe`/`it` with behavior-focused names.
57. 2. One assertion per `it()` block.
58. 3. Test through route handlers using supertest-style requests.
59. 4. Annotate false-positive and hard-negative tests with comments.
60. 5. Do not mock business rule functions — test them through real call paths.
61. 
62. ## Handoff Protocols
63. 
64. ### Tester → Implementer
65. 
66. ```
67. Failing tests:
68.   - test name: "expected behavior description"
69.   - file: src/backend/tests/unit/xxx.test.ts
70. 
71. Files that need changes:
72.   - src/backend/src/rules/xxx.ts — add/modify rule
73.   - src/backend/src/routes/xxx.ts — wire in rule check
74. 
75. Relevant specs:
76.   - NFR-X: requirement summary
77.   - FR-X: functional requirement
78. ```
79. 
80. ### Implementer → Reviewer
81. 
82. ```
83. Changed files:
84.   - src/backend/src/rules/xxx.ts — what changed
85.   - src/backend/src/routes/xxx.ts — what changed
86. 
87. Tests that should pass:
88.   - "test name" in src/backend/tests/unit/xxx.test.ts
89. 
90. NFRs touched:
91.   - NFR-X: how it's addressed
92. ```
93. 
94. ### Reviewer → Team
95. 
96. ```
97. Review Summary:
98.   Verdict: APPROVE | REQUEST_CHANGES
99.   Files: list
100.   Issues: count
101. 
102. Issues (if any):
103.   1. [SEVERITY] description — file — spec reference
104. ```
105. 
106. ## Anti-Patterns
107. 
108. | Anti-Pattern               | Why It's Wrong                                   | Correct Approach                  |
109. | -------------------------- | ------------------------------------------------ | --------------------------------- |
110. | One agent does everything  | No independent validation                        | Three-agent role separation       |
111. | Implementer runs own tests | "Tests pass" because they were adjusted to match | Tester owns execution             |
112. | Reviewer pushes fixes      | No independent review trail                      | Reviewer flags, implementer fixes |
113. | Skipping the red step      | No proof the test catches the defect             | Always start with a failing test  |
114. | Batching unrelated changes | Review scope explosion                           | One feature per TDD cycle         |
115.
````

</details>


---

<sub>⏱️ 35s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\implementation-workflow-example.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\docs\implementation-workflow-example.md (lines 1-220)

<details>
<summary>100 lines</summary>

```
1. # Lesson 05 — Implementation Workflow Example
2. 
3. This document defines the concrete example used in Lesson 05.
4. 
5. ## Prerequisite Context
6. 
7. This lesson consumes `docs/notification-preferences-plan.md`, the structured
8. implementation plan produced by the Lesson 04 planning workflow. The plan maps
9. out all backend, frontend, audit, and observability surfaces for the full
10. notification-preferences feature. Lesson 05 implements only **one focused slice**
11. of that plan — hardening the notification-preference write path.
12. 
13. ## Objective
14. 
15. Show that a constrained implementation workflow can make a focused production change with matching tests instead of attempting the entire notification-preferences feature at once.
16. 
17. ## Expected Change Shape
18. 
19. The preferred output for this lesson is a small change set with:
20. 
21. 1. One new pure rule module under `src/backend/src/rules/`
22. 2. One matching unit test file under `src/backend/tests/unit/`
23. 3. One targeted wiring change to `src/backend/src/routes/notifications.ts`
24. 4. No edits to protected config or database files
25. 
26. ## Required Constraints
27. 
28. 1. The workflow must implement code, not only describe it.
29. 2. The new rule must use explicit inputs and existing domain types instead of direct database access.
30. 3. The change must preserve delegated-session and role guards already present in the route.
31. 4. The implementation must cover a mandatory-event rule and the California `LEGAL-218` restriction.
32. 5. The implementation must call out at least one false positive and one hard negative in the new rule module comments.
33. 6. The run must not execute shell commands.
34. 7. The run must not edit protected files such as feature flags, schema, or seed data.
35. 8. The run must not use SQL or task/todo write tools.
36. 9. The final handoff should explain the expected red/green test behavior and name any deferred follow-up surfaces that remain intentionally out of scope.
37. 10. The workflow should discover the current notification-preference write surfaces before editing and make the chosen slice boundary explicit.
38. 11. The write path must keep `loanState` as the direct request input for this route. Do not replace it with a new `loanId` lookup contract.
39. 12. The lesson is not complete until `python util.py --test` passes after the demo or manual implementation.
40. 
41. ## Concrete Scenario
42. 
43. Harden notification preference writes so the existing route cannot:
44. 
45. - disable the last available channel for `manual-review-escalation`
46. - enable decline SMS for California loan context
47. 
48. Good output should keep the change local and avoid sprawling refactors.
49. 
50. It should also make the intentional scope boundary visible: this lesson is about hardening the current notification write path, not implementing every preference mutation surface in the repository at once.
51. 
52. Good output should explicitly name the deferred write surfaces in the handoff instead of silently implying that the whole notification-preferences domain is now complete.
53. 
54. ## What Good Output Looks Like
55. 
56. Good output will usually:
57. 
58. - create a pure rule file and a matching unit test file
59. - wire the route to call the rule rather than embedding the full policy inline
60. - preserve existing delegated-session and permission checks
61. - keep the route contract direct and explicit by passing `loanState` into the rule instead of adding loan repository lookups
62. - cite or encode the false-positive case where escalation SMS is disabled but escalation email remains enabled
63. - encode the hard-negative case where all escalation channels end up disabled
64. - explain which test cases would fail before the production change and which should pass after it
65. - survive the end-to-end `python util.py --test` gate after the code change is produced
66. 
67. ## Test Authoring Quality Bar
68. 
69. Generated tests must be durable across semantically equivalent implementations.
70. That matters in this lesson because `python util.py --demo` recreates `src/` from
71. the app baseline before each run, so any test fix that lives only in generated
72. source will be lost on the next demo.
73. 
74. When a rule returns a human-readable reason string:
75. 
76. - assert the invariant, not one exact sentence or capitalization pattern
77. - normalize text before matching, such as lowercasing the reason
78. - prefer checking stable business terms like `manual-review-escalation`,
79.   `at least one`, or `LEGAL-218`
80. - avoid brittle exact-string checks for explanatory prose unless the exact text
81.   is part of the contract
82. 
83. For this lesson, the mandatory-event tests should prove that the rejection
84. mentions the escalation invariant and the "at least one channel" rule, even if
85. the final sentence shape differs.
86. 
87. The `LEGAL-218` checks may assert the literal token `LEGAL-218`, because that
88. identifier is a stable contract signal rather than free-form wording.
89. 
90. When the current route rejects a business-rule violation, stable semantics matter
91. more than one exact HTTP code. In this lesson, a semantically equivalent
92. implementation may surface the rejection as `400` or `422` while still returning
93. the correct business explanation. Unless the lesson is explicitly about HTTP
94. status design, tests should accept either status for these rule rejections and
95. assert the business invariant from the payload.
96. 
97. If the implementation can preserve the route's existing rejection style without
98. extra complexity, prefer `400` for this lesson so the API remains aligned with
99. the rest of the simple validation surfaces.
100.
```

</details>


---

<sub>⏱️ 35s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\specs\product-spec-notification-preferences.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\specs\product-spec-notification-preferences.md (lines 40-140)

<details>
<summary>101 lines</summary>

```
40. - Push notifications
41. - Per-loan notification overrides
42. - Customer-facing borrower communications
43. 
44. ---
45. 
46. ## User Roles
47. 
48. ### Underwriter
49. 
50. - Can edit their own notification preferences
51. - **Cannot suppress mandatory manual-review-escalation notifications**
52. 
53. ### Analyst Manager
54. 
55. - Can edit their own notification preferences
56. - Receives additional portfolio-level digest notifications (later release)
57. - Can operate in **delegated mode** on behalf of another user
58. 
59. ### Compliance Reviewer
60. 
61. - **Read-only** access to effective preference configuration for audit review
62. - Cannot change operational preferences from the UI
63. 
64. ---
65. 
66. ## Functional Requirements
67. 
68. ### FR-1: Preference Matrix
69. 
70. Users can configure email and SMS independently for these event types:
71. 
72. | Event                    | Email        | SMS            |
73. | ------------------------ | ------------ | -------------- |
74. | Approval decision issued | configurable | configurable   |
75. | Decline decision issued  | configurable | configurable\* |
76. | Document request created | configurable | configurable   |
77. | Manual-review escalation | configurable | configurable   |
78. 
79. \*Subject to state-specific restrictions — see FR-4.
80. 
81. ### FR-2: Mandatory Event Rules
82. 
83. Manual-review escalation is a **mandatory notification**. Users may change the
84. secondary channel, but **at least one channel must remain enabled**.
85. 
86. > **HARD NEGATIVE pattern:** Without this rule, an AI generating the preference
87. > update handler will produce code that allows disabling all channels. The UI
88. > and API must both enforce this constraint.
89. 
90. > **FALSE POSITIVE pattern:** A user disabling SMS for escalation while email
91. > remains enabled is NOT a violation. The constraint is about having zero
92. > channels, not about which specific channel is active.
93. 
94. ### FR-3: Role-Based Defaults
95. 
96. | Role                | Email default                            | SMS default     |
97. | ------------------- | ---------------------------------------- | --------------- |
98. | Underwriter         | All events enabled                       | Escalation only |
99. | Analyst Manager     | All events enabled                       | Escalation only |
100. | Compliance Reviewer | No operational defaults (read-only role) | N/A             |
101. 
102. New users without saved preferences must receive these defaults on first access
103. **without requiring a data backfill migration**.
104. 
105. ### FR-4: Temporary SMS Restriction — California
106. 
107. SMS for decline decisions must remain **disabled for California loans** until
108. the legal review tracked in `LEGAL-218` is complete.
109. 
110. - The UI must explain why the option is unavailable when the active loan context
111.   is California.
112. - The restriction is based on loan jurisdiction (`loanState`), not borrower
113.   address, when the two differ.
114. - From a **multi-state portfolio view**, state-specific restrictions should be
115.   shown as conditional rules rather than blanket-disabling all SMS controls.
116. 
117. > **HARD NEGATIVE pattern:** Enabling decline SMS on a CA loan looks like normal
118. > toggle behavior in code. The restriction is invisible without this spec.
119. 
120. ### FR-5: Degraded Delivery Fallback
121. 
122. If the SMS provider is unavailable:
123. 
124. 1. Delivery falls back to email when email is enabled for that event.
125. 2. **Stored preferences must NOT be modified by the fallback.**
126. 3. Fallback invocations must be logged with a separate metric.
127. 
128. > **FALSE POSITIVE pattern:** A user receiving an email instead of SMS during
129. > an outage is NOT a preference bug. Support agents must check delivery logs,
130. > not the preference store, to diagnose delivery complaints.
131. 
132. ### FR-6: Auditability
133. 
134. Every preference change must record:
135. 
136. - Actor identity
137. - Timestamp
138. - Previous value
139. - New value
140. - Source channel
```

</details>


---

<sub>⏱️ 35s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\specs\product-spec-notification-preferences.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\specs\product-spec-notification-preferences.md (lines 140-210)

<details>
<summary>55 lines</summary>

```
140. - Source channel
141. - Delegated-for user (if applicable)
142. 
143. ---
144. 
145. ## Special Conditions
146. 
147. ### SC-1: Locked (Finalized) Applications
148. 
149. When a loan application is in `finalized` state, users can still update their
150. preferences globally, but the settings screen must clarify that changes **do not
151. affect notifications already queued** for that application.
152. 
153. ### SC-2: Delegated Sessions
154. 
155. If an analyst manager is operating in delegated mode:
156. 
157. - They may **view** the delegate's notification preferences.
158. - They may **not modify** the delegate's preferences.
159. - The UI must visually indicate delegated-session mode.
160. - Audit entries must record both the actor and the delegated-for user.
161. 
162. > **HARD NEGATIVE pattern:** A delegated save that shows a "success" toast but
163. > reverts on refresh indicates the UI is optimistically updating local state
164. > without checking the server rejection. This is a real bug already reported.
165. 
166. ### SC-3: Mixed Portfolio Context
167. 
168. When the settings screen is opened from a portfolio view containing loans
169. across multiple states, state-specific restrictions should be explained as
170. conditional rules rather than blanket-disabling controls.
171. 
172. ---
173. 
174. ## UX Notes
175. 
176. - Show channel controls in a matrix grid by event type.
177. - Mandatory events should be **visually marked** and explained inline.
178. - Disabled controls must include persistent helper text, not just tooltips.
179. - Saving should be optimistic **only if rollback is supported by the store**.
180. 
181. ## Success Metrics
182. 
183. - 30% reduction in document-request alert-mute requests within 60 days
184. - < 1% failed preference saves during pilot
185. - Zero Sev2 incidents caused by suppressed mandatory escalation alerts
186. 
187. ## Open Questions
188. 
189. 1. Should compliance reviewers access audit history from the same settings page
190.    or a separate audit viewer?
191. 2. Is the California decline SMS restriction loan-state based or borrower-state
192.    based when they differ? **Answer: loan-state** (per legal review 2026-02).
193. 3. Should portfolio-view restrictions show a summary banner or per-row indicators?
194.
```

</details>


---

<sub>⏱️ 35s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\specs\non-functional-requirements.md.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\specs\non-functional-requirements.md (lines 1-180)

<details>
<summary>109 lines</summary>

```
1. # Non-Functional Requirements — Implementation Workflows
2. 
3. These NFRs apply during implementation. Each includes the **AI mistake without
4. context** annotation showing what goes wrong when the AI doesn't have this NFR.
5. 
6. ---
7. 
8. ## NFR-1: Audit Trail Integrity (Fail-Closed)
9. 
10. **Requirement**: Every mutation that changes user data must write an audit entry
11. BEFORE persisting the change. If the audit write fails, the mutation MUST fail
12. with a 503 error. No silent fallback.
13. 
14. **AI mistake without context**: AI implements try-catch around the audit write
15. and proceeds with the mutation anyway. "Best-effort logging" sounds reasonable
16. but violates a compliance requirement.
17. 
18. > **HARD NEGATIVE**: The AI generates code that catches audit failures and logs
19. > a warning instead of aborting. This passes basic tests but fails compliance.
20. 
21. **Test signal**: Any test that mocks audit failure should assert the mutation
22. did NOT persist AND the response is 503.
23. 
24. ---
25. 
26. ## NFR-2: Degraded Mode for Non-Critical Services
27. 
28. **Requirement**: Notification delivery failures must fall back to email when SMS
29. is unavailable. The fallback must NOT modify stored user preferences.
30. 
31. **AI mistake without context**: AI implements the fallback but also updates the
32. user's stored channel preference from SMS to email "for consistency."
33. 
34. > **FALSE POSITIVE**: AI flags the inconsistency between stored preference (SMS)
35. > and actual delivery (email) as a bug. It's intentional — delivery degrades
36. > but preferences don't change.
37. 
38. **Test signal**: After a degraded delivery, GET /preferences should still show
39. the original SMS preference.
40. 
41. ---
42. 
43. ## NFR-3: Request Latency Budget
44. 
45. **Requirement**: Preference save operations must complete in <200ms under normal
46. conditions. Sequential I/O should be minimized.
47. 
48. **AI mistake without context**: AI adds synchronous delivery confirmation after
49. every preference save, doubling latency. Delivery is async by design.
50. 
51. > **FALSE POSITIVE**: AI suggests adding `await deliverNotification()` to the
52. > save handler for "consistency." Delivery is fire-and-forget by design.
53. 
54. ---
55. 
56. ## NFR-4: Role-Scoped Data Access
57. 
58. **Requirement**: Underwriters can only see their own audit entries. Analyst-managers
59. see entries for their team. Compliance reviewers see all entries.
60. 
61. **AI mistake without context**: AI implements a single `/audit` endpoint that
62. returns all entries regardless of role, adding a client-side filter. Server-side
63. scoping is the requirement.
64. 
65. > **HARD NEGATIVE**: The AI returns all audit data and filters in the response
66. > mapper. This "works" for underwriters viewing their own data but leaks
67. > everyone else's data in the response payload.
68. 
69. ---
70. 
71. ## NFR-5: Feature Flag Behavior (404 Not 403)
72. 
73. **Requirement**: Non-pilot users hitting gated endpoints must receive 404 (Not
74. Found), not 403 (Forbidden). This prevents information leakage about unreleased
75. features.
76. 
77. **AI mistake without context**: AI uses 403 because "the user isn't authorized
78. for this feature." The distinction matters — 403 confirms the endpoint exists.
79. 
80. > **HARD NEGATIVE**: AI returns 403 for non-pilot users. Security scanners and
81. > curious users now know the feature endpoint exists and is gated.
82. 
83. ---
84. 
85. ## NFR-6: Schema Backward Compatibility
86. 
87. **Requirement**: API schema changes must be additive. Existing clients must not
88. break when new fields are added. Removed fields must be deprecated with a
89. minimum two-release notice.
90. 
91. **AI mistake without context**: AI renames a response field from `channels` to
92. `notificationChannels` for "clarity." All existing clients break.
93. 
94. > **HARD NEGATIVE**: The AI improves naming but breaks every consumer. Additive
95. > changes (adding `notificationChannels` alongside `channels`) are safe.
96. 
97. ---
98. 
99. ## NFR-7: Structured Logging and Observability
100. 
101. **Requirement**: All log entries must be structured JSON with `correlationId`,
102. `userId`, `action`, and `timestamp`. No `console.log()` with string concatenation.
103. 
104. **AI mistake without context**: AI uses `console.log(\`User ${userId} saved preferences\`)`
105. which is unstructured and not machine-parseable.
106. 
107. > **FALSE POSITIVE**: AI flags existing structured logging as "verbose" and
108. > simplifies to `console.log()`. The structured format is a requirement.
109.
```

</details>


---

<sub>⏱️ 35s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts (lines 1-260)

<details>
<summary>260 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Notification Preference Routes
3. // ---------------------------------------------------------------------------
4. //
5. // IMPORTANT — AUTHORIZATION:
6. //   All roles can READ preferences (for display purposes).
7. //   Only underwriters and analyst-managers can WRITE preferences.
8. //   Compliance reviewers are READ-ONLY for notification preferences.
9. //
10. // IMPORTANT — DELEGATED SESSIONS:
11. //   A delegated session (x-delegated-for header) can read the delegate's
12. //   preferences but CANNOT modify them.  The route handler must check
13. //   session.delegatedFor before allowing writes.
14. // ---------------------------------------------------------------------------
15. 
16. import { Router } from "express";
17. import { requireRole } from "../middleware/auth.js";
18. import { validateBody } from "../middleware/request-validator.js";
19. import { hasPermission } from "../rules/role-permissions.js";
20. import { auditAction } from "../services/audit-service.js";
21. import * as prefRepo from "../models/preference-repository.js";
22. import type {
23.   SessionContext,
24.   NotificationPreference,
25. } from "../models/types.js";
26. 
27. export const notificationRoutes = Router();
28. 
29. function firstParam(value: string | string[]): string {
30.   return Array.isArray(value) ? value[0] : value;
31. }
32. 
33. /** GET /api/notifications/preferences/:userId — get preferences for a user. */
34. notificationRoutes.get(
35.   "/preferences/:userId",
36.   requireRole("underwriter", "analyst-manager", "compliance-reviewer"),
37.   (req, res) => {
38.     const prefs = prefRepo.findPreferencesForUser(
39.       firstParam(req.params.userId),
40.     );
41.     res.json(prefs);
42.   },
43. );
44. 
45. /** PUT /api/notifications/preferences — set a notification preference. */
46. notificationRoutes.put(
47.   "/preferences",
48.   requireRole("underwriter", "analyst-manager"),
49.   validateBody([
50.     { field: "userId", type: "string", required: true },
51.     { field: "event", type: "string", required: true },
52.     { field: "channel", type: "string", required: true },
53.     { field: "enabled", type: "boolean", required: true },
54.   ]),
55.   (req, res, next) => {
56.     try {
57.       const session = req.session as SessionContext;
58. 
59.       // Block writes in delegated sessions
60.       if (session.delegatedFor) {
61.         res.status(403).json({
62.           error: "Delegated sessions cannot modify notification preferences.",
63.         });
64.         return;
65.       }
66. 
67.       // Additional permission check
68.       if (!hasPermission(session.actor.role, "notification-pref:write")) {
69.         res.status(403).json({
70.           error: `Role '${session.actor.role}' cannot modify notification preferences.`,
71.         });
72.         return;
73.       }
74. 
75.       const { userId, event, channel, enabled } = req.body;
76.       const now = new Date().toISOString();
77. 
78.       const previous = prefRepo.findPreference(userId, event, channel);
79. 
80.       const pref: NotificationPreference = {
81.         userId,
82.         event,
83.         channel,
84.         enabled,
85.         updatedAt: now,
86.         updatedBy: session.actor.id,
87.       };
88. 
89.       prefRepo.setPreference(pref);
90. 
91.       // Audit the preference change
92.       auditAction(
93.         session,
94.         "preference.updated",
95.         previous ?? null,
96.         pref,
97.         "notification-routes",
98.       );
99. 
100.       res.json(pref);
101.     } catch (err) {
102.       next(err);
103.     }
104.   },
105. );
106. 
107. /**
108.  * PUT /api/notifications/preferences/:userId/email — set email notification preferences for all events.
109.  * Updates the enabled flag for all notification events on the email channel.
110.  * Only the owner can modify their own preferences. Delegated sessions are blocked.
111.  */
112. notificationRoutes.put(
113.   "/preferences/:userId/email",
114.   requireRole("underwriter", "analyst-manager"),
115.   validateBody([
116.     { field: "enabled", type: "boolean", required: true },
117.   ]),
118.   (req, res, next) => {
119.     try {
120.       const session = req.session as SessionContext;
121.       const targetUserId = firstParam(req.params.userId);
122. 
123.       // Block writes in delegated sessions
124.       if (session.delegatedFor) {
125.         res.status(403).json({
126.           error: "FORBIDDEN: Delegated sessions cannot modify notification preferences.",
127.         });
128.         return;
129.       }
130. 
131.       // Enforce owner-only writes
132.       if (session.actor.id !== targetUserId) {
133.         res.status(403).json({
134.           error: `FORBIDDEN: Users can only modify their own notification preferences.`,
135.         });
136.         return;
137.       }
138. 
139.       // Permission check
140.       if (!hasPermission(session.actor.role, "notification-pref:write")) {
141.         res.status(403).json({
142.           error: `FORBIDDEN: Role '${session.actor.role}' cannot modify notification preferences.`,
143.         });
144.         return;
145.       }
146. 
147.       const { enabled } = req.body;
148.       const now = new Date().toISOString();
149.       const events: Array<"approval" | "decline" | "document-request" | "manual-review-escalation"> = [
150.         "approval",
151.         "decline",
152.         "document-request",
153.         "manual-review-escalation",
154.       ];
155. 
156.       const updates: NotificationPreference[] = [];
157. 
158.       for (const event of events) {
159.         const previous = prefRepo.findPreference(targetUserId, event, "email");
160. 
161.         const pref: NotificationPreference = {
162.           userId: targetUserId,
163.           event,
164.           channel: "email",
165.           enabled,
166.           updatedAt: now,
167.           updatedBy: session.actor.id,
168.         };
169. 
170.         prefRepo.setPreference(pref);
171.         updates.push(pref);
172. 
173.         // Audit each preference change
174.         auditAction(
175.           session,
176.           "preference.updated",
177.           previous ?? null,
178.           pref,
179.           "notification-routes",
180.         );
181.       }
182. 
183.       res.json(updates);
184.     } catch (err) {
185.       next(err);
186.     }
187.   },
188. );
189. 
190. /**
191.  * PUT /api/notifications/preferences/:userId/sms — set SMS notification preferences for all events.
192.  * Updates the enabled flag for all notification events on the SMS channel.
193.  * Only the owner can modify their own preferences. Delegated sessions are blocked.
194.  */
195. notificationRoutes.put(
196.   "/preferences/:userId/sms",
197.   requireRole("underwriter", "analyst-manager"),
198.   validateBody([
199.     { field: "enabled", type: "boolean", required: true },
200.   ]),
201.   (req, res, next) => {
202.     try {
203.       const session = req.session as SessionContext;
204.       const targetUserId = firstParam(req.params.userId);
205. 
206.       // Block writes in delegated sessions
207.       if (session.delegatedFor) {
208.         res.status(403).json({
209.           error: "FORBIDDEN: Delegated sessions cannot modify notification preferences.",
210.         });
211.         return;
212.       }
213. 
214.       // Enforce owner-only writes
215.       if (session.actor.id !== targetUserId) {
216.         res.status(403).json({
217.           error: `FORBIDDEN: Users can only modify their own notification preferences.`,
218.         });
219.         return;
220.       }
221. 
222.       // Permission check
223.       if (!hasPermission(session.actor.role, "notification-pref:write")) {
224.         res.status(403).json({
225.           error: `FORBIDDEN: Role '${session.actor.role}' cannot modify notification preferences.`,
226.         });
227.         return;
228.       }
229. 
230.       const { enabled } = req.body;
231.       const now = new Date().toISOString();
232.       const events: Array<"approval" | "decline" | "document-request" | "manual-review-escalation"> = [
233.         "approval",
234.         "decline",
235.         "document-request",
236.         "manual-review-escalation",
237.       ];
238. 
239.       const updates: NotificationPreference[] = [];
240. 
241.       for (const event of events) {
242.         const previous = prefRepo.findPreference(targetUserId, event, "sms");
243. 
244.         const pref: NotificationPreference = {
245.           userId: targetUserId,
246.           event,
247.           channel: "sms",
248.           enabled,
249.           updatedAt: now,
250.           updatedBy: session.actor.id,
251.         };
252. 
253.         prefRepo.setPreference(pref);
254.         updates.push(pref);
255. 
256.         // Audit each preference change
257.         auditAction(
258.           session,
259.           "preference.updated",
260.           previous ?? null,
```

</details>


---

<sub>⏱️ 35s</sub>

### ❌ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\rules\notification-channel-rules.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\rules\notification-channel-rules.ts (lines 1-220)

```
Path does not exist
```


---

<sub>⏱️ 35s</sub>

### ❌ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\tests\unit\notification-channel-rules.test.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\tests\unit\notification-channel-rules.test.ts (lines 1-260)

```
Path does not exist
```


---

<sub>⏱️ 35s</sub>

### ❌ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\types.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\types.ts (lines 1-260)

```
Path does not exist
```


---

<sub>⏱️ 45s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src**

"**\types.ts" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\models\types.ts
```


---

<sub>⏱️ 45s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\tests**

"**\*.test.ts" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\tests

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\tests\integration\decisions.test.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\tests\integration\applications.test.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\tests\unit\business-rules.test.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\tests\unit\notification-service.test.ts
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\tests\unit\state-machine.test.ts
```


---

<sub>⏱️ 45s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts (lines 261-420)

<details>
<summary>12 lines</summary>

```
261.           pref,
262.           "notification-routes",
263.         );
264.       }
265. 
266.       res.json(updates);
267.     } catch (err) {
268.       next(err);
269.     }
270.   },
271. );
272.
```

</details>


---

<sub>⏱️ 45s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "NotificationPreference|type Notification|interface Notification|loanState",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\ghctx-tut\\lessons\\05-implementation-workflows\\src\\backend\\src",
  "output_mode": "content",
  "glob": "**/*.{ts,tsx}",
  "-n": true,
  "head_limit": 200
}
```

</details>

<details>
<summary>26 lines</summary>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\models\loan-repository.ts:19:  loan_state AS loanState,
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\models\loan-repository.ts:66:  loanState: string;
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\models\loan-repository.ts:80:    data.loanState.toUpperCase(),
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\models\types.ts:38:export type NotificationEvent =
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\models\types.ts:45:export type NotificationChannel = "email" | "sms";
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\models\types.ts:75:  loanState: string;
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\models\types.ts:93:export interface NotificationPreference {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\services\loan-service.ts:31:  data: { borrowerName: string; amount: number; loanState: string },
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\services\loan-service.ts:40:    loanState: data.loanState.toUpperCase(),
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\services\loan-service.ts:52:    loanState: data.loanState,
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\routes\applications.ts:56:    { field: "loanState", type: "string", required: true },
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\rules\business-rules.ts:46:  if (featureFlags.californiaRules && loan.loanState === "CA") {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\queue\contracts.ts:31:export interface NotificationRequestedEvent extends BaseEvent {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:24:  NotificationPreference,
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:80:      const pref: NotificationPreference = {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:156:      const updates: NotificationPreference[] = [];
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:161:        const pref: NotificationPreference = {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:239:      const updates: NotificationPreference[] = [];
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:244:        const pref: NotificationPreference = {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\models\preference-repository.ts:15:  NotificationPreference,
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\models\preference-repository.ts:29:type PreferenceRow = NotificationPreference & { enabled: number | boolean };
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\models\preference-repository.ts:33:): NotificationPreference[] {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\models\preference-repository.ts:44:    })) as NotificationPreference[];
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\models\preference-repository.ts:51:): NotificationPreference | undefined {
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\models\preference-repository.ts:58:    | (NotificationPreference & { enabled: number | boolean })
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\models\preference-repository.ts:64:export function setPreference(pref: NotificationPreference): void {
```

</details>


---

<sub>⏱️ 45s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\tests**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "request-validator|requireRole|supertest|express",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\ghctx-tut\\lessons\\05-implementation-workflows\\src\\backend\\tests",
  "output_mode": "content",
  "glob": "**/*.test.ts",
  "-n": true,
  "head_limit": 200
}
```

</details>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\tests\integration\applications.test.ts:12:    // To run: set up test DB, import app, use supertest
```


---

<sub>⏱️ 59s</sub>

### 💬 Copilot

The route surface is smaller than the plan: one single-item write endpoint plus two bulk channel endpoints. I’m checking the existing types and test style now so I can keep this slice scoped to the current single-item write path and call the bulk endpoints out as deferred.

---

<sub>⏱️ 59s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\models\types.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\models\types.ts (lines 1-220)

<details>
<summary>112 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Loan Workbench — Domain Types
3. // ---------------------------------------------------------------------------
4. // This file defines the core domain model for the Loan Workbench platform.
5. // Business rules, state machines, authorization logic, queue contracts, and
6. // database schema all depend on these types.  Changes here affect nearly
7. // every module in the project.
8. // ---------------------------------------------------------------------------
9. 
10. /** Lifecycle states for a commercial loan application. */
11. export type ApplicationState =
12.   | "intake"
13.   | "review"
14.   | "underwriting"
15.   | "decision"
16.   | "finalized";
17. 
18. /**
19.  * Valid state transitions.
20.  * Transitions not listed here are forbidden — the system must never allow
21.  * a finalized application to move backward.
22.  */
23. export const VALID_TRANSITIONS: Record<ApplicationState, ApplicationState[]> = {
24.   intake: ["review"],
25.   review: ["underwriting", "intake"], // can return to intake for rework
26.   underwriting: ["decision"],
27.   decision: ["finalized", "underwriting"], // can push back to underwriting
28.   finalized: [], // terminal — no transitions allowed
29. };
30. 
31. /** Organizational roles recognized by the Loan Workbench. */
32. export type UserRole =
33.   | "underwriter"
34.   | "analyst-manager"
35.   | "compliance-reviewer";
36. 
37. /** Notification event types that can trigger user-facing alerts. */
38. export type NotificationEvent =
39.   | "approval"
40.   | "decline"
41.   | "document-request"
42.   | "manual-review-escalation";
43. 
44. /** Delivery channels available for notifications. */
45. export type NotificationChannel = "email" | "sms";
46. 
47. // ---------------------------------------------------------------------------
48. // Entity interfaces
49. // ---------------------------------------------------------------------------
50. 
51. export interface User {
52.   id: string;
53.   role: UserRole;
54.   name: string;
55.   email: string;
56.   phone?: string;
57. }
58. 
59. /**
60.  * Session context attached to every authenticated request.
61.  *
62.  * When `delegatedFor` is present the actor is operating on behalf of another
63.  * user.  Delegated sessions restrict write operations — see auth middleware.
64.  */
65. export interface SessionContext {
66.   actor: User;
67.   delegatedFor?: User;
68. }
69. 
70. export interface LoanApplication {
71.   id: string;
72.   borrowerName: string;
73.   amount: number;
74.   /** US state / jurisdiction — affects business rules (e.g. California). */
75.   loanState: string;
76.   status: ApplicationState;
77.   assignedUnderwriter: string;
78.   riskScore: number | null;
79.   createdAt: string;
80.   updatedAt: string;
81. }
82. 
83. export interface Decision {
84.   id: string;
85.   applicationId: string;
86.   type: "approved" | "declined" | "conditional";
87.   rationale: string;
88.   decidedBy: string;
89.   decidedAt: string;
90.   conditions?: string[];
91. }
92. 
93. export interface NotificationPreference {
94.   userId: string;
95.   event: NotificationEvent;
96.   channel: NotificationChannel;
97.   enabled: boolean;
98.   updatedAt: string;
99.   updatedBy: string;
100. }
101. 
102. export interface AuditEntry {
103.   id: string;
104.   action: string;
105.   actor: string;
106.   delegatedFor: string | null;
107.   timestamp: string;
108.   previousValue: string | null;
109.   newValue: string | null;
110.   source: string;
111. }
112.
```

</details>


---

<sub>⏱️ 59s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\models\preference-repository.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\models\preference-repository.ts (lines 1-220)

<details>
<summary>86 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Notification Preference Repository
3. // ---------------------------------------------------------------------------
4. // Database operations for notification preferences.
5. //
6. // KEY NUANCE — UPSERT BEHAVIOR:
7. //   The `setPreference` function uses INSERT OR REPLACE on the composite
8. //   primary key (user_id, event, channel).  This means updating a preference
9. //   replaces the entire row — there is no partial update.  The `updated_by`
10. //   field MUST always be set (it tracks who last changed the preference).
11. // ---------------------------------------------------------------------------
12. 
13. import { getDb } from "../db/connection.js";
14. import type {
15.   NotificationPreference,
16.   NotificationEvent,
17.   NotificationChannel,
18. } from "./types.js";
19. 
20. const PREFERENCE_COLUMNS = `
21.   user_id AS userId,
22.   event,
23.   channel,
24.   enabled,
25.   updated_at AS updatedAt,
26.   updated_by AS updatedBy
27. `;
28. 
29. type PreferenceRow = NotificationPreference & { enabled: number | boolean };
30. 
31. export function findPreferencesForUser(
32.   userId: string,
33. ): NotificationPreference[] {
34.   const db = getDb();
35.   return db
36.     .prepare(
37.       `SELECT ${PREFERENCE_COLUMNS} FROM notification_preferences WHERE user_id = ?`,
38.     )
39.     .all(userId)
40.     .map((pref) => pref as PreferenceRow)
41.     .map((pref) => ({
42.       ...pref,
43.       enabled: Boolean(pref.enabled),
44.     })) as NotificationPreference[];
45. }
46. 
47. export function findPreference(
48.   userId: string,
49.   event: NotificationEvent,
50.   channel: NotificationChannel,
51. ): NotificationPreference | undefined {
52.   const db = getDb();
53.   const pref = db
54.     .prepare(
55.       `SELECT ${PREFERENCE_COLUMNS} FROM notification_preferences WHERE user_id = ? AND event = ? AND channel = ?`,
56.     )
57.     .get(userId, event, channel) as
58.     | (NotificationPreference & { enabled: number | boolean })
59.     | undefined;
60. 
61.   return pref ? { ...pref, enabled: Boolean(pref.enabled) } : undefined;
62. }
63. 
64. export function setPreference(pref: NotificationPreference): void {
65.   const db = getDb();
66.   db.prepare(
67.     `INSERT OR REPLACE INTO notification_preferences (user_id, event, channel, enabled, updated_at, updated_by)
68.      VALUES (?, ?, ?, ?, ?, ?)`,
69.   ).run(
70.     pref.userId,
71.     pref.event,
72.     pref.channel,
73.     pref.enabled ? 1 : 0,
74.     pref.updatedAt,
75.     pref.updatedBy,
76.   );
77. }
78. 
79. export function deletePreferencesForUser(userId: string): number {
80.   const db = getDb();
81.   const result = db
82.     .prepare("DELETE FROM notification_preferences WHERE user_id = ?")
83.     .run(userId);
84.   return result.changes;
85. }
86.
```

</details>


---

<sub>⏱️ 59s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\rules\business-rules.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\rules\business-rules.ts (lines 1-220)

<details>
<summary>84 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Business Rules
3. // ---------------------------------------------------------------------------
4. // Domain-specific validation rules.  These are checked by services BEFORE
5. // persisting changes.
6. //
7. // CALIFORNIA RULES — REGULATORY REQUIREMENT:
8. //   Loans in California (loan_state = "CA") have additional requirements:
9. //   - Minimum loan amount: $50,000
10. //   - Maximum loan amount: $5,000,000
11. //   - Mandatory 3-day cooling-off period between "review" → "underwriting"
12. //   - Additional disclosure document required before finalization
13. //
14. //   These rules are gated behind the `californiaRules` feature flag.
15. //   When disabled, California loans follow standard rules.
16. //
17. // AMOUNT THRESHOLDS:
18. //   - Loans over $1,000,000 require analyst-manager approval (not just underwriter)
19. //   - Loans over $2,500,000 require compliance-reviewer sign-off
20. // ---------------------------------------------------------------------------
21. 
22. import { featureFlags } from "../config/feature-flags.js";
23. import type { LoanApplication, UserRole } from "../models/types.js";
24. 
25. export interface RuleViolation {
26.   rule: string;
27.   message: string;
28. }
29. 
30. /**
31.  * Validate a loan application against all business rules.
32.  * Returns an empty array if all rules pass.
33.  */
34. export function validateLoanRules(loan: LoanApplication): RuleViolation[] {
35.   const violations: RuleViolation[] = [];
36. 
37.   // Standard rules
38.   if (loan.amount <= 0) {
39.     violations.push({
40.       rule: "positive-amount",
41.       message: "Loan amount must be positive.",
42.     });
43.   }
44. 
45.   // California-specific rules
46.   if (featureFlags.californiaRules && loan.loanState === "CA") {
47.     if (loan.amount < 50_000) {
48.       violations.push({
49.         rule: "ca-min-amount",
50.         message: "California loans must be at least $50,000.",
51.       });
52.     }
53.     if (loan.amount > 5_000_000) {
54.       violations.push({
55.         rule: "ca-max-amount",
56.         message: "California loans cannot exceed $5,000,000.",
57.       });
58.     }
59.   }
60. 
61.   return violations;
62. }
63. 
64. /**
65.  * Determine which roles are required to approve a loan at the given amount.
66.  */
67. export function requiredApprovalRoles(amount: number): UserRole[] {
68.   if (amount > 2_500_000) {
69.     return ["analyst-manager", "compliance-reviewer"];
70.   }
71.   if (amount > 1_000_000) {
72.     return ["analyst-manager"];
73.   }
74.   return ["underwriter"];
75. }
76. 
77. /**
78.  * Check if a role is authorized to approve a loan of the given amount.
79.  */
80. export function canApprove(role: UserRole, amount: number): boolean {
81.   const required = requiredApprovalRoles(amount);
82.   return required.includes(role);
83. }
84.
```

</details>


---

<sub>⏱️ 59s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\tests\unit\business-rules.test.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\tests\unit\business-rules.test.ts (lines 1-260)

<details>
<summary>72 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Business Rules Tests
3. // ---------------------------------------------------------------------------
4. 
5. import { describe, it, expect } from "vitest";
6. import {
7.   validateLoanRules,
8.   requiredApprovalRoles,
9.   canApprove,
10. } from "../../src/rules/business-rules.js";
11. import type { LoanApplication } from "../../src/models/types.js";
12. 
13. const baseLoan: LoanApplication = {
14.   id: "test-1",
15.   borrowerName: "Test Corp",
16.   amount: 100000,
17.   loanState: "NY",
18.   status: "intake",
19.   assignedUnderwriter: "u-1",
20.   riskScore: null,
21.   createdAt: new Date().toISOString(),
22.   updatedAt: new Date().toISOString(),
23. };
24. 
25. describe("Business Rules", () => {
26.   it("passes for a valid standard loan", () => {
27.     expect(validateLoanRules(baseLoan)).toEqual([]);
28.   });
29. 
30.   it("rejects zero amount", () => {
31.     const violations = validateLoanRules({ ...baseLoan, amount: 0 });
32.     expect(violations).toHaveLength(1);
33.     expect(violations[0].rule).toBe("positive-amount");
34.   });
35. 
36.   it("rejects California loan below minimum", () => {
37.     const violations = validateLoanRules({
38.       ...baseLoan,
39.       loanState: "CA",
40.       amount: 10000,
41.     });
42.     expect(violations.some((v) => v.rule === "ca-min-amount")).toBe(true);
43.   });
44. 
45.   it("rejects California loan above maximum", () => {
46.     const violations = validateLoanRules({
47.       ...baseLoan,
48.       loanState: "CA",
49.       amount: 6_000_000,
50.     });
51.     expect(violations.some((v) => v.rule === "ca-max-amount")).toBe(true);
52.   });
53. });
54. 
55. describe("Approval Roles", () => {
56.   it("underwriter can approve loans up to $1M", () => {
57.     expect(canApprove("underwriter", 500000)).toBe(true);
58.   });
59. 
60.   it("underwriter cannot approve loans over $1M", () => {
61.     expect(canApprove("underwriter", 1_500_000)).toBe(false);
62.   });
63. 
64.   it("analyst-manager required for loans over $1M", () => {
65.     expect(requiredApprovalRoles(1_500_000)).toContain("analyst-manager");
66.   });
67. 
68.   it("compliance-reviewer required for loans over $2.5M", () => {
69.     expect(requiredApprovalRoles(3_000_000)).toContain("compliance-reviewer");
70.   });
71. });
72.
```

</details>


---

<sub>⏱️ 59s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\middleware\request-validator.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\middleware\request-validator.ts (lines 1-220)

<details>
<summary>51 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Request Validator Middleware
3. // ---------------------------------------------------------------------------
4. // Validates request bodies against expected shapes before they reach
5. // route handlers.  Returns 400 with descriptive errors on failure.
6. //
7. // This is intentionally simple — no JSON Schema library dependency.
8. // For production, consider ajv or zod.
9. // ---------------------------------------------------------------------------
10. 
11. import type { Request, Response, NextFunction } from "express";
12. 
13. export type ValidationRule = {
14.   field: string;
15.   type: "string" | "number" | "boolean";
16.   required?: boolean;
17. };
18. 
19. /**
20.  * Factory that returns middleware validating req.body against the given rules.
21.  */
22. export function validateBody(rules: ValidationRule[]) {
23.   return (req: Request, res: Response, next: NextFunction): void => {
24.     const errors: string[] = [];
25. 
26.     for (const rule of rules) {
27.       const value = req.body?.[rule.field];
28. 
29.       if (value === undefined || value === null) {
30.         if (rule.required) {
31.           errors.push(`Missing required field: '${rule.field}'`);
32.         }
33.         continue;
34.       }
35. 
36.       if (typeof value !== rule.type) {
37.         errors.push(
38.           `Field '${rule.field}' must be ${rule.type}, got ${typeof value}`,
39.         );
40.       }
41.     }
42. 
43.     if (errors.length > 0) {
44.       res.status(400).json({ error: "Validation failed.", details: errors });
45.       return;
46.     }
47. 
48.     next();
49.   };
50. }
51.
```

</details>


---

<sub>⏱️ 59s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\middleware\auth.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\middleware\auth.ts (lines 1-240)

<details>
<summary>98 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Authentication & Authorization Middleware
3. // ---------------------------------------------------------------------------
4. //
5. // KEY NUANCE — DELEGATED SESSIONS:
6. //   When the `x-delegated-for` header is present, the session is marked as
7. //   delegated.  Delegated sessions allow READ operations on the delegate's
8. //   data but BLOCK writes.  An AI assistant without context would likely
9. //   skip this distinction, producing code that allows delegated writes.
10. //
11. // KEY NUANCE — COMPLIANCE REVIEWER:
12. //   Compliance reviewers can view notification preferences and audit logs
13. //   but cannot modify operational settings.  This is a read-only role for
14. //   the notification feature, even though the role has write permissions
15. //   in other parts of the system.
16. // ---------------------------------------------------------------------------
17. 
18. import type { Request, Response, NextFunction } from "express";
19. import type { UserRole, SessionContext } from "../models/types.js";
20. import { findUserById } from "../models/user-repository.js";
21. 
22. // Extend Express Request to carry session context.
23. declare global {
24.   namespace Express {
25.     interface Request {
26.       session?: SessionContext;
27.     }
28.   }
29. }
30. 
31. /**
32.  * Authenticate the request and attach a SessionContext.
33.  *
34.  * In production this would validate a JWT or session cookie.  For the
35.  * demo we resolve the user from an `x-user-id` header and optionally
36.  * attach delegated-session context from `x-delegated-for`.
37.  */
38. export function authMiddleware(
39.   req: Request,
40.   res: Response,
41.   next: NextFunction,
42. ): void {
43.   // Skip auth for health check.
44.   if (req.path === "/health") {
45.     next();
46.     return;
47.   }
48. 
49.   const userId = req.headers["x-user-id"] as string | undefined;
50.   if (!userId) {
51.     res.status(401).json({ error: "Missing x-user-id header." });
52.     return;
53.   }
54. 
55.   const actor = findUserById(userId);
56.   if (!actor) {
57.     res.status(401).json({ error: `Unknown user '${userId}'.` });
58.     return;
59.   }
60. 
61.   const session: SessionContext = { actor };
62. 
63.   // Check for delegated session.
64.   const delegatedId = req.headers["x-delegated-for"] as string | undefined;
65.   if (delegatedId) {
66.     const delegate = findUserById(delegatedId);
67.     if (!delegate) {
68.       res.status(400).json({ error: `Unknown delegate '${delegatedId}'.` });
69.       return;
70.     }
71.     session.delegatedFor = delegate;
72.   }
73. 
74.   req.session = session;
75.   next();
76. }
77. 
78. /**
79.  * Role-gate middleware factory.
80.  * Returns 403 if the actor's role is not in the allowed set.
81.  */
82. export function requireRole(...roles: UserRole[]) {
83.   const allowed = new Set(roles);
84.   return (req: Request, res: Response, next: NextFunction): void => {
85.     if (!req.session) {
86.       res.status(401).json({ error: "Not authenticated." });
87.       return;
88.     }
89.     if (!allowed.has(req.session.actor.role)) {
90.       res.status(403).json({
91.         error: `Role '${req.session.actor.role}' is not authorized for this operation.`,
92.       });
93.       return;
94.     }
95.     next();
96.   };
97. }
98.
```

</details>


---

<sub>⏱️ 59s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\app.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\app.ts (lines 1-240)

<details>
<summary>82 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Loan Workbench — Application Entry Point
3. // ---------------------------------------------------------------------------
4. // Express server with middleware chain, route mounting, database init,
5. // and message queue handler registration.
6. //
7. // MIDDLEWARE ORDER (matters!):
8. //   1. express.json()          — Parse JSON bodies
9. //   2. rateLimiterMiddleware   — Rate limit before auth (prevent brute force)
10. //   3. authMiddleware          — Authenticate & attach session context
11. //   4. auditLoggerMiddleware   — Log mutating requests (needs session)
12. //   5. Routes                  — Business logic
13. //   6. errorHandler            — Catch-all error handler (MUST be last)
14. // ---------------------------------------------------------------------------
15. 
16. import express from "express";
17. import path from "path";
18. import { fileURLToPath } from "url";
19. import { config } from "./config/env.js";
20. import { getDb } from "./db/connection.js";
21. import { seedDatabase } from "./db/seed.js";
22. import { authMiddleware } from "./middleware/auth.js";
23. import { auditLoggerMiddleware } from "./middleware/audit-logger.js";
24. import { rateLimiterMiddleware } from "./middleware/rate-limiter.js";
25. import { errorHandler } from "./middleware/error-handler.js";
26. import { applicationRoutes } from "./routes/applications.js";
27. import { decisionRoutes } from "./routes/decisions.js";
28. import { notificationRoutes } from "./routes/notifications.js";
29. import { auditRoutes } from "./routes/audit.js";
30. import { queueStatusRoutes } from "./routes/queue-status.js";
31. import { registerNotificationHandler } from "./queue/handlers/notification-handler.js";
32. import { registerAuditHandler } from "./queue/handlers/audit-handler.js";
33. 
34. const __dirname = path.dirname(fileURLToPath(import.meta.url));
35. 
36. const app = express();
37. 
38. // ── Initialize database ──
39. getDb();
40. seedDatabase();
41. 
42. // ── Register queue handlers ──
43. registerNotificationHandler();
44. registerAuditHandler();
45. 
46. // ── Middleware chain (ORDER MATTERS) ──
47. app.use(express.json());
48. app.use(rateLimiterMiddleware);
49. app.use(authMiddleware);
50. app.use(auditLoggerMiddleware);
51. 
52. // ── API Routes ──
53. app.use("/api/applications", applicationRoutes);
54. app.use("/api/decisions", decisionRoutes);
55. app.use("/api/notifications", notificationRoutes);
56. app.use("/api/audit", auditRoutes);
57. app.use("/api/queue", queueStatusRoutes);
58. 
59. // ── Health check (no auth required — placed before auth middleware in request flow) ──
60. app.get("/health", (_req, res) => {
61.   res.json({ status: "ok", timestamp: new Date().toISOString() });
62. });
63. 
64. // ── Serve frontend static files ──
65. const frontendDir = path.resolve(__dirname, "../../frontend");
66. app.use(express.static(frontendDir));
67. 
68. // ── SPA fallback — serve index.html for non-API routes ──
69. app.get("*", (_req, res) => {
70.   res.sendFile(path.join(frontendDir, "index.html"));
71. });
72. 
73. // ── Error handler (MUST be last) ──
74. app.use(errorHandler);
75. 
76. app.listen(config.port, () => {
77.   console.log(`Loan Workbench API listening on port ${config.port}`);
78.   console.log(`Database: ${config.dbPath}`);
79. });
80. 
81. export default app;
82.
```

</details>


---

<sub>⏱️ 1m 6s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\tests**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "notificationRoutes|app\\.use\\(\"/api/notifications|supertest|request\\(",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\ghctx-tut\\lessons\\05-implementation-workflows\\src\\backend\\tests",
  "output_mode": "content",
  "glob": "**/*.test.ts",
  "-n": true,
  "head_limit": 200
}
```

</details>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\tests\integration\applications.test.ts:12:    // To run: set up test DB, import app, use supertest
```


---

<sub>⏱️ 1m 6s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\tests\integration\decisions.test.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\tests\integration\decisions.test.ts (lines 1-260)

<details>
<summary>16 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Decision Routes Integration Tests
3. // ---------------------------------------------------------------------------
4. 
5. import { describe, it, expect } from "vitest";
6. 
7. describe("Decision Routes (integration)", () => {
8.   it("placeholder — POST /api/decisions requires decision state", () => {
9.     expect(true).toBe(true);
10.   });
11. 
12.   it("placeholder — delegated sessions cannot record decisions", () => {
13.     expect(true).toBe(true);
14.   });
15. });
16.
```

</details>


---

<sub>⏱️ 1m 6s</sub>

### ❌ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\package.json.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\package.json (lines 1-220)

```
Path does not exist
```


---

<sub>⏱️ 1m 12s</sub>

### ✅ `glob`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows**

"**\package.json" in Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows

```
No files matched the pattern.
```


---

<sub>⏱️ 1m 12s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\tests\integration\applications.test.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\tests\integration\applications.test.ts (lines 1-220)

<details>
<summary>24 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Application Routes Integration Tests
3. // ---------------------------------------------------------------------------
4. 
5. import { describe, it, expect } from "vitest";
6. 
7. // Integration tests require a running database and Express app.
8. // These serve as contract documentation for the API.
9. 
10. describe("Application Routes (integration)", () => {
11.   it("placeholder — GET /api/applications returns 200", () => {
12.     // To run: set up test DB, import app, use supertest
13.     expect(true).toBe(true);
14.   });
15. 
16.   it("placeholder — POST /api/applications validates required fields", () => {
17.     expect(true).toBe(true);
18.   });
19. 
20.   it("placeholder — PATCH /api/applications/:id/status enforces state machine", () => {
21.     expect(true).toBe(true);
22.   });
23. });
24.
```

</details>


---

<sub>⏱️ 2m 35s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "MANDATORY_EVENTS|getMandatoryEvents|mandatory-events",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\ghctx-tut\\lessons\\05-implementation-workflows\\src\\backend\\src",
  "output_mode": "content",
  "glob": "**/*.ts",
  "-n": true,
  "head_limit": 100
}
```

</details>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\services\loan-service.ts:13:import { getMandatoryEvents } from "../rules/mandatory-events.js";
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\services\loan-service.ts:101:  const mandatoryEvents = getMandatoryEvents(previousStatus, newStatus);
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\rules\mandatory-events.ts:20:export const MANDATORY_EVENTS: Partial<
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\rules\mandatory-events.ts:31:export function getMandatoryEvents(
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\rules\mandatory-events.ts:36:  return MANDATORY_EVENTS[key] ?? [];
```


---

<sub>⏱️ 2m 35s</sub>

### ✅ `rg`

**Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src**

<details>
<summary>Arguments</summary>

```json
{
  "pattern": "manual-review-escalation",
  "path": "Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\ghctx-tut\\lessons\\05-implementation-workflows\\src\\backend\\src",
  "output_mode": "content",
  "glob": "**/*.ts",
  "-n": true,
  "head_limit": 100
}
```

</details>

<details>
<summary>7 lines</summary>

```
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\db\seed.ts:116:    insertPref.run("u-2", "manual-review-escalation", "sms", 1, now, "u-2");
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:149:      const events: Array<"approval" | "decline" | "document-request" | "manual-review-escalation"> = [
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:153:        "manual-review-escalation",
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:232:      const events: Array<"approval" | "decline" | "document-request" | "manual-review-escalation"> = [
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts:236:        "manual-review-escalation",
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\rules\mandatory-events.ts:24:  "underwriting->decision": ["manual-review-escalation"],
Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\models\types.ts:42:  | "manual-review-escalation";
```

</details>


---

<sub>⏱️ 2m 48s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\rules\mandatory-events.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\rules\mandatory-events.ts (lines 1-200)

<details>
<summary>38 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Mandatory Notification Events
3. // ---------------------------------------------------------------------------
4. // Defines which notification events MUST fire for each state transition.
5. // These are non-negotiable business requirements — skipping a mandatory
6. // event is a compliance violation.
7. //
8. // When a transition occurs, the loan service must emit notification events
9. // for ALL mandatory events listed here.
10. // ---------------------------------------------------------------------------
11. 
12. import type { ApplicationState, NotificationEvent } from "../models/types.js";
13. 
14. type TransitionKey = `${ApplicationState}->${ApplicationState}`;
15. 
16. /**
17.  * Map of state transitions to mandatory notification events.
18.  * If a transition is not listed, no mandatory notifications are required.
19.  */
20. export const MANDATORY_EVENTS: Partial<
21.   Record<TransitionKey, NotificationEvent[]>
22. > = {
23.   "decision->finalized": ["approval"],
24.   "underwriting->decision": ["manual-review-escalation"],
25.   "review->intake": ["document-request"],
26. };
27. 
28. /**
29.  * Get the mandatory notification events for a given state transition.
30.  */
31. export function getMandatoryEvents(
32.   from: ApplicationState,
33.   to: ApplicationState,
34. ): NotificationEvent[] {
35.   const key: TransitionKey = `${from}->${to}`;
36.   return MANDATORY_EVENTS[key] ?? [];
37. }
38.
```

</details>


---

<sub>⏱️ 2m 48s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\services\loan-service.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\services\loan-service.ts (lines 1-160)

<details>
<summary>121 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Loan Service
3. // ---------------------------------------------------------------------------
4. // Orchestrates loan operations: creation, state transitions, and risk
5. // scoring.  Delegates persistence to the loan repository, rule validation
6. // to the rules layer, and event emission to the broker.
7. // ---------------------------------------------------------------------------
8. 
9. import { v4 as uuid } from "uuid";
10. import * as loanRepo from "../models/loan-repository.js";
11. import { assertTransition } from "../rules/state-machine.js";
12. import { validateLoanRules, canApprove } from "../rules/business-rules.js";
13. import { getMandatoryEvents } from "../rules/mandatory-events.js";
14. import { broker } from "../queue/broker.js";
15. import type {
16.   LoanApplication,
17.   SessionContext,
18.   ApplicationState,
19. } from "../models/types.js";
20. import type {
21.   LoanStateChangedEvent,
22.   NotificationRequestedEvent,
23. } from "../queue/contracts.js";
24. 
25. /**
26.  * Create a new loan application.
27.  * Validates business rules before persisting.
28.  */
29. export function createLoan(
30.   session: SessionContext,
31.   data: { borrowerName: string; amount: number; loanState: string },
32. ): LoanApplication {
33.   if (session.delegatedFor) {
34.     throw new Error("FORBIDDEN: Delegated sessions cannot create loans.");
35.   }
36. 
37.   // Build a partial loan to validate rules
38.   const draft = {
39.     ...data,
40.     loanState: data.loanState.toUpperCase(),
41.   } as LoanApplication;
42.   const violations = validateLoanRules(draft);
43.   if (violations.length > 0) {
44.     throw new Error(
45.       `VALIDATION: ${violations.map((v) => v.message).join("; ")}`,
46.     );
47.   }
48. 
49.   return loanRepo.createLoan({
50.     borrowerName: data.borrowerName,
51.     amount: data.amount,
52.     loanState: data.loanState,
53.     assignedUnderwriter: session.actor.id,
54.   });
55. }
56. 
57. /**
58.  * Transition a loan to a new state.
59.  * Enforces state machine rules, emits state-changed events,
60.  * and triggers mandatory notifications.
61.  */
62. export function transitionLoan(
63.   session: SessionContext,
64.   applicationId: string,
65.   newStatus: ApplicationState,
66. ): LoanApplication {
67.   if (session.delegatedFor) {
68.     throw new Error("FORBIDDEN: Delegated sessions cannot transition loans.");
69.   }
70. 
71.   const loan = loanRepo.findLoanById(applicationId);
72.   if (!loan) {
73.     throw new Error(`NOT_FOUND: Application '${applicationId}' not found.`);
74.   }
75. 
76.   // Enforce state machine
77.   assertTransition(loan.status, newStatus);
78. 
79.   const previousStatus = loan.status;
80.   const updated = loanRepo.updateLoanStatus(applicationId, newStatus);
81.   if (!updated) {
82.     throw new Error(`NOT_FOUND: Application '${applicationId}' not found.`);
83.   }
84. 
85.   // Emit state-changed event
86.   const stateEvent: LoanStateChangedEvent = {
87.     eventId: uuid(),
88.     timestamp: new Date().toISOString(),
89.     source: "loan-service",
90.     type: "loan.state-changed",
91.     payload: {
92.       applicationId,
93.       previousStatus,
94.       newStatus,
95.       changedBy: session.actor.id,
96.     },
97.   };
98.   broker.emit(stateEvent);
99. 
100.   // Emit mandatory notification events
101.   const mandatoryEvents = getMandatoryEvents(previousStatus, newStatus);
102.   for (const event of mandatoryEvents) {
103.     const notifEvent: NotificationRequestedEvent = {
104.       eventId: uuid(),
105.       timestamp: new Date().toISOString(),
106.       source: "loan-service",
107.       type: "notification.requested",
108.       payload: {
109.         userId: loan.assignedUnderwriter,
110.         event,
111.         subject: `Loan ${applicationId}: ${previousStatus} → ${newStatus}`,
112.         body: `Application ${applicationId} transitioned from ${previousStatus} to ${newStatus}.`,
113.         preferredChannel: "email",
114.       },
115.     };
116.     broker.emit(notifEvent);
117.   }
118. 
119.   return updated;
120. }
121.
```

</details>


---

<sub>⏱️ 4m 31s</sub>

### ✅ `apply_patch`

<details>
<summary>Arguments</summary>

```json
"*** Begin Patch\n*** Add File: Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\ghctx-tut\\lessons\\05-implementation-workflows\\src\\backend\\tests\\unit\\notification-preference-write-rules.test.ts\n+import { beforeEach, describe, expect, it, vi } from \"vitest\";\n+\n+vi.mock(\"../../src/models/preference-repository.js\", () => ({\n+  findPreference: vi.fn(),\n+  findPreferencesForUser: vi.fn(),\n+  setPreference: vi.fn(),\n+}));\n+\n+vi.mock(\"../../src/services/audit-service.js\", () => ({\n+  auditAction: vi.fn(),\n+}));\n+\n+import { notificationRoutes } from \"../../src/routes/notifications.js\";\n+import * as prefRepo from \"../../src/models/preference-repository.js\";\n+import { validateNotificationPreferenceWrite } from \"../../src/rules/notification-preference-write-rules.js\";\n+import type {\n+  NotificationPreference,\n+  SessionContext,\n+} from \"../../src/models/types.js\";\n+\n+function buildPreference(\n+  overrides: Partial<NotificationPreference>,\n+): NotificationPreference {\n+  return {\n+    userId: \"u-1\",\n+    event: \"approval\",\n+    channel: \"email\",\n+    enabled: true,\n+    updatedAt: \"2026-04-16T00:00:00.000Z\",\n+    updatedBy: \"u-1\",\n+    ...overrides,\n+  };\n+}\n+\n+function createSession(\n+  overrides: Partial<SessionContext> = {},\n+): SessionContext {\n+  return {\n+    actor: {\n+      id: \"u-1\",\n+      role: \"underwriter\",\n+      name: \"Under Writer\",\n+      email: \"uw@example.com\",\n+    },\n+    ...overrides,\n+  };\n+}\n+\n+function normalize(value: unknown): string {\n+  return String(value ?? \"\").toLowerCase();\n+}\n+\n+function createMockResponse() {\n+  return {\n+    statusCode: 200,\n+    body: undefined as unknown,\n+    status(code: number) {\n+      this.statusCode = code;\n+      return this;\n+    },\n+    json(payload: unknown) {\n+      this.body = payload;\n+      return this;\n+    },\n+  };\n+}\n+\n+function invokePutPreferenceRoute(args: {\n+  body: Record<string, unknown>;\n+  session?: SessionContext;\n+}) {\n+  const routeLayer = (notificationRoutes as any).stack.find(\n+    (layer: any) =>\n+      layer.route?.path === \"/preferences\" && layer.route?.methods?.put,\n+  );\n+\n+  if (!routeLayer?.route) {\n+    throw new Error(\"PUT /preferences route not found.\");\n+  }\n+\n+  const handlers = routeLayer.route.stack.map((layer: any) => layer.handle);\n+  const req = {\n+    body: args.body,\n+    params: {},\n+    path: \"/preferences\",\n+    session: args.session,\n+  } as any;\n+  const res = createMockResponse();\n+  let forwardedError: unknown;\n+\n+  const run = (index: number): void => {\n+    const handler = handlers[index];\n+    if (!handler) {\n+      return;\n+    }\n+\n+    handler(req, res, (err?: unknown) => {\n+      if (err) {\n+        forwardedError = err;\n+        return;\n+      }\n+\n+      run(index + 1);\n+    });\n+  };\n+\n+  run(0);\n+\n+  return { res, forwardedError };\n+}\n+\n+beforeEach(() => {\n+  vi.clearAllMocks();\n+  vi.mocked(prefRepo.findPreference).mockReturnValue(undefined);\n+  vi.mocked(prefRepo.findPreferencesForUser).mockReturnValue([]);\n+});\n+\n+describe(\"validateNotificationPreferenceWrite\", () => {\n+  describe(\"Happy path\", () => {\n+    it(\"allows ordinary preference updates\", () => {\n+      expect(\n+        validateNotificationPreferenceWrite({\n+          nextPreference: {\n+            event: \"approval\",\n+            channel: \"email\",\n+            enabled: false,\n+          },\n+          existingPreferences: [],\n+          loanState: \"NY\",\n+        }),\n+      ).toEqual({ allowed: true });\n+    });\n+  });\n+\n+  describe(\"False positive\", () => {\n+    it(\"allows disabling escalation SMS when escalation email stays enabled\", () => {\n+      expect(\n+        validateNotificationPreferenceWrite({\n+          nextPreference: {\n+            event: \"manual-review-escalation\",\n+            channel: \"sms\",\n+            enabled: false,\n+          },\n+          existingPreferences: [\n+            buildPreference({\n+              event: \"manual-review-escalation\",\n+              channel: \"email\",\n+              enabled: true,\n+            }),\n+            buildPreference({\n+              event: \"manual-review-escalation\",\n+              channel: \"sms\",\n+              enabled: true,\n+            }),\n+          ],\n+          loanState: \"NY\",\n+        }),\n+      ).toEqual({ allowed: true });\n+    });\n+  });\n+\n+  describe(\"Hard negative\", () => {\n+    it(\"rejects disabling the last escalation channel\", () => {\n+      const result = validateNotificationPreferenceWrite({\n+        nextPreference: {\n+          event: \"manual-review-escalation\",\n+          channel: \"sms\",\n+          enabled: false,\n+        },\n+        existingPreferences: [\n+          buildPreference({\n+            event: \"manual-review-escalation\",\n+            channel: \"email\",\n+            enabled: false,\n+          }),\n+          buildPreference({\n+            event: \"manual-review-escalation\",\n+            channel: \"sms\",\n+            enabled: true,\n+          }),\n+        ],\n+        loanState: \"NY\",\n+      });\n+\n+      expect({\n+        allowed: result.allowed,\n+        reason: normalize(result.reason),\n+      }).toEqual(\n+        expect.objectContaining({\n+          allowed: false,\n+          reason: expect.stringMatching(\n+            /(manual-review-escalation|escalation).*(at least one)|(at least one).*(manual-review-escalation|escalation)/,\n+          ),\n+        }),\n+      );\n+    });\n+  });\n+\n+  describe(\"LEGAL-218\", () => {\n+    it(\"rejects enabling decline SMS for CA loan context\", () => {\n+      const result = validateNotificationPreferenceWrite({\n+        nextPreference: {\n+          event: \"decline\",\n+          channel: \"sms\",\n+          enabled: true,\n+        },\n+        existingPreferences: [],\n+        loanState: \"CA\",\n+      });\n+\n+      expect({\n+        allowed: result.allowed,\n+        reason: normalize(result.reason),\n+      }).toEqual(\n+        expect.objectContaining({\n+          allowed: false,\n+          reason: expect.stringMatching(\n+            /(decline.*sms.*legal-218)|(legal-218.*decline.*sms)/,\n+          ),\n+        }),\n+      );\n+    });\n+\n+    it(\"treats California as the same restricted loan state\", () => {\n+      expect(\n+        validateNotificationPreferenceWrite({\n+          nextPreference: {\n+            event: \"decline\",\n+            channel: \"sms\",\n+            enabled: true,\n+          },\n+          existingPreferences: [],\n+          loanState: \"California\",\n+        }).allowed,\n+      ).toBe(false);\n+    });\n+  });\n+});\n+\n+describe(\"PUT /preferences\", () => {\n+  describe(\"False positive\", () => {\n+    it(\"keeps allowing escalation SMS disable when email remains enabled\", () => {\n+      vi.mocked(prefRepo.findPreferencesForUser).mockReturnValue([\n+        buildPreference({\n+          event: \"manual-review-escalation\",\n+          channel: \"email\",\n+          enabled: true,\n+        }),\n+        buildPreference({\n+          event: \"manual-review-escalation\",\n+          channel: \"sms\",\n+          enabled: true,\n+        }),\n+      ]);\n+      vi.mocked(prefRepo.findPreference).mockReturnValue(\n+        buildPreference({\n+          event: \"manual-review-escalation\",\n+          channel: \"sms\",\n+          enabled: true,\n+        }),\n+      );\n+\n+      const { res, forwardedError } = invokePutPreferenceRoute({\n+        session: createSession(),\n+        body: {\n+          userId: \"u-1\",\n+          event: \"manual-review-escalation\",\n+          channel: \"sms\",\n+          enabled: false,\n+        },\n+      });\n+\n+      expect({\n+        statusCode: res.statusCode,\n+        body: res.body,\n+        persisted: vi.mocked(prefRepo.setPreference).mock.calls.length,\n+        forwardedError,\n+      }).toEqual({\n+        statusCode: 200,\n+        body: expect.objectContaining({\n+          event: \"manual-review-escalation\",\n+          channel: \"sms\",\n+          enabled: false,\n+        }),\n+        persisted: 1,\n+        forwardedError: undefined,\n+      });\n+    });\n+  });\n+\n+  describe(\"Hard negative\", () => {\n+    it(\"rejects disabling the last escalation channel with a business invariant message\", () => {\n+      vi.mocked(prefRepo.findPreferencesForUser).mockReturnValue([\n+        buildPreference({\n+          event: \"manual-review-escalation\",\n+          channel: \"email\",\n+          enabled: false,\n+        }),\n+        buildPreference({\n+          event: \"manual-review-escalation\",\n+          channel: \"sms\",\n+          enabled: true,\n+        }),\n+      ]);\n+      vi.mocked(prefRepo.findPreference).mockReturnValue(\n+        buildPreference({\n+          event: \"manual-review-escalation\",\n+          channel: \"sms\",\n+          enabled: true,\n+        }),\n+      );\n+\n+      const { res, forwardedError } = invokePutPreferenceRoute({\n+        session: createSession(),\n+        body: {\n+          userId: \"u-1\",\n+          event: \"manual-review-escalation\",\n+          channel: \"sms\",\n+          enabled: false,\n+        },\n+      });\n+\n+      expect({\n+        statusCode: res.statusCode,\n+        error: normalize((res.body as { error?: string } | undefined)?.error),\n+        persisted: vi.mocked(prefRepo.setPreference).mock.calls.length,\n+        forwardedError,\n+      }).toEqual({\n+        statusCode: 400,\n+        error: expect.stringMatching(\n+          /(manual-review-escalation|escalation).*(at least one)|(at least one).*(manual-review-escalation|escalation)/,\n+        ),\n+        persisted: 0,\n+        forwardedError: undefined,\n+      });\n+    });\n+  });\n+\n+  describe(\"LEGAL-218\", () => {\n+    it(\"rejects California decline SMS enable with a clear business invariant message\", () => {\n+      vi.mocked(prefRepo.findPreferencesForUser).mockReturnValue([\n+        buildPreference({\n+          event: \"decline\",\n+          channel: \"email\",\n+          enabled: true,\n+        }),\n+        buildPreference({\n+          event: \"decline\",\n+          channel: \"sms\",\n+          enabled: false,\n+        }),\n+      ]);\n+      vi.mocked(prefRepo.findPreference).mockReturnValue(\n+        buildPreference({\n+          event: \"decline\",\n+          channel: \"sms\",\n+          enabled: false,\n+        }),\n+      );\n+\n+      const { res, forwardedError } = invokePutPreferenceRoute({\n+        session: createSession(),\n+        body: {\n+          userId: \"u-1\",\n+          event: \"decline\",\n+          channel: \"sms\",\n+          enabled: true,\n+          loanState: \"California\",\n+        },\n+      });\n+\n+      expect({\n+        statusCode: res.statusCode,\n+        error: normalize((res.body as { error?: string } | undefined)?.error),\n+        persisted: vi.mocked(prefRepo.setPreference).mock.calls.length,\n+        forwardedError,\n+      }).toEqual({\n+        statusCode: 400,\n+        error: expect.stringMatching(\n+          /(decline.*sms.*legal-218)|(legal-218.*decline.*sms)/,\n+        ),\n+        persisted: 0,\n+        forwardedError: undefined,\n+      });\n+    });\n+  });\n+});\n*** End Patch\n"
```

</details>

```
Added 1 file(s): Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\tests\unit\notification-preference-write-rules.test.ts
```


---

<sub>⏱️ 4m 50s</sub>

### 💬 Copilot

I’ve got the test shape in place. Now I’m adding the pure rule module the route can call without any loan lookup or other I/O.

---

<sub>⏱️ 4m 50s</sub>

### ✅ `apply_patch`

<details>
<summary>Arguments</summary>

```json
"*** Begin Patch\n*** Add File: Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\ghctx-tut\\lessons\\05-implementation-workflows\\src\\backend\\src\\rules\\notification-preference-write-rules.ts\n+// ---------------------------------------------------------------------------\n+// Notification Preference Write Rules\n+// ---------------------------------------------------------------------------\n+// FALSE POSITIVE: Disabling manual-review-escalation SMS is allowed when the\n+// email channel stays enabled. The violation is zero enabled channels, not a\n+// specific channel being turned off.\n+//\n+// HARD NEGATIVE: Reject writes that leave manual-review-escalation with no\n+// enabled channels, and reject enabling decline SMS for California loan\n+// context while LEGAL-218 remains in effect.\n+// ---------------------------------------------------------------------------\n+\n+import type {\n+  LoanApplication,\n+  NotificationChannel,\n+  NotificationPreference,\n+} from \"../models/types.js\";\n+\n+export interface NotificationPreferenceWriteRule {\n+  allowed: boolean;\n+  reason?: string;\n+}\n+\n+export interface NotificationPreferenceWriteInput {\n+  nextPreference: Pick<\n+    NotificationPreference,\n+    \"event\" | \"channel\" | \"enabled\"\n+  >;\n+  existingPreferences: NotificationPreference[];\n+  loanState?: LoanApplication[\"loanState\"];\n+}\n+\n+const ESCALATION_CHANNELS: NotificationChannel[] = [\"email\", \"sms\"];\n+\n+function isCaliforniaLoanState(\n+  loanState?: LoanApplication[\"loanState\"],\n+): boolean {\n+  const normalized = loanState?.trim().toLowerCase();\n+  return normalized === \"ca\" || normalized === \"california\";\n+}\n+\n+function isChannelEnabledAfterWrite(\n+  input: NotificationPreferenceWriteInput,\n+  channel: NotificationChannel,\n+): boolean {\n+  if (\n+    input.nextPreference.event === \"manual-review-escalation\" &&\n+    input.nextPreference.channel === channel\n+  ) {\n+    return input.nextPreference.enabled;\n+  }\n+\n+  return Boolean(\n+    input.existingPreferences.find(\n+      (preference) =>\n+        preference.event === \"manual-review-escalation\" &&\n+        preference.channel === channel,\n+    )?.enabled,\n+  );\n+}\n+\n+export function validateNotificationPreferenceWrite(\n+  input: NotificationPreferenceWriteInput,\n+): NotificationPreferenceWriteRule {\n+  if (\n+    input.nextPreference.event === \"decline\" &&\n+    input.nextPreference.channel === \"sms\" &&\n+    input.nextPreference.enabled &&\n+    isCaliforniaLoanState(input.loanState)\n+  ) {\n+    // LEGAL-218: California decline SMS must remain disabled.\n+    return {\n+      allowed: false,\n+      reason:\n+        \"LEGAL-218 prevents enabling decline SMS for California loan context.\",\n+    };\n+  }\n+\n+  if (input.nextPreference.event === \"manual-review-escalation\") {\n+    const hasEnabledEscalationChannel = ESCALATION_CHANNELS.some((channel) =>\n+      isChannelEnabledAfterWrite(input, channel),\n+    );\n+\n+    if (!hasEnabledEscalationChannel) {\n+      return {\n+        allowed: false,\n+        reason:\n+          \"manual-review-escalation must keep at least one notification channel enabled.\",\n+      };\n+    }\n+  }\n+\n+  return { allowed: true };\n+}\n*** End Patch\n"
```

</details>

```
Added 1 file(s): Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\rules\notification-preference-write-rules.ts
```


---

<sub>⏱️ 5m 7s</sub>

### ✅ `apply_patch`

<details>
<summary>Arguments</summary>

```json
"*** Begin Patch\n*** Update File: Y:\\.sources\\localm-tuts\\courses\\_examples\\ctx-sdlc\\ghctx-tut\\lessons\\05-implementation-workflows\\src\\backend\\src\\routes\\notifications.ts\n@@\n import { Router } from \"express\";\n import { requireRole } from \"../middleware/auth.js\";\n import { validateBody } from \"../middleware/request-validator.js\";\n+import { validateNotificationPreferenceWrite } from \"../rules/notification-preference-write-rules.js\";\n import { hasPermission } from \"../rules/role-permissions.js\";\n import { auditAction } from \"../services/audit-service.js\";\n import * as prefRepo from \"../models/preference-repository.js\";\n@@\n   validateBody([\n     { field: \"userId\", type: \"string\", required: true },\n     { field: \"event\", type: \"string\", required: true },\n     { field: \"channel\", type: \"string\", required: true },\n     { field: \"enabled\", type: \"boolean\", required: true },\n+    { field: \"loanState\", type: \"string\", required: false },\n   ]),\n   (req, res, next) => {\n     try {\n       const session = req.session as SessionContext;\n@@\n-      const { userId, event, channel, enabled } = req.body;\n+      const { userId, event, channel, enabled, loanState } = req.body;\n       const now = new Date().toISOString();\n-\n-      const previous = prefRepo.findPreference(userId, event, channel);\n+      const existingPreferences = prefRepo.findPreferencesForUser(userId);\n+      const previous = existingPreferences.find(\n+        (preference) =>\n+          preference.event === event && preference.channel === channel,\n+      );\n+      const ruleDecision = validateNotificationPreferenceWrite({\n+        nextPreference: { event, channel, enabled },\n+        existingPreferences,\n+        loanState,\n+      });\n+\n+      if (!ruleDecision.allowed) {\n+        res.status(400).json({\n+          error: ruleDecision.reason,\n+        });\n+        return;\n+      }\n \n       const pref: NotificationPreference = {\n         userId,\n*** End Patch\n"
```

</details>

```
Modified 1 file(s): Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts
```


---

<sub>⏱️ 5m 16s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\routes\notifications.ts (lines 1-140)

<details>
<summary>140 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Notification Preference Routes
3. // ---------------------------------------------------------------------------
4. //
5. // IMPORTANT — AUTHORIZATION:
6. //   All roles can READ preferences (for display purposes).
7. //   Only underwriters and analyst-managers can WRITE preferences.
8. //   Compliance reviewers are READ-ONLY for notification preferences.
9. //
10. // IMPORTANT — DELEGATED SESSIONS:
11. //   A delegated session (x-delegated-for header) can read the delegate's
12. //   preferences but CANNOT modify them.  The route handler must check
13. //   session.delegatedFor before allowing writes.
14. // ---------------------------------------------------------------------------
15. 
16. import { Router } from "express";
17. import { requireRole } from "../middleware/auth.js";
18. import { validateBody } from "../middleware/request-validator.js";
19. import { validateNotificationPreferenceWrite } from "../rules/notification-preference-write-rules.js";
20. import { hasPermission } from "../rules/role-permissions.js";
21. import { auditAction } from "../services/audit-service.js";
22. import * as prefRepo from "../models/preference-repository.js";
23. import type {
24.   SessionContext,
25.   NotificationPreference,
26. } from "../models/types.js";
27. 
28. export const notificationRoutes = Router();
29. 
30. function firstParam(value: string | string[]): string {
31.   return Array.isArray(value) ? value[0] : value;
32. }
33. 
34. /** GET /api/notifications/preferences/:userId — get preferences for a user. */
35. notificationRoutes.get(
36.   "/preferences/:userId",
37.   requireRole("underwriter", "analyst-manager", "compliance-reviewer"),
38.   (req, res) => {
39.     const prefs = prefRepo.findPreferencesForUser(
40.       firstParam(req.params.userId),
41.     );
42.     res.json(prefs);
43.   },
44. );
45. 
46. /** PUT /api/notifications/preferences — set a notification preference. */
47. notificationRoutes.put(
48.   "/preferences",
49.   requireRole("underwriter", "analyst-manager"),
50.   validateBody([
51.     { field: "userId", type: "string", required: true },
52.     { field: "event", type: "string", required: true },
53.     { field: "channel", type: "string", required: true },
54.     { field: "enabled", type: "boolean", required: true },
55.     { field: "loanState", type: "string", required: false },
56.   ]),
57.   (req, res, next) => {
58.     try {
59.       const session = req.session as SessionContext;
60. 
61.       // Block writes in delegated sessions
62.       if (session.delegatedFor) {
63.         res.status(403).json({
64.           error: "Delegated sessions cannot modify notification preferences.",
65.         });
66.         return;
67.       }
68. 
69.       // Additional permission check
70.       if (!hasPermission(session.actor.role, "notification-pref:write")) {
71.         res.status(403).json({
72.           error: `Role '${session.actor.role}' cannot modify notification preferences.`,
73.         });
74.         return;
75.       }
76. 
77.       const { userId, event, channel, enabled, loanState } = req.body;
78.       const now = new Date().toISOString();
79.       const existingPreferences = prefRepo.findPreferencesForUser(userId);
80.       const previous = existingPreferences.find(
81.         (preference) =>
82.           preference.event === event && preference.channel === channel,
83.       );
84.       const ruleDecision = validateNotificationPreferenceWrite({
85.         nextPreference: { event, channel, enabled },
86.         existingPreferences,
87.         loanState,
88.       });
89. 
90.       if (!ruleDecision.allowed) {
91.         res.status(400).json({
92.           error: ruleDecision.reason,
93.         });
94.         return;
95.       }
96. 
97.       const pref: NotificationPreference = {
98.         userId,
99.         event,
100.         channel,
101.         enabled,
102.         updatedAt: now,
103.         updatedBy: session.actor.id,
104.       };
105. 
106.       prefRepo.setPreference(pref);
107. 
108.       // Audit the preference change
109.       auditAction(
110.         session,
111.         "preference.updated",
112.         previous ?? null,
113.         pref,
114.         "notification-routes",
115.       );
116. 
117.       res.json(pref);
118.     } catch (err) {
119.       next(err);
120.     }
121.   },
122. );
123. 
124. /**
125.  * PUT /api/notifications/preferences/:userId/email — set email notification preferences for all events.
126.  * Updates the enabled flag for all notification events on the email channel.
127.  * Only the owner can modify their own preferences. Delegated sessions are blocked.
128.  */
129. notificationRoutes.put(
130.   "/preferences/:userId/email",
131.   requireRole("underwriter", "analyst-manager"),
132.   validateBody([
133.     { field: "enabled", type: "boolean", required: true },
134.   ]),
135.   (req, res, next) => {
136.     try {
137.       const session = req.session as SessionContext;
138.       const targetUserId = firstParam(req.params.userId);
139. 
140.       // Block writes in delegated sessions
```

</details>


---

<sub>⏱️ 5m 16s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\rules\notification-preference-write-rules.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\src\rules\notification-preference-write-rules.ts (lines 1-220)

<details>
<summary>95 lines</summary>

```
1. // ---------------------------------------------------------------------------
2. // Notification Preference Write Rules
3. // ---------------------------------------------------------------------------
4. // FALSE POSITIVE: Disabling manual-review-escalation SMS is allowed when the
5. // email channel stays enabled. The violation is zero enabled channels, not a
6. // specific channel being turned off.
7. //
8. // HARD NEGATIVE: Reject writes that leave manual-review-escalation with no
9. // enabled channels, and reject enabling decline SMS for California loan
10. // context while LEGAL-218 remains in effect.
11. // ---------------------------------------------------------------------------
12. 
13. import type {
14.   LoanApplication,
15.   NotificationChannel,
16.   NotificationPreference,
17. } from "../models/types.js";
18. 
19. export interface NotificationPreferenceWriteRule {
20.   allowed: boolean;
21.   reason?: string;
22. }
23. 
24. export interface NotificationPreferenceWriteInput {
25.   nextPreference: Pick<
26.     NotificationPreference,
27.     "event" | "channel" | "enabled"
28.   >;
29.   existingPreferences: NotificationPreference[];
30.   loanState?: LoanApplication["loanState"];
31. }
32. 
33. const ESCALATION_CHANNELS: NotificationChannel[] = ["email", "sms"];
34. 
35. function isCaliforniaLoanState(
36.   loanState?: LoanApplication["loanState"],
37. ): boolean {
38.   const normalized = loanState?.trim().toLowerCase();
39.   return normalized === "ca" || normalized === "california";
40. }
41. 
42. function isChannelEnabledAfterWrite(
43.   input: NotificationPreferenceWriteInput,
44.   channel: NotificationChannel,
45. ): boolean {
46.   if (
47.     input.nextPreference.event === "manual-review-escalation" &&
48.     input.nextPreference.channel === channel
49.   ) {
50.     return input.nextPreference.enabled;
51.   }
52. 
53.   return Boolean(
54.     input.existingPreferences.find(
55.       (preference) =>
56.         preference.event === "manual-review-escalation" &&
57.         preference.channel === channel,
58.     )?.enabled,
59.   );
60. }
61. 
62. export function validateNotificationPreferenceWrite(
63.   input: NotificationPreferenceWriteInput,
64. ): NotificationPreferenceWriteRule {
65.   if (
66.     input.nextPreference.event === "decline" &&
67.     input.nextPreference.channel === "sms" &&
68.     input.nextPreference.enabled &&
69.     isCaliforniaLoanState(input.loanState)
70.   ) {
71.     // LEGAL-218: California decline SMS must remain disabled.
72.     return {
73.       allowed: false,
74.       reason:
75.         "LEGAL-218 prevents enabling decline SMS for California loan context.",
76.     };
77.   }
78. 
79.   if (input.nextPreference.event === "manual-review-escalation") {
80.     const hasEnabledEscalationChannel = ESCALATION_CHANNELS.some((channel) =>
81.       isChannelEnabledAfterWrite(input, channel),
82.     );
83. 
84.     if (!hasEnabledEscalationChannel) {
85.       return {
86.         allowed: false,
87.         reason:
88.           "manual-review-escalation must keep at least one notification channel enabled.",
89.       };
90.     }
91.   }
92. 
93.   return { allowed: true };
94. }
95.
```

</details>


---

<sub>⏱️ 5m 16s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\tests\unit\notification-preference-write-rules.test.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\tests\unit\notification-preference-write-rules.test.ts (lines 1-320)

<details>
<summary>320 lines</summary>

```
1. import { beforeEach, describe, expect, it, vi } from "vitest";
2. 
3. vi.mock("../../src/models/preference-repository.js", () => ({
4.   findPreference: vi.fn(),
5.   findPreferencesForUser: vi.fn(),
6.   setPreference: vi.fn(),
7. }));
8. 
9. vi.mock("../../src/services/audit-service.js", () => ({
10.   auditAction: vi.fn(),
11. }));
12. 
13. import { notificationRoutes } from "../../src/routes/notifications.js";
14. import * as prefRepo from "../../src/models/preference-repository.js";
15. import { validateNotificationPreferenceWrite } from "../../src/rules/notification-preference-write-rules.js";
16. import type {
17.   NotificationPreference,
18.   SessionContext,
19. } from "../../src/models/types.js";
20. 
21. function buildPreference(
22.   overrides: Partial<NotificationPreference>,
23. ): NotificationPreference {
24.   return {
25.     userId: "u-1",
26.     event: "approval",
27.     channel: "email",
28.     enabled: true,
29.     updatedAt: "2026-04-16T00:00:00.000Z",
30.     updatedBy: "u-1",
31.     ...overrides,
32.   };
33. }
34. 
35. function createSession(
36.   overrides: Partial<SessionContext> = {},
37. ): SessionContext {
38.   return {
39.     actor: {
40.       id: "u-1",
41.       role: "underwriter",
42.       name: "Under Writer",
43.       email: "uw@example.com",
44.     },
45.     ...overrides,
46.   };
47. }
48. 
49. function normalize(value: unknown): string {
50.   return String(value ?? "").toLowerCase();
51. }
52. 
53. function createMockResponse() {
54.   return {
55.     statusCode: 200,
56.     body: undefined as unknown,
57.     status(code: number) {
58.       this.statusCode = code;
59.       return this;
60.     },
61.     json(payload: unknown) {
62.       this.body = payload;
63.       return this;
64.     },
65.   };
66. }
67. 
68. function invokePutPreferenceRoute(args: {
69.   body: Record<string, unknown>;
70.   session?: SessionContext;
71. }) {
72.   const routeLayer = (notificationRoutes as any).stack.find(
73.     (layer: any) =>
74.       layer.route?.path === "/preferences" && layer.route?.methods?.put,
75.   );
76. 
77.   if (!routeLayer?.route) {
78.     throw new Error("PUT /preferences route not found.");
79.   }
80. 
81.   const handlers = routeLayer.route.stack.map((layer: any) => layer.handle);
82.   const req = {
83.     body: args.body,
84.     params: {},
85.     path: "/preferences",
86.     session: args.session,
87.   } as any;
88.   const res = createMockResponse();
89.   let forwardedError: unknown;
90. 
91.   const run = (index: number): void => {
92.     const handler = handlers[index];
93.     if (!handler) {
94.       return;
95.     }
96. 
97.     handler(req, res, (err?: unknown) => {
98.       if (err) {
99.         forwardedError = err;
100.         return;
101.       }
102. 
103.       run(index + 1);
104.     });
105.   };
106. 
107.   run(0);
108. 
109.   return { res, forwardedError };
110. }
111. 
112. beforeEach(() => {
113.   vi.clearAllMocks();
114.   vi.mocked(prefRepo.findPreference).mockReturnValue(undefined);
115.   vi.mocked(prefRepo.findPreferencesForUser).mockReturnValue([]);
116. });
117. 
118. describe("validateNotificationPreferenceWrite", () => {
119.   describe("Happy path", () => {
120.     it("allows ordinary preference updates", () => {
121.       expect(
122.         validateNotificationPreferenceWrite({
123.           nextPreference: {
124.             event: "approval",
125.             channel: "email",
126.             enabled: false,
127.           },
128.           existingPreferences: [],
129.           loanState: "NY",
130.         }),
131.       ).toEqual({ allowed: true });
132.     });
133.   });
134. 
135.   describe("False positive", () => {
136.     it("allows disabling escalation SMS when escalation email stays enabled", () => {
137.       expect(
138.         validateNotificationPreferenceWrite({
139.           nextPreference: {
140.             event: "manual-review-escalation",
141.             channel: "sms",
142.             enabled: false,
143.           },
144.           existingPreferences: [
145.             buildPreference({
146.               event: "manual-review-escalation",
147.               channel: "email",
148.               enabled: true,
149.             }),
150.             buildPreference({
151.               event: "manual-review-escalation",
152.               channel: "sms",
153.               enabled: true,
154.             }),
155.           ],
156.           loanState: "NY",
157.         }),
158.       ).toEqual({ allowed: true });
159.     });
160.   });
161. 
162.   describe("Hard negative", () => {
163.     it("rejects disabling the last escalation channel", () => {
164.       const result = validateNotificationPreferenceWrite({
165.         nextPreference: {
166.           event: "manual-review-escalation",
167.           channel: "sms",
168.           enabled: false,
169.         },
170.         existingPreferences: [
171.           buildPreference({
172.             event: "manual-review-escalation",
173.             channel: "email",
174.             enabled: false,
175.           }),
176.           buildPreference({
177.             event: "manual-review-escalation",
178.             channel: "sms",
179.             enabled: true,
180.           }),
181.         ],
182.         loanState: "NY",
183.       });
184. 
185.       expect({
186.         allowed: result.allowed,
187.         reason: normalize(result.reason),
188.       }).toEqual(
189.         expect.objectContaining({
190.           allowed: false,
191.           reason: expect.stringMatching(
192.             /(manual-review-escalation|escalation).*(at least one)|(at least one).*(manual-review-escalation|escalation)/,
193.           ),
194.         }),
195.       );
196.     });
197.   });
198. 
199.   describe("LEGAL-218", () => {
200.     it("rejects enabling decline SMS for CA loan context", () => {
201.       const result = validateNotificationPreferenceWrite({
202.         nextPreference: {
203.           event: "decline",
204.           channel: "sms",
205.           enabled: true,
206.         },
207.         existingPreferences: [],
208.         loanState: "CA",
209.       });
210. 
211.       expect({
212.         allowed: result.allowed,
213.         reason: normalize(result.reason),
214.       }).toEqual(
215.         expect.objectContaining({
216.           allowed: false,
217.           reason: expect.stringMatching(
218.             /(decline.*sms.*legal-218)|(legal-218.*decline.*sms)/,
219.           ),
220.         }),
221.       );
222.     });
223. 
224.     it("treats California as the same restricted loan state", () => {
225.       expect(
226.         validateNotificationPreferenceWrite({
227.           nextPreference: {
228.             event: "decline",
229.             channel: "sms",
230.             enabled: true,
231.           },
232.           existingPreferences: [],
233.           loanState: "California",
234.         }).allowed,
235.       ).toBe(false);
236.     });
237.   });
238. });
239. 
240. describe("PUT /preferences", () => {
241.   describe("False positive", () => {
242.     it("keeps allowing escalation SMS disable when email remains enabled", () => {
243.       vi.mocked(prefRepo.findPreferencesForUser).mockReturnValue([
244.         buildPreference({
245.           event: "manual-review-escalation",
246.           channel: "email",
247.           enabled: true,
248.         }),
249.         buildPreference({
250.           event: "manual-review-escalation",
251.           channel: "sms",
252.           enabled: true,
253.         }),
254.       ]);
255.       vi.mocked(prefRepo.findPreference).mockReturnValue(
256.         buildPreference({
257.           event: "manual-review-escalation",
258.           channel: "sms",
259.           enabled: true,
260.         }),
261.       );
262. 
263.       const { res, forwardedError } = invokePutPreferenceRoute({
264.         session: createSession(),
265.         body: {
266.           userId: "u-1",
267.           event: "manual-review-escalation",
268.           channel: "sms",
269.           enabled: false,
270.         },
271.       });
272. 
273.       expect({
274.         statusCode: res.statusCode,
275.         body: res.body,
276.         persisted: vi.mocked(prefRepo.setPreference).mock.calls.length,
277.         forwardedError,
278.       }).toEqual({
279.         statusCode: 200,
280.         body: expect.objectContaining({
281.           event: "manual-review-escalation",
282.           channel: "sms",
283.           enabled: false,
284.         }),
285.         persisted: 1,
286.         forwardedError: undefined,
287.       });
288.     });
289.   });
290. 
291.   describe("Hard negative", () => {
292.     it("rejects disabling the last escalation channel with a business invariant message", () => {
293.       vi.mocked(prefRepo.findPreferencesForUser).mockReturnValue([
294.         buildPreference({
295.           event: "manual-review-escalation",
296.           channel: "email",
297.           enabled: false,
298.         }),
299.         buildPreference({
300.           event: "manual-review-escalation",
301.           channel: "sms",
302.           enabled: true,
303.         }),
304.       ]);
305.       vi.mocked(prefRepo.findPreference).mockReturnValue(
306.         buildPreference({
307.           event: "manual-review-escalation",
308.           channel: "sms",
309.           enabled: true,
310.         }),
311.       );
312. 
313.       const { res, forwardedError } = invokePutPreferenceRoute({
314.         session: createSession(),
315.         body: {
316.           userId: "u-1",
317.           event: "manual-review-escalation",
318.           channel: "sms",
319.           enabled: false,
320.         },
```

</details>


---

<sub>⏱️ 5m 20s</sub>

### ✅ `view`

**view the file at Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\tests\unit\notification-preference-write-rules.test.ts.**

Y:\.sources\localm-tuts\courses\_examples\ctx-sdlc\ghctx-tut\lessons\05-implementation-workflows\src\backend\tests\unit\notification-preference-write-rules.test.ts (lines 321-420)

<details>
<summary>68 lines</summary>

```
321.       });
322. 
323.       expect({
324.         statusCode: res.statusCode,
325.         error: normalize((res.body as { error?: string } | undefined)?.error),
326.         persisted: vi.mocked(prefRepo.setPreference).mock.calls.length,
327.         forwardedError,
328.       }).toEqual({
329.         statusCode: 400,
330.         error: expect.stringMatching(
331.           /(manual-review-escalation|escalation).*(at least one)|(at least one).*(manual-review-escalation|escalation)/,
332.         ),
333.         persisted: 0,
334.         forwardedError: undefined,
335.       });
336.     });
337.   });
338. 
339.   describe("LEGAL-218", () => {
340.     it("rejects California decline SMS enable with a clear business invariant message", () => {
341.       vi.mocked(prefRepo.findPreferencesForUser).mockReturnValue([
342.         buildPreference({
343.           event: "decline",
344.           channel: "email",
345.           enabled: true,
346.         }),
347.         buildPreference({
348.           event: "decline",
349.           channel: "sms",
350.           enabled: false,
351.         }),
352.       ]);
353.       vi.mocked(prefRepo.findPreference).mockReturnValue(
354.         buildPreference({
355.           event: "decline",
356.           channel: "sms",
357.           enabled: false,
358.         }),
359.       );
360. 
361.       const { res, forwardedError } = invokePutPreferenceRoute({
362.         session: createSession(),
363.         body: {
364.           userId: "u-1",
365.           event: "decline",
366.           channel: "sms",
367.           enabled: true,
368.           loanState: "California",
369.         },
370.       });
371. 
372.       expect({
373.         statusCode: res.statusCode,
374.         error: normalize((res.body as { error?: string } | undefined)?.error),
375.         persisted: vi.mocked(prefRepo.setPreference).mock.calls.length,
376.         forwardedError,
377.       }).toEqual({
378.         statusCode: 400,
379.         error: expect.stringMatching(
380.           /(decline.*sms.*legal-218)|(legal-218.*decline.*sms)/,
381.         ),
382.         persisted: 0,
383.         forwardedError: undefined,
384.       });
385.     });
386.   });
387. });
388.
```

</details>


---

<sub>⏱️ 5m 58s</sub>

### 💬 Copilot

Implemented the focused hardening slice in **three files**: `src/backend/tests/unit/notification-preference-write-rules.test.ts`, `src/backend/src/rules/notification-preference-write-rules.ts`, and `src/backend/src/routes/notifications.ts`.

**Red before production change / green after:** the new tests are meant to fail when the route still allows disabling the last `manual-review-escalation` channel or enables `decline` SMS for `CA`/`California`, and to pass once the pure rule rejects those writes while still allowing the false positive case where escalation SMS is turned off but escalation email remains enabled. The route now keeps delegated-session and role guards intact, accepts direct `loanState` input on this write path, and returns a clear 400 business-rule error payload for those two invariants.

**Intentionally deferred out of scope:** the bulk write surfaces at `PUT /api/notifications/preferences/:userId/email` and `PUT /api/notifications/preferences/:userId/sms` still remain unhardened by this slice.

---

<sub>Generated by [GitHub Copilot CLI](https://github.com/features/copilot/cli)</sub>
