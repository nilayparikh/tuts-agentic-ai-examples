# Lesson 09 — AI-Assisted SDLC Capstone — Run Analysis

> **Session ID:** `35d07442-2296-471f-a324-415461eec70a`
> **Started:** 14/03/2026, 17:13:27 · **Duration:** 3m 57s
> **Model:** GPT-5.4 · **Reasoning:** medium

---

## 1. Thinking Trajectory

```mermaid
flowchart TD
    A[Receive prompt] --> B[Discover project context]
    B --> C[view repo root + glob × 2: .github, architecture]
    C --> D[rg: notification/preference/LEGAL-218/mandatory patterns]
    D --> E[💬 Copilot: Mapping capstone guidance and notification flow]
    E --> F[view × 5: copilot-instructions, api.instructions, frontend.instructions, architecture, capstone-example]
    F --> G[💬 Copilot: Now mapping notification backend surfaces]
    G --> H[glob × 5: rules, routes, models, tests, services]
    H --> I[rg × 2: mandatory events + notification preference patterns]
    I --> J[💬 Copilot: Scanning implementation surfaces in detail]
    J --> K[view × 12: rules, routes, models, services, existing tests]
    K --> L[💬 Copilot: Found the gap — no event-channel validator exists]
    L --> M[store_memory: session plan]
    M --> N[apply_patch 1: create validator + tests + route wiring]
    N --> O[💬 Copilot: Spot-checking for TS issues]
    O --> P[view × 6: read-back created/modified files]
    P --> Q[💬 Copilot: Tighten Object.values().flat() typing]
    Q --> R[apply_patch 2: fix .flat() → .flatMap() with filter]
    R --> S[view × 4: re-check modified surfaces]
    S --> T[💬 Copilot: Route has no loan-state context — make validator conservative]
    T --> U[apply_patch 3: rename isCaliforniaLoan → isCaliforniaRestrictedContext, default to true]
    U --> V[apply_patch 4: add explanatory comment]
    V --> W[💬 Final summary]
```

## 2. Context at Each Stage

| Phase                    | Time          | Context Loaded                                                                                                                                                         | Purpose                                                                                                |
| ------------------------ | ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| **Surface discovery**    | 0s–21s        | `view` root, 2× `glob`, 1× `rg`                                                                                                                                        | Map .github, architecture, notification surfaces                                                       |
| **Instruction reading**  | 21s–50s       | 5× `view`: copilot-instructions, api.instructions, frontend.instructions, architecture, capstone-example                                                               | Load project conventions, scoped rules, architecture doc, lesson constraints                           |
| **Backend mapping**      | 50s–1m 23s    | 5× `glob` + 2× `rg` + 2× `glob` follow-ups                                                                                                                             | Discover rules, routes, models, tests, services; search for mandatory events and notification patterns |
| **Deep source reading**  | 1m 23s–2m 36s | 12× `view`: mandatory-events.ts, role-permissions.ts, business-rules.ts, notifications.ts, notification-service.ts, preference-repository.ts, types.ts, existing tests | Understand existing rule patterns, route wiring, model types, test conventions                         |
| **Planning**             | 2m 36s–3m 5s  | More views of route/preference shapes + session plan                                                                                                                   | Finalize implementation plan                                                                           |
| **Implementation**       | 3m 5s–3m 13s  | `apply_patch` 1: create 2 files + modify 1                                                                                                                             | Core validator + tests + route wiring                                                                  |
| **Verification + fixes** | 3m 13s–3m 57s | Views, 3× `apply_patch` (type fix, conservative rename, comment)                                                                                                       | Self-corrections for TS typing and route-shape alignment                                               |

## 3. Tool Calls Timeline

| #     | Tool              | Target                                                                      | Result                            |
| ----- | ----------------- | --------------------------------------------------------------------------- | --------------------------------- |
| 1     | `view`            | Repo root directory listing                                                 | 7 items                           |
| 2     | `glob`            | `.github/**/*.md`                                                           | 3 instruction files               |
| 3     | `glob`            | `**/architecture*.md`                                                       | 1 architecture doc                |
| 4     | `rg`              | notification/preference/LEGAL-218/mandatory                                 | Multi-file matches                |
| 5     | `view`            | `.github/copilot-instructions.md`                                           | Project-wide conventions          |
| 6     | `view`            | `.github/instructions/api.instructions.md`                                  | Backend API patterns              |
| 7     | `view`            | `.github/instructions/frontend.instructions.md`                             | Frontend patterns                 |
| 8     | `view`            | `docs/architecture.md`                                                      | System architecture               |
| 9     | `view`            | `docs/capstone-example.md`                                                  | Lesson constraints                |
| 10–14 | `glob` × 5        | rules/, routes/, models/, tests/, services/                                 | Backend file inventory            |
| 15–16 | `rg` × 2          | mandatory events, notification patterns                                     | Pattern search                    |
| 17    | `view`            | `src/backend/src/rules/mandatory-events.ts`                                 | Mandatory event definitions       |
| 18    | `view`            | `src/backend/src/rules/role-permissions.ts`                                 | Role permission patterns          |
| 19    | `view`            | `src/backend/src/rules/business-rules.ts`                                   | Business rule patterns            |
| 20    | `view`            | `src/backend/src/routes/notifications.ts`                                   | Current route (target for wiring) |
| 21    | `view`            | `src/backend/src/services/notification-service.ts`                          | Service layer                     |
| 22    | `view`            | `src/backend/src/models/preference-repository.ts`                           | Data access layer                 |
| 23    | `view`            | `src/backend/src/models/types.ts`                                           | Domain types                      |
| 24–26 | `view` × 3        | Existing test files                                                         | Test conventions                  |
| 27–28 | `view` × 2 + `rg` | Additional route/model details                                              | Gap analysis                      |
| 29    | `apply_patch`     | Session plan                                                                | Created                           |
| 30    | `apply_patch`     | **Core implementation**: validator.ts, tests, route wiring                  | 2 created + 1 modified            |
| 31–36 | `view` × 6        | Read-back all changed files                                                 | Verification pass                 |
| 37    | `apply_patch`     | Fix `.flat()` → `.flatMap()` with type guard                                | TS type safety                    |
| 38–39 | `view` × 2        | Re-verify typing                                                            | Check                             |
| 40    | `apply_patch`     | Rename `isCaliforniaLoan` → `isCaliforniaRestrictedContext`, default `true` | Route-shape alignment             |
| 41    | `apply_patch`     | Add explanatory comment for conservative default                            | Documentation                     |

**Total: ~41 tool calls per session summary** → actually **~77 including parallel batches** (10 glob, 4 rg, ~50 view, 4 apply_patch, 1 store_memory)

## 4. Assumptions & Decisions

| #   | Decision                                                                                         | Validation                                                                               |
| --- | ------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| 1   | Imported `MANDATORY_EVENTS` from existing `mandatory-events.ts`                                  | ✅ Reuses established rule surface                                                       |
| 2   | Created pure validation function (no I/O) in `rules/`                                            | ✅ Matches project's rules = pure business logic convention                              |
| 3   | Used `NotificationChannel` and `NotificationEvent` types from `models/types.ts`                  | ✅ No ad-hoc type definitions                                                            |
| 4   | Wired validator into route before persistence/audit                                              | ✅ Matches audit-first pattern: validate → assert → audit → persist                      |
| 5   | Called `prefRepo.findPreferencesForUser()` to get existing channel state                         | ✅ Validator needs current state to check "last channel" scenario                        |
| 6   | Created focused tests: valid case, mandatory violation, LEGAL-218 false positive + hard negative | ✅ Matches lesson's assessment expectations                                              |
| 7   | Used `.flatMap()` with type guard instead of `.flat()`                                           | ✅ Self-correction for TS strict mode compatibility                                      |
| 8   | Renamed `isCaliforniaLoan()` → `isCaliforniaRestrictedContext()` with `undefined → true` default | ✅ Route has no loan-state context; conservative approach prevents California violations |
| 9   | Added comment explaining conservative default reasoning                                          | ✅ Makes the design choice explicit for next developer                                   |
| 10  | Did not run tests or shell commands                                                              | ✅ Adhered to denied tools                                                               |

## 5. Constraint Compliance

| #   | Constraint                                          | Status | Evidence                                                  |
| --- | --------------------------------------------------- | ------ | --------------------------------------------------------- |
| 1   | Discover relevant files, don't assume fixed list    | ✅     | 10 glob + 4 rg discovery queries                          |
| 2   | Create pure validation rule in `backend/src/rules/` | ✅     | `preference-event-channel-validator.ts`                   |
| 3   | Validate event-channel combinations                 | ✅     | `validatePreferenceEventChannel()` checks combinations    |
| 4   | Mandatory events can't disable all channels         | ✅     | `MANDATORY_NOTIFICATION_EVENTS` check                     |
| 5   | LEGAL-218 California SMS restriction respected      | ✅     | `isCaliforniaRestrictedContext()` + decline/sms check     |
| 6   | Create unit tests at `backend/tests/unit/`          | ✅     | `preference-event-channel-validator.test.ts`              |
| 7   | Cover valid combinations                            | ✅     | "allows mandatory events when another channel remains"    |
| 8   | Cover mandatory-event violations                    | ✅     | "rejects disabling the last channel"                      |
| 9   | Cover LEGAL-218 false positive                      | ✅     | "avoids LEGAL-218 false positive for non-California"      |
| 10  | Cover LEGAL-218 hard negative                       | ✅     | "rejects California decline SMS disable without fallback" |
| 11  | Wire validator into notification write route        | ✅     | Import + `assertPreferenceEventChannelAllowed()` call     |
| 12  | Follow repository conventions                       | ✅     | Rules pure, services I/O, tests Vitest                    |
| 13  | No shell commands or npm install/test               | ✅     | None used                                                 |
| 14  | No SQL                                              | ✅     | None used                                                 |

## 6. Files Created / Modified

| File                                                                | Action   | Lines    | Description                                                                               |
| ------------------------------------------------------------------- | -------- | -------- | ----------------------------------------------------------------------------------------- |
| `src/backend/src/rules/preference-event-channel-validator.ts`       | Created  | ~105     | Event-channel validation rule with LEGAL-218 support                                      |
| `src/backend/tests/unit/preference-event-channel-validator.test.ts` | Created  | ~95      | 5 test cases: valid, mandatory violation, false positive, hard negative, allowed fallback |
| `src/backend/src/routes/notifications.ts`                           | Modified | +8 lines | Import validator + call `assertPreferenceEventChannelAllowed()` before persistence        |

## 7. Session Metadata

| Field                     | Value                                                               |
| ------------------------- | ------------------------------------------------------------------- |
| CLI version               | Copilot CLI v1.0.5                                                  |
| Node.js                   | v24.11.1                                                            |
| Platform                  | win32                                                               |
| Model                     | GPT-5.4                                                             |
| Reasoning                 | medium                                                              |
| Denied tools              | `powershell`, `sql`                                                 |
| Discovery time            | ~3m 5s (78% of session)                                             |
| Writing time              | ~52s (22% of session)                                               |
| Self-corrections          | 3 (TS typing, conservative California default, explanatory comment) |
| Total apply_patch calls   | 4 (1 core + 3 refinements)                                          |
| Files read before writing | ~30 unique files                                                    |

## 8. What This Lesson Proves

1. **Cross-stack synthesis is feasible**: The capstone required reading project instructions, backend-scoped instructions, frontend-scoped instructions, architecture docs, existing rules, routes, services, models, and tests — then synthesizing a new validator that fits all those conventions. The model read ~30 files before its first write.

2. **Existing rule reuse**: The validator imports `MANDATORY_EVENTS` from the existing `mandatory-events.ts` rather than re-defining them, demonstrating the model understands the "reuse, don't duplicate" principle.

3. **Progressive refinement**: The model made 4 `apply_patch` calls — one core implementation plus three iterative refinements (type safety, conservative default, documentation comment). Each refinement addressed a real issue found during verification.

4. **Context-sensitive conservatism**: When the model discovered the notification route has no loan-state context, it didn't skip the LEGAL-218 check — it made the validator conservative by defaulting to California-restricted behavior when loan state is unknown. This is exactly the kind of domain-aware decision context engineering enables.

5. **Largest session by tool count**: With ~77 tool calls across 3m 57s, this was the most intensive session in the course. The capstone appropriately demands the deepest discovery and the most careful integration, validating that context engineering scales to real-world complexity.
