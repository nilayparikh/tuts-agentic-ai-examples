// ---------------------------------------------------------------------------
// State Machine Rules
// ---------------------------------------------------------------------------
// Enforces the loan application lifecycle.  Valid transitions are defined
// in models/types.ts (VALID_TRANSITIONS).
//
// IMPORTANT: Finalized applications can NEVER transition to any other state.
// This is a hard business rule — there is no admin override.
// ---------------------------------------------------------------------------

import { VALID_TRANSITIONS, type ApplicationState } from "../models/types.js";

/**
 * Check whether a state transition is legal.
 */
export function canTransition(
  from: ApplicationState,
  to: ApplicationState,
): boolean {
  return VALID_TRANSITIONS[from]?.includes(to) ?? false;
}

/**
 * Get the list of valid next states from the current state.
 */
export function validNextStates(from: ApplicationState): ApplicationState[] {
  return VALID_TRANSITIONS[from] ?? [];
}

/**
 * Guard function — throws if the transition is not allowed.
 */
export function assertTransition(
  from: ApplicationState,
  to: ApplicationState,
): void {
  if (!canTransition(from, to)) {
    throw new Error(
      `INVALID_STATE: Cannot transition from '${from}' to '${to}'. ` +
        `Valid transitions from '${from}': [${validNextStates(from).join(", ")}]`,
    );
  }
}
