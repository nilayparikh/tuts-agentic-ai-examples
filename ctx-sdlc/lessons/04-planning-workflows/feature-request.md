# Feature Request: Notification Preferences

Add notification preferences to the Loan Workbench settings area.

## Requested Behavior

- Underwriters can control email and SMS notifications per event type.
- Preferences persist across sessions and devices.
- Separate toggles for: approval, decline, document-request, and manual-review-escalation.
- Manual-review escalation requires at least one enabled channel.
- The plan must account for delegated sessions, audit logging, and state-based restrictions.

## Product Context

- Full product specification: `specs/product-spec-notification-preferences.md`
- Non-functional requirements: `specs/non-functional-requirements.md`
- The release is **pilot-gated** and must not change behavior for non-pilot users.

## Special Conditions To Account For

- **California loans** cannot enable SMS for decline decisions (LEGAL-218).
- **Delegated sessions**: analyst managers may inspect but not edit another user's preferences.
- **SMS degraded mode**: email fallback must preserve the stored preference model.
- **Mandatory escalation events** must remain deliverable even when users change preferences.
- **Audit writes** must fail closed — no silent saves without an audit trail.
- **Existing users** may not have stored preferences and need role-based defaults on first access.

## Known Constraints

- Current settings screens do not expose notification preferences.
- Shared workflow state follows [ADR-003](docs/adr/ADR-003-frontend-state.md).
- Backend routes live under `src/routes/`.
- Business rules live under `src/rules/`.
- The team wants a **plan before implementation begins**.

## Deliverable Expectation

The plan should identify open questions, affected surfaces, validation steps,
and risks that come specifically from the product spec and NFRs — not just from
the visible UI request. A shallow "add a toggle page" plan is insufficient.
