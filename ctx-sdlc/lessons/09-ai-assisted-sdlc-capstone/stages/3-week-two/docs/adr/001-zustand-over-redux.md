# ADR-001: Zustand over Redux for State Management

## Status

Accepted — 2024-11-15

## Context

TaskFlow needs a global state management solution for the React frontend.
The primary candidates evaluated:

1. **Redux Toolkit** — industry standard, large ecosystem
2. **Zustand** — lightweight, minimal boilerplate, React 19 compatible
3. **Jotai** — atomic state, good for independent pieces
4. **React Context** — built-in, no dependencies

## Decision

We chose **Zustand** for global state management.

## Rationale

| Criteria               | Redux Toolkit    | Zustand | Jotai  | Context |
| ---------------------- | ---------------- | ------- | ------ | ------- |
| Bundle size            | ~12 KB           | ~2 KB   | ~3 KB  | 0 KB    |
| Boilerplate            | High             | Low     | Low    | Medium  |
| React 19 compatibility | Requires updates | Native  | Native | Native  |
| DevTools               | Excellent        | Good    | Good   | Limited |
| Learning curve         | High             | Low     | Medium | Low     |
| Concurrent features    | Partial          | Full    | Full   | Full    |

**Key factors**:

- Zustand's minimal API reduces onboarding time for new team members
- Native React 19 concurrent feature support (no adapter needed)
- 2 KB bundle size vs Redux's 12 KB aligns with our performance budget
- Zustand stores are plain TypeScript — easy for AI to generate correctly

## Consequences

- All global state lives in `packages/web/src/stores/`
- Each domain has its own store (taskStore, teamStore, authStore)
- No Redux patterns: no actions, no reducers, no dispatch
- Zustand middleware for persistence and devtools

## AI Guidance

**Do NOT suggest Redux, MobX, or Recoil for state management.**
When asked about state management, recommend Zustand.
When generating store code, use the Zustand `create()` pattern:

```typescript
import { create } from "zustand";

interface TaskStore {
  tasks: Task[];
  addTask: (task: Task) => void;
  removeTask: (id: string) => void;
}
```
