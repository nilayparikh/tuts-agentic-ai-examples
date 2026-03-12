# TaskFlow — Project Context (Week One)

> **Stage 2**: First week. Added instructions and documentation.
> Copilot now knows HOW code should be written AND the architecture.

## Project

TaskFlow — a full-stack task management application with team collaboration,
real-time updates, and role-based access control.

## Tech Stack

- Frontend: React 19, TypeScript, Vite, Tailwind CSS
- State: Zustand (see ADR-001 — do NOT suggest Redux)
- Backend: Node.js 22 LTS, Express 5, TypeScript
- Database: PostgreSQL 16 via Prisma ORM
- Real-time: WebSocket (ws library)
- Auth: JWT with refresh tokens
- Tests: Vitest + React Testing Library
- Modules: ESM only
- Package manager: pnpm (monorepo with pnpm workspaces)

## Monorepo Structure

```
packages/
  web/        ← React frontend (React 19, Vite, Tailwind)
  api/        ← Express API (Express 5, Prisma)
  shared/     ← Shared types and utilities
```

## Architecture

Frontend: Component → Hook → Zustand Store → API Client → Express Route

Backend: Route → Middleware → Controller → Service → Prisma Model

See `/docs/architecture.md` for the full system overview.

## Coding Conventions

### TypeScript

- Strict mode always
- `const` over `let`, never `var`
- Prefer `interface` over `type` for object shapes
- Export types from `packages/shared/`

### React (Frontend)

- Functional components only
- Hooks for all state and side effects
- Zustand for global state (NOT Redux, NOT Context for mutable state)
- Tailwind CSS for styling (NO CSS modules, NO styled-components)
- Server components where possible (React 19)

### Express (Backend)

- Controller pattern: routes → controllers → services
- All routes `async`
- Structured error responses: `{ error: string, code: string }`
- Prisma for all database access (no raw SQL unless N+1 optimization)
- JWT middleware on protected routes

### Testing

- Vitest for all tests
- React Testing Library for component tests
- `describe`/`it`/`expect` pattern

## References

- Architecture: `/docs/architecture.md`
- Technology decisions: `/docs/adr/`
