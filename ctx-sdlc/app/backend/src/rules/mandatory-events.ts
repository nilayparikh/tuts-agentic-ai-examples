// ---------------------------------------------------------------------------
// Mandatory Notification Events
// ---------------------------------------------------------------------------
// Defines which notification events MUST fire for each state transition.
// These are non-negotiable business requirements — skipping a mandatory
// event is a compliance violation.
//
// When a transition occurs, the loan service must emit notification events
// for ALL mandatory events listed here.
// ---------------------------------------------------------------------------

import type { ApplicationState, NotificationEvent } from "../models/types.js";

type TransitionKey = `${ApplicationState}->${ApplicationState}`;

/**
 * Map of state transitions to mandatory notification events.
 * If a transition is not listed, no mandatory notifications are required.
 */
export const MANDATORY_EVENTS: Partial<
  Record<TransitionKey, NotificationEvent[]>
> = {
  "decision->finalized": ["approval"],
  "underwriting->decision": ["manual-review-escalation"],
  "review->intake": ["document-request"],
};

/**
 * Get the mandatory notification events for a given state transition.
 */
export function getMandatoryEvents(
  from: ApplicationState,
  to: ApplicationState,
): NotificationEvent[] {
  const key: TransitionKey = `${from}->${to}`;
  return MANDATORY_EVENTS[key] ?? [];
}
