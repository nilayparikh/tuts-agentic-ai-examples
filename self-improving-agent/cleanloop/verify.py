"""verify.py — Environment verification script.

Run this before starting the hands-on lessons to confirm your
Python version, packages, credentials, and LLM connectivity.

Lesson references:
  - Lesson 05: Lines 20-95  (all four verification checks)

Usage:
    python -m cleanloop.verify

Environment variables (from .env):
    AZURE_ENDPOINT  — Azure AI Foundry or Foundry Local endpoint
    AZURE_API_KEY   — API key
    MODEL_NAME      — Model deployment name (default: gpt-4o)
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")


# =====================================================================
# SECTION: Verification Checks
# Lesson 05 — Four checks that confirm the environment is ready.
# Each check prints [OK], [FAIL], or [SKIP] with details.
# =====================================================================

def check_python_version() -> bool:
    """Verify Python 3.11+ is installed."""
    ok = sys.version_info >= (3, 11)
    tag = "OK" if ok else "FAIL"
    print(f"  [{tag}] Python: {sys.version.split()[0]}")
    return ok


def check_packages() -> bool:
    """Verify all required packages are importable."""
    required = {
        "pandas": "pandas",
        "git": "gitpython",
        "openai": "openai",
        "streamlit": "streamlit",
        "dotenv": "python-dotenv",
    }
    missing = []
    for module, package in required.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)

    if missing:
        print(f"  [FAIL] Missing: pip install {' '.join(missing)}")
        return False

    print(f"  [OK] All {len(required)} packages installed")
    return True


def check_credentials() -> bool:
    """Verify API credentials are configured in .env."""
    endpoint = os.getenv("AZURE_ENDPOINT")
    api_key = os.getenv("AZURE_API_KEY")

    if endpoint and api_key:
        masked = endpoint[:35] + "..." if len(endpoint) > 35 else endpoint
        print(f"  [OK] Endpoint: {masked}")
        return True

    env_path = PROJECT_ROOT / ".env"
    if not env_path.exists():
        print(f"  [FAIL] No .env file. Copy .env.example to .env")
    elif not endpoint:
        print("  [FAIL] AZURE_ENDPOINT not set in .env")
    else:
        print("  [FAIL] AZURE_API_KEY not set in .env")
    return False


def check_llm_call() -> bool:
    """Verify an end-to-end LLM call works."""
    endpoint = os.getenv("AZURE_ENDPOINT")
    api_key = os.getenv("AZURE_API_KEY")
    model = os.getenv("MODEL_NAME", "gpt-4o")

    if not endpoint or not api_key:
        print("  [SKIP] No credentials — configure .env first")
        return True  # Non-blocking

    try:
        from openai import OpenAI  # pylint: disable=import-outside-toplevel
        client = OpenAI(base_url=endpoint, api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": "Reply with only: hello"}
            ],
            max_tokens=10,
        )
        reply = response.choices[0].message.content.strip()
        print(f"  [OK] LLM replied: {reply}")
        return True
    except Exception as exc:
        print(f"  [FAIL] {exc}")
        return False


def main() -> None:
    """Run all verification checks."""
    print("CleanLoop — Environment Verification\n")

    checks = [
        ("Python version", check_python_version),
        ("Required packages", check_packages),
        ("API credentials", check_credentials),
        ("LLM connectivity", check_llm_call),
    ]

    results = []
    for name, fn in checks:
        print(f"{name}:")
        results.append(fn())
        print()

    passed = sum(results)
    total = len(results)
    print(f"Result: {passed}/{total} checks passed.")

    if all(results):
        print("\nReady for Lesson 06.")
    else:
        print("\nFix failing checks before proceeding.")
        sys.exit(1)


if __name__ == "__main__":
    main()
