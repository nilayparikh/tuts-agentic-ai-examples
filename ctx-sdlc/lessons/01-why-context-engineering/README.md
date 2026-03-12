# Lesson 01 — Why Context Engineering

> **Template app:** `apps/complex/` (Loan Workbench)
> **Topic:** Demonstrating that the same prompt produces different code depending on what context the repository provides.

## Setup

```bash
python default.py --clean
cd src && npm install
```

See [SETUP.md](SETUP.md) for full details and validation scenarios.

## What This Lesson Demonstrates

This lesson runs **the same prompt** with and without custom instructions to
show how repository context changes Copilot output:

| Scenario          | Context Available                         | Expected Quality                      |
| ----------------- | ----------------------------------------- | ------------------------------------- |
| `without-context` | `--no-custom-instructions` — nothing read | Generic, misses domain rules          |
| `with-context`    | `.github/` + `docs/` auto-loaded          | Architecturally correct, domain-aware |

The **prompt is identical**. The **repository context** is what changes.

## Context Files

| Path                              | Purpose                                     |
| --------------------------------- | ------------------------------------------- |
| `.github/copilot-instructions.md` | Global project identity and rules           |
| `docs/architecture.md`            | System shape, domain model, key constraints |

## Validation

```bash
python validate.py --all
```

| Scenario          | Flag                       | What It Shows                                    |
| ----------------- | -------------------------- | ------------------------------------------------ |
| `without-context` | `--no-custom-instructions` | AI ignores `.github/` + `docs/` — generic output |
| `with-context`    | (default)                  | AI reads all context files — domain-aware output |

Outputs are saved to `output/` for comparison.

## Teaching Outcome

Learners should understand:

1. **Context engineering is not prompt engineering** — the prompt stays the same;
   the repository context changes.
2. **`.github/` files are automatically consumed** by Copilot — no manual
   attachment needed for instructions.
3. **`docs/` files provide architectural context** that instructions alone cannot
   capture (system shape, conventions, fallback behavior).
4. **Context is iterative** — you discover gaps by observing what the AI gets
   wrong and adding targeted context files.
