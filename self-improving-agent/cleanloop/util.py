"""Example-local environment, AutoGen helpers, and local CLI for CleanLoop."""

from __future__ import annotations

import argparse
import importlib
import importlib.util
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, cast

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EXAMPLE_ROOT = Path(__file__).resolve().parent
VENV_DIR = PROJECT_ROOT / ".venv"
INPUT_DIR = EXAMPLE_ROOT / ".input"
OUTPUT_DIR = EXAMPLE_ROOT / ".output"
GENOME_PATH = EXAMPLE_ROOT / "clean_data.py"
STARTER_GENOME_PATH = EXAMPLE_ROOT / "clean_data_starter.py"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

ENV_FILE = EXAMPLE_ROOT / ".env"
FALLBACK_ENV_FILE = PROJECT_ROOT / ".env"
DEFAULT_MODEL = "gpt-4.1-mini"
DEFAULT_API_VERSION = "2024-06-01"


def _load_dotenv_file(path: Path) -> bool:
    """Load one dotenv file if python-dotenv is installed and the file exists."""
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
    """Load the example-local .env first, then fall back to the shared example root."""
    _load_dotenv_file(ENV_FILE)
    _load_dotenv_file(FALLBACK_ENV_FILE)


def _resolve_llm_env() -> dict[str, str]:
    """Resolve the provider-agnostic LLM configuration for CleanLoop."""
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT") or ""
    generic_endpoint = os.getenv("LLM_ENDPOINT") or ""

    if azure_endpoint:
        endpoint_var = "AZURE_OPENAI_ENDPOINT"
    elif generic_endpoint:
        endpoint_var = "LLM_ENDPOINT"
    elif os.getenv("OPENAI_BASE_URL"):
        endpoint_var = "OPENAI_BASE_URL"
    else:
        endpoint_var = "AZURE_ENDPOINT"

    azure_api_key = os.getenv("AZURE_OPENAI_API_KEY") or ""
    generic_api_key = os.getenv("LLM_API_KEY") or ""

    if azure_endpoint and azure_api_key:
        api_key_var = "AZURE_OPENAI_API_KEY"
    elif generic_api_key:
        api_key_var = "LLM_API_KEY"
    elif os.getenv("OPENAI_API_KEY"):
        api_key_var = "OPENAI_API_KEY"
    elif os.getenv("GITHUB_TOKEN"):
        api_key_var = "GITHUB_TOKEN"
    else:
        api_key_var = "AZURE_API_KEY"

    endpoint = (
        azure_endpoint
        or generic_endpoint
        or os.getenv("OPENAI_BASE_URL")
        or os.getenv("AZURE_ENDPOINT")
        or ""
    )
    api_key = (
        (azure_api_key if azure_endpoint else "")
        or generic_api_key
        or os.getenv("OPENAI_API_KEY")
        or os.getenv("AZURE_API_KEY")
        or os.getenv("GITHUB_TOKEN")
        or ""
    )
    if azure_endpoint and os.getenv("AZURE_OPENAI_DEPLOY_NAME"):
        model = os.getenv("AZURE_OPENAI_DEPLOY_NAME") or DEFAULT_MODEL
    else:
        model = (
            os.getenv("MODEL_NAME")
            or os.getenv("AZURE_OPENAI_DEPLOY_NAME")
            or DEFAULT_MODEL
        )
    api_version = (
        os.getenv("LLM_API_VERSION")
        or os.getenv("AZURE_OPENAI_API_VERSION")
        or os.getenv("AZURE_API_VERSION")
        or DEFAULT_API_VERSION
    )

    if not endpoint:
        raise RuntimeError(
            "Missing LLM endpoint. Set LLM_ENDPOINT in cleanloop/.env or the example root .env."
        )
    if not api_key:
        raise RuntimeError(
            "Missing LLM API key. Set LLM_API_KEY in cleanloop/.env or the example root .env."
        )

    return {
        "endpoint": endpoint.rstrip("/"),
        "api_key": api_key,
        "model": model,
        "api_version": api_version,
        "endpoint_var": endpoint_var,
        "api_key_var": api_key_var,
    }


def resolve_llm_env() -> dict[str, str]:
    """Return the resolved CleanLoop LLM configuration."""
    return _resolve_llm_env()


def _is_azure_openai_endpoint(endpoint: str) -> bool:
    """Return whether the endpoint targets Azure OpenAI."""
    return ".openai.azure.com" in endpoint.lower()


def _is_github_models_endpoint(endpoint: str) -> bool:
    """Return whether the endpoint targets GitHub Models."""
    return "models.github.ai/inference" in endpoint.lower()


def _is_azure_ai_inference_endpoint(endpoint: str) -> bool:
    """Return whether the endpoint targets Azure AI Inference, not OpenAI-compatible chat."""
    normalized = endpoint.lower().rstrip("/")
    return (
        normalized.endswith("/models") or ".services.ai.azure.com/models" in normalized
    )


def _default_model_info() -> dict[str, object]:
    """Return a permissive model capability profile for OpenAI-compatible endpoints."""
    return {
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "family": "unknown",
        "structured_output": True,
    }


def _build_llm_client(endpoint: str, api_key: str, api_version: str) -> Any:
    """Build the correct AutoGen model client for the configured endpoint."""
    config = _resolve_llm_env()
    model = config["model"]
    temperature = float(os.getenv("AUTOGEN_TEMPERATURE", "0.2"))

    if _is_azure_ai_inference_endpoint(endpoint):
        azure_credentials_module = importlib.import_module("azure.core.credentials")
        azure_models_module = importlib.import_module("autogen_ext.models.azure")
        azure_key_credential = getattr(azure_credentials_module, "AzureKeyCredential")
        azure_client = getattr(azure_models_module, "AzureAIChatCompletionClient")
        return azure_client(
            model=model,
            endpoint=endpoint,
            credential=azure_key_credential(api_key),
            model_info=_default_model_info(),
            temperature=temperature,
        )

    openai_models_module = importlib.import_module("autogen_ext.models.openai")
    if _is_azure_openai_endpoint(endpoint):
        azure_openai_client = getattr(
            openai_models_module, "AzureOpenAIChatCompletionClient"
        )
        return azure_openai_client(
            model=model,
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOY_NAME") or model,
            azure_endpoint=endpoint,
            api_version=api_version,
            api_key=api_key,
            model_info=_default_model_info(),
            parallel_tool_calls=False,
            temperature=temperature,
        )

    openai_client = getattr(openai_models_module, "OpenAIChatCompletionClient")
    client_kwargs: dict[str, object] = {
        "model": model,
        "api_key": api_key,
        "parallel_tool_calls": False,
        "temperature": temperature,
    }
    if endpoint:
        client_kwargs["base_url"] = endpoint
        # OpenAI-compatible providers can expose non-OpenAI model IDs behind a
        # standard /v1 route, so always provide capabilities when base_url is explicit.
        client_kwargs["model_info"] = _default_model_info()
    return openai_client(**client_kwargs)


def build_llm_client(endpoint: str, api_key: str, api_version: str) -> Any:
    """Build an AutoGen model client from the resolved endpoint settings."""
    return _build_llm_client(endpoint, api_key, api_version)


def _is_capacity_error(exc: Exception) -> bool:
    """Return whether an exception looks like transient provider saturation."""
    status_code = getattr(exc, "status_code", None)
    if status_code == 429:
        return True

    message = str(exc).lower()
    return any(
        marker in message
        for marker in (
            "maximum concurrent capacity",
            "too many pending requests",
            "429",
            "rate limit",
        )
    )


def _format_llm_exception(exc: Exception) -> str:
    """Convert provider errors into clearer learner-facing messages."""
    if isinstance(exc, TimeoutError):
        return f"LLM request timed out: {exc}"
    if _is_capacity_error(exc):
        return (
            "Endpoint busy (429 capacity): "
            f"{exc}. The provider rejected the request before the model completed."
        )
    return f"LLM call failed: {exc}"


def format_llm_exception(exc: Exception) -> str:
    """Convert provider errors into clearer learner-facing messages."""
    return _format_llm_exception(exc)


def _build_text_completion_create_args(
    *,
    max_tokens: int,
    temperature: float | None,
) -> dict[str, object]:
    """Build provider-specific request args for plain text completions."""
    create_args: dict[str, object] = {"max_tokens": max_tokens}
    if temperature is not None:
        create_args["temperature"] = temperature

    return create_args


def create_text_completion(
    client: Any,
    *,
    system_prompt: str | None,
    user_prompt: str,
    max_tokens: int,
    timeout_seconds: int | None = None,
    temperature: float | None = None,
) -> str:
    """Run one plain-text completion through the AutoGen model client."""
    models_module = importlib.import_module("autogen_core.models")
    system_message_class = getattr(models_module, "SystemMessage")
    user_message_class = getattr(models_module, "UserMessage")
    messages: list[Any] = []
    if system_prompt:
        messages.append(system_message_class(content=system_prompt))
    messages.append(user_message_class(content=user_prompt, source="user"))

    create_args = _build_text_completion_create_args(
        max_tokens=max_tokens,
        temperature=temperature,
    )

    response = _run_coro(
        client.create(messages=messages, extra_create_args=create_args),
        timeout_seconds=timeout_seconds,
    )
    content = getattr(response, "content", "")
    if isinstance(content, str):
        return content.strip()
    raise RuntimeError(f"Expected a text response, received {type(content).__name__}.")


def _run_coro(coro: Any, timeout_seconds: int | None = None) -> Any:
    """Run a coroutine from the synchronous lesson modules."""
    import asyncio

    if timeout_seconds is not None:
        coro = asyncio.wait_for(coro, timeout=timeout_seconds)

    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)
    raise RuntimeError(
        "CleanLoop sync helpers cannot run inside an existing event loop."
    )


def _count_data_rows(path: Path) -> int:
    """Return the number of data rows in one UTF-8 CSV file."""
    return max(len(path.read_text(encoding="utf-8").strip().splitlines()) - 1, 0)


def _get_python_path() -> Path:
    """Return the Python interpreter path inside the shared example venv."""
    if platform.system() == "Windows":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def get_python_path() -> Path:
    """Return the Python interpreter path used by public CleanLoop wrappers."""
    return _get_python_path()


def _venv_is_ready() -> bool:
    """Return whether the shared example venv exists and is runnable."""
    return _get_python_path().exists()


def _should_bootstrap_to_venv(
    argv: list[str], current_python: Path | None = None
) -> bool:
    """Return whether the local CLI should re-exec inside the shared example venv."""
    if len(argv) < 2:
        return False
    if not _venv_is_ready():
        return False
    active_python = current_python or Path(sys.executable).resolve()
    return _get_python_path().resolve() != active_python.resolve()


def should_bootstrap_to_venv(
    argv: list[str], current_python: Path | None = None
) -> bool:
    """Return whether a public CleanLoop wrapper should re-exec in the venv."""
    return _should_bootstrap_to_venv(argv, current_python=current_python)


def _run_module_main(module_name: str, argv: list[str]) -> int:
    """Import a CleanLoop module and invoke its main() with temporary argv."""
    module = importlib.import_module(module_name)
    module_main = getattr(module, "main")
    old_argv = sys.argv[:]
    try:
        sys.argv = [module_name.rsplit(".", maxsplit=1)[-1], *argv]
        module_main()
    finally:
        sys.argv = old_argv
    return 0


def _cmd_status(_args: argparse.Namespace) -> int:
    """Print the local CleanLoop dataset and environment status."""
    from cleanloop.status_snapshot import (
        build_status_snapshot,
    )

    # Keep the CLI output simple while delegating the fact-gathering into a
    # small helper that lesson docs can point to directly.
    snapshot = build_status_snapshot(INPUT_DIR)

    print("CleanLoop — Project Status")
    print("\nInput Files:")
    input_rows = cast(dict[str, int], snapshot["input_rows"])
    for name, row_count in input_rows.items():
        print(f"  {name:<32} {int(row_count):>4} rows")

    print("\nEnvironment:")
    print(f"  Python:   {snapshot['python']}")
    print(f"  .env:     {'exists' if snapshot['env_exists'] else 'missing'}")
    print(f"  Model:    {snapshot['model']}")
    print(f"  Output:   {'exists' if snapshot['output_exists'] else 'missing'}")
    print(f"  Dataset:  {snapshot['dataset']}")
    return 0


def _cmd_verify(_args: argparse.Namespace) -> int:
    """Run the local CleanLoop environment verification."""
    return _run_module_main("cleanloop.verify", [])


def _cmd_evaluate(args: argparse.Namespace) -> int:
    """Evaluate the current genome output against the fixed referee."""
    from cleanloop import (
        clean_data,
        datasets,
        prepare,
    )

    target = (
        Path(args.output_csv).resolve()
        if args.output_csv
        else datasets.get_output_path(OUTPUT_DIR)
    )
    should_refresh_output = args.output_csv is None
    if should_refresh_output or not target.exists():
        OUTPUT_DIR.mkdir(exist_ok=True)
        clean_data.clean(INPUT_DIR, target)
        print(f"Ran genome. Output: {target}")

    results = prepare.evaluate(target)
    prepare.print_results(results)
    return 0


def _cmd_loop(args: argparse.Namespace) -> int:
    """Run the local self-improving loop."""
    from cleanloop import loop

    loop.run_loop(
        max_iterations=args.max_iterations,
        use_reranker=args.rerank,
        n_candidates=args.candidates,
        named_instance=args.named_instance,
    )
    return 0


def _cmd_challenge(args: argparse.Namespace) -> int:
    """Generate adversarial CSV files from the local CleanLoop folder."""
    argv: list[str] = []
    if args.levels:
        argv.extend(["--levels", *[str(level) for level in args.levels]])
    else:
        argv.extend(["--difficulty", str(args.difficulty), "--count", str(args.count)])
    return _run_module_main("cleanloop.challenger", argv)


def _cmd_sandbox(args: argparse.Namespace) -> int:
    """Run the genome in the sandbox from the local CleanLoop folder."""
    return _run_module_main("cleanloop.sandbox", ["--timeout", str(args.timeout)])


def _cmd_autonomy(args: argparse.Namespace) -> int:
    """Run the local autonomy simulation."""
    from cleanloop import autonomy

    autonomy.simulate(n_rounds=args.rounds)
    return 0


def _cmd_dashboard(_args: argparse.Namespace) -> int:
    """Launch the Streamlit dashboard from the local CleanLoop folder."""
    command = _streamlit_run_command(EXAMPLE_ROOT / "dashboard.py")
    if command is None:
        print(
            "ERROR: Streamlit is not installed and uvx is unavailable. "
            "Run `python -m pip install streamlit pandas` and retry."
        )
        return 1
    result = subprocess.run(
        command,
        cwd=str(PROJECT_ROOT),
        env=_streamlit_env(),
        check=False,
    )
    return int(result.returncode)


def _streamlit_env() -> dict[str, str]:
    """Return environment variables for non-interactive Streamlit launch."""
    streamlit_env = dict(os.environ)
    streamlit_env["STREAMLIT_SERVER_HEADLESS"] = "true"
    streamlit_env["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
    streamlit_env["STREAMLIT_CLIENT_TOOLBAR_MODE"] = "minimal"
    return streamlit_env


def _streamlit_run_args(dashboard_path: Path) -> list[str]:
    """Return the shared Streamlit dashboard arguments."""
    return [
        "run",
        str(dashboard_path),
        "--server.headless=true",
        "--browser.gatherUsageStats=false",
        "--client.toolbarMode=minimal",
    ]


def _streamlit_run_command(dashboard_path: Path) -> list[str] | None:
    """Return a Streamlit launch command, falling back to uvx when needed."""
    if importlib.util.find_spec("streamlit") is not None:
        return [sys.executable, "-m", "streamlit", *_streamlit_run_args(dashboard_path)]

    uvx_path = shutil.which("uvx")
    if uvx_path:
        return [
            uvx_path,
            "--with",
            "pandas>=2.2.0",
            "--from",
            "streamlit>=1.45.0",
            "streamlit",
            *_streamlit_run_args(dashboard_path),
        ]
    return None


def _cmd_reset(_args: argparse.Namespace) -> int:
    """Restore the starter genome without deleting the shipped sample outputs."""
    from cleanloop.reset_workflow import (
        reset_to_starter,
    )

    # Reset stays explicit so learners can see the trust-recovery path in one
    # place instead of hunting through a lesson-specific wrapper package.
    return reset_to_starter(
        output_dir=OUTPUT_DIR,
        genome_path=GENOME_PATH,
        starter_genome_path=STARTER_GENOME_PATH,
    )


def build_parser() -> argparse.ArgumentParser:
    """Build the CleanLoop-local command parser."""
    parser = argparse.ArgumentParser(description="CleanLoop — Local example commands")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("status", help="Show local dataset and environment status")
    subparsers.add_parser(
        "verify", help="Verify Python, packages, credentials, and connectivity"
    )

    evaluate_parser = subparsers.add_parser("evaluate", help="Run the fixed referee")
    evaluate_parser.add_argument(
        "output_csv", nargs="?", help="Optional output CSV to evaluate"
    )

    loop_parser = subparsers.add_parser("loop", help="Run the bounded mutation loop")
    loop_parser.add_argument(
        "--max-iterations",
        type=int,
        default=5,
        help="Maximum loop iterations (default: 5)",
    )
    loop_parser.add_argument(
        "--rerank",
        action="store_true",
        help="Use best-of-N reranking before committing a mutation",
    )
    loop_parser.add_argument(
        "--candidates",
        type=int,
        default=3,
        help="Number of reranker candidates (default: 3)",
    )
    loop_parser.add_argument(
        "--named-instance",
        default=None,
        help="Optional run-instance name for per-run logs, traces, and diagnostics",
    )

    challenge_parser = subparsers.add_parser(
        "challenge", help="Generate adversarial CSV files"
    )
    challenge_parser.add_argument(
        "--levels",
        type=int,
        nargs="+",
        help="Generate one adversarial CSV for each listed difficulty level",
    )
    challenge_parser.add_argument(
        "--difficulty",
        type=int,
        default=2,
        help="Difficulty 1-5 (default: 2)",
    )
    challenge_parser.add_argument(
        "--count",
        type=int,
        default=2,
        help="Number of files to generate when --levels is not used",
    )

    sandbox_parser = subparsers.add_parser(
        "sandbox", help="Run the genome in a subprocess"
    )
    sandbox_parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Sandbox timeout in seconds (default: 30)",
    )

    autonomy_parser = subparsers.add_parser(
        "autonomy", help="Run the trust-ladder simulation"
    )
    autonomy_parser.add_argument(
        "--rounds",
        type=int,
        default=10,
        help="Number of autonomy rounds (default: 10)",
    )

    subparsers.add_parser("dashboard", help="Launch the Streamlit dashboard")
    subparsers.add_parser("reset", help="Delete .output and restore the starter genome")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the CleanLoop-local CLI."""
    if argv is None and _should_bootstrap_to_venv(sys.argv):
        target_python = _get_python_path().resolve()
        result = subprocess.run(
            [str(target_python), str(EXAMPLE_ROOT / "util.py"), *sys.argv[1:]],
            cwd=str(PROJECT_ROOT),
            check=False,
        )
        return int(result.returncode)

    parser = build_parser()
    args = parser.parse_args(argv)
    handlers = {
        "status": _cmd_status,
        "verify": _cmd_verify,
        "evaluate": _cmd_evaluate,
        "loop": _cmd_loop,
        "challenge": _cmd_challenge,
        "sandbox": _cmd_sandbox,
        "autonomy": _cmd_autonomy,
        "dashboard": _cmd_dashboard,
        "reset": _cmd_reset,
    }
    return handlers[args.command](args)


if __name__ == "__main__":
    raise SystemExit(main())
