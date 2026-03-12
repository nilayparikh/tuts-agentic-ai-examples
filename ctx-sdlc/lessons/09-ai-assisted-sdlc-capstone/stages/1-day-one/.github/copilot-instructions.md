# TaskFlow — Project Context (Day One)

> **Stage 1**: Day one on a new project. Minimal context — just enough for
> Copilot to know what the project IS.

## Project

TaskFlow — a full-stack task management application with team collaboration,
real-time updates, and role-based access control.

## Tech Stack

- Frontend: React 19, TypeScript, Vite, Tailwind CSS
- Backend: Node.js 22 LTS, Express 5, TypeScript
- Database: PostgreSQL 16 via Prisma ORM
- Real-time: WebSocket (ws library)
- Tests: Vitest
- Modules: ESM only
- Package manager: pnpm (monorepo with pnpm workspaces)

## Monorepo Structure

```
packages/
  web/        ← React frontend
  api/        ← Express API
  shared/     ← Shared types and utilities
```

## Quick Start

```bash
pnpm install
pnpm --filter api db:migrate
pnpm dev          # starts both frontend and API
```
