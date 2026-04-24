"""autonomy.py — Graduated Trust / Autonomy Ladder.

Four-level trust system that adjusts human oversight based on the
agent's track record. Starts with full human review and graduates
to full autonomy as the agent proves itself.

Levels:
  0 = SUPERVISED   — human approves every code change
  1 = MONITORED    — auto-applied, human notified
  2 = AUTONOMOUS   — auto-applied, human reviews async
  3 = FULL_AUTO    — no human in the loop

Lesson references:
  - Lesson 11: Lines 30-50   (trust levels + promotion thresholds)
  - Lesson 11: Lines 53-120  (TrustState class — the autonomy ladder)
  - Lesson 11: Lines 123-185 (simulation — watch trust evolve over rounds)

Usage:
    python -m cleanloop.autonomy
    python -m cleanloop.autonomy --rounds 20

No environment variables required (uses simulated data).
"""

import argparse
import random
from dataclasses import dataclass, field


# =====================================================================
# SECTION: Trust Configuration
# Lesson 11 — Four levels of autonomy. The thresholds are the
# minimum rolling pass rate needed to advance to the next level.
# These are deliberately conservative — it's easy to earn trust
# and very easy to lose it (any critical failure resets to L0).
# =====================================================================

TRUST_LEVELS: dict[int, str] = {
    0: "SUPERVISED",
    1: "MONITORED",
    2: "AUTONOMOUS",
    3: "FULL_AUTO",
}

# Rolling pass rate thresholds for promotion
PROMOTE_THRESHOLDS: dict[int, float] = {
    0: 0.70,   # SUPERVISED -> MONITORED: need 70% pass rate
    1: 0.85,   # MONITORED -> AUTONOMOUS: need 85% pass rate
    2: 0.95,   # AUTONOMOUS -> FULL_AUTO: need 95% pass rate
}

# Minimum rounds at current level before eligible for promotion
MIN_ROUNDS_FOR_PROMOTION = 3

# Number of recent rounds used for rolling average
WINDOW_SIZE = 5


# =====================================================================
# SECTION: TrustState — The Autonomy Ladder
# Lesson 11 — This class tracks the agent's trust level and
# makes promotion/demotion decisions based on performance.
#
# Key design decisions:
#   1. Rolling window (not lifetime average) — recent performance
#      matters more than ancient history
#   2. Instant demotion on critical failure — one zero-score round
#      drops trust all the way to SUPERVISED
#   3. Minimum tenure — must spend N rounds at a level before
#      promotion, even if pass rate is high (prevents lucky streaks)
# =====================================================================

@dataclass
class TrustState:
    """Track the agent's trust level and make autonomy decisions."""

    level: int = 0
    history: list[float] = field(default_factory=list)
    rounds_at_level: int = 0

    @property
    def level_name(self) -> str:
        """Human-readable name for the current trust level."""
        return TRUST_LEVELS.get(self.level, "UNKNOWN")

    @property
    def rolling_score(self) -> float:
        """Rolling average pass rate over the last WINDOW_SIZE rounds."""
        if not self.history:
            return 0.0
        window = self.history[-WINDOW_SIZE:]
        return sum(window) / len(window)

    def record_round(self, pass_rate: float) -> str:
        """Record a round and return the action taken.

        Returns one of: 'PROMOTED: X -> Y', 'DEMOTED: X -> Y', 'HOLD'.
        """
        self.history.append(pass_rate)
        self.rounds_at_level += 1

        # Critical failure: instant demotion to SUPERVISED
        if pass_rate == 0.0 and self.level > 0:
            old = self.level_name
            self.level = 0
            self.rounds_at_level = 0
            return f"DEMOTED: {old} -> SUPERVISED (critical failure)"

        # Check for promotion
        threshold = PROMOTE_THRESHOLDS.get(self.level, 1.0)
        if (
            self.level < 3
            and self.rounds_at_level >= MIN_ROUNDS_FOR_PROMOTION
            and self.rolling_score >= threshold
        ):
            old = self.level_name
            self.level += 1
            self.rounds_at_level = 0
            return f"PROMOTED: {old} -> {self.level_name}"

        return "HOLD"

    def should_auto_approve(self) -> bool:
        """Whether the agent's changes can be applied without review."""
        return self.level >= 2

    def needs_human_review(self) -> bool:
        """Whether a human must approve before applying changes."""
        return self.level == 0

    def needs_notification(self) -> bool:
        """Whether to notify the human (non-blocking)."""
        return self.level == 1


# =====================================================================
# SECTION: Simulation
# Lesson 11 — Simulates 10-20 rounds of the loop with realistic
# pass rates to demonstrate how trust evolves. Includes occasional
# critical failures to show the demotion mechanism.
# =====================================================================

def simulate(n_rounds: int = 10) -> None:
    """Simulate loop iterations with graduated autonomy."""
    trust = TrustState()

    print("Graduated Autonomy Simulation")
    print("=" * 65)
    print(
        f"{'Round':<7} {'Rate':<8} {'Level':<14} "
        f"{'Action':<32} {'Mode'}"
    )
    print("-" * 65)

    for i in range(1, n_rounds + 1):
        # Simulate improving pass rates with variance
        base = min(0.95, 0.3 + i * 0.06)
        noise = random.uniform(-0.15, 0.10)
        rate = max(0.0, min(1.0, base + noise))

        # 5% chance of critical failure
        if random.random() < 0.05:
            rate = 0.0

        action = trust.record_round(rate)

        # Determine approval mode
        if trust.needs_human_review():
            mode = "[REVIEW]"
        elif trust.needs_notification():
            mode = "[NOTIFY]"
        elif trust.should_auto_approve():
            mode = "[AUTO]"
        else:
            mode = ""

        print(
            f"  {i:<5} {rate:<8.2f} {trust.level_name:<14} "
            f"{action:<32} {mode}"
        )

    print("-" * 65)
    print(f"\nFinal: {trust.level_name} (score: {trust.rolling_score:.2f})")


def main() -> None:
    """Run the autonomy simulation."""
    parser = argparse.ArgumentParser(
        description="Autonomy — Graduated trust simulation"
    )
    parser.add_argument(
        "--rounds", type=int, default=10,
        help="Number of rounds (default: 10)",
    )
    args = parser.parse_args()
    simulate(n_rounds=args.rounds)


if __name__ == "__main__":
    main()
