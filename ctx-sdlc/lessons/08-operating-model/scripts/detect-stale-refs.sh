#!/usr/bin/env bash
# detect-stale-refs.sh — Dead Reference Detection
#
# Scans all .md files in .github/ and docs/ for internal path references
# and reports any that point to files or directories that don't exist.
#
# Run from the project root: bash scripts/detect-stale-refs.sh

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

STALE=0
CHECKED=0

echo "Scanning for stale references..."
echo ""

# Collect all markdown files in context directories
FILES=$(find .github docs -name "*.md" 2>/dev/null)

for file in $FILES; do
  # Extract paths that look like file references:
  #   /docs/something.md, docs/adr/, src/routes/, etc.
  # Patterns matched:
  #   - backtick-wrapped paths: `src/routes/`
  #   - "see" references: see /docs/architecture.md
  #   - markdown links: [text](path)
  refs=$(grep -oP '(?:`|see\s+|See\s+|\]\()/?([a-zA-Z][\w./-]+\.(?:md|ts|js|json|yaml|yml))' "$file" 2>/dev/null \
    | grep -oP '[a-zA-Z][\w./-]+\.\w+' || true)

  dir_refs=$(grep -oP '(?:`|see\s+|See\s+|\]\()/?([a-zA-Z][\w/-]+/)' "$file" 2>/dev/null \
    | grep -oP '[a-zA-Z][\w/-]+/' || true)

  for ref in $refs; do
    ((CHECKED++))
    clean="${ref#/}"
    if [ ! -f "$clean" ]; then
      echo -e "${RED}✗ STALE${NC} $file → $clean (file not found)"
      ((STALE++))
    fi
  done

  for ref in $dir_refs; do
    ((CHECKED++))
    clean="${ref#/}"
    if [ ! -d "$clean" ]; then
      echo -e "${RED}✗ STALE${NC} $file → $clean (directory not found)"
      ((STALE++))
    fi
  done
done

echo ""
echo "────────────────────────"
echo "Checked: $CHECKED references"
if [ "$STALE" -gt 0 ]; then
  echo -e "${RED}Found: $STALE stale reference(s)${NC}"
  exit 1
else
  echo -e "${GREEN}All references valid.${NC}"
  exit 0
fi
