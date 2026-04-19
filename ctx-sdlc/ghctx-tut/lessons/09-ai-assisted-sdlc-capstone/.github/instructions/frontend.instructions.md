---
applyTo: "app/frontend/src/**"
---

# Frontend Instructions — Vanilla TypeScript SPA

## Component Pattern

The frontend is a vanilla TypeScript single-page application — no framework.

- All UI logic lives in `app/frontend/src/`
- API calls go through the client in `app/frontend/src/api/`
- Page rendering is in `app/frontend/src/pages/`
- Reusable UI elements are in `app/frontend/src/components/`

## Conventions

- TypeScript strict mode
- ESM imports only
- No external UI framework (no React, Vue, Angular)
- Styling via plain CSS in `app/frontend/styles/`

## Accessibility

- All interactive elements must be keyboard accessible
- Images require `alt` text
- Form inputs require `label` elements
- Use semantic HTML (`nav`, `main`, `section`, `article`)
