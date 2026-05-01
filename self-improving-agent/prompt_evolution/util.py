"""Local CLI and environment helpers for Prompt Evolution Studio.

Run from this folder:
    python util.py scenarios
    python util.py loop --scenario makerspace_missing_booking
    python util.py dashboard

Environment:
    Loads prompt_evolution/.env first, then falls back to ../.env. Supports
    LLM_ENDPOINT, LLM_API_KEY, MODEL_NAME, LLM_API_VERSION, OPENAI_BASE_URL,
    OPENAI_API_KEY, AZURE_ENDPOINT, and AZURE_API_KEY.
"""

from __future__ import annotations

import argparse
import importlib
import importlib.util
import os
import platform
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Callable

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EXAMPLE_ROOT = Path(__file__).resolve().parent
VENV_DIR = PROJECT_ROOT / ".venv"
ENV_FILE = EXAMPLE_ROOT / ".env"
FALLBACK_ENV_FILE = PROJECT_ROOT / ".env"
DEFAULT_MODEL = "gpt-4.1-mini"
DEFAULT_API_VERSION = "2024-12-01-preview"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
sys.modules.setdefault("util", sys.modules[__name__])

CommandHandler = Callable[[argparse.Namespace], int]


def _load_dotenv_file(path: Path) -> bool:
    """Load one dotenv file if python-dotenv is available."""
    if not path.exists():
        return False
    try:
        dotenv_module = importlib.import_module("dotenv")
    except ImportError:
        return False
    load_dotenv = getattr(dotenv_module, "load_dotenv")
    load_dotenv(path, override=False)
    return True


def load_env() -> None:
    """Load the local .env first, then the shared parent .env."""
    _load_dotenv_file(ENV_FILE)
    _load_dotenv_file(FALLBACK_ENV_FILE)


def _is_azure_openai_endpoint(endpoint: str) -> bool:
    """Return whether an endpoint targets Azure OpenAI."""
    return ".openai.azure.com" in endpoint.lower()


def _normalize_endpoint(endpoint: str) -> str:
    """Normalize Azure OpenAI resources to their OpenAI-compatible route."""
    normalized = endpoint.rstrip("/")
    if _is_azure_openai_endpoint(normalized) and "/openai/v1" not in normalized:
        return f"{normalized}/openai/v1"
    return normalized


def resolve_llm_env() -> dict[str, str]:
    """Resolve OpenAI-compatible endpoint settings from the active environment."""
    load_env()
    endpoint = (
        os.getenv("LLM_ENDPOINT")
        or os.getenv("OPENAI_BASE_URL")
        or os.getenv("AZURE_ENDPOINT")
        or os.getenv("AZURE_OPENAI_ENDPOINT")
        or ""
    )
    api_key = (
        os.getenv("LLM_API_KEY")
        or os.getenv("OPENAI_API_KEY")
        or os.getenv("AZURE_API_KEY")
        or os.getenv("AZURE_OPENAI_API_KEY")
        or ""
    )
    model = (
        os.getenv("MODEL_NAME")
        or os.getenv("AZURE_OPENAI_DEPLOY_NAME")
        or DEFAULT_MODEL
    )
    api_version = (
        os.getenv("LLM_API_VERSION")
        or os.getenv("AZURE_API_VERSION")
        or os.getenv("AZURE_OPENAI_API_VERSION")
        or DEFAULT_API_VERSION
    )
    return {
        "endpoint": endpoint,
        "api_key": api_key,
        "model": model,
        "api_version": api_version,
    }


def build_llm_client(endpoint: str, api_key: str, api_version: str) -> Any:
    """Build an OpenAI-compatible client for verification probes."""
    openai_module = importlib.import_module("openai")
    normalized_endpoint = _normalize_endpoint(endpoint)
    if _is_azure_openai_endpoint(endpoint) and "/openai/v1" not in endpoint:
        azure_openai = getattr(openai_module, "AzureOpenAI")
        return azure_openai(
            azure_endpoint=endpoint.rstrip("/"),
            api_key=api_key,
            api_version=api_version,
            max_retries=1,
        )
    openai_client = getattr(openai_module, "OpenAI")
    return openai_client(base_url=normalized_endpoint, api_key=api_key, max_retries=1)


def _is_capacity_error(exc: Exception) -> bool:
    """Return whether an exception looks like transient provider saturation."""
    status_code = getattr(exc, "status_code", None)
    message = str(exc).lower()
    return status_code == 429 or "429" in message or "rate limit" in message


def format_llm_exception(exc: Exception) -> str:
    """Render provider exceptions as learner-facing messages."""
    if _is_capacity_error(exc):
        return f"Endpoint busy or rate limited: {exc}"
    return f"LLM call failed: {exc}"


def create_chat_completion_with_backoff(client: Any, **kwargs: Any) -> Any:
    """Run a chat completion with short retries for transient capacity failures."""
    last_exc: Exception | None = None
    for attempt in range(1, 4):
        try:
            return client.chat.completions.create(**kwargs)
        except Exception as exc:  # pylint: disable=broad-exception-caught
            last_exc = exc
            if not _is_capacity_error(exc) or attempt == 3:
                raise
            time.sleep(float(attempt))
    raise RuntimeError(f"completion retry failed: {last_exc}")


def chat_completion_options(max_tokens: int, temperature: float | None = None) -> dict:
    """Return shared completion options for local helper modules."""
    options: dict[str, object] = {"max_tokens": max_tokens, "reasoning_effort": "low"}
    if temperature is not None:
        options["temperature"] = temperature
    return options


def _normalize_probe_reply(content: str | None) -> str:
    """Return a safe display string for an LLM verification reply."""
    if content is None:
        return "(empty reply)"
    return content.strip() or "(empty reply)"


def _get_python_path() -> Path:
    """Return the shared parent virtual environment interpreter."""
    if platform.system() == "Windows":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def _venv_is_ready() -> bool:
    """Return whether the shared parent virtual environment exists."""
    return _get_python_path().exists()


def _should_bootstrap_to_venv(
    argv: list[str], current_python: Path | None = None
) -> bool:
    """Return whether this local command should re-run inside the shared venv."""
    if len(argv) < 2 or not _venv_is_ready():
        return False
    active_python = current_python or Path(sys.executable).resolve()
    return active_python.resolve() != _get_python_path().resolve()


def _catalog() -> tuple[Any, Any]:
    """Load the Prompt Evolution config module and catalog."""
    config_module = importlib.import_module("prompt_evolution.config")
    return config_module, config_module.load_catalog(EXAMPLE_ROOT / ".data")


def _default_scenario_slug(catalog: Any) -> str:
    """Return a stable default scenario slug."""
    if "makerspace_missing_booking" in catalog.scenarios:
        return "makerspace_missing_booking"
    return next(iter(catalog.scenarios))


def _profile(args: argparse.Namespace) -> tuple[Any, Any]:
    """Resolve CLI arguments into one prompt evolution selection profile."""
    config_module, catalog = _catalog()
    scenario = args.scenario or _default_scenario_slug(catalog)
    if scenario:
        return catalog, config_module.resolve_scenario_profile(
            catalog,
            scenario_slug=scenario,
            context_slug=args.context,
            overrides=tuple(args.preference or []),
            problem=args.problem,
        )
    return catalog, config_module.resolve_selection_profile(
        catalog,
        context_slug=args.context,
        preference_overrides=tuple(args.preference or []),
        problem=args.problem,
    )


def _dashboard_command() -> list[str] | None:
    """Return a Streamlit command for the local dashboard."""
    dashboard_path = EXAMPLE_ROOT / "dashboard.py"
    args = [
        "run",
        str(dashboard_path),
        "--server.headless=true",
        "--browser.gatherUsageStats=false",
        "--client.toolbarMode=minimal",
    ]
    if importlib.util.find_spec("streamlit") is not None:
        return [sys.executable, "-m", "streamlit", *args]
    uvx_path = shutil.which("uvx")
    if uvx_path:
        return [
            uvx_path,
            "--with",
            "pandas>=2.2.0",
            "--from",
            "streamlit>=1.45.0",
            "streamlit",
            *args,
        ]
    return None


def cmd_catalog(_args: argparse.Namespace) -> int:
    """List context packs and preference axes."""
    config_module, catalog = _catalog()
    print(config_module.describe_catalog(catalog))
    return 0


def cmd_scenarios(_args: argparse.Namespace) -> int:
    """List repeatable prompt evolution scenarios."""
    config_module, catalog = _catalog()
    print(config_module.describe_scenarios(catalog))
    return 0


def cmd_loop(args: argparse.Namespace) -> int:
    """Run the instruction evolution loop from this folder."""
    load_env()
    catalog, profile = _profile(args)
    loop_module = importlib.import_module("prompt_evolution.loop")
    history = loop_module.run_prompt_evolution(
        catalog,
        profile,
        max_iterations=args.max_iterations,
        log_sink=lambda message: print(f"NOTE: {message}"),
        run_instance=args.named_instance,
        use_reranker=args.rerank,
        candidate_count=args.candidates,
    )
    best = max(history, key=lambda item: (item["score"], item["round"]))
    print(f"Best score: {best['score']}/{best['total']}")
    print("Best response: .output/best_response.md")
    print("Best instructions: .output/best_instructions.md")
    return 0


def cmd_dashboard(_args: argparse.Namespace) -> int:
    """Launch the local Streamlit dashboard."""
    history_path = EXAMPLE_ROOT / ".output" / "latest_session.json"
    if not history_path.exists():
        print("No latest_session.json found. Run `python util.py loop` first.")
        return 1
    command = _dashboard_command()
    if command is None:
        print("ERROR: Streamlit is not installed and uvx is unavailable.")
        return 1
    env = os.environ.copy()
    pythonpath = env.get("PYTHONPATH")
    env["PYTHONPATH"] = (
        str(PROJECT_ROOT)
        if not pythonpath
        else str(PROJECT_ROOT) + os.pathsep + pythonpath
    )
    return int(
        subprocess.run(
            command,
            cwd=str(EXAMPLE_ROOT),
            env=env,
            check=False,
        ).returncode
    )


def cmd_status(_args: argparse.Namespace) -> int:
    """Print the Prompt Evolution project status."""
    status_module = importlib.import_module("prompt_evolution.status_snapshot")
    print(status_module.render_status(status_module.collect_status()))
    return 0


def cmd_verify(_args: argparse.Namespace) -> int:
    """Run Prompt Evolution verification checks."""
    verify_module = importlib.import_module("prompt_evolution.verify")
    return int(verify_module.main())


def cmd_evaluate(args: argparse.Namespace) -> int:
    """Evaluate a candidate response against a scenario."""
    if not args.candidate:
        print("ERROR: evaluate requires --candidate")
        return 1
    config_module, catalog = _catalog()
    scenario = args.scenario or _default_scenario_slug(catalog)
    _ = config_module
    prepare_module = importlib.import_module("prompt_evolution.prepare")
    candidate_text = Path(args.candidate).read_text(encoding="utf-8")
    result = prepare_module.evaluate_candidate(
        catalog,
        scenario_slug=scenario,
        candidate_text=candidate_text,
    )
    print(prepare_module.render_result(result))
    return 0


def cmd_sandbox(args: argparse.Namespace) -> int:
    """Run one isolated prompt evolution round."""
    load_env()
    catalog, profile = _profile(args)
    sandbox_module = importlib.import_module("prompt_evolution.sandbox")
    result = sandbox_module.run_one_round(
        catalog=catalog,
        profile=profile,
        timeout_seconds=float(args.timeout),
        max_iterations=1,
    )
    print(sandbox_module.render_result(result))
    return 0


def cmd_autonomy(args: argparse.Namespace) -> int:
    """Run sandbox rounds through the autonomy ladder."""
    load_env()
    catalog, profile = _profile(args)
    sandbox_module = importlib.import_module("prompt_evolution.sandbox")
    autonomy_module = importlib.import_module("prompt_evolution.autonomy")
    snapshots = []
    for _index in range(1, args.rounds + 1):
        outcome = sandbox_module.run_one_round(
            catalog=catalog,
            profile=profile,
            timeout_seconds=float(args.timeout),
            max_iterations=1,
        )
        snapshots.append(
            autonomy_module.RoundSnapshot(
                score=outcome.evaluation.total_score,
                total=outcome.evaluation.max_score,
            )
        )
    print(autonomy_module.render_decision(autonomy_module.evaluate_ladder(snapshots)))
    return 0


def cmd_challenge(args: argparse.Namespace) -> int:
    """Generate adversarial scenario variants."""
    _config_module, catalog = _catalog()
    challenger_module = importlib.import_module("prompt_evolution.challenger")
    scenario = args.scenario or _default_scenario_slug(catalog)
    case = catalog.scenarios[scenario]
    variants = challenger_module.generate_variants(case, tiers=args.levels)
    print(challenger_module.render_variant_summary(variants))
    return 0


def cmd_reset(_args: argparse.Namespace) -> int:
    """Reset Prompt Evolution runtime outputs while preserving gold references."""
    reset_module = importlib.import_module("prompt_evolution.reset_workflow")
    report = reset_module.reset(output_dir=EXAMPLE_ROOT / ".output")
    print(reset_module.render_report(report))
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Build the local Prompt Evolution command parser."""
    parser = argparse.ArgumentParser(description="Prompt Evolution local commands")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("catalog", help="List contexts and preferences")
    subparsers.add_parser("scenarios", help="List scenario cases")
    loop_parser = subparsers.add_parser("loop", help="Run the instruction loop")
    loop_parser.add_argument("--scenario", default=None)
    loop_parser.add_argument("--context", default=None)
    loop_parser.add_argument("--problem", default=None)
    loop_parser.add_argument("--preference", action="append", default=[])
    loop_parser.add_argument("--max-iterations", type=int, default=3)
    loop_parser.add_argument("--rerank", action="store_true")
    loop_parser.add_argument("--candidates", type=int, default=3)
    loop_parser.add_argument("--named-instance", default=None)
    subparsers.add_parser("dashboard", help="Launch Streamlit dashboard")
    subparsers.add_parser("status", help="Show project status")
    subparsers.add_parser("verify", help="Verify environment")
    evaluate_parser = subparsers.add_parser("evaluate", help="Evaluate candidate text")
    evaluate_parser.add_argument("--scenario", default=None)
    evaluate_parser.add_argument("--candidate", required=True)
    sandbox_parser = subparsers.add_parser("sandbox", help="Run one isolated round")
    sandbox_parser.add_argument("--scenario", default=None)
    sandbox_parser.add_argument("--context", default=None)
    sandbox_parser.add_argument("--problem", default=None)
    sandbox_parser.add_argument("--preference", action="append", default=[])
    sandbox_parser.add_argument("--timeout", type=int, default=30)
    autonomy_parser = subparsers.add_parser("autonomy", help="Run trust ladder rounds")
    autonomy_parser.add_argument("--scenario", default=None)
    autonomy_parser.add_argument("--context", default=None)
    autonomy_parser.add_argument("--problem", default=None)
    autonomy_parser.add_argument("--preference", action="append", default=[])
    autonomy_parser.add_argument("--rounds", type=int, default=5)
    autonomy_parser.add_argument("--timeout", type=int, default=30)
    challenge_parser = subparsers.add_parser("challenge", help="Generate variants")
    challenge_parser.add_argument("--scenario", default=None)
    challenge_parser.add_argument("--levels", type=int, nargs="+", default=[1, 2, 3])
    subparsers.add_parser("reset", help="Reset output artifacts")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the local Prompt Evolution command line."""
    if argv is None and _should_bootstrap_to_venv(sys.argv):
        result = subprocess.run(
            [str(_get_python_path()), str(EXAMPLE_ROOT / "util.py"), *sys.argv[1:]],
            cwd=str(EXAMPLE_ROOT),
            check=False,
        )
        return int(result.returncode)
    parser = build_parser()
    args = parser.parse_args(argv)
    handlers: dict[str, CommandHandler] = {
        "catalog": cmd_catalog,
        "scenarios": cmd_scenarios,
        "loop": cmd_loop,
        "dashboard": cmd_dashboard,
        "status": cmd_status,
        "verify": cmd_verify,
        "evaluate": cmd_evaluate,
        "sandbox": cmd_sandbox,
        "autonomy": cmd_autonomy,
        "challenge": cmd_challenge,
        "reset": cmd_reset,
    }
    return handlers[args.command](args)


if __name__ == "__main__":
    raise SystemExit(main())
