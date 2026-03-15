## 7 · Context Validation

> When and how was non-system (private) context accessed during the session?

### Implicit Context (auto-injected)

| File | Type |
| --- | --- |
| `api.instructions.md` | scoped |
| `copilot-instructions.md` | project-level |
| `portable-baseline.instructions.md` | scoped |

### Context Access Timeline

| Turn | Action | Target |
| ---: | --- | --- |
| 1 | search | `glob(.github/**/*)` |
| 1 | search | `glob(docs/**/*)` |
| 1 | search | `glob(**/*.md)` |
| 1 | search | `rg(applyTo:\|copilot\|prompt\|agent\|mcp\|hook\|instruction)` |
| 2 | read | `.github/copilot-instructions.md` |
| 2 | read | `.github/instructions/api.instructions.md` |
| 2 | read | `.github/agents/reviewer.agent.md` |
| 2 | read | `README.md` |
| 2 | read | `docs/portability-matrix.md` |
| 2 | read | `docs/cli-guide.md` |
| 2 | read | `docs/surface-strategy-example.md` |
| 3 | search | `glob(.github/prompts/**/*)` |
| 3 | search | `glob(.github/hooks/**/*)` |
| 3 | search | `glob(.github/mcp*)` |
| 3 | read | `ASSESSMENT.md` |
| 4 | **write** | `.github/instructions/portable-baseline.instructions.md` |
| 4 | **write** | `docs/surface-portability-notes.md` |
| 5 | read | `.github/instructions/portable-baseline.instructions.md` |
| 5 | read | `docs/surface-portability-notes.md` |

### Files Written

- `.github/instructions/portable-baseline.instructions.md`
- `docs/surface-portability-notes.md`

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
    S->>M: portable-baseline.instructions.md

    U->>M: prompt


    Note over M,T: Turn 1
    Note over M: Intent: Exploring artifacts
    M->>T: glob(.github/**/*)
    T-->>M: file list
    M->>T: glob(docs/**/*)
    T-->>M: file list
    M->>T: glob(**/*.md)
    T-->>M: file list
    M->>T: rg(...|copilot|prompt|agent|mcp|hook|i)
    T-->>M: matches

    Note over M,T: Turn 2
    M->>T: view(.github/copilot-instructions.md)
    T->>C: read
    C-->>M: content
    M->>T: view(.github/instructions/api.instructions.md)
    T->>C: read
    C-->>M: content
    M->>T: view(.github/agents/reviewer.agent.md)
    T->>C: read
    C-->>M: content
    M->>T: view(README.md)
    T->>C: read
    C-->>M: content
    M->>T: view(docs/portability-matrix.md)
    T->>C: read
    C-->>M: content
    M->>T: view(docs/cli-guide.md)
    T->>C: read
    C-->>M: content
    M->>T: view(docs/surface-strategy-example.md)
    T->>C: read
    C-->>M: content

    Note over M,T: Turn 3
    Note over M: Intent: Reading assessment
    M->>T: glob(.github/prompts/**/*)
    T-->>M: file list
    M->>T: glob(.github/hooks/**/*)
    T-->>M: file list
    M->>T: glob(.github/mcp*)
    T-->>M: file list
    M->>T: view(ASSESSMENT.md)
    T->>C: read
    C-->>M: content

    Note over M,T: Turn 4
    M->>T: write(...ructions/portable-baseline.instructions.md)
    T->>C: patch
    C-->>M: ok
    M->>T: write(docs/surface-portability-notes.md)
    T->>C: patch
    C-->>M: ok

    Note over M,T: Turn 5
    Note over M: Intent: Verifying changes
    M->>T: view(...ructions/portable-baseline.instructions.md)
    T->>C: read
    C-->>M: content
    M->>T: view(docs/surface-portability-notes.md)
    T->>C: read
    C-->>M: content

    Note over M,T: Turn 6

    M->>U: Return results
```

### Validation Summary

- **Implicit context:** 3 instruction file(s) injected at session start
- **Files read:** 10 unique files across 6 turns
- **Files written:** 2 codebase file(s)
- **First codebase read:** turn 2
- **First codebase write:** turn 4
- **Discovery-before-write gap:** 2 turn(s)
