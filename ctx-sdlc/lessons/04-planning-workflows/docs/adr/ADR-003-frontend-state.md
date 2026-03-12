# ADR-003: Frontend State Strategy

## Status

Accepted

## Context

The Loan Workbench has multiple screens that share underwriting workflow state:
application lists, decision forms, notification settings, and audit viewers.
The team evaluated component-local state, context providers, and a central
client store.

## Decision

Loan Workbench uses a **central client store** for cross-screen workflow state.
Local component state is acceptable for purely presentational concerns (e.g.
form input focus, tooltip visibility), but NOT for:

- Shared underwriting workflow state
- Persisted user preferences
- Any data that survives navigation or page refresh

## Consequences

- Feature plans must NOT default to component-local state for persisted data.
- Planning outputs should explicitly call out state ownership for every new
  data entity.
- UI features that survive navigation or refresh need both store and API changes.
- Optimistic updates in the store must be paired with rollback logic that fires
  when the API rejects the change.

## Implications for AI-Assisted Development

An AI assistant generating a notification-preferences UI will default to
`useState` or component-local state. The instruction context must surface
ADR-003 so the assistant uses the central store pattern instead.
