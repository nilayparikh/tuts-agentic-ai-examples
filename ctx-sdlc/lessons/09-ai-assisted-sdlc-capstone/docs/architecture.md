# TaskFlow — System Architecture

## Overview

TaskFlow is a monorepo (pnpm workspaces) with three packages:

```
┌──────────────────────────────────────────────┐
│                   Browser                     │
│  React 19 + Vite + Tailwind + Zustand         │
├──────────────────────────────────────────────┤
│              HTTP / WebSocket                  │
├──────────────────────────────────────────────┤
│               Express 5 API                    │
│  Routes → Controllers → Services → Prisma     │
├──────────────────────────────────────────────┤
│              PostgreSQL 16                     │
└──────────────────────────────────────────────┘
```

## Frontend Architecture

```
packages/web/src/
  components/     ← Presentational components (no state logic)
  pages/          ← Route pages (React Router v7)
  stores/         ← Zustand stores (global state)
  hooks/          ← Custom hooks (data fetching, subscriptions)
  lib/            ← API client, WebSocket client, utilities
```

**Data flow**: Component → Hook → Store → API Client → Express Route

**State strategy**:

- Local UI state: `useState` / `useReducer`
- Global app state: Zustand stores
- Server state: Fetched via API client, cached in stores
- Real-time state: WebSocket events update stores

## Backend Architecture

```
packages/api/src/
  routes/         ← Express route definitions
  controllers/    ← Request handling, response formatting
  services/       ← Business logic, Prisma queries
  middleware/     ← Auth, validation, error handling
  websocket/      ← WebSocket event emitters
```

**Request flow**: Route → Middleware (auth, validation) → Controller → Service → Prisma → Response

**Key patterns**:

- Controllers never access Prisma directly
- Services are the only layer that touches the database
- WebSocket events are emitted AFTER successful database writes
- All mutations are wrapped in Prisma transactions

## Data Model

```
User
  id          String   @id @default(uuid())
  email       String   @unique
  name        String
  role        Role     @default(MEMBER)
  teams       TeamMember[]
  tasks       Task[]   @relation("assignee")

Team
  id          String   @id @default(uuid())
  name        String
  members     TeamMember[]
  projects    Project[]

Project
  id          String   @id @default(uuid())
  name        String
  teamId      String
  tasks       Task[]

Task
  id          String   @id @default(uuid())
  title       String
  description String?
  status      TaskStatus  @default(TODO)
  priority    Priority    @default(MEDIUM)
  assigneeId  String?
  projectId   String
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt

enum Role     { ADMIN, MEMBER, VIEWER }
enum TaskStatus { TODO, IN_PROGRESS, IN_REVIEW, DONE }
enum Priority { LOW, MEDIUM, HIGH, URGENT }
```
