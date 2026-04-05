## 7 · Context Validation

> When and how was non-system (private) context accessed during the session?

### Implicit Context (auto-injected)

| File | Type |
| --- | --- |
| `api.instructions.md` | scoped |
| `copilot-instructions.md` | project-level |
| `notifications.instructions.md` | scoped |
| `test.instructions.md` | scoped |

### Context Access Timeline

| Turn | Action | Target |
| ---: | --- | --- |
| 1 | search | `glob(**/.github/**/*)` |
| 1 | search | `glob(**/docs/**/*)` |
| 1 | search | `rg(audit_context\|detect_stale_refs\|context-maintenance\|stale refs\|drift)` |
| 2 | read | `.github/copilot-instructions.md` |
| 2 | read | `.github/examples/clean/copilot-instructions.md` |
| 2 | read | `.github/examples/drifted/copilot-instructions.md` |
| 2 | read | `docs/maintenance-schedule.md` |
| 2 | read | `docs/operating-model-example.md` |
| 2 | read | `.github/scripts/audit_context.py` |
| 2 | read | `.github/scripts/detect_stale_refs.py` |
| 2 | read | `plan.md` |
| 3 | search | `glob(app/backend/src/**/*)` |
| 3 | search | `glob(.github/instructions/**/*)` |
| 3 | search | `glob(docs/**/*)` |
| 3 | search | `glob(**/helpers/**/*)` |
| 5 | **write** | `.github/examples/drifted/copilot-instructions.md` |
| 6 | read | `.github/examples/drifted/copilot-instructions.md` |
| 6 | read | `plan.md` |

### Files Written

- `.github/examples/drifted/copilot-instructions.md`

### Context Flow Diagram

```mermaid
sequenceDiagram
    participant U as User/Prompt
    participant S as Copilot Runtime
    participant M as Model
    participant T as Tools
    participant C as Codebase

    Note over S,M: Implicit Context (auto-injected)
    S->>M: api.instructions.md
    S->>M: copilot-instructions.md
    S->>M: notifications.instructions.md
    S->>M: test.instructions.md

    U->>M: prompt


    Note over M,T: Turn 1
    Note over M: Intent: Inspecting artifacts
    M->>T: glob(**/.github/**/*)
    T-->>M: file list
    M->>T: glob(**/docs/**/*)
    T-->>M: file list
    M->>T: rg(..._refs|context-maintenance|stale )
    T-->>M: matches

    Note over M,T: Turn 2
    Note over M: Intent: Comparing examples
    M->>T: view(.github/copilot-instructions.md)
    T->>C: read
    C-->>M: content
    M->>T: view(...hub/examples/clean/copilot-instructions.md)
    T->>C: read
    C-->>M: content
    M->>T: view(...b/examples/drifted/copilot-instructions.md)
    T->>C: read
    C-->>M: content
    M->>T: view(docs/maintenance-schedule.md)
    T->>C: read
    C-->>M: content
    M->>T: view(docs/operating-model-example.md)
    T->>C: read
    C-->>M: content
    M->>T: view(.github/scripts/audit_context.py)
    T->>C: read
    C-->>M: content
    M->>T: view(.github/scripts/detect_stale_refs.py)
    T->>C: read
    C-->>M: content
    M->>T: view(plan.md)
    T->>C: read
    C-->>M: content

    Note over M,T: Turn 3
    Note over M: Intent: Verifying references
    M->>T: glob(app/backend/src/**/*)
    T-->>M: file list
    M->>T: glob(.github/instructions/**/*)
    T-->>M: file list
    M->>T: glob(docs/**/*)
    T-->>M: file list
    M->>T: glob(**/helpers/**/*)
    T-->>M: file list

    Note over M,T: Turn 4
    Note over M: Update plan.md

    Note over M,T: Turn 5
    M->>T: write(...b/examples/drifted/copilot-instructions.md)
    T->>C: patch
    C-->>M: ok

    Note over M,T: Turn 6
    Note over M: Intent: Verifying edits
    M->>T: view(...b/examples/drifted/copilot-instructions.md)
    T->>C: read
    C-->>M: content
    M->>T: view(plan.md)
    T->>C: read
    C-->>M: content

    M->>U: Return results
```

### Validation Summary

- **Implicit context:** 4 instruction file(s) injected at session start
- **Files read:** 8 unique files across 7 turns
- **Files written:** 1 codebase file(s)
- **First codebase read:** turn 2
- **First codebase write:** turn 5
- **Discovery-before-write gap:** 3 turn(s)
