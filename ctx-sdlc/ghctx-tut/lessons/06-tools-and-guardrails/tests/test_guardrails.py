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
EVIDENCE_DIR = LESSON / ".output" / "evidence"
EVIDENCE_LOG = EVIDENCE_DIR / "guardrail-evidence.jsonl"

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


@pytest.fixture(scope="session", autouse=True)
def _reset_evidence_log() -> None:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    if EVIDENCE_LOG.exists():
        EVIDENCE_LOG.unlink()


def _append_evidence(
    classname: str,
    test_name: str,
    scenario: str,
    observed: str,
) -> None:
    record = {
        "classname": classname,
        "test_name": test_name,
        "scenario": scenario,
        "observed": observed,
    }
    with EVIDENCE_LOG.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record) + "\n")


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


def _hook_case(
    classname: str,
    test_name: str,
    script: Path,
    tool_name: str,
    tool_input: dict,
    expected_decision: str,
    expected_reason_fragment: str | None = None,
) -> None:
    return_code, stdout = _run_hook_script(script, tool_name, tool_input)
    actual_decision = _parse_decision(stdout)
    reason = ""
    if stdout.strip():
        try:
            reason = json.loads(stdout).get("hookSpecificOutput", {}).get(
                "permissionDecisionReason", ""
            )
        except json.JSONDecodeError:
            reason = "invalid-json"

    scenario = (
        f"script={script.relative_to(LESSON).as_posix()} tool={tool_name} "
        f"payload={json.dumps(tool_input, sort_keys=True)} expected={expected_decision}"
    )
    observed = (
        f"rc={return_code} decision={actual_decision} "
        f"stdout={stdout.strip() or '<empty>'}"
    )
    _append_evidence(classname, test_name, scenario, observed)

    assert actual_decision == expected_decision
    if expected_reason_fragment is not None:
        assert expected_reason_fragment.lower() in reason.lower()


def _static_case(
    classname: str,
    test_name: str,
    scenario: str,
    observed: str,
) -> None:
    _append_evidence(classname, test_name, scenario, observed)


# ══════════════════════════════════════════════════════════════════════════════
#  1.  FILE-PROTECTION HOOK  — check_protected_files.py
# ══════════════════════════════════════════════════════════════════════════════


class TestFileProtectionDeny:
    """Negative cases — file-protection script MUST deny these edits."""

    SCRIPT = SCRIPTS_DIR / "check_protected_files.py"

    def test_deny_env(self) -> None:
        """editFiles on .env → deny."""
        _hook_case(self.__class__.__name__, "test_deny_env", self.SCRIPT, "editFiles", {"files": [".env"]}, "deny")

    def test_deny_env_local(self) -> None:
        """editFiles on .env.local → deny."""
        _hook_case(self.__class__.__name__, "test_deny_env_local", self.SCRIPT, "editFiles", {"files": [".env.local"]}, "deny")

    def test_deny_env_production(self) -> None:
        """editFiles on .env.production → deny."""
        _hook_case(self.__class__.__name__, "test_deny_env_production", self.SCRIPT, "editFiles", {"files": [".env.production"]}, "deny")

    def test_deny_feature_flags(self) -> None:
        """editFiles on feature-flags.ts → deny."""
        _hook_case(
            self.__class__.__name__,
            "test_deny_feature_flags",
            self.SCRIPT,
            "editFiles",
            {"files": ["src/backend/src/config/feature-flags.ts"]},
            "deny",
        )

    def test_deny_connection_ts(self) -> None:
        """editFiles on db/connection.ts → deny."""
        _hook_case(
            self.__class__.__name__,
            "test_deny_connection_ts",
            self.SCRIPT,
            "editFiles",
            {"files": ["src/backend/src/db/connection.ts"]},
            "deny",
        )

    def test_deny_create_env(self) -> None:
        """createFile on .env → deny."""
        _hook_case(self.__class__.__name__, "test_deny_create_env", self.SCRIPT, "createFile", {"filePath": ".env"}, "deny")


class TestFileProtectionAllow:
    """Positive cases — file-protection script MUST allow these operations."""

    SCRIPT = SCRIPTS_DIR / "check_protected_files.py"

    def test_allow_regular_route(self) -> None:
        """editFiles on a normal route → allow."""
        _hook_case(
            self.__class__.__name__,
            "test_allow_regular_route",
            self.SCRIPT,
            "editFiles",
            {"files": ["src/backend/src/routes/notifications.ts"]},
            "allow",
        )

    def test_allow_test_file(self) -> None:
        """editFiles on a test file → allow."""
        _hook_case(
            self.__class__.__name__,
            "test_allow_test_file",
            self.SCRIPT,
            "editFiles",
            {"files": ["src/backend/tests/unit/some.test.ts"]},
            "allow",
        )

    def test_allow_non_edit_tool(self) -> None:
        """readFile on .env → allow (only write tools are blocked)."""
        _hook_case(self.__class__.__name__, "test_allow_non_edit_tool", self.SCRIPT, "readFile", {"filePath": ".env"}, "allow")

    def test_allow_docs(self) -> None:
        """editFiles on docs/ → allow."""
        _hook_case(
            self.__class__.__name__,
            "test_allow_docs",
            self.SCRIPT,
            "editFiles",
            {"files": ["docs/security-policy.md"]},
            "allow",
        )


class TestFileProtectionDenyMessage:
    """Deny reason must reference the security-policy doc."""

    SCRIPT = SCRIPTS_DIR / "check_protected_files.py"

    def test_deny_reason_cites_policy(self) -> None:
        _hook_case(
            self.__class__.__name__,
            "test_deny_reason_cites_policy",
            self.SCRIPT,
            "editFiles",
            {"files": [".env"]},
            "deny",
            "security",
        )


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
        _hook_case(
            self.__class__.__name__,
            "test_deny_direct_rule_import",
            self.SCRIPT,
            "createFile",
            {
                "filePath": "src/backend/src/routes/loans.ts",
                "file_text": content,
            },
            "deny",
        )

    def test_deny_direct_service_import(self) -> None:
        """createFile with import from '../services/audit-service' → deny."""
        content = (
            'import { log } from "../services/audit-service";\n'
            "export function handler() { log(); }\n"
        )
        _hook_case(
            self.__class__.__name__,
            "test_deny_direct_service_import",
            self.SCRIPT,
            "createFile",
            {
                "filePath": "src/backend/src/routes/audit.ts",
                "file_text": content,
            },
            "deny",
        )

    def test_deny_hyphenated_module_import(self) -> None:
        """createFile with any hyphenated deep-module import → deny."""
        content = (
            'import { machine } from "../models/state-machine";\n'
            "export const m = machine;\n"
        )
        _hook_case(
            self.__class__.__name__,
            "test_deny_hyphenated_module_import",
            self.SCRIPT,
            "createFile",
            {
                "filePath": "src/backend/src/routes/workflow.ts",
                "file_text": content,
            },
            "deny",
        )


class TestImportValidationAllow:
    """Positive cases — import-validation script MUST allow these patterns."""

    SCRIPT = SCRIPTS_DIR / "validate_imports.py"

    def test_allow_barrel_import(self) -> None:
        """createFile with import from '../rules' (barrel) → allow."""
        content = (
            'import { validateLoan } from "../rules";\n'
            "export function handler() { return validateLoan(); }\n"
        )
        _hook_case(
            self.__class__.__name__,
            "test_allow_barrel_import",
            self.SCRIPT,
            "createFile",
            {
                "filePath": "src/backend/src/routes/loans.ts",
                "file_text": content,
            },
            "allow",
        )

    def test_allow_package_import(self) -> None:
        """createFile with import from 'express' (package) → allow."""
        content = (
            'import express from "express";\n'
            "const app = express();\n"
        )
        _hook_case(
            self.__class__.__name__,
            "test_allow_package_import",
            self.SCRIPT,
            "createFile",
            {
                "filePath": "src/backend/src/app.ts",
                "file_text": content,
            },
            "allow",
        )

    def test_allow_non_src_file(self) -> None:
        """createFile outside src tree → allow (no barrel enforcement)."""
        content = (
            'import { helper } from "../utils/some-helper";\n'
            "export const x = helper;\n"
        )
        _hook_case(
            self.__class__.__name__,
            "test_allow_non_src_file",
            self.SCRIPT,
            "createFile",
            {
                "filePath": "scripts/build.ts",
                "file_text": content,
            },
            "allow",
        )


class TestDemoHarness:
    """Demo prompt and command must inject the lesson-local .github context."""

    def test_demo_prompt_targets_local_github(self) -> None:
        from util import _demo_prompt

        prompt = _demo_prompt()
        _static_case(
            self.__class__.__name__,
            "test_demo_prompt_targets_local_github",
            "prompt must explicitly target lesson-local .github paths",
            prompt,
        )
        assert "local .github" in prompt
        assert ".github/hooks/import-validation.json" in prompt
        assert ".github/scripts/validate_imports.py" in prompt

    def test_demo_command_injects_lesson_and_src(self) -> None:
        from util import _build_copilot_command

        command = _build_copilot_command("prompt", LESSON / "src", "copilot", "gpt-5.4")
        add_dirs = [command[i + 1] for i, token in enumerate(command[:-1]) if token == "--add-dir"]
        observed = f"add_dirs={json.dumps(add_dirs)}"
        _static_case(
            self.__class__.__name__,
            "test_demo_command_injects_lesson_and_src",
            "copilot command must inject lesson root and lesson src into context",
            observed,
        )
        assert str(LESSON) in add_dirs
        assert str(LESSON / "src") in add_dirs


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
        _static_case(self.__class__.__name__, "test_sqlite_read_only", "sqlite permissions must stay read-only", f"observed={json.dumps(perms, sort_keys=True)}")
        assert perms["read"] is True and perms["write"] is False

    def test_filesystem_read_only(self, mcp: dict) -> None:
        """Filesystem server must be read=true, write=false."""
        perms = mcp["servers"]["filesystem"]["permissions"]
        _static_case(self.__class__.__name__, "test_filesystem_read_only", "filesystem permissions must stay read-only", f"observed={json.dumps(perms, sort_keys=True)}")
        assert perms["read"] is True and perms["write"] is False

    def test_sqlite_targets_database(self, mcp: dict) -> None:
        args = " ".join(mcp["servers"]["sqlite"]["args"])
        _static_case(self.__class__.__name__, "test_sqlite_targets_database", "sqlite args must target the lesson database", f"args={args}")
        assert "loan-workbench.db" in args

    def test_filesystem_excludes_secrets(self, mcp: dict) -> None:
        """No .env or node_modules in filesystem server scope."""
        args = mcp["servers"]["filesystem"]["args"]
        _static_case(self.__class__.__name__, "test_filesystem_excludes_secrets", "filesystem args must exclude secrets and bulky folders", f"args={json.dumps(args)}")
        for a in args:
            assert ".env" not in a and "node_modules" not in a

    def test_filesystem_scopes_to_source(self, mcp: dict) -> None:
        args = " ".join(mcp["servers"]["filesystem"]["args"])
        _static_case(self.__class__.__name__, "test_filesystem_scopes_to_source", "filesystem args must stay scoped to source and docs", f"args={args}")
        assert "backend" in args and "docs" in args

    def test_servers_have_descriptions(self, mcp: dict) -> None:
        _static_case(self.__class__.__name__, "test_servers_have_descriptions", "every MCP server entry must carry a description", f"servers={json.dumps(sorted(mcp['servers'].keys()))}")
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
        _static_case(self.__class__.__name__, f"test_valid_event_types[{name}]", f"{name} must only use supported hook events", f"events={json.dumps(sorted(data.get('hooks', {}).keys()))}")
        for event_type in data.get("hooks", {}):
            assert event_type in VALID_HOOK_EVENTS, f"{name}: unknown event '{event_type}'"

    def test_entries_have_type_and_command(self, hook_config: tuple[str, dict]) -> None:
        name, data = hook_config
        _static_case(self.__class__.__name__, f"test_entries_have_type_and_command[{name}]", f"{name} entries must declare type and command", f"hook_count={sum(len(entries) for entries in data.get('hooks', {}).values())}")
        for event_type, entries in data.get("hooks", {}).items():
            for i, entry in enumerate(entries):
                assert "type" in entry and "command" in entry, (
                    f"{name}.{event_type}[{i}] missing type/command"
                )

    def test_referenced_scripts_exist(self, hook_config: tuple[str, dict]) -> None:
        name, data = hook_config
        script_refs = []
        for entries in data.get("hooks", {}).values():
            for entry in entries:
                for part in entry["command"].split():
                    if part.endswith(".py"):
                        script_refs.append(part)
                        assert (LESSON / part).exists(), f"{name} refs missing {part}"
        _static_case(self.__class__.__name__, f"test_referenced_scripts_exist[{name}]", f"{name} must point to scripts inside the lesson", f"script_refs={json.dumps(sorted(script_refs))}")


# ══════════════════════════════════════════════════════════════════════════════
#  5.  CROSS-CONSISTENCY — docs ↔ config ↔ scripts
# ══════════════════════════════════════════════════════════════════════════════


class TestCrossConsistency:
    """Hook scripts, configs, docs, and instructions agree with each other."""

    def test_all_scripts_valid_python(self) -> None:
        compiled = []
        for script in SCRIPTS_DIR.glob("*.py"):
            result = subprocess.run(
                [sys.executable, "-m", "py_compile", str(script)],
                capture_output=True, text=True, timeout=10,
            )
            compiled.append(script.name)
            assert result.returncode == 0, f"{script.name}: {result.stderr}"
        _static_case(self.__class__.__name__, "test_all_scripts_valid_python", "all lesson-local hook scripts must compile", f"compiled={json.dumps(sorted(compiled))}")

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
        _static_case(self.__class__.__name__, "test_no_orphaned_scripts", "every lesson-local script must be referenced by a hook or documented inline alternative", f"commands={json.dumps(cmds)}")

    def test_trust_doc_covers_mcp_servers(self) -> None:
        trust = (DOCS_DIR / "tool-trust-boundaries.md").read_text(encoding="utf-8").lower()
        mcp = json.loads(MCP_CONFIG.read_text(encoding="utf-8"))
        _static_case(self.__class__.__name__, "test_trust_doc_covers_mcp_servers", "trust boundaries doc must name every MCP server", f"servers={json.dumps(sorted(mcp['servers'].keys()))}")
        for name in mcp["servers"]:
            assert name in trust, f"MCP server '{name}' not in trust boundaries doc"

    def test_security_policy_covers_protected_files(self) -> None:
        policy = (DOCS_DIR / "security-policy.md").read_text(encoding="utf-8")
        _static_case(self.__class__.__name__, "test_security_policy_covers_protected_files", "security policy must mention protected files", "required_terms=['.env','feature-flags']")
        assert ".env" in policy and "feature-flags" in policy

    def test_instructions_reference_all_guardrails(self) -> None:
        inst = COPILOT_INSTRUCTIONS.read_text(encoding="utf-8").lower()
        _static_case(self.__class__.__name__, "test_instructions_reference_all_guardrails", "lesson-local copilot instructions must reference core guardrail concepts", "required_terms=['mcp','hook','read-only','pre-commit','security']")
        for term in ["mcp", "hook", "read-only", "pre-commit", "security"]:
            assert term in inst, f"copilot-instructions.md missing '{term}'"

    def test_hook_count(self) -> None:
        hook_count = len(list(HOOKS_DIR.glob("*.json")))
        _static_case(self.__class__.__name__, "test_hook_count", "lesson-local .github/hooks must contain the full guardrail set", f"hook_count={hook_count}")
        assert hook_count >= 4

    def test_script_count(self) -> None:
        script_count = len(list(SCRIPTS_DIR.glob("*.py")))
        _static_case(self.__class__.__name__, "test_script_count", "lesson-local .github/scripts must contain the expected scripts", f"script_count={script_count}")
        assert script_count >= 4
