// ---------------------------------------------------------------------------
// Message Queue — Event Contracts
// ---------------------------------------------------------------------------
// Defines the typed message contracts for the in-process event broker.
// All producers and consumers MUST use these types.
//
// IMPORTANT — CONTRACT CHANGES:
//   Changing a message contract is a BREAKING CHANGE.  When modifying:
//   1. Update the type here
//   2. Update ALL handlers that consume the event
//   3. Update ALL producers that emit the event
//   4. Add an audit entry for the contract change
//
// This is a common source of bugs when AI assistants generate code without
// seeing the consumer side of a contract.
// ---------------------------------------------------------------------------

import type {
  NotificationEvent,
  NotificationChannel,
} from "../models/types.js";

/** Base event structure — all events must include these fields. */
export interface BaseEvent {
  eventId: string;
  timestamp: string;
  source: string;
}

/** Emitted when a notification must be delivered to a user. */
export interface NotificationRequestedEvent extends BaseEvent {
  type: "notification.requested";
  payload: {
    userId: string;
    event: NotificationEvent;
    subject: string;
    body: string;
    preferredChannel: NotificationChannel;
  };
}

/** Emitted when an audit entry must be persisted. */
export interface AuditRequestedEvent extends BaseEvent {
  type: "audit.requested";
  payload: {
    action: string;
    actor: string;
    delegatedFor?: string;
    previousValue?: unknown;
    newValue?: unknown;
    source: string;
  };
}

/** Emitted when a loan application changes state. */
export interface LoanStateChangedEvent extends BaseEvent {
  type: "loan.state-changed";
  payload: {
    applicationId: string;
    previousStatus: string;
    newStatus: string;
    changedBy: string;
  };
}

/** Union of all event types the broker can handle. */
export type BrokerEvent =
  | NotificationRequestedEvent
  | AuditRequestedEvent
  | LoanStateChangedEvent;

export type EventType = BrokerEvent["type"];
