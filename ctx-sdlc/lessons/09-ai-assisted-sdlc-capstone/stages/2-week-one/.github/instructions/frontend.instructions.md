---
applyTo: "packages/web/**"
---

# Frontend Instructions — React 19 + Tailwind

## Component Pattern

All components MUST follow this structure:

```typescript
interface Props {
  // Explicit props — no `any`
}

export function ComponentName({ prop1, prop2 }: Props) {
  // Hooks first
  // Event handlers
  // Return JSX
}
```

## State Management

- Local state: `useState` / `useReducer`
- Global state: Zustand stores in `packages/web/src/stores/`
- Server state: React 19 `use()` + Suspense boundaries
- Do NOT use Redux, MobX, or React Context for mutable state

## Styling

- Tailwind utility classes only
- No CSS modules, styled-components, or emotion
- Custom design tokens in `tailwind.config.ts`
- Dark mode: use `dark:` variant classes

## Accessibility

- All interactive elements must be keyboard accessible
- Images require `alt` text
- Form inputs require `label` elements
- Use semantic HTML (`nav`, `main`, `section`, `article`)
