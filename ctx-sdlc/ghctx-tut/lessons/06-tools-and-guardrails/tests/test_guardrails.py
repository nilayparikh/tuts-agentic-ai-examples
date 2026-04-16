"""Lesson 06 — Tools & Guardrails — execution-based validation tests.

Each test actually executes the guardrail script with simulated hook payloads
and checks the real stdout/exit-code.  Positive (allow) and negative (deny)
cases are paired so the VERIFICATION report shows both sides fired.

Test groups:
  1. File-protection hook    — 6 deny + 4 allow + 1 deny-message check
  2. Import-validation hook  — 3 deny + 3 allow
  3. MCP config permissions  — structural + read-only enforcement
  4. Cross-consistency       — hook↔script↔doc alignment
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

LESSON = Path(__file__).resolve().parent.parent
HOOKS_DIR = LESSON / ".github" / "hooks"
SCRIPTS_DIR = LESSON / ".github" / "scripts"
MCP_CONFIG = LESSON / ".github" / "mcp.json"
COPILOT_INSTRUCTIONS = LESSON / ".github" / "copilot-instructions.md"
DOCS_DIR = LESSON / "docs"

VALID_HOOK_EVENTS = {
    "PreToolUse",
    "PostToolUse",
    "PreAgentTurn",
    "PostAgentTurn",
    "PreStep",
    "PostStep",
    "OnError",
    "OnComplete",
}


# ── Shared helpers ──────────────────────────────────────────────────────────


def _run_hook_script(
    script: Path,
    tool_name: str,
    tool_input: dict,
) -> tuple[int, str]:
    """Execute a hook script with a JSON payload on stdin, return (rc, stdout)."""
    payload = json.dumps({"tool_name": tool_name, "tool_input": tool_input})
    result = subprocess.run(
        [sys.executable, str(script)],
        input=payload,
        capture_output=True,
        text=True,
        timeout=10,
    )
    return result.returncode, result.stdout


def _parse_decision(stdout: str) -> str:
    """Return 'deny', 'allow', or '' from hook stdout."""
    if not stdout.strip():
        return "allow"  # empty stdout = no objection
    try:
        data = json.loads(stdout)
    except json.JSONDecodeError:
        return ""
    return data.get("hookSpecificOutput", {}).get("permissionDecision", "allow")


# ══════════════════════════════════════════════════════════════════════════════
#  1.  FILE-PROTECTION HOOK  — check_protected_files.py
# ══════════════════════════════════════════════════════════════════════════════


class TestFileProtectionDeny:
    """Negative cases — file-protection script MUST deny these edits."""

    SCRIPT = SCRIPTS_DIR / "check_protected_files.py"

    def test_deny_env(self) -> None:
        """editFiles on .env → deny."""
        _, out = _run_hook_script(self.SCRIPT, "editFiles", {"files": [".env"]})
        assert _parse_decision(out) == "deny"

    def test_deny_env_local(self) -> None:
        """editFiles on .env.local → deny."""
        _, out = _run_hook_script(self.SCRIPT, "editFiles", {"files": [".env.local"]})
        assert _parse_decision(out) == "deny"

    def test_deny_env_production(self) -> None:
        """editFiles on .env.production → deny."""
        _, out = _run_hook_script(self.SCRIPT, "editFiles", {"files": [".env.production"]})
        assert _parse_decision(out) == "deny"

    def test_deny_feature_flags(self) -> None:
        """editFiles on feature-flags.ts → deny."""
        _, out = _run_hook_script(
            self.SCRIPT, "editFiles",
            {"files": ["src/backend/src/config/feature-flags.ts"]},
        )
        assert _parse_decision(out) == "deny"

    def test_deny_connection_ts(self) -> None:
        """editFiles on db/connection.ts → deny."""
        _, out = _run_hook_script(
            self.SCRIPT, "editFiles",
            {"files": ["src/backend/src/db/connection.ts"]},
        )
        assert _parse_decision(out) == "deny"

    def test_deny_create_env(self) -> None:
        """createFile on .env → deny."""
        _, out = _run_hook_script(self.SCRIPT, "createFile", {"filePath": ".env"})
        assert _parse_decision(out) == "deny"


class TestFileProtectionAllow:
    """Positive cases — file-protection script MUST allow these operations."""

    SCRIPT = SCRIPTS_DIR / "check_protected_files.py"

    def test_allow_regular_route(self) -> None:
        """editFiles on a normal route → allow."""
        _, out = _run_hook_script(
            self.SCRIPT, "editFiles",
            {"files": ["src/backend/src/routes/notifications.ts"]},
        )
        assert _parse_decision(out) == "allow"

    def test_allow_test_file(self) -> None:
        """editFiles on a test file → allow."""
        _, out = _run_hook_script(
            self.SCRIPT, "editFiles",
            {"files": ["src/backend/tests/unit/some.test.ts"]},
        )
        assert _parse_decision(out) == "allow"

    def test_allow_non_edit_tool(self) -> None:
        """readFile on .env → allow (only write tools are blocked)."""
        _, out = _run_hook_script(self.SCRIPT, "readFile", {"filePath": ".env"})
        assert _parse_decision(out) == "allow"

    def test_allow_docs(self) -> None:
        """editFiles on docs/ → allow."""
        _, out = _run_hook_script(
            self.SCRIPT, "editFiles",
            {"files": ["docs/security-policy.md"]},
        )
        assert _parse_decision(out) == "allow"


class TestFileProtectionDenyMessage:
    """Deny reason must reference the security-policy doc."""

    SCRIPT = SCRIPTS_DIR / "check_protected_files.py"

    def test_deny_reason_cites_policy(self) -> None:
        _, out = _run_hook_script(self.SCRIPT, "editFiles", {"files": [".env"]})
        data = json.loads(out)
        reason = data["hookSpecificOutput"]["permissionDecisionReason"]
        assert "security-policy" in reason.lower() or "security policy" in reason.lower()


# ══════════════════════════════════════════════════════════════════════════════
#  2.  IMPORT-VALIDATION HOOK  — validate_imports.py
# ══════════════════════════════════════════════════════════════════════════════


class TestImportValidationDeny:
    """Negative cases — import-validation script MUST deny barrel bypasses."""

    SCRIPT = SCRIPTS_DIR / "validate_imports.py"

    def test_deny_direct_rule_import(self) -> None:
        """createFile with import from '../rules/business-rules' → deny."""
        content = (
            'import { validateLoan } from "../rules/business-rules";\n'
            "export function handler() { return validateLoan(); }\n"
        )
        _, out = _run_hook_script(
            self.SCRIPT, "createFile",
            {
                "filePath": "src/backend/src/routes/loans.ts",
                "file_text": content,
            },
        )
        assert _parse_decision(out) == "deny"

    def test_deny_direct_service_import(self) -> None:
        """createFile with import from '../services/audit-service' → deny."""
        content = (
            'import { log } from "../services/audit-service";\n'
            "export function handler() { log(); }\n"
        )
        _, out = _run_hook_script(
            self.SCRIPT, "createFile",
            {
                "filePath": "src/backend/src/routes/audit.ts",
                "file_text": content,
            },
        )
        assert _parse_decision(out) == "deny"

    def test_deny_hyphenated_module_import(self) -> None:
        """createFile with any hyphenated deep-module import → deny."""
        content = (
            'import { machine } from "../models/state-machine";\n'
            "export const m = machine;\n"
        )
        _, out = _run_hook_script(
            self.SCRIPT, "createFile",
            {
                "filePath": "src/backend/src/routes/workflow.ts",
                "file_text": content,
            },
        )
        assert _parse_decision(out) == "deny"


class TestImportValidationAllow:
    """Positive cases — import-validation script MUST allow these patterns."""

    SCRIPT = SCRIPTS_DIR / "validate_imports.py"

    def test_allow_barrel_import(self) -> None:
        """createFile with import from '../rules' (barrel) → allow."""
        content = (
            'import { validateLoan } from "../rules";\n'
            "export function handler() { return validateLoan(); }\n"
        )
        _, out = _run_hook_script(
            self.SCRIPT, "createFile",
            {
                "filePath": "src/backend/src/routes/loans.ts",
                "file_text": content,
            },
        )
        assert _parse_decision(out) == "allow"

    def test_allow_package_import(self) -> None:
        """createFile with import from 'express' (package) → allow."""
        content = (
            'import express from "express";\n'
            "const app = express();\n"
        )
        _, out = _run_hook_script(
            self.SCRIPT, "createFile",
            {
                "filePath": "src/backend/src/app.ts",
                "file_text": content,
            },
        )
        assert _parse_decision(out) == "allow"

    def test_allow_non_src_file(self) -> None:
        """createFile outside src tree → allow (no barrel enforcement)."""
        content = (
            'import { helper } from "../utils/some-helper";\n'
            "export const x = helper;\n"
        )
        _, out = _run_hook_script(
            self.SCRIPT, "createFile",
            {
                "filePath": "scripts/build.ts",
                "file_text": content,
            },
        )
        assert _parse_decision(out) == "allow"


# ══════════════════════════════════════════════════════════════════════════════
#  3.  MCP CONFIG — read-only permissions + server scope
# ══════════════════════════════════════════════════════════════════════════════


class TestMCPConfig:
    """Validate .github/mcp.json structure and enforced permissions."""

    @pytest.fixture
    def mcp(self) -> dict:
        assert MCP_CONFIG.exists(), ".github/mcp.json not found"
        return json.loads(MCP_CONFIG.read_text(encoding="utf-8"))

    def test_sqlite_read_only(self, mcp: dict) -> None:
        """SQLite server must be read=true, write=false."""
        perms = mcp["servers"]["sqlite"]["permissions"]
        assert perms["read"] is True and perms["write"] is False

    def test_filesystem_read_only(self, mcp: dict) -> None:
        """Filesystem server must be read=true, write=false."""
        perms = mcp["servers"]["filesystem"]["permissions"]
        assert perms["read"] is True and perms["write"] is False

    def test_sqlite_targets_database(self, mcp: dict) -> None:
        args = " ".join(mcp["servers"]["sqlite"]["args"])
        assert "loan-workbench.db" in args

    def test_filesystem_excludes_secrets(self, mcp: dict) -> None:
        """No .env or node_modules in filesystem server scope."""
        args = mcp["servers"]["filesystem"]["args"]
        for a in args:
            assert ".env" not in a and "node_modules" not in a

    def test_filesystem_scopes_to_source(self, mcp: dict) -> None:
        args = " ".join(mcp["servers"]["filesystem"]["args"])
        assert "backend" in args and "docs" in args

    def test_servers_have_descriptions(self, mcp: dict) -> None:
        for name, server in mcp["servers"].items():
            assert "description" in server, f"'{name}' missing description"


# ══════════════════════════════════════════════════════════════════════════════
#  4.  HOOK CONFIG STRUCTURE
# ══════════════════════════════════════════════════════════════════════════════


class TestHookConfigs:
    """All hook JSON files are structurally valid."""

    @pytest.fixture(params=sorted(HOOKS_DIR.glob("*.json")), ids=lambda p: p.name)
    def hook_config(self, request: pytest.FixtureRequest) -> tuple[str, dict]:
        path: Path = request.param
        data = json.loads(path.read_text(encoding="utf-8"))
        return path.name, data

    def test_valid_event_types(self, hook_config: tuple[str, dict]) -> None:
        name, data = hook_config
        for event_type in data.get("hooks", {}):
            assert event_type in VALID_HOOK_EVENTS, f"{name}: unknown event '{event_type}'"

    def test_entries_have_type_and_command(self, hook_config: tuple[str, dict]) -> None:
        name, data = hook_config
        for event_type, entries in data.get("hooks", {}).items():
            for i, entry in enumerate(entries):
                assert "type" in entry and "command" in entry, (
                    f"{name}.{event_type}[{i}] missing type/command"
                )

    def test_referenced_scripts_exist(self, hook_config: tuple[str, dict]) -> None:
        name, data = hook_config
        for entries in data.get("hooks", {}).values():
            for entry in entries:
                for part in entry["command"].split():
                    if part.endswith(".py"):
                        assert (LESSON / part).exists(), f"{name} refs missing {part}"


# ══════════════════════════════════════════════════════════════════════════════
#  5.  CROSS-CONSISTENCY — docs ↔ config ↔ scripts
# ══════════════════════════════════════════════════════════════════════════════


class TestCrossConsistency:
    """Hook scripts, configs, docs, and instructions agree with each other."""

    def test_all_scripts_valid_python(self) -> None:
        for script in SCRIPTS_DIR.glob("*.py"):
            result = subprocess.run(
                [sys.executable, "-m", "py_compile", str(script)],
                capture_output=True, text=True, timeout=10,
            )
            assert result.returncode == 0, f"{script.name}: {result.stderr}"

    def test_no_orphaned_scripts(self) -> None:
        """Each script is referenced by a hook or is the inline-prettier alternative."""
        cmds = []
        for path in HOOKS_DIR.glob("*.json"):
            data = json.loads(path.read_text(encoding="utf-8"))
            for entries in data.get("hooks", {}).values():
                cmds.extend(e.get("command", "") for e in entries)
        all_cmds = " ".join(cmds)
        for script in SCRIPTS_DIR.glob("*.py"):
            if script.stem == "format_file":
                assert "prettier" in all_cmds  # inline alternative
                continue
            assert script.stem in all_cmds, f"{script.name} orphaned"

    def test_trust_doc_covers_mcp_servers(self) -> None:
        trust = (DOCS_DIR / "tool-trust-boundaries.md").read_text(encoding="utf-8").lower()
        mcp = json.loads(MCP_CONFIG.read_text(encoding="utf-8"))
        for name in mcp["servers"]:
            assert name in trust, f"MCP server '{name}' not in trust boundaries doc"

    def test_security_policy_covers_protected_files(self) -> None:
        policy = (DOCS_DIR / "security-policy.md").read_text(encoding="utf-8")
        assert ".env" in policy and "feature-flags" in policy

    def test_instructions_reference_all_guardrails(self) -> None:
        inst = COPILOT_INSTRUCTIONS.read_text(encoding="utf-8").lower()
        for term in ["mcp", "hook", "read-only", "pre-commit", "security"]:
            assert term in inst, f"copilot-instructions.md missing '{term}'"

    def test_hook_count(self) -> None:
        assert len(list(HOOKS_DIR.glob("*.json"))) >= 4

    def test_script_count(self) -> None:
        assert len(list(SCRIPTS_DIR.glob("*.py"))) >= 4
