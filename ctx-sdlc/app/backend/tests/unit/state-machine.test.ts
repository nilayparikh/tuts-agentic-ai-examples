// ---------------------------------------------------------------------------
// State Machine Tests
// ---------------------------------------------------------------------------

import { describe, it, expect } from "vitest";
import {
  canTransition,
  validNextStates,
  assertTransition,
} from "../../src/rules/state-machine.js";

describe("State Machine", () => {
  it("allows intake → review", () => {
    expect(canTransition("intake", "review")).toBe(true);
  });

  it("allows review → underwriting", () => {
    expect(canTransition("review", "underwriting")).toBe(true);
  });

  it("allows review → intake (rework)", () => {
    expect(canTransition("review", "intake")).toBe(true);
  });

  it("blocks intake → decision (skip)", () => {
    expect(canTransition("intake", "decision")).toBe(false);
  });

  it("blocks finalized → any state", () => {
    expect(canTransition("finalized", "intake")).toBe(false);
    expect(canTransition("finalized", "review")).toBe(false);
    expect(canTransition("finalized", "underwriting")).toBe(false);
    expect(canTransition("finalized", "decision")).toBe(false);
  });

  it("returns valid next states", () => {
    expect(validNextStates("decision")).toEqual(["finalized", "underwriting"]);
    expect(validNextStates("finalized")).toEqual([]);
  });

  it("assertTransition throws for invalid transitions", () => {
    expect(() => assertTransition("intake", "finalized")).toThrow(
      "INVALID_STATE",
    );
  });
});
