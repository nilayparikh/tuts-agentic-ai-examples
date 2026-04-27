"""verify.py — Environment verification script.

Run this before starting the hands-on lessons to confirm your
Python version, packages, credentials, and LLM connectivity.

Course alignment:
    - Run this before the CleanLoop build lessons so environment failures are
        caught before you start the loop, dashboard, challenger, or reranker.

Usage:
    Preferred from cleanloop/:
        python util.py verify

    Direct module alternative:
        python -m cleanloop.verify

Environment variables (from .env):
    LLM_ENDPOINT    — Agnostic OpenAI-compatible endpoint
    LLM_API_KEY     — Agnostic API key
    MODEL_NAME      — Model deployment or model name
    LLM_API_VERSION — Optional provider-specific API version
    OPENAI_BASE_URL — Legacy fallback
    OPENAI_API_KEY  — Legacy fallback
    AZURE_ENDPOINT  — Legacy fallback
    AZURE_API_KEY   — Legacy fallback
"""

import sys
import warnings
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from cleanloop import util

util.load_env()


# =====================================================================
# SECTION: Verification Checks
# Four checks that confirm the local CleanLoop runtime is ready.
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
        "autogen_agentchat": "autogen-agentchat",
        "autogen_ext": "autogen-ext[openai,azure]",
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


def _safe_resolve_llm_env() -> dict[str, str] | None:
    """Resolve LLM config without crashing the learner-facing verify flow."""
    try:
        return util.resolve_llm_env()
    except RuntimeError as exc:
        print(f"  [FAIL] {exc}")
        return None


def check_credentials() -> bool:
    """Verify API credentials are configured in .env."""
    config = _safe_resolve_llm_env()
    if config is None:
        return False

    endpoint = config["endpoint"]
    api_key = config["api_key"]

    if endpoint and api_key:
        masked = endpoint[:35] + "..." if len(endpoint) > 35 else endpoint
        print(f"  [OK] Endpoint: {masked}")
        return True

    env_path = util.ENV_FILE
    if not env_path.exists():
        print(
            "  [FAIL] No cleanloop/.env file. Copy cleanloop/.env.example to cleanloop/.env"
        )
    elif not endpoint:
        print(f"  [FAIL] {config['endpoint_var']} not set in .env")
    else:
        print(f"  [FAIL] {config['api_key_var']} not set in .env")
    return False


def _resolve_verify_timeout_seconds() -> int:
    """Return the live LLM timeout budget for the verify command."""
    raw_value = util.os.getenv("CLEANLOOP_VERIFY_TIMEOUT_SECONDS", "20")
    try:
        timeout_seconds = int(raw_value)
    except ValueError:
        return 20
    return max(timeout_seconds, 1)


def check_llm_call() -> bool:
    """Verify an end-to-end LLM call works."""
    config = _safe_resolve_llm_env()
    if config is None:
        print("  [SKIP] No credentials — configure .env first")
        return True

    endpoint = config["endpoint"]
    api_key = config["api_key"]
    timeout_seconds = _resolve_verify_timeout_seconds()

    if not endpoint or not api_key:
        print("  [SKIP] No credentials — configure .env first")
        return True  # Non-blocking

    try:
        client = util.build_llm_client(endpoint, api_key, config["api_version"])
        # Suppress the known AutoGen model-alias warning so verify stays readable.
        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore",
                message=r"Resolved model mismatch: .*",
                category=UserWarning,
            )
            reply = util.create_text_completion(
                client,
                system_prompt="Reply with only the word hello.",
                user_prompt="Say hello.",
                max_tokens=10,
                timeout_seconds=timeout_seconds,
            )
        print(f"  [OK] LLM replied: {reply}")
        return True
    except TimeoutError:
        print(f"  [FAIL] LLM call timed out after {timeout_seconds}s")
        return False
    except Exception as exc:  # pylint: disable=broad-exception-caught
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
        print("\nReady for: python util.py loop")
    else:
        print("\nFix failing checks before proceeding.")
        sys.exit(1)


if __name__ == "__main__":
    main()
