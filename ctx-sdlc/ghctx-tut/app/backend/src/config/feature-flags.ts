// ---------------------------------------------------------------------------
// Feature Flags
// ---------------------------------------------------------------------------
// Runtime feature flags that control business behavior.
// These are loaded from environment variables via config/env.ts.
//
// IMPORTANT: Feature flags affect business rules, notification delivery,
// and audit behavior.  When adding a new flag, update:
//   1. config/env.ts  — add the env var mapping
//   2. This file      — add the typed accessor
//   3. docs/          — document the flag's behavior and rollout plan
// ---------------------------------------------------------------------------

import { config } from "./env.js";

export const featureFlags = {
  /** Enable California-specific lending regulations (higher thresholds, extra disclosures). */
  californiaRules: config.features.californiaRules,

  /** Enable SMS → email fallback when SMS provider is unavailable. */
  smsFallback: config.features.smsFallback,

  /** Route audit writes through the message queue instead of synchronous DB writes. */
  queueAudit: config.features.queueAudit,
} as const;

export type FeatureFlag = keyof typeof featureFlags;
