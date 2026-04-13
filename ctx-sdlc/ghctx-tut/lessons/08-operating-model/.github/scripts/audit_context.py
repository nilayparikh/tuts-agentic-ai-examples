#!/usr/bin/env python3
"""Context health audit script (Python replacement for audit-context.sh).

Scans a project's .github/ and docs/ for common context health issues.
Usage: python audit_context.py [--project-dir <path>]
"""
import argparse
import os
import re
import sys
import time
from pathlib import Path


class AuditCounter:
    def __init__(self) -> None:
        self.warnings = 0
        self.errors = 0

    def warn(self, msg: str) -> None:
        print(f"  ⚠ WARNING: {msg}")
        self.warnings += 1

    def error(self, msg: str) -> None:
        print(f"  ✗ ERROR: {msg}")
        self.errors += 1

    def ok(self, msg: str) -> None:
        print(f"  ✓ PASS: {msg}")

    def info(self, msg: str) -> None:
        print(f"  ℹ INFO: {msg}")


def audit(project_dir: Path) -> int:
    c = AuditCounter()

    print("═" * 45)
    print(f" Context Health Audit")
    print(f" Project: {project_dir.name}")
    print("═" * 45)

    # ─── 1. Foundation ─────────────────────────────
    print("\n── 1. Foundation ──")
    ci = project_dir / ".github" / "copilot-instructions.md"
    if ci.exists():
        lines = ci.read_text(encoding="utf-8").splitlines()
        n = len(lines)
        if n > 200:
            c.warn(f".github/copilot-instructions.md is {n} lines (max recommended: 200)")
        elif n < 10:
            c.warn(f".github/copilot-instructions.md is only {n} lines (too minimal)")
        else:
            c.ok(f".github/copilot-instructions.md exists ({n} lines)")
    else:
        c.error(".github/copilot-instructions.md not found")

    # ─── 2. Instruction files ──────────────────────
    print("\n── 2. Instruction Files ──")
    inst_dir = project_dir / ".github" / "instructions"
    if inst_dir.is_dir():
        inst_files = list(inst_dir.rglob("*.instructions.md"))
        no_scope = 0
        for f in inst_files:
            head = f.read_text(encoding="utf-8")[:300]
            if "applyTo" not in head:
                c.warn(f"{f.relative_to(project_dir)} missing applyTo frontmatter")
                no_scope += 1
        if inst_files:
            c.ok(f"Found {len(inst_files)} instruction file(s)")
        if no_scope:
            c.warn(f"{no_scope} instruction file(s) without applyTo scope")
    else:
        c.info("No .github/instructions/ directory (optional — added in Lesson 03)")

    # ─── 3. Agents ─────────────────────────────────
    print("\n── 3. Agents ──")
    agents_dir = project_dir / ".github" / "agents"
    if agents_dir.is_dir():
        agent_files = list(agents_dir.rglob("*.agent.md"))
        for f in agent_files:
            head = f.read_text(encoding="utf-8")[:500]
            if "tools:" not in head:
                c.warn(f"{f.relative_to(project_dir)} has no tools: restriction")
        c.ok(f"Found {len(agent_files)} agent(s)")
    else:
        c.info("No .github/agents/ directory (optional — added in Lesson 05)")

    # ─── 4. Prompts ────────────────────────────────
    print("\n── 4. Prompts ──")
    prompts_dir = project_dir / ".github" / "prompts"
    if prompts_dir.is_dir():
        prompt_count = len(list(prompts_dir.rglob("*.prompt.md")))
        c.ok(f"Found {prompt_count} prompt file(s)")
    else:
        c.info("No .github/prompts/ directory (optional — added in Lesson 04)")

    # ─── 5. Documentation ──────────────────────────
    print("\n── 5. Documentation ──")
    docs_dir = project_dir / "docs"
    if docs_dir.is_dir():
        doc_count = len(list(docs_dir.rglob("*.md")))
        c.ok(f"Found {doc_count} doc file(s) in docs/")
        adr_dir = docs_dir / "adr"
        if adr_dir.is_dir():
            adr_count = len(list(adr_dir.rglob("*.md")))
            c.ok(f"Found {adr_count} ADR(s)")
        else:
            c.info("No docs/adr/ directory (recommended for technology decisions)")
    else:
        c.warn("No docs/ directory (knowledge context layer missing)")

    # ─── 6. Cross-Reference Integrity ──────────────
    print("\n── 6. Cross-Reference Integrity ──")
    stale_refs = 0
    if ci.exists():
        text = ci.read_text(encoding="utf-8")
        # Match paths like /docs/something.md or docs/adr/
        refs = re.findall(r'[`/]([\w][\w./-]+\.(?:md|ts|js|json|yaml))[`\s]', text)
        refs += re.findall(r'(?:see |See )[`/]?([\w][\w./-]+)[`\s]', text)
        for ref in refs:
            ref_path = ref.lstrip("/")
            full = project_dir / ref_path
            if not full.exists():
                c.warn(f"copilot-instructions.md references '{ref_path}' but it doesn't exist")
                stale_refs += 1
    if stale_refs == 0:
        c.ok("No stale cross-references detected")

    # ─── 7. Content Freshness ──────────────────────
    print("\n── 7. Content Freshness ──")
    stale_days = 90
    stale_count = 0
    now = time.time()
    for search_dir in [project_dir / ".github", project_dir / "docs"]:
        if search_dir.is_dir():
            for f in search_dir.rglob("*.md"):
                age_days = int((now - f.stat().st_mtime) / 86400)
                if age_days > stale_days:
                    c.warn(f"{f.relative_to(project_dir)} not modified in {age_days} days (threshold: {stale_days})")
                    stale_count += 1
    if stale_count == 0:
        c.ok(f"All context files modified within {stale_days} days")

    # ─── 8. Anti-Pattern Detection ─────────────────
    print("\n── 8. Anti-Pattern Detection ──")
    if ci.exists():
        lines = ci.read_text(encoding="utf-8").splitlines()
        if len(lines) > 300:
            c.error(f"copilot-instructions.md is {len(lines)} lines — split into .instructions.md files")

    if agents_dir.is_dir():
        for f in agents_dir.rglob("*.agent.md"):
            head = f.read_text(encoding="utf-8")[:1000]
            if "tools:" not in head:
                c.error(f"{f.relative_to(project_dir)} has no tool restrictions — over-privileged agent")

    # ─── Summary ───────────────────────────────────
    print(f"\n{'═' * 45}")
    print(f" Summary: Warnings: {c.warnings} | Errors: {c.errors}")
    if c.errors > 0:
        print(f" ACTION REQUIRED: Fix {c.errors} error(s) before proceeding.")
        return 2
    elif c.warnings > 0:
        print(f" Review {c.warnings} warning(s).")
        return 1
    else:
        print(" All checks passed.")
        return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Context health audit")
    parser.add_argument("--project-dir", type=Path, default=Path.cwd(),
                        help="Project root to audit (default: cwd)")
    args = parser.parse_args()
    sys.exit(audit(args.project_dir))


if __name__ == "__main__":
    main()
