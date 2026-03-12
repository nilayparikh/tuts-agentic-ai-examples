#!/usr/bin/env bash
# Post-save formatting script.
# Called by the post-save hook to auto-format TypeScript files.

set -euo pipefail

FILE="$1"

if [[ "$FILE" == *.ts ]]; then
  npx prettier --write "$FILE"
fi
