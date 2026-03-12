#!/usr/bin/env bash
# Pre-commit validation script.
# Called by the pre-commit hook to ensure code quality before committing.

set -euo pipefail

echo "=== Pre-commit validation ==="

# Step 1: TypeScript compilation check
echo "[1/3] Checking TypeScript compilation..."
npx tsc --noEmit
if [ $? -ne 0 ]; then
  echo "FAIL: TypeScript compilation errors found."
  exit 1
fi
echo "  OK"

# Step 2: Lint check (if eslint is configured)
if [ -f ".eslintrc.json" ] || [ -f "eslint.config.js" ]; then
  echo "[2/3] Running lint..."
  npx eslint src/ tests/ --max-warnings 0
  if [ $? -ne 0 ]; then
    echo "FAIL: Lint errors found."
    exit 1
  fi
  echo "  OK"
else
  echo "[2/3] Lint skipped (no eslint config found)"
fi

# Step 3: Run tests
echo "[3/3] Running tests..."
npx vitest run --reporter=verbose
if [ $? -ne 0 ]; then
  echo "FAIL: Test failures detected."
  exit 1
fi
echo "  OK"

echo "=== All checks passed ==="
