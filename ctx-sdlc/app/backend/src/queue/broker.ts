// ---------------------------------------------------------------------------
// In-Process Event Broker
// ---------------------------------------------------------------------------
// A lightweight pub/sub broker for decoupling producers from consumers.
// Events are processed asynchronously but in-process (no external MQ).
//
// IMPORTANT — ORDERING:
//   Events are delivered in FIFO order per event type.  Handlers for the
//   same event type run sequentially; handlers for different types run
//   concurrently.  Do NOT rely on cross-type ordering.
//
// IMPORTANT — ERROR HANDLING:
//   If a handler throws, the error is logged but does NOT prevent other
//   handlers from running.  For critical operations (like audit writes),
//   the handler must implement its own retry logic.
// ---------------------------------------------------------------------------

import type { BrokerEvent, EventType } from "./contracts.js";

type EventHandler<T extends BrokerEvent = BrokerEvent> = (
  event: T,
) => Promise<void>;

class EventBroker {
  private handlers = new Map<EventType, EventHandler[]>();
  private pendingCount = 0;
  private eventHistory: Array<{ event: BrokerEvent; processedAt: string }> = [];
  private readonly maxHistory = 200;

  /**
   * Register a handler for a specific event type.
   * Handlers are called in registration order.
   */
  on<T extends BrokerEvent>(type: T["type"], handler: EventHandler<T>): void {
    const existing = this.handlers.get(type) ?? [];
    existing.push(handler as EventHandler);
    this.handlers.set(type, existing);
  }

  /**
   * Emit an event.  All registered handlers are invoked asynchronously.
   * Returns immediately — use `flush()` in tests to await completion.
   */
  emit(event: BrokerEvent): void {
    const handlers = this.handlers.get(event.type) ?? [];
    if (handlers.length === 0) {
      console.warn(
        `[broker] No handlers registered for event type: ${event.type}`,
      );
      return;
    }

    this.pendingCount++;
    this.eventHistory.push({ event, processedAt: new Date().toISOString() });
    if (this.eventHistory.length > this.maxHistory) {
      this.eventHistory.shift();
    }
    this.processHandlers(event, handlers).finally(() => {
      this.pendingCount--;
    });
  }

  /**
   * Wait for all pending event processing to complete.
   * Used in tests to ensure deterministic assertions.
   */
  async flush(): Promise<void> {
    // Spin-wait with setImmediate until all handlers finish
    while (this.pendingCount > 0) {
      await new Promise((resolve) => setImmediate(resolve));
    }
  }

  private async processHandlers(
    event: BrokerEvent,
    handlers: EventHandler[],
  ): Promise<void> {
    for (const handler of handlers) {
      try {
        await handler(event);
      } catch (err) {
        console.error(`[broker] Handler error for ${event.type}:`, err);
      }
    }
  }

  /** Return the list of registered event types and handler counts. */
  getSubscriptions(): Array<{ type: string; handlerCount: number }> {
    return Array.from(this.handlers.entries()).map(([type, handlers]) => ({
      type,
      handlerCount: handlers.length,
    }));
  }

  /** Return recent event history. */
  getHistory(limit = 50): Array<{ event: BrokerEvent; processedAt: string }> {
    return this.eventHistory.slice(-limit).reverse();
  }

  /** Return pending event count. */
  getPendingCount(): number {
    return this.pendingCount;
  }
}

/** Singleton broker instance — import this in producers and consumers. */
export const broker = new EventBroker();
