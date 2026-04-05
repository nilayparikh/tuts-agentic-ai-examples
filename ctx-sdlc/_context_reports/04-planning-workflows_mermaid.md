# Context Flow — 04-planning-workflows

```mermaid
sequenceDiagram
    participant U as User/Prompt
    participant S as Copilot Runtime
    participant M as Model
    participant T as Tools
    participant C as Codebase

    U->>M: prompt


    Note over M,T: Turn 1
    Note over M: Intent: Exploring sources
    M->>T: glob(docs//**//*)
    T-->>M: file list
    M->>T: glob(specs//**//*)
    T-->>M: file list
    M->>T: rg(...it|degraded|mandatory|fallback|f)
    T-->>M: matches
    M->>T: rg(...it|degraded|mandatory|fallback|f)
    T-->>M: matches
    M->>T: rg(...it|degraded|mandatory|fallback|f)
    T-->>M: matches

    Note over M,T: Turn 2
    Note over M: Intent: Reading context
    M->>T: view(docs)
    T->>C: read
    C-->>M: content
    M->>T: view(specs)
    T->>C: read
    C-->>M: content
    M->>T: view(src)
    T->>C: read
    C-->>M: content
    M->>T: view(plan.md)
    T->>C: read
    C-->>M: content
    M->>T: glob(src//**//*notification*)
    T-->>M: file list
    M->>T: glob(src//**//*preference*)
    T-->>M: file list

    Note over M,T: Turn 3
    Note over M: Intent: Finding surfaces
    M->>T: view(src/backend)
    T->>C: read
    C-->>M: content
    M->>T: view(src/frontend)
    T->>C: read
    C-->>M: content
    M->>T: rg(...legated|LEGAL-218|audit|fallback)
    T-->>M: matches
    M->>T: rg(...legated|LEGAL-218|audit|fallback)
    T-->>M: matches
    M->>T: view(docs/architecture.md)
    T->>C: read
    C-->>M: content
    M->>T: view(docs/adr/ADR-003-frontend-state.md)
    T->>C: read
    C-->>M: content
    M->>T: view(specs/feature-request.md)
    T->>C: read
    C-->>M: content
    M->>T: view(...s/product-spec-notification-preferences.md)
    T->>C: read
    C-->>M: content
    M->>T: view(specs/non-functional-requirements.md)
    T->>C: read
    C-->>M: content
    M->>T: view(specs/bug-report.md)
    T->>C: read
    C-->>M: content

    Note over M,T: Turn 4
    Note over M: Intent: Inspecting code
    M->>T: view(src/backend/src)
    T->>C: read
    C-->>M: content
    M->>T: view(src/frontend/src)
    T->>C: read
    C-->>M: content
    M->>T: rg(...ore|useState|optimistic|rollback)
    T-->>M: matches
    M->>T: view(...nd/tests/unit/notification-service.test.ts)
    T->>C: read
    C-->>M: content
    M->>T: view(...ackend/tests/integration/decisions.test.ts)
    T->>C: read
    C-->>M: content

    Note over M,T: Turn 5
    M->>T: view(src/backend/src/routes)
    T->>C: read
    C-->>M: content
    M->>T: view(src/backend/src/middleware)
    T->>C: read
    C-->>M: content
    M->>T: view(src/backend/src/rules)
    T->>C: read
    C-->>M: content
    M->>T: view(src/backend/src/services)
    T->>C: read
    C-->>M: content
    M->>T: view(src/frontend/src/pages)
    T->>C: read
    C-->>M: content
    M->>T: view(src/frontend/src/api)
    T->>C: read
    C-->>M: content
    M->>T: view(src/frontend/src/components)
    T->>C: read
    C-->>M: content
    M->>T: view(src/backend/tests/unit/business-rules.test.ts)
    T->>C: read
    C-->>M: content

    Note over M,T: Turn 6
    Note over M: Intent: Reading implementation
    M->>T: view(src/backend/src/routes/notifications.ts)
    T->>C: read
    C-->>M: content
    M->>T: view(src/backend/src/middleware/auth.ts)
    T->>C: read
    C-->>M: content
    M->>T: view(...ckend/src/services/notification-service.ts)
    T->>C: read
    C-->>M: content
    M->>T: view(src/backend/src/services/audit-service.ts)
    T->>C: read
    C-->>M: content
    M->>T: view(src/backend/src/rules/mandatory-events.ts)
    T->>C: read
    C-->>M: content
    M->>T: view(src/backend/src/rules/role-permissions.ts)
    T->>C: read
    C-->>M: content
    M->>T: view(src/backend/src/queue/contracts.ts)
    T->>C: read
    C-->>M: content
    M->>T: view(src/frontend/src/api/client.ts)
    T->>C: read
    C-->>M: content
    M->>T: view(src/frontend/src/api/types.ts)
    T->>C: read
    C-->>M: content
    M->>T: view(src/frontend/src/pages/preferences.ts)
    T->>C: read
    C-->>M: content
    M->>T: view(...tend/src/components/notification-toggle.ts)
    T->>C: read
    C-->>M: content

    Note over M,T: Turn 7
    M->>T: view(src/backend/src/models/types.ts)
    T->>C: read
    C-->>M: content
    M->>T: view(...ackend/src/models/preference-repository.ts)
    T->>C: read
    C-->>M: content
    M->>T: view(src/backend/src/config/feature-flags.ts)
    T->>C: read
    C-->>M: content
    M->>T: view(src/backend/src/queue)
    T->>C: read
    C-->>M: content
    M->>T: view(src/frontend/src/main.ts)
    T->>C: read
    C-->>M: content
    M->>T: view(src/frontend/src/components/app-shell.ts)
    T->>C: read
    C-->>M: content
    M->>T: view(src/backend/src/app.ts)
    T->>C: read
    C-->>M: content
    M->>T: view(docs/adr)
    T->>C: read
    C-->>M: content

    Note over M,T: Turn 8
    M->>T: rg(...e//.latency|metric|telemetry|obs)
    T-->>M: matches
    M->>T: view(src/backend/src/queue/handlers)
    T->>C: read
    C-->>M: content
    M->>T: view(...src/queue/handlers/notification-handler.ts)
    T->>C: read
    C-->>M: content
    M->>T: view(...ackend/src/queue/handlers/audit-handler.ts)
    T->>C: read
    C-->>M: content
    M->>T: view(src/backend/src/middleware/error-handler.ts)
    T->>C: read
    C-->>M: content
    M->>T: view(src/backend/src/routes/audit.ts)
    T->>C: read
    C-->>M: content

    Note over M,T: Turn 9
    M->>T: view(src/frontend/src/pages/dashboard.ts)
    T->>C: read
    C-->>M: content
    M->>T: view(src/frontend/src/pages/application-detail.ts)
    T->>C: read
    C-->>M: content
    M->>T: view(src/backend/src/services/loan-service.ts)
    T->>C: read
    C-->>M: content
    M->>T: view(src/backend/src/routes/applications.ts)
    T->>C: read
    C-->>M: content
    M->>T: view(src/backend/src/routes/decisions.ts)
    T->>C: read
    C-->>M: content

    Note over M,T: Turn 10
    M->>T: view(docs/planning-workflow-example.md)
    T->>C: read
    C-->>M: content
    M->>T: rg(404|pilot|release flag|feature flag)
    T-->>M: matches
    M->>T: rg(404|pilot|release flag|feature flag)
    T-->>M: matches
    M->>T: rg(...cation_preferences|audit_entries)
    T-->>M: matches
    M->>T: view(src/backend/src/db/schema.sql)
    T->>C: read
    C-->>M: content

    Note over M,T: Turn 11
    M->>T: view(src/backend/src/rules/business-rules.ts)
    T->>C: read
    C-->>M: content
    M->>T: view(src/backend/src/db/seed.ts)
    T->>C: read
    C-->>M: content
    M->>T: view(src/backend/src/models/audit-repository.ts)
    T->>C: read
    C-->>M: content
    M->>T: view(src/backend/package.json)
    T->>C: read
    C-->>M: content
    M->>T: view(src/package.json)
    T->>C: read
    C-->>M: content

    Note over M,T: Turn 12
    M->>T: write(docs/notification-preferences-plan.md)
    T->>C: patch
    C-->>M: ok

    Note over M,T: Turn 13
    Note over M: Intent: Verifying plan
    M->>T: view(docs/notification-preferences-plan.md)
    T->>C: read
    C-->>M: content
    M->>T: view(docs/notification-preferences-plan.md)
    T->>C: read
    C-->>M: content

    Note over M,T: Turn 14
    M->>T: view(docs/notification-preferences-plan.md)
    T->>C: read
    C-->>M: content

    Note over M,T: Turn 15

    M->>U: Return results
```
