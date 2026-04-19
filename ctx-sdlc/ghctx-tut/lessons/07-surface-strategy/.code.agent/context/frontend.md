# Frontend Application Contract

## Scope

`src/frontend/src/**/*.ts` and `src/frontend/styles/**/*.css`

## Stack

- Plain TypeScript, not React.
- Vite serves the frontend.
- Hash-based routing in `src/frontend/src/main.ts`.
- Route rendering in `src/frontend/src/pages/`.
- Reusable components in `src/frontend/src/components/`.
- HTTP client and types in `src/frontend/src/api/`.

## Rendering

- `render*` functions take an `HTMLElement` container.
- DOM updates through `innerHTML` or targeted helpers.
- Lazy loading for non-default pages where it already exists.
- `renderAppShell` renders the SPA shell.

## Styling

- Application CSS in `src/frontend/styles/main.css`.
- Dashboard, queue monitor, preferences, and API explorer are the main surfaces.
- Frontend terminology matches backend: applications, decisions, notifications,
  audit, queue.

## API Boundary

- If backend response shapes change, update `src/frontend/src/api/types.ts`
  and the affected page or component in the same change.
- Do not hardcode response shapes inside page renderers.
