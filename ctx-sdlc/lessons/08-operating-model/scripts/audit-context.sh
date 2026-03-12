#!/usr/bin/env bash
# audit-context.sh — Context Health Audit Script
#
# Scans a project's .github/ and docs/ for common context health issues.
# Run from the project root: bash scripts/audit-context.sh
#
# Exit codes:
#   0 — all checks passed
#   1 — warnings found (non-critical)
#   2 — errors found (action required)

set -euo pipefail

RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

WARNINGS=0
ERRORS=0

warn()  { echo -e "${YELLOW}⚠ WARNING:${NC} $1"; ((WARNINGS++)); }
error() { echo -e "${RED}✗ ERROR:${NC} $1";   ((ERRORS++)); }
pass()  { echo -e "${GREEN}✓ PASS:${NC} $1"; }
info()  { echo -e "${CYAN}ℹ INFO:${NC} $1"; }

echo "═══════════════════════════════════════════"
echo " Context Health Audit"
echo " Project: $(basename "$(pwd)")"
echo " Date:    $(date -Iseconds)"
echo "═══════════════════════════════════════════"
echo ""

# ─── 1. Foundation Check ────────────────────────────────────
echo "── 1. Foundation ──"

if [ -f ".github/copilot-instructions.md" ]; then
  LINES=$(wc -l < ".github/copilot-instructions.md")
  if [ "$LINES" -gt 200 ]; then
    warn ".github/copilot-instructions.md is $LINES lines (max recommended: 200)"
  elif [ "$LINES" -lt 10 ]; then
    warn ".github/copilot-instructions.md is only $LINES lines (too minimal)"
  else
    pass ".github/copilot-instructions.md exists ($LINES lines)"
  fi
else
  error ".github/copilot-instructions.md not found (required for all surfaces)"
fi

# ─── 2. Instruction Files ───────────────────────────────────
echo ""
echo "── 2. Instruction Files ──"

INST_COUNT=0
INST_NO_SCOPE=0
if [ -d ".github/instructions" ]; then
  while IFS= read -r f; do
    ((INST_COUNT++))
    if ! head -5 "$f" | grep -q "applyTo"; then
      warn "$f missing applyTo frontmatter"
      ((INST_NO_SCOPE++))
    fi
  done < <(find .github/instructions -name "*.instructions.md" 2>/dev/null)
  if [ "$INST_COUNT" -gt 0 ]; then
    pass "Found $INST_COUNT instruction file(s)"
  fi
  if [ "$INST_NO_SCOPE" -gt 0 ]; then
    warn "$INST_NO_SCOPE instruction file(s) without applyTo scope"
  fi
else
  info "No .github/instructions/ directory (optional — added in Lesson 03)"
fi

# ─── 3. Agent Files ─────────────────────────────────────────
echo ""
echo "── 3. Agents ──"

if [ -d ".github/agents" ]; then
  AGENT_COUNT=0
  AGENT_NO_TOOLS=0
  while IFS= read -r f; do
    ((AGENT_COUNT++))
    if ! head -10 "$f" | grep -q "tools:"; then
      warn "$f has no tools: restriction (over-privileged agent)"
    fi
  done < <(find .github/agents -name "*.agent.md" 2>/dev/null)
  pass "Found $AGENT_COUNT agent(s)"
else
  info "No .github/agents/ directory (optional — added in Lesson 05)"
fi

# ─── 4. Prompt Files ────────────────────────────────────────
echo ""
echo "── 4. Prompts ──"

if [ -d ".github/prompts" ]; then
  PROMPT_COUNT=$(find .github/prompts -name "*.prompt.md" 2>/dev/null | wc -l)
  pass "Found $PROMPT_COUNT prompt file(s)"
else
  info "No .github/prompts/ directory (optional — added in Lesson 04)"
fi

# ─── 5. Documentation ───────────────────────────────────────
echo ""
echo "── 5. Documentation ──"

if [ -d "docs" ]; then
  DOC_COUNT=$(find docs -name "*.md" 2>/dev/null | wc -l)
  pass "Found $DOC_COUNT doc file(s) in docs/"

  # Check for ADRs
  if [ -d "docs/adr" ]; then
    ADR_COUNT=$(find docs/adr -name "*.md" 2>/dev/null | wc -l)
    pass "Found $ADR_COUNT ADR(s)"
  else
    info "No docs/adr/ directory (recommended for technology decisions)"
  fi
else
  warn "No docs/ directory (knowledge context layer missing)"
fi

# ─── 6. Stale References ────────────────────────────────────
echo ""
echo "── 6. Cross-Reference Integrity ──"

STALE_REFS=0
# Check if copilot-instructions.md references files that exist
if [ -f ".github/copilot-instructions.md" ]; then
  while IFS= read -r ref; do
    # Extract path-like references (e.g., /docs/architecture.md, docs/adr/)
    ref_path="${ref#/}"
    if [ ! -e "$ref_path" ] && [ ! -d "$ref_path" ]; then
      warn "copilot-instructions.md references '$ref_path' but it doesn't exist"
      ((STALE_REFS++))
    fi
  done < <(grep -oP '(?:see |See |reference )[`/]([^`\s]+)[`\s]' \
           .github/copilot-instructions.md 2>/dev/null \
           | grep -oP '[/\w][\w./-]+' || true)
fi

if [ "$STALE_REFS" -eq 0 ]; then
  pass "No stale cross-references detected"
fi

# ─── 7. Content Freshness ───────────────────────────────────
echo ""
echo "── 7. Content Freshness ──"

STALE_DAYS=90
STALE_COUNT=0
NOW=$(date +%s)

while IFS= read -r f; do
  MOD=$(stat -c %Y "$f" 2>/dev/null || stat -f %m "$f" 2>/dev/null || echo "$NOW")
  AGE=$(( (NOW - MOD) / 86400 ))
  if [ "$AGE" -gt "$STALE_DAYS" ]; then
    warn "$f not modified in $AGE days (threshold: $STALE_DAYS)"
    ((STALE_COUNT++))
  fi
done < <(find .github docs -name "*.md" 2>/dev/null)

if [ "$STALE_COUNT" -eq 0 ]; then
  pass "All context files modified within $STALE_DAYS days"
fi

# ─── 8. Anti-Pattern Detection ──────────────────────────────
echo ""
echo "── 8. Anti-Pattern Detection ──"

# Check for bloated instructions
if [ -f ".github/copilot-instructions.md" ]; then
  LINES=$(wc -l < ".github/copilot-instructions.md")
  if [ "$LINES" -gt 300 ]; then
    error "copilot-instructions.md is $LINES lines — split into .instructions.md files"
  fi
fi

# Check for duplicate rules across files
if [ -d ".github/instructions" ]; then
  DUP_CHECK=$(cat .github/copilot-instructions.md .github/instructions/*.instructions.md 2>/dev/null \
    | grep -i "^- " | sort | uniq -d | head -5)
  if [ -n "$DUP_CHECK" ]; then
    warn "Possible duplicate rules across instruction files:"
    echo "  $DUP_CHECK"
  fi
fi

# Check for agents without tool restrictions
if [ -d ".github/agents" ]; then
  while IFS= read -r f; do
    TOOL_LINE=$(head -20 "$f" | grep -c "tools:" || true)
    if [ "$TOOL_LINE" -eq 0 ]; then
      error "$f has no tool restrictions — over-privileged agent (anti-pattern #3)"
    fi
  done < <(find .github/agents -name "*.agent.md" 2>/dev/null)
fi

# ─── Summary ────────────────────────────────────────────────
echo ""
echo "═══════════════════════════════════════════"
echo " Summary"
echo "═══════════════════════════════════════════"
echo -e " ${GREEN}Passed${NC}    | ${YELLOW}Warnings: $WARNINGS${NC} | ${RED}Errors: $ERRORS${NC}"

if [ "$ERRORS" -gt 0 ]; then
  echo -e " ${RED}ACTION REQUIRED: Fix $ERRORS error(s) before proceeding.${NC}"
  exit 2
elif [ "$WARNINGS" -gt 0 ]; then
  echo -e " ${YELLOW}Review $WARNINGS warning(s) at your next maintenance cycle.${NC}"
  exit 1
else
  echo -e " ${GREEN}All checks passed. Context is healthy.${NC}"
  exit 0
fi
