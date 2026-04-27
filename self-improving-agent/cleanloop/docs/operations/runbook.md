# Runbook

Use this order when teaching or validating CleanLoop.

1. `python util.py status`
2. `python util.py verify`
3. `python util.py evaluate`
4. `python util.py loop --max-iterations 5`
5. `python util.py dashboard`
6. `python util.py reset`

## Why This Order Works

- `status` proves the fixture is present.
- `verify` proves the runtime and `.env` work.
- `evaluate` proves the current genome and exports.
- `loop` demonstrates bounded mutation.
- `dashboard` exposes history and diagnostics.
- `reset` gets back to a known baseline without deleting the shipped sample outputs.
