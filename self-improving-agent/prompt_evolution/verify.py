"""Prompt Evolution environment and provider verification.

Mirrors `cleanloop/verify.py` for the support-desk example. Confirms that
the local Python interpreter, packaged dependencies, and Hermes-compatible
endpoint are reachable before a learner runs the loop.
"""

from __future__ import annotations

import importlib
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import util

PROJECT_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_PACKAGES = (
    "streamlit",
    "pandas",
    "openai",
    "dotenv",
)


@dataclass(frozen=True)
class CheckResult:
    """One verification check outcome."""

    name: str
    passed: bool
    detail: str


def _check_python_version() -> CheckResult:
    """Confirm the active interpreter satisfies the lesson minimum."""
    is_ok = sys.version_info >= (3, 11)
    return CheckResult(
        name="python_version",
        passed=is_ok,
        detail=f"running {sys.version_info.major}.{sys.version_info.minor}, requires 3.11+",
    )


def _check_required_packages() -> CheckResult:
    """Confirm Streamlit and the LLM client packages are importable."""
    missing: list[str] = []
    for package in REQUIRED_PACKAGES:
        try:
            importlib.import_module(package)
        except ImportError:
            missing.append(package)
    if missing:
        return CheckResult(
            name="required_packages",
            passed=False,
            detail="missing: " + ", ".join(missing),
        )
    return CheckResult(
        name="required_packages",
        passed=True,
        detail="all required packages importable",
    )


def _check_env_resolution() -> CheckResult:
    """Confirm the shared environment file resolves a model and endpoint."""
    util.load_env()
    config = util.resolve_llm_env()
    if not config.get("model"):
        return CheckResult(
            name="env_resolution",
            passed=False,
            detail="MODEL is not set in the active .env",
        )
    if not config.get("endpoint"):
        return CheckResult(
            name="env_resolution",
            passed=False,
            detail="endpoint is not set in the active .env",
        )
    if not config.get("api_key"):
        return CheckResult(
            name="env_resolution",
            passed=False,
            detail="API key is not set in the active .env",
        )
    return CheckResult(
        name="env_resolution",
        passed=True,
        detail=f"model={config['model']}",
    )


def _check_live_completion() -> CheckResult:
    """Confirm the configured endpoint accepts a tiny live completion."""
    util.load_env()
    config = util.resolve_llm_env()
    try:
        client = util.build_llm_client(
            endpoint=config["endpoint"],
            api_key=config["api_key"],
            api_version=config.get("api_version", ""),
        )
        completion = util.create_chat_completion_with_backoff(
            client,
            model=config["model"],
            messages=[
                {"role": "system", "content": "Reply with just OK."},
                {"role": "user", "content": "ping"},
            ],
            max_tokens=4,
            temperature=0,
        )
    except Exception as exc:  # pylint: disable=broad-except
        return CheckResult(
            name="live_completion",
            passed=False,
            detail=util.format_llm_exception(exc),
        )
    content = None
    try:
        content = completion.choices[0].message.content
    except (AttributeError, IndexError):
        content = None
    text = util._normalize_probe_reply(content)  # pylint: disable=protected-access
    return CheckResult(
        name="live_completion",
        passed=True,
        detail=f"reply={text}",
    )


CHECKS: tuple[Callable[[], CheckResult], ...] = (
    _check_python_version,
    _check_required_packages,
    _check_env_resolution,
    _check_live_completion,
)


def run_checks() -> list[CheckResult]:
    """Run all verification checks in order."""
    return [check() for check in CHECKS]


def render_results(results: list[CheckResult]) -> str:
    """Render verification results as plain-text output."""
    lines: list[str] = []
    passed = 0
    for result in results:
        marker = "[OK]" if result.passed else "[FAIL]"
        lines.append(f"{marker} {result.name}: {result.detail}")
        if result.passed:
            passed += 1
    lines.append("")
    lines.append(f"Result: {passed}/{len(results)} checks passed.")
    return "\n".join(lines)


def main() -> int:
    """CLI entrypoint that runs every verification check and prints results."""
    results = run_checks()
    print(render_results(results))
    return 0 if all(result.passed for result in results) else 1
