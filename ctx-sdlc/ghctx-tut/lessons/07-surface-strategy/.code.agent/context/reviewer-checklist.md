# Reviewer Checklist

## Context Alignment

- Generated context files reflect the current `src/` application.
- Backend, frontend, and test rules match real source paths.
- Shared rules are not trapped inside scoped files.

## Application Consistency

- Backend response shapes match frontend type definitions.
- Route changes include matching integration test updates.
- Rule changes include matching unit test updates.
- Middleware order in `app.ts` has not been silently changed.

## Code Quality

- Route handlers delegate to rules and services instead of containing logic.
- Error handling follows the existing `{ error: string }` shape.
- New code matches existing patterns in the codebase.
