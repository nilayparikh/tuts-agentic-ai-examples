"""util.py — Self-Improving Agent Entry Point & Environment Manager.

Single entry point for the runnable tutorial demos. Uses ``--example`` to
route per-demo commands:

    python util.py setup                              Set up .venv
    python util.py verify                             Verify environment
    python util.py status                             Show full inventory

    python util.py --example cleanloop evaluate        Run referee
    python util.py --example cleanloop loop            Karpathy Loop
    python util.py --example cleanloop loop --rerank   Best-of-N
    python util.py -e cleanloop loop --named-instance nightly
    python util.py --example cleanloop dashboard       Streamlit UI
    python util.py --example cleanloop challenge       Adversarial data
    python util.py --example cleanloop sandbox         Subprocess isolation
    python util.py --example cleanloop autonomy        Trust ladder sim
    python util.py --example prompt_evolution catalog  Show contexts
    python util.py --example prompt_evolution scenarios Show demo cases
    python util.py --example prompt_evolution loop     Evolve instructions
    python util.py --example skill_mastery usecases    Show habit demos
    python util.py --example skill_mastery loop        Compose with habits
    python util.py --example skill_mastery loop --rerank --candidates 3
    python util.py --example skill_mastery sandbox     Single isolated round
    python util.py --example skill_mastery autonomy    Trust ladder sim
    python util.py --example skill_mastery challenge   Adversarial variants
    python util.py --example skill_mastery evaluate --candidate <path>
    python util.py --example skill_mastery verify      Env health checks
    python util.py --example skill_mastery status      Project snapshot

Short form:  python util.py -e cleanloop loop --rerank

Environment:
    Reads .env automatically from the project root.
    Supports Azure AI Foundry, Foundry Local, and OpenAI endpoints.
"""

# pylint: disable=too-many-lines

from __future__ import annotations

import argparse
import importlib
import importlib.util
import json
import os
import platform
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

CommandHandler = Callable[[argparse.Namespace], int]

from cleanloop import datasets as cleanloop_datasets  # noqa: E402

# ─── Project root: directory containing util.py ─────────────────────
ROOT = Path(__file__).resolve().parent
VENV_DIR = ROOT / ".venv"
INPUT_DIR = ROOT / "cleanloop" / ".input"
ENV_FILE = ROOT / ".env"
MIN_SUPPORTED_PYTHON = (3, 11)
MIN_SUPPORTED_PYTHON_TEXT = "3.11+"


def _output_dir(example: str) -> Path:
    """Return the .output directory for a given example project."""
    return ROOT / example / ".output"


def _activate_cleanloop_dataset(args: argparse.Namespace):
    """Persist the finance-only CleanLoop arena in the process environment."""
    dataset_name = getattr(args, "dataset", None)
    if not isinstance(dataset_name, str):
        dataset_name = None
    config = cleanloop_datasets.get_dataset_config(dataset_name)
    os.environ[cleanloop_datasets.CLEANLOOP_DATASET_ENV] = config.name
    return config


def _prompt_evolution_root() -> Path:
    """Return the prompt evolution example root."""
    return ROOT / "prompt_evolution"


def _skill_mastery_root() -> Path:
    """Return the Skill Mastery example root."""
    return ROOT / "skill_mastery"


def _is_supported_python(version_info) -> bool:
    """Return whether the supplied Python version meets the minimum requirement."""
    if hasattr(version_info, "major") and hasattr(version_info, "minor"):
        major = int(version_info.major)
        minor = int(version_info.minor)
    else:
        major = int(version_info[0])
        minor = int(version_info[1])
    return (major, minor) >= MIN_SUPPORTED_PYTHON


# =====================================================================
# Logging helpers — coloured, timestamped, learner-friendly
# =====================================================================


class _Colors:
    """ANSI colour codes (disabled when NO_COLOR is set or not a TTY)."""

    _enabled = sys.stdout.isatty() and "NO_COLOR" not in os.environ
    RESET = "\033[0m" if _enabled else ""
    BOLD = "\033[1m" if _enabled else ""
    GREEN = "\033[92m" if _enabled else ""
    YELLOW = "\033[93m" if _enabled else ""
    RED = "\033[91m" if _enabled else ""
    CYAN = "\033[96m" if _enabled else ""
    DIM = "\033[2m" if _enabled else ""
    BLUE = "\033[94m" if _enabled else ""
    MAGENTA = "\033[95m" if _enabled else ""


C = _Colors


def _ts() -> str:
    return datetime.now().strftime("%H:%M:%S")


def _status_prefix(kind: str) -> str:
    """Return an ASCII-only prefix for console status messages."""
    prefixes = {
        "ok": "OK:",
        "warn": "WARN:",
        "fail": "ERROR:",
        "info": "NOTE:",
    }
    return prefixes[kind]


def log_header(title: str) -> None:
    """Print a prominent section header."""
    width = 60
    print(f"\n{C.CYAN}{'=' * width}{C.RESET}")
    print(f"{C.CYAN}{C.BOLD}  {title}{C.RESET}")
    print(f"{C.CYAN}{'=' * width}{C.RESET}")


def log_step(step: int, total: int, msg: str) -> None:
    """Print a numbered step."""
    print(f"\n{C.BLUE}[{_ts()}]{C.RESET} {C.BOLD}Step {step}/{total}{C.RESET} — {msg}")


def log_ok(msg: str) -> None:
    """Print a success message."""
    print(f"  {C.GREEN}{_status_prefix('ok')}{C.RESET} {msg}")


def log_warn(msg: str) -> None:
    """Print a warning message."""
    print(f"  {C.YELLOW}{_status_prefix('warn')}{C.RESET} {msg}")


def log_fail(msg: str) -> None:
    """Print a failure message."""
    print(f"  {C.RED}{_status_prefix('fail')}{C.RESET} {msg}")


def log_info(msg: str) -> None:
    """Print an informational message."""
    print(f"  {C.DIM}{_status_prefix('info')}{C.RESET} {msg}")


def log_cmd(cmd: str) -> None:
    """Show a command being executed."""
    print(f"  {C.MAGENTA}${C.RESET} {C.DIM}{cmd}{C.RESET}")


# =====================================================================
# Command: setup — create .venv and install dependencies
# =====================================================================


def cmd_setup(_args: argparse.Namespace) -> int:
    """Set up virtual environment and install dependencies."""
    log_header("CleanLoop — Environment Setup")
    total_steps = 4

    # Step 1: Check Python version
    log_step(1, total_steps, "Checking Python version")
    v = sys.version_info
    if _is_supported_python(v):
        log_ok(f"Python {v.major}.{v.minor}.{v.micro}")
    else:
        log_fail(
            f"Python {v.major}.{v.minor}.{v.micro} — need {MIN_SUPPORTED_PYTHON_TEXT}"
        )
        log_info(f"Install Python {MIN_SUPPORTED_PYTHON_TEXT} from https://python.org")
        return 1

    # Step 2: Create virtual environment
    log_step(2, total_steps, "Creating virtual environment")
    if _venv_is_ready():
        log_ok(f".venv already exists at {VENV_DIR}")
    else:
        if VENV_DIR.exists():
            log_warn("Existing .venv is incomplete — recreating it")
            shutil.rmtree(VENV_DIR)
        log_cmd(f"python -m venv {VENV_DIR}")
        subprocess.run(
            [sys.executable, "-m", "venv", str(VENV_DIR)],
            check=True,
            cwd=str(ROOT),
        )
        log_ok(f"Created .venv at {VENV_DIR}")

    # Step 3: Install dependencies
    log_step(3, total_steps, "Installing dependencies")
    pip = _get_pip_path()
    req_file = ROOT / "requirements.txt"
    if not req_file.exists():
        log_fail("requirements.txt not found")
        return 1

    log_cmd(f"{pip} install -r requirements.txt")
    result = subprocess.run(
        [str(pip), "install", "-r", str(req_file)],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
        check=False,
    )
    if result.returncode == 0:
        # Count installed packages
        lines = [
            line
            for line in result.stdout.splitlines()
            if "Successfully" in line or "already satisfied" in line
        ]
        log_ok("All dependencies installed")
        for line in lines[:3]:
            log_info(line.strip())
    else:
        log_fail("pip install failed")
        for line in result.stderr.splitlines()[:5]:
            log_info(line)
        return 1

    # Step 4: Check .env
    log_step(4, total_steps, "Checking .env configuration")
    if ENV_FILE.exists():
        log_ok(f".env found at {ENV_FILE}")
        _show_env_summary()
    else:
        example = ROOT / ".env.example"
        if example.exists():
            log_warn(".env not found — copying from .env.example")
            log_info("Edit .env with your Azure AI Foundry credentials")
            shutil.copy(example, ENV_FILE)
            log_ok("Created .env from .env.example")
        else:
            log_fail("No .env or .env.example found")
            return 1

    log_header("Setup Complete")
    print("\n  Next steps:")
    print(f"  {C.CYAN}1.{C.RESET} Edit {C.BOLD}.env{C.RESET} with your credentials")
    print(f"  {C.CYAN}2.{C.RESET} Run: {C.BOLD}python util.py verify{C.RESET}")
    print(
        f"  {C.CYAN}3.{C.RESET} Run: "
        f"{C.BOLD}python util.py -e cleanloop loop{C.RESET}\n"
    )
    return 0


# =====================================================================
# Command: verify — check environment, credentials, LLM connectivity
# =====================================================================


def cmd_verify(_args: argparse.Namespace) -> int:
    """Verify environment is ready for the loop."""
    log_header("CleanLoop — Environment Verification")
    _load_env()

    checks = [
        ("Python version", _check_python),
        ("Required packages", _check_packages),
        ("Input data files", _check_input_files),
        ("API credentials", _check_credentials),
        ("LLM connectivity", _check_llm),
    ]

    results = []
    for i, (name, fn) in enumerate(checks, 1):
        log_step(i, len(checks), name)
        results.append(fn())

    passed = sum(results)
    total = len(results)
    print()
    if all(results):
        log_header(f"Verification Passed — {passed}/{total}")
        print(f"\n  Ready for: " f"{C.BOLD}python util.py -e cleanloop loop{C.RESET}\n")
        return 0
    else:
        log_header(f"Verification: {passed}/{total} passed")
        print(
            f"\n  Fix the failing checks, then re-run: {C.BOLD}python util.py verify{C.RESET}\n"
        )
        return 1


def _check_python() -> bool:
    v = sys.version_info
    ok = _is_supported_python(v)
    if ok:
        log_ok(f"Python {v.major}.{v.minor}.{v.micro}")
    else:
        log_fail(
            f"Python {v.major}.{v.minor}.{v.micro} — need {MIN_SUPPORTED_PYTHON_TEXT}"
        )
    return ok


def _check_packages() -> bool:
    required = {
        "pandas": "pandas",
        "git": "gitpython",
        "openai": "openai",
        "streamlit": "streamlit",
        "dotenv": "python-dotenv",
        "run_agent": "hermes-agent",
    }
    missing = []
    for module, package in required.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)

    if missing:
        log_fail(f"Missing: {', '.join(missing)}")
        log_info(f"Run: pip install {' '.join(missing)}")
        return False
    log_ok(f"All {len(required)} packages installed")
    return True


def _check_input_files() -> bool:
    if not INPUT_DIR.exists():
        log_fail("input/ directory not found")
        return False
    csv_files = sorted(INPUT_DIR.glob("*.csv"))
    if not csv_files:
        log_fail("No CSV files in input/")
        return False
    total_rows = 0
    total_files = 0
    config = cleanloop_datasets.get_dataset_config()
    log_info(f"Arena: {config.name} ({config.label})")
    for path in cleanloop_datasets.get_input_paths(INPUT_DIR):
        if not path.exists():
            log_fail(f"Missing dataset file: {path.name}")
            return False
        lines = _count_data_rows(path)
        total_rows += max(lines, 0)
        total_files += 1
        log_ok(f"{path.name} ({lines} rows)")
    log_info(f"Total: {total_files} files, ~{total_rows} data rows")
    return True


def _safe_resolve_llm_env() -> dict[str, str] | None:
    """Resolve LLM config without aborting the guided verify flow."""
    try:
        return _resolve_llm_env()
    except RuntimeError as exc:
        log_fail(str(exc))
        return None


def _check_credentials() -> bool:
    config = _safe_resolve_llm_env()
    if config is None:
        return False

    endpoint = config["endpoint"]
    api_key = config["api_key"]
    if endpoint and api_key:
        masked_endpoint = endpoint[:30] + "..." if len(endpoint) > 30 else endpoint
        masked_key = _mask_secret(api_key)
        log_ok(f"Endpoint: {masked_endpoint}")
        log_ok(f"API Key:  {masked_key}")
        model = config["model"]
        log_info(f"Model:    {model}")
        return True
    if not endpoint:
        log_fail(f"{config['endpoint_var']} not set in .env")
    if not api_key:
        log_fail(f"{config['api_key_var']} not set in .env")
    return False


def _check_llm() -> bool:
    config = _safe_resolve_llm_env()
    if config is None:
        log_warn("Skipped — configure credentials first")
        return True

    endpoint = config["endpoint"]
    api_key = config["api_key"]
    model = config["model"]
    api_version = config["api_version"]
    if not endpoint or not api_key:
        log_warn("Skipped — configure credentials first")
        return True  # Non-blocking

    try:
        client = _build_llm_client(endpoint, api_key, api_version)

        start = time.time()
        response = _create_chat_completion_with_backoff(
            client,
            model=model,
            messages=[{"role": "user", "content": "Reply with only: hello"}],
            retry_label="LLM connectivity probe",
            **_chat_completion_options(max_tokens=200, temperature=0),
        )
        elapsed = time.time() - start
        reply = _normalize_probe_reply(response.choices[0].message.content)
        log_ok(f'LLM replied: "{reply}" ({elapsed:.1f}s)')
        return True
    except Exception as exc:  # pylint: disable=broad-exception-caught
        log_fail(_format_llm_exception(exc))
        return False


# =====================================================================
# Command: evaluate — run referee on current output
# =====================================================================


def cmd_evaluate(args: argparse.Namespace) -> int:
    """Run the referee against the genome's output."""
    config = _activate_cleanloop_dataset(args)
    log_header(f"CleanLoop — Evaluate ({config.label})")
    _ensure_in_venv()

    cl_out = _output_dir("cleanloop")
    output_path = cleanloop_datasets.get_output_path(cl_out)

    # If no output exists, run the genome first
    if not output_path.exists():
        log_step(1, 2, "Running genome (no output yet)")
        log_info(f"Dataset: {config.name}")
        log_cmd(f"cleanloop.clean_data.clean(input/, .output/{output_path.name})")
        cl_out.mkdir(parents=True, exist_ok=True)
        from cleanloop import clean_data

        clean_data.clean(INPUT_DIR, output_path)
        log_ok(f"Output generated: {output_path}")
    else:
        log_step(1, 2, "Using existing output")
        log_ok(f"Found: {output_path}")

    # Evaluate
    log_step(2, 2, "Running binary assertions")
    from cleanloop import prepare

    results = prepare.evaluate(output_path)

    # Detailed results
    score = results["score"]
    total = results["total"]
    for item in results.get("passed", []):
        log_ok(f"PASS  {item}")
    for item in results.get("failed", []):
        log_fail(f"FAIL  {item}")

    print()
    if score == total:
        log_header(f"Score: {score}/{total} — All Assertions Pass!")
    else:
        log_header(f"Score: {score}/{total} — {total - score} Failing")
        print(
            f"\n  Run: {C.BOLD}python util.py -e cleanloop loop"
            f"{C.RESET} to fix automatically\n"
        )

    return 0 if score == total else 1


# =====================================================================
# Command: loop — run the self-improving Karpathy Loop
# =====================================================================


def cmd_loop(args: argparse.Namespace) -> int:
    """Run the self-improving loop."""
    config = _activate_cleanloop_dataset(args)
    rerank = getattr(args, "rerank", False)
    max_iter = getattr(args, "max_iterations", 5)
    candidates = getattr(args, "candidates", 3)
    named_instance = getattr(args, "named_instance", None)

    mode = "Best-of-N Reranking" if rerank else "Standard"
    log_header(f"CleanLoop — Karpathy Loop ({config.label}, {mode})")
    _ensure_in_venv()
    _load_env()

    log_info(f"Dataset: {config.name}")
    log_info(f"Max iterations: {max_iter}")
    if named_instance:
        log_info(f"Run instance: {named_instance}")
    log_info(f"Model: {os.getenv('MODEL_NAME', 'gpt-4o')}")
    if rerank:
        log_info(f"Candidates per round: {candidates}")

    log_step(1, 1, "Starting loop")
    print()

    from cleanloop.loop import run_loop

    history = run_loop(
        max_iterations=max_iter,
        use_reranker=rerank,
        n_candidates=candidates,
        named_instance=named_instance,
    )

    # Summary
    if history:
        final = history[-1]
        log_header(
            f"Loop Complete — {final['score']}/{final['total']} "
            f"in {len(history)} rounds"
        )
        print(
            f"\n  View results: "
            f"{C.BOLD}python util.py -e cleanloop dashboard{C.RESET}\n"
        )
    return 0


def _prompt_evolution_catalog():
    """Load the Prompt Evolution catalog lazily."""
    module = importlib.import_module("prompt_evolution.config")
    return module, module.load_catalog(_prompt_evolution_root() / ".data")


def _skill_mastery_catalog():
    """Load the Skill Mastery catalog lazily."""
    module = importlib.import_module("skill_mastery.config")
    return module, module.load_catalog(_skill_mastery_root() / ".data")


def _prompt_evolution_profile(args: argparse.Namespace):
    """Resolve CLI or interactive input into one prompt evolution profile."""
    config_module, catalog = _prompt_evolution_catalog()
    scenario = getattr(args, "scenario", None)
    context = getattr(args, "context", None)
    problem = getattr(args, "problem", None)
    preference_pairs = list(getattr(args, "preference", []) or [])

    if scenario:
        return catalog, config_module.resolve_scenario_profile(
            catalog,
            scenario_slug=scenario,
            preference_pairs=preference_pairs,
            problem=problem,
            context_slug=context,
        )

    if not context:
        print("\nAvailable contexts:")
        for slug, item in catalog.contexts.items():
            print(f"  - {slug}: {item.label}")
        context = input("Select context slug: ").strip()

    if len(preference_pairs) < 2:
        print("\nSelect at least two preferences.")
        for axis in catalog.preference_axes.values():
            options = ", ".join(sorted(axis.options))
            answer = input(f"  {axis.slug} [{options}] (blank to skip): ").strip()
            if answer:
                preference_pairs.append(f"{axis.slug}={answer}")

    if not problem:
        problem = input("\nDescribe the customer problem: ").strip()

    return catalog, config_module.resolve_selection_profile(
        catalog,
        problem=problem,
        context_slug=context,
        preference_pairs=preference_pairs,
    )


def _skill_mastery_profile(args: argparse.Namespace):
    """Resolve CLI or interactive input into one Skill Mastery profile."""
    config_module, catalog = _skill_mastery_catalog()
    usecase = getattr(args, "usecase", None)
    context = getattr(args, "context", None)
    problem = getattr(args, "problem", None)

    if usecase:
        return catalog, config_module.resolve_usecase_profile(
            catalog,
            usecase_slug=usecase,
            context_slug=context,
            problem=problem,
        )

    if not context:
        print("\nAvailable contexts:")
        for slug, item in catalog.contexts.items():
            print(f"  - {slug}: {item.label}")
        context = input("Select context slug: ").strip()

    if not problem:
        problem = input("\nDescribe the service problem: ").strip()

    return catalog, config_module.resolve_skill_profile(
        catalog,
        context_slug=context,
        problem=problem,
    )


def _best_history_round(history: list[dict[str, Any]]) -> dict[str, Any]:
    """Return the highest-scoring round from a local interactive review history."""
    return max(history, key=lambda item: (item["score"], item["round"]))


def _selected_history_round(history: list[dict[str, Any]]) -> dict[str, Any] | None:
    """Return the user-accepted round when interactive review marked one."""
    for round_data in reversed(history):
        if round_data.get("selected"):
            return round_data
    return None


def _selected_or_best_history_round(history: list[dict[str, Any]]) -> dict[str, Any]:
    """Return the accepted round when present, otherwise the evaluator-best round."""
    return _selected_history_round(history) or _best_history_round(history)


def _mark_selected_history_round(
    history: list[dict[str, Any]], round_data: dict[str, Any]
) -> None:
    """Mark one round as the user-selected output and clear older selections."""
    for entry in history:
        entry.pop("selected", None)
    round_data["selected"] = True


def _print_intermediate_round(example_label: str, round_data: dict[str, Any]) -> None:
    """Show one intermediate output snapshot before asking for more feedback."""
    print(
        f"\n{example_label} intermediate output "
        f"(round {round_data['round']}, score {round_data['score']}/{round_data['total']}):"
    )
    print(str(round_data["response"]).strip())
    issues = list(round_data.get("issues", []))
    if issues:
        print("\nEvaluator issues still visible:")
        for issue in issues:
            print(f"- {issue}")


def _interactive_review_loop(
    *,
    example_label: str,
    initial_history: list[dict[str, Any]],
    guidance_text: str,
    refine_once: Callable[[str, dict[str, Any], int], dict[str, Any]],
) -> list[dict[str, Any]]:
    """Ask for more feedback until the user accepts the current intermediate output."""
    history = list(initial_history)
    print("\nInteractive review guide:")
    print(guidance_text)

    while True:
        current_round = history[-1]
        _print_intermediate_round(example_label, current_round)
        print("\nAre you happy with this output? [Y/n]")
        happy_answer = input().strip().lower()
        if happy_answer in {"", "y", "yes"}:
            _mark_selected_history_round(history, current_round)
            break

        print("What should change next?")
        feedback = input().strip()
        if not feedback:
            log_info("No extra feedback entered. Keeping the current output.")
            _mark_selected_history_round(history, current_round)
            break

        updated_round = refine_once(
            feedback, current_round, int(current_round["round"]) + 1
        )
        history.append(updated_round)

    return history


def _should_offer_interactive_review() -> bool:
    """Return whether the current terminal session can support follow-up prompts."""
    return sys.stdin.isatty() and sys.stdout.isatty()


def cmd_prompt_evolution_catalog(_args: argparse.Namespace) -> int:
    """List the shipped context packs and preference axes."""
    config_module, catalog = _prompt_evolution_catalog()
    log_header("Prompt Evolution — Catalog")
    print(config_module.describe_catalog(catalog))
    print()
    return 0


def cmd_prompt_evolution_scenarios(_args: argparse.Namespace) -> int:
    """List the shipped Prompt Evolution scenario cases."""
    config_module, catalog = _prompt_evolution_catalog()
    log_header("Prompt Evolution — Scenarios")
    print(config_module.describe_scenarios(catalog))
    print()
    return 0


def cmd_skill_mastery_catalog(_args: argparse.Namespace) -> int:
    """List the shipped Skill Mastery contexts and habit seeds."""
    config_module, catalog = _skill_mastery_catalog()
    log_header("Skill Mastery — Catalog")
    print(config_module.describe_catalog(catalog))
    print()
    return 0


def cmd_skill_mastery_usecases(_args: argparse.Namespace) -> int:
    """List the shipped Skill Mastery use cases."""
    config_module, catalog = _skill_mastery_catalog()
    log_header("Skill Mastery — Use Cases")
    print(config_module.describe_usecases(catalog))
    print()
    return 0


def cmd_prompt_evolution_loop(args: argparse.Namespace) -> int:
    """Run the Hermes-backed instruction mutation loop."""
    log_header("Prompt Evolution — Instruction Loop")
    _ensure_in_venv()
    _load_env()

    try:
        catalog, profile = _prompt_evolution_profile(args)
    except ValueError as exc:
        log_fail(str(exc))
        return 1

    log_info(f"Context: {profile.context.label}")
    if profile.scenario is not None:
        log_info(f"Scenario: {profile.scenario.label}")
    log_info(
        f"Preferences: {', '.join(f'{k}={v}' for k, v in profile.selected_preferences.items())}"
    )
    log_info(f"Max iterations: {getattr(args, 'max_iterations', 3)}")

    loop_module = importlib.import_module("prompt_evolution.loop")
    history = loop_module.run_prompt_evolution(
        catalog,
        profile,
        max_iterations=getattr(args, "max_iterations", 3),
        log_sink=log_info,
        run_instance=getattr(args, "named_instance", None),
        use_reranker=bool(getattr(args, "rerank", False)),
        candidate_count=int(getattr(args, "candidates", 3)),
    )

    if _should_offer_interactive_review():
        guidance_text = loop_module.build_user_feedback_guide(catalog, profile)

        def refine_once(
            feedback: str, current_round: dict[str, Any], next_round: int
        ) -> dict[str, Any]:
            return loop_module.run_feedback_refinement(
                catalog,
                profile,
                current_instructions=str(current_round["instructions"]),
                current_response=str(current_round["response"]),
                round_number=next_round,
                user_feedback=feedback,
                log_sink=log_info,
            )

        history = _interactive_review_loop(
            example_label="Prompt Evolution",
            initial_history=history,
            guidance_text=guidance_text,
            refine_once=refine_once,
        )
        loop_module.save_outputs(profile, history)

    best = _selected_or_best_history_round(history)
    log_header(
        f"Prompt Evolution Complete — {best['score']}/{best['total']} in {len(history)} rounds"
    )
    print(
        f"\n  Best response: {C.BOLD}prompt_evolution/.output/best_response.md{C.RESET}"
    )
    print(
        f"  Best instructions: {C.BOLD}prompt_evolution/.output/best_instructions.md"
        f"{C.RESET}\n"
    )
    return 0


def cmd_skill_mastery_loop(args: argparse.Namespace) -> int:
    """Run the MaestroMotif-style habit learning and composition loop."""
    log_header("Skill Mastery — Habit Loop")
    _ensure_in_venv()
    _load_env()

    try:
        catalog, profile = _skill_mastery_profile(args)
    except ValueError as exc:
        log_fail(str(exc))
        return 1

    log_info(f"Context: {profile.context.label}")
    if profile.usecase is not None:
        log_info(f"Use case: {profile.usecase.label}")
    log_info(f"Max iterations: {getattr(args, 'max_iterations', 2)}")

    loop_module = importlib.import_module("skill_mastery.loop")
    history = loop_module.run_skill_mastery(
        catalog,
        profile,
        max_iterations=min(getattr(args, "max_iterations", 2), 3),
        log_sink=log_info,
        run_instance=getattr(args, "named_instance", None),
        use_reranker=bool(getattr(args, "rerank", False)),
        candidate_count=int(getattr(args, "candidates", 3) or 3),
    )

    if _should_offer_interactive_review():
        learner_module = importlib.import_module("skill_mastery.learner")
        selector_module = importlib.import_module("skill_mastery.selector")
        learned_habits = learner_module.learn_reusable_habits(catalog)
        selected_habits = selector_module.select_habits(profile, learned_habits)
        guidance_text = loop_module.build_user_feedback_guide(profile, selected_habits)

        def refine_once(
            feedback: str, current_round: dict[str, Any], next_round: int
        ) -> dict[str, Any]:
            return loop_module.run_feedback_refinement(
                profile,
                selected_habits,
                current_response=str(current_round["response"]),
                round_number=next_round,
                user_feedback=feedback,
                log_sink=log_info,
            )

        history = _interactive_review_loop(
            example_label="Skill Mastery",
            initial_history=history,
            guidance_text=guidance_text,
            refine_once=refine_once,
        )
        loop_module.save_outputs(profile, learned_habits, selected_habits, history)

    best = _selected_or_best_history_round(history)
    log_header(
        f"Skill Mastery Complete — {best['score']}/{best['total']} in {len(history)} rounds"
    )
    print(
        f"\n  Learned habits: {C.BOLD}skill_mastery/.output/learned_habits.json{C.RESET}"
    )
    print(
        f"  Selected habits: {C.BOLD}skill_mastery/.output/selected_habits.md{C.RESET}"
    )
    print(f"  Best response: {C.BOLD}skill_mastery/.output/best_response.md{C.RESET}\n")
    return 0


# =====================================================================
# Command: dashboard — launch Streamlit monitoring
# =====================================================================


def cmd_dashboard(args: argparse.Namespace) -> int:
    """Launch the Streamlit dashboard."""
    config = _activate_cleanloop_dataset(args)
    log_header(f"CleanLoop — Monitoring Dashboard ({config.label})")
    _ensure_in_venv()

    history_file = cleanloop_datasets.get_history_path(_output_dir("cleanloop"))
    if not history_file.exists():
        log_warn(f"No {history_file.name} found — run the loop first")
        log_info(f"Run: {C.BOLD}python util.py -e cleanloop loop{C.RESET}")
        return 1

    argv = _streamlit_run_command(ROOT / "cleanloop" / "dashboard.py")
    if argv is None:
        _log_missing_streamlit()
        return 1
    env = _streamlit_env()

    log_step(1, 1, "Launching Streamlit")
    log_cmd(" ".join(argv))
    print()

    os.execve(argv[0], argv, env)
    return 0  # unreachable after execv


def _streamlit_env() -> dict[str, str]:
    """Return environment variables for non-interactive Streamlit launch."""
    env = os.environ.copy()
    env["STREAMLIT_SERVER_HEADLESS"] = "true"
    env["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
    env["STREAMLIT_CLIENT_TOOLBAR_MODE"] = "minimal"
    return env


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
    streamlit_exe = _get_bin_path("streamlit")
    if streamlit_exe.exists():
        return [str(streamlit_exe), *_streamlit_run_args(dashboard_path)]
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


def _log_missing_streamlit() -> None:
    """Print the dashboard dependency recovery command."""
    log_fail("Streamlit is not installed and uvx is unavailable")
    log_info("Run: python -m pip install streamlit pandas")


def _run_example_dashboard(
    *,
    dashboard_path: Path,
    history_path: Path,
    title: str,
    rerun_cmd: str,
) -> int:
    """Launch a Streamlit dashboard for a non-CleanLoop example."""
    log_header(title)
    _ensure_in_venv()

    if not history_path.exists():
        log_warn(f"No {history_path.name} found — run the loop first")
        log_info(f"Run: {C.BOLD}{rerun_cmd}{C.RESET}")
        return 1

    argv = _streamlit_run_command(dashboard_path)
    if argv is None:
        _log_missing_streamlit()
        return 1
    env = _streamlit_env()
    log_step(1, 1, "Launching Streamlit")
    log_cmd(" ".join(argv))
    print()
    os.execve(argv[0], argv, env)
    return 0


def cmd_prompt_evolution_dashboard(_args: argparse.Namespace) -> int:
    """Launch the Prompt Evolution dashboard."""
    return _run_example_dashboard(
        dashboard_path=_prompt_evolution_root() / "dashboard.py",
        history_path=_output_dir("prompt_evolution") / "latest_session.json",
        title="Prompt Evolution — Dashboard",
        rerun_cmd="python util.py -e prompt_evolution loop",
    )


def cmd_prompt_evolution_status(_args: argparse.Namespace) -> int:
    """Render a prompt evolution project status snapshot."""
    log_header("Prompt Evolution — Status")
    status_module = importlib.import_module("prompt_evolution.status_snapshot")
    status = status_module.collect_status()
    print(status_module.render_status(status))
    return 0


def cmd_prompt_evolution_verify(_args: argparse.Namespace) -> int:
    """Run the prompt evolution environment verification checks."""
    log_header("Prompt Evolution — Verify")
    _ensure_in_venv()
    _load_env()
    verify_module = importlib.import_module("prompt_evolution.verify")
    return int(verify_module.main())


def cmd_prompt_evolution_evaluate(args: argparse.Namespace) -> int:
    """Score a candidate reply against a scenario gold target."""
    log_header("Prompt Evolution — Evaluate Candidate")
    scenario = getattr(args, "scenario", None)
    candidate_path = getattr(args, "candidate", None)
    if not scenario or not candidate_path:
        log_fail("evaluate requires --scenario and --candidate")
        return 1
    prepare_module = importlib.import_module("prompt_evolution.prepare")
    _config_module, catalog = _prompt_evolution_catalog()
    candidate_text = Path(candidate_path).read_text(encoding="utf-8")
    result = prepare_module.evaluate_candidate(
        catalog,
        scenario_slug=scenario,
        candidate_text=candidate_text,
    )
    print(prepare_module.render_result(result))
    return 0


def cmd_prompt_evolution_sandbox(args: argparse.Namespace) -> int:
    """Run a single isolated prompt-evolution round (no mutation, no persistence)."""
    log_header("Prompt Evolution — Sandbox Round")
    _ensure_in_venv()
    _load_env()
    try:
        catalog, profile = _prompt_evolution_profile(args)
    except ValueError as exc:
        log_fail(str(exc))
        return 1
    sandbox_module = importlib.import_module("prompt_evolution.sandbox")
    result = sandbox_module.run_one_round(
        catalog=catalog,
        profile=profile,
        timeout_seconds=float(getattr(args, "timeout", 30)),
        max_iterations=1,
    )
    print(sandbox_module.render_result(result))
    return 0


def cmd_prompt_evolution_autonomy(args: argparse.Namespace) -> int:
    """Run multiple sandbox rounds and grade trust on the autonomy ladder."""
    log_header("Prompt Evolution — Autonomy Ladder")
    _ensure_in_venv()
    _load_env()
    try:
        catalog, profile = _prompt_evolution_profile(args)
    except ValueError as exc:
        log_fail(str(exc))
        return 1
    sandbox_module = importlib.import_module("prompt_evolution.sandbox")
    autonomy_module = importlib.import_module("prompt_evolution.autonomy")
    rounds = int(getattr(args, "rounds", 5))
    snapshots = []
    for index in range(1, rounds + 1):
        log_info(f"sandbox round {index}/{rounds}")
        outcome = sandbox_module.run_one_round(
            catalog=catalog,
            profile=profile,
            timeout_seconds=float(getattr(args, "timeout", 30)),
            max_iterations=1,
        )
        snapshots.append(
            autonomy_module.RoundSnapshot(
                score=outcome.evaluation.total_score,
                total=outcome.evaluation.max_score,
            )
        )
    decision = autonomy_module.evaluate_ladder(snapshots)
    log_header(f"Autonomy Tier: {decision.level}")
    print(autonomy_module.render_decision(decision))
    return 0


def cmd_prompt_evolution_challenge(args: argparse.Namespace) -> int:
    """Generate adversarial scenario variants for prompt evolution."""
    log_header("Prompt Evolution — Adversarial Variants")
    _config_module, catalog = _prompt_evolution_catalog()
    challenger_module = importlib.import_module("prompt_evolution.challenger")
    levels = list(getattr(args, "levels", [1, 2, 3]) or [1, 2, 3])
    scenario_slug = getattr(args, "scenario", None)
    if scenario_slug:
        case = catalog.scenarios.get(scenario_slug)
        if case is None:
            log_fail(f"unknown scenario slug: {scenario_slug}")
            return 1
        variants = challenger_module.generate_variants(case, tiers=levels)
        print(challenger_module.render_variant_summary(variants))
        return 0
    for case in catalog.scenarios.values():
        log_info(case.label)
        variants = challenger_module.generate_variants(case, tiers=levels)
        print(challenger_module.render_variant_summary(variants))
    return 0


def cmd_skill_mastery_dashboard(_args: argparse.Namespace) -> int:
    """Launch the Skill Mastery dashboard."""
    return _run_example_dashboard(
        dashboard_path=_skill_mastery_root() / "dashboard.py",
        history_path=_output_dir("skill_mastery") / "latest_session.json",
        title="Skill Mastery — Dashboard",
        rerun_cmd="python util.py -e skill_mastery loop",
    )


# =====================================================================
# Command: challenge — generate adversarial test data
# =====================================================================


def cmd_challenge(args: argparse.Namespace) -> int:
    """Generate adversarial data at specified difficulty levels."""
    levels = getattr(args, "levels", [1, 2, 3])
    log_header(f"CleanLoop — Adversarial Data Generator (Levels: {levels})")
    _ensure_in_venv()
    _load_env()

    log_step(1, 1, "Generating adversarial CSV files")
    # Delegate to challenger module
    sys.argv = ["cleanloop.challenger", "--levels"] + [str(level) for level in levels]
    from cleanloop import challenger

    challenger.main()
    return 0


# =====================================================================
# Command: sandbox — run genome in isolated subprocess
# =====================================================================


def cmd_sandbox(args: argparse.Namespace) -> int:
    """Run genome in sandboxed subprocess."""
    config = _activate_cleanloop_dataset(args)
    timeout = getattr(args, "timeout", 30)
    log_header(f"CleanLoop — Sandbox ({config.label}, timeout={timeout}s)")
    _ensure_in_venv()

    from cleanloop.sandbox import run_sandboxed, GENOME_PATH

    cl_out = _output_dir("cleanloop")
    cl_out.mkdir(parents=True, exist_ok=True)
    output_path = cleanloop_datasets.get_output_path(cl_out)

    log_step(1, 2, "Running genome in isolated subprocess")
    log_info(f"Dataset: {config.name}")
    log_info(f"Genome: {GENOME_PATH.relative_to(ROOT)}")
    log_info(f"Timeout: {timeout}s")

    result = run_sandboxed(GENOME_PATH, INPUT_DIR, output_path, timeout)

    if result["success"]:
        log_ok("Genome completed successfully")
    elif result["timed_out"]:
        log_fail(f"Timed out after {timeout}s")
    else:
        log_fail(f"Exit code: {result['return_code']}")

    if result["stderr"]:
        log_warn(f"stderr: {result['stderr'][:200]}")

    # Evaluate if output exists
    if result["success"] and output_path.exists():
        log_step(2, 2, "Evaluating sandboxed output")
        from cleanloop import prepare

        eval_result = prepare.evaluate(output_path)
        score = eval_result["score"]
        total = eval_result["total"]
        log_info(f"Score: {score}/{total}")
    else:
        log_step(2, 2, "Skipping evaluation — no output")

    return 0


# =====================================================================
# Command: autonomy — simulate graduated trust
# =====================================================================


def cmd_autonomy(args: argparse.Namespace) -> int:
    """Run the autonomy trust ladder simulation."""
    rounds = getattr(args, "rounds", 10)
    log_header(f"CleanLoop — Autonomy Simulation ({rounds} rounds)")

    from cleanloop.autonomy import simulate

    simulate(n_rounds=rounds)
    return 0


# =====================================================================
# Command: reset — clear output and revert genome to initial state
# =====================================================================

_GENOME_MAP: dict[str, str] = {
    "cleanloop": "cleanloop/clean_data.py",
}


def _cmd_reset(example: str) -> int:
    """Reset an example by deleting output and restoring the starter genome."""
    label = example.title().replace("loop", "Loop").replace("store", "Store")
    log_header(f"{label} — Reset")

    out_dir = _output_dir(example)
    genome_rel = _GENOME_MAP[example]
    genome_path = ROOT / genome_rel

    # 1. Remove .output/ directory
    if out_dir.exists():
        shutil.rmtree(out_dir)
        log_ok(f"Deleted {out_dir.relative_to(ROOT)}")
    else:
        log_info("No .output/ directory to delete")

    # 2. Restore genome
    log_step(2, 2, "Restoring genome to last committed state")
    starter_path = ROOT / "cleanloop" / "clean_data_starter.py"
    genome_path.write_text(starter_path.read_text(encoding="utf-8"), encoding="utf-8")
    log_ok("Restored cleanloop/clean_data.py from clean_data_starter.py")

    print(f"\n  Ready to re-run: {C.BOLD}python util.py -e {example} loop{C.RESET}\n")
    return 0


def cmd_reset_cleanloop(_args: argparse.Namespace) -> int:
    """Reset CleanLoop."""
    return _cmd_reset("cleanloop")


def cmd_reset_prompt_evolution(_args: argparse.Namespace) -> int:
    """Reset Prompt Evolution outputs while preserving gold targets."""
    log_header("Prompt Evolution — Reset")
    reset_module = importlib.import_module("prompt_evolution.reset_workflow")
    out_dir = _output_dir("prompt_evolution")
    report = reset_module.reset(output_dir=out_dir)
    print(reset_module.render_report(report))
    print(
        f"\n  Ready to re-run: {C.BOLD}python util.py -e prompt_evolution loop"
        f"{C.RESET}\n"
    )
    return 0


def cmd_reset_skill_mastery(_args: argparse.Namespace) -> int:
    """Reset Skill Mastery outputs while preserving gold reference replies."""
    log_header("Skill Mastery — Reset")
    reset_module = importlib.import_module("skill_mastery.reset_workflow")
    report = reset_module.reset()
    print(reset_module.render_report(report))
    print(
        f"\n  Ready to re-run: {C.BOLD}python util.py -e skill_mastery loop"
        f"{C.RESET}\n"
    )
    return 0


def cmd_skill_mastery_status(_args: argparse.Namespace) -> int:
    """Render a Skill Mastery project status snapshot."""
    log_header("Skill Mastery — Status")
    status_module = importlib.import_module("skill_mastery.status_snapshot")
    status = status_module.collect_status()
    print(status_module.render_status(status))
    return 0


def cmd_skill_mastery_verify(_args: argparse.Namespace) -> int:
    """Run the Skill Mastery environment verification checks."""
    log_header("Skill Mastery — Verify")
    _ensure_in_venv()
    _load_env()
    verify_module = importlib.import_module("skill_mastery.verify")
    return int(verify_module.main())


def cmd_skill_mastery_evaluate(args: argparse.Namespace) -> int:
    """Score a candidate reply against a use case gold target."""
    log_header("Skill Mastery — Evaluate Candidate")
    usecase = getattr(args, "usecase", None)
    candidate_path = getattr(args, "candidate", None)
    if not usecase or not candidate_path:
        log_fail("evaluate requires --usecase and --candidate")
        return 1
    prepare_module = importlib.import_module("skill_mastery.prepare")
    _config_module, catalog = _skill_mastery_catalog()
    candidate_text = Path(candidate_path).read_text(encoding="utf-8")
    result = prepare_module.evaluate_candidate(
        catalog,
        usecase_slug=usecase,
        candidate_text=candidate_text,
    )
    print(prepare_module.render_result(result))
    return 0


def cmd_skill_mastery_sandbox(args: argparse.Namespace) -> int:
    """Run a single isolated Skill Mastery round (no mutation, no persistence)."""
    log_header("Skill Mastery — Sandbox Round")
    _ensure_in_venv()
    _load_env()
    try:
        catalog, profile = _skill_mastery_profile(args)
    except ValueError as exc:
        log_fail(str(exc))
        return 1
    sandbox_module = importlib.import_module("skill_mastery.sandbox")
    result = sandbox_module.run_one_round(
        catalog=catalog,
        profile=profile,
        timeout_seconds=float(getattr(args, "timeout", 30) or 30),
        max_iterations=1,
    )
    print(sandbox_module.render_result(result))
    return 0


def cmd_skill_mastery_autonomy(args: argparse.Namespace) -> int:
    """Run multiple sandbox rounds and grade trust on the autonomy ladder."""
    log_header("Skill Mastery — Autonomy Ladder")
    _ensure_in_venv()
    _load_env()
    try:
        catalog, profile = _skill_mastery_profile(args)
    except ValueError as exc:
        log_fail(str(exc))
        return 1
    sandbox_module = importlib.import_module("skill_mastery.sandbox")
    autonomy_module = importlib.import_module("skill_mastery.autonomy")
    rounds = int(getattr(args, "rounds", 5) or 5)
    snapshots = []
    for index in range(1, rounds + 1):
        log_info(f"sandbox round {index}/{rounds}")
        outcome = sandbox_module.run_one_round(
            catalog=catalog,
            profile=profile,
            timeout_seconds=float(getattr(args, "timeout", 30) or 30),
            max_iterations=1,
        )
        snapshots.append(
            autonomy_module.RoundSnapshot(
                score=outcome.evaluation.total_score,
                total=outcome.evaluation.max_score,
            )
        )
    decision = autonomy_module.evaluate_ladder(snapshots)
    log_header(f"Autonomy Tier: {decision.level}")
    print(autonomy_module.render_decision(decision))
    return 0


def cmd_skill_mastery_challenge(args: argparse.Namespace) -> int:
    """Generate adversarial use case variants for Skill Mastery."""
    log_header("Skill Mastery — Adversarial Variants")
    _config_module, catalog = _skill_mastery_catalog()
    challenger_module = importlib.import_module("skill_mastery.challenger")
    levels = list(getattr(args, "levels", [1, 2, 3]) or [1, 2, 3])
    usecase_slug = getattr(args, "usecase", None)
    if usecase_slug:
        case = catalog.usecases.get(usecase_slug)
        if case is None:
            log_fail(f"unknown use case slug: {usecase_slug}")
            return 1
        variants = challenger_module.generate_variants(case, tiers=levels)
        print(challenger_module.render_variant_summary(variants))
        return 0
    for case in catalog.usecases.values():
        log_info(case.label)
        variants = challenger_module.generate_variants(case, tiers=levels)
        print(challenger_module.render_variant_summary(variants))
    return 0


# =====================================================================
# Command: status — show project overview
# =====================================================================


def cmd_status(_args: argparse.Namespace) -> int:
    """Show project status and file inventory."""
    log_header("Self-Improving Agent — Project Status")

    config = cleanloop_datasets.get_dataset_config()

    # CleanLoop inputs
    print(f"\n  {C.BOLD}CleanLoop Input Files:{C.RESET}")
    if INPUT_DIR.exists():
        print(f"    {config.name:<10} {config.label}")
        for f in cleanloop_datasets.get_input_paths(INPUT_DIR):
            lines = len(f.read_text(encoding="utf-8").strip().splitlines()) - 1
            size_kb = f.stat().st_size / 1024
            print(
                f"      {C.GREEN}●{C.RESET} {f.name:<28} {lines:>4} rows  {size_kb:.1f} KB"
            )
    else:
        print(f"    {C.RED}●{C.RESET} No input/cleanloop/ directory")

    # Output
    print(f"\n  {C.BOLD}Output:{C.RESET}")
    cleanloop_out = _output_dir("cleanloop")
    master = cleanloop_datasets.get_output_path(cleanloop_out)
    if master.exists():
        lines = len(master.read_text(encoding="utf-8").strip().splitlines()) - 1
        print(f"    {C.GREEN}●{C.RESET} {master.name}  ({lines} rows)")
    else:
        print(f"    {C.DIM}●{C.RESET} No cleanloop output yet")

    history = cleanloop_datasets.get_history_path(cleanloop_out)
    if history.exists():
        data = json.loads(history.read_text(encoding="utf-8"))
        last = data[-1] if data else {}
        print(
            f"    {C.GREEN}●{C.RESET} {history.name}  "
            f"({len(data)} rounds, last score: {last.get('score', '?')}/{last.get('total', '?')})"
        )
    else:
        print(f"    {C.DIM}●{C.RESET} No cleanloop eval history")

    print(f"\n  {C.BOLD}Prompt Evolution:{C.RESET}")
    prompt_out = _output_dir("prompt_evolution")
    best_response = prompt_out / "best_response.md"
    best_instructions = prompt_out / "best_instructions.md"
    latest_session = prompt_out / "latest_session.json"
    if best_response.exists():
        print(f"    {C.GREEN}●{C.RESET} best_response.md")
    else:
        print(f"    {C.DIM}●{C.RESET} No prompt evolution response yet")
    if best_instructions.exists():
        print(f"    {C.GREEN}●{C.RESET} best_instructions.md")
    else:
        print(f"    {C.DIM}●{C.RESET} No prompt evolution instructions yet")
    if latest_session.exists():
        payload = json.loads(latest_session.read_text(encoding="utf-8"))
        print(
            f"    {C.GREEN}●{C.RESET} latest_session.json  "
            f"(best round: {payload.get('best_round', '?')})"
        )
    else:
        print(f"    {C.DIM}●{C.RESET} No prompt evolution session history")
    try:
        _, prompt_catalog = _prompt_evolution_catalog()
        print(
            f"    {C.GREEN}●{C.RESET} "
            f"{len(prompt_catalog.scenarios)} prompt evolution scenarios"
        )
    except (ImportError, OSError, ValueError, KeyError, AttributeError) as exc:
        print(f"    {C.YELLOW}●{C.RESET} Scenario catalog unavailable: {exc}")
    trace_dir = prompt_out / "traces"
    if trace_dir.exists():
        trace_files = sorted(trace_dir.glob("*.jsonl"))
        print(
            f"    {C.GREEN}●{C.RESET} traces/  "
            f"({len(trace_files)} top-level JSONL files)"
        )
    else:
        print(f"    {C.DIM}●{C.RESET} No prompt evolution traces yet")

    print(f"\n  {C.BOLD}Skill Mastery:{C.RESET}")
    mastery_out = _output_dir("skill_mastery")
    learned_habits = mastery_out / "learned_habits.json"
    selected_habits = mastery_out / "selected_habits.md"
    mastery_response = mastery_out / "best_response.md"
    mastery_session = mastery_out / "latest_session.json"
    if learned_habits.exists():
        print(f"    {C.GREEN}●{C.RESET} learned_habits.json")
    else:
        print(f"    {C.DIM}●{C.RESET} No learned Skill Mastery habits yet")
    if selected_habits.exists():
        print(f"    {C.GREEN}●{C.RESET} selected_habits.md")
    else:
        print(f"    {C.DIM}●{C.RESET} No selected Skill Mastery habits yet")
    if mastery_response.exists():
        print(f"    {C.GREEN}●{C.RESET} best_response.md")
    else:
        print(f"    {C.DIM}●{C.RESET} No Skill Mastery response yet")
    if mastery_session.exists():
        payload = json.loads(mastery_session.read_text(encoding="utf-8"))
        print(
            f"    {C.GREEN}●{C.RESET} latest_session.json  "
            f"(best round: {payload.get('best_round', '?')})"
        )
    else:
        print(f"    {C.DIM}●{C.RESET} No Skill Mastery session history")
    try:
        _, mastery_catalog = _skill_mastery_catalog()
        print(
            f"    {C.GREEN}●{C.RESET} "
            f"{len(mastery_catalog.usecases)} Skill Mastery use cases"
        )
    except (ImportError, OSError, ValueError, KeyError, AttributeError) as exc:
        print(f"    {C.YELLOW}●{C.RESET} Use case catalog unavailable: {exc}")
    mastery_trace_dir = mastery_out / "traces"
    if mastery_trace_dir.exists():
        trace_files = sorted(mastery_trace_dir.glob("*.jsonl"))
        print(
            f"    {C.GREEN}●{C.RESET} traces/  "
            f"({len(trace_files)} top-level JSONL files)"
        )
    else:
        print(f"    {C.DIM}●{C.RESET} No Skill Mastery traces yet")

    # Environment
    print(f"\n  {C.BOLD}Environment:{C.RESET}")
    print(f"    Python:    {sys.version.split()[0]}")
    print(f"    Platform:  {platform.system()} {platform.machine()}")
    print(f"    .venv:     {'exists' if VENV_DIR.exists() else 'not created'}")
    print(f"    .env:      {'exists' if ENV_FILE.exists() else 'not found'}")

    if ENV_FILE.exists():
        _load_env()
        _show_env_summary()

    # Genome status
    print(f"\n  {C.BOLD}Genomes:{C.RESET}")
    genome_clean = ROOT / "cleanloop" / "clean_data.py"
    if genome_clean.exists():
        lines = len(genome_clean.read_text().strip().splitlines())
        print(f"    {C.GREEN}●{C.RESET} cleanloop/clean_data.py  ({lines} lines)")
    prompt_readme = _prompt_evolution_root() / "README.md"
    if prompt_readme.exists():
        lines = len(prompt_readme.read_text(encoding="utf-8").strip().splitlines())
        print(f"    {C.GREEN}●{C.RESET} prompt_evolution/README.md  ({lines} lines)")
    mastery_readme = _skill_mastery_root() / "README.md"
    if mastery_readme.exists():
        lines = len(mastery_readme.read_text(encoding="utf-8").strip().splitlines())
        print(f"    {C.GREEN}●{C.RESET} skill_mastery/README.md  ({lines} lines)")
    print()
    return 0


# =====================================================================
# Utility helpers
# =====================================================================


def _load_env() -> None:
    """Load .env file if it exists."""
    if ENV_FILE.exists():
        dotenv_module = importlib.import_module("dotenv")
        load_dotenv = getattr(dotenv_module, "load_dotenv")
        load_dotenv(ENV_FILE, override=True)


def load_env() -> None:
    """Load the shared example .env file into the current process."""
    _load_env()


def _resolve_llm_env() -> dict[str, str]:
    """Resolve OpenAI-compatible endpoint settings from shared environment names."""
    endpoint = (
        os.getenv("LLM_ENDPOINT")
        or os.getenv("OPENAI_BASE_URL")
        or os.getenv("AZURE_ENDPOINT")
        or ""
    )
    api_key = (
        os.getenv("LLM_API_KEY")
        or os.getenv("OPENAI_API_KEY")
        or os.getenv("AZURE_API_KEY")
        or ""
    )
    model = os.getenv("MODEL_NAME", "gpt-4o")
    api_version = (
        os.getenv("LLM_API_VERSION")
        or os.getenv("AZURE_API_VERSION")
        or "2024-12-01-preview"
    )
    if os.getenv("LLM_ENDPOINT"):
        endpoint_var = "LLM_ENDPOINT"
    elif os.getenv("OPENAI_BASE_URL"):
        endpoint_var = "OPENAI_BASE_URL"
    else:
        endpoint_var = "AZURE_ENDPOINT"
    if os.getenv("LLM_API_KEY"):
        api_key_var = "LLM_API_KEY"
    elif os.getenv("OPENAI_API_KEY"):
        api_key_var = "OPENAI_API_KEY"
    else:
        api_key_var = "AZURE_API_KEY"
    return {
        "endpoint": endpoint,
        "api_key": api_key,
        "model": model,
        "api_version": api_version,
        "endpoint_var": endpoint_var,
        "api_key_var": api_key_var,
    }


def resolve_llm_env() -> dict[str, str]:
    """Return the shared OpenAI-compatible endpoint configuration."""
    return _resolve_llm_env()


def _show_env_summary() -> None:
    """Print a masked summary of .env config."""
    _load_env()
    config = _resolve_llm_env()
    endpoint = config["endpoint"]
    model = config["model"]
    if endpoint:
        masked = endpoint[:30] + "..." if len(endpoint) > 30 else endpoint
        log_info(f"Endpoint: {masked}")
    log_info(f"Model:    {model}")


def _count_data_rows(path: Path) -> int:
    """Count data rows in a UTF-8 CSV file, excluding the header line."""
    lines = path.read_text(encoding="utf-8").strip().splitlines()
    return max(len(lines) - 1, 0)


def _mask_secret(value: str, visible_prefix: int = 2, visible_suffix: int = 2) -> str:
    """Mask a secret while keeping a small prefix and suffix visible."""
    if len(value) <= visible_prefix + visible_suffix:
        return "*" * len(value)
    return f"{value[:visible_prefix]}****{value[-visible_suffix:]}"


def _is_azure_openai_endpoint(endpoint: str) -> bool:
    """Return whether the endpoint targets an Azure OpenAI resource."""
    return ".openai.azure.com" in endpoint.lower()


def _normalize_endpoint(endpoint: str) -> str:
    """Normalize supported endpoint shapes for OpenAI-compatible clients."""
    normalized = endpoint.rstrip("/")
    if _is_azure_openai_endpoint(normalized) and "/openai/v1" not in normalized:
        return f"{normalized}/openai/v1"
    return normalized


def _normalize_probe_reply(content: str | None) -> str:
    """Return a safe, printable reply string for the LLM health probe."""
    if content is None:
        return "(empty reply)"
    reply = content.strip()
    return reply or "(empty reply)"


def _is_capacity_error(exc: Exception) -> bool:
    """Return whether an exception represents transient endpoint saturation."""
    status_code = getattr(exc, "status_code", None)
    if status_code == 429:
        return True

    message = str(exc).lower()
    markers = (
        "maximum concurrent capacity",
        "too many pending requests",
        "try again later",
        '"code": 429',
    )
    return any(marker in message for marker in markers)


def _format_llm_exception(exc: Exception) -> str:
    """Convert raw LLM exceptions into clearer operator-facing messages."""
    if _is_capacity_error(exc):
        return (
            "Endpoint busy (429 capacity): "
            f"{exc}. The deployment is saturated, so the request was rejected "
            "before the model produced a final answer."
        )
    return f"LLM call failed: {exc}"


def _create_chat_completion_with_backoff(
    client,
    *,
    max_attempts: int = 3,
    base_delay_seconds: float = 1.0,
    retry_label: str = "LLM request",
    **kwargs,
):
    """Run a chat completion with bounded retries for transient 429 capacity errors."""
    last_exc: Exception | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            return client.chat.completions.create(**kwargs)
        except Exception as exc:  # pylint: disable=W0718  # noqa: BLE001
            last_exc = exc
            if not _is_capacity_error(exc) or attempt >= max_attempts:
                raise
            delay = base_delay_seconds * (2 ** (attempt - 1))
            log_warn(
                f"{retry_label} hit 429 capacity. Retrying in {delay:.1f}s "
                f"({attempt}/{max_attempts})"
            )
            time.sleep(delay)

    if last_exc is not None:
        raise last_exc
    raise RuntimeError("chat completion retry wrapper exited unexpectedly")


def _build_llm_client(endpoint: str, api_key: str, api_version: str):
    """Build the correct OpenAI client for the configured endpoint."""
    normalized_endpoint = _normalize_endpoint(endpoint)
    openai_module = importlib.import_module("openai")

    if (
        _is_azure_openai_endpoint(normalized_endpoint)
        and "/openai/v1" not in normalized_endpoint
    ):
        azure_openai_client = getattr(openai_module, "AzureOpenAI")

        return azure_openai_client(
            azure_endpoint=normalized_endpoint,
            api_key=api_key,
            api_version=api_version,
            max_retries=1,
        )

    openai_client = getattr(openai_module, "OpenAI")

    return openai_client(base_url=normalized_endpoint, api_key=api_key, max_retries=1)


def build_llm_client(endpoint: str, api_key: str, api_version: str):
    """Build an OpenAI-compatible client from shared endpoint settings."""
    return _build_llm_client(endpoint, api_key, api_version)


def format_llm_exception(exc: Exception) -> str:
    """Convert raw LLM exceptions into clearer operator-facing messages."""
    return _format_llm_exception(exc)


def create_chat_completion_with_backoff(
    client: Any,
    **kwargs: Any,
) -> Any:
    """Run a chat completion with bounded retries for transient capacity errors."""
    return _create_chat_completion_with_backoff(client, **kwargs)


def chat_completion_options(
    max_tokens: int,
    temperature: float | None = None,
) -> dict[str, object]:
    """Return shared completion options tuned for reasoning-heavy models."""
    return _chat_completion_options(max_tokens, temperature)


def _chat_completion_options(max_tokens: int, temperature: float | None = None) -> dict:
    """Return shared completion options tuned for reasoning-heavy models."""
    options: dict[str, object] = {
        "max_tokens": max_tokens,
        "reasoning_effort": "low",
    }
    if temperature is not None:
        options["temperature"] = temperature
    return options


def _get_python_path() -> Path:
    """Get the Python executable path inside .venv."""
    if platform.system() == "Windows":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def _get_verify_python_path() -> Path:
    """Pick the Python interpreter verify should use."""
    venv_python = _get_python_path()
    if venv_python.exists():
        return venv_python
    return Path(sys.executable)


def _venv_is_ready() -> bool:
    """Return whether the project virtual environment exists and is runnable."""
    return _get_python_path().exists() and _get_pip_path().exists()


def _should_bootstrap_to_venv(
    argv: list[str], current_python: Path | None = None
) -> bool:
    """Return whether the current command should be re-executed inside .venv."""
    if len(argv) < 2:
        return False
    if argv[1] == "setup":
        return False
    if not _venv_is_ready():
        return False
    active_python = current_python or Path(sys.executable).resolve()
    return _get_python_path().resolve() != active_python.resolve()


def _get_pip_path() -> Path:
    """Get the pip executable path inside .venv."""
    if platform.system() == "Windows":
        return VENV_DIR / "Scripts" / "pip.exe"
    return VENV_DIR / "bin" / "pip"


def _get_bin_path(name: str) -> Path:
    """Get an executable path inside .venv."""
    if platform.system() == "Windows":
        return VENV_DIR / "Scripts" / f"{name}.exe"
    return VENV_DIR / "bin" / name


def _ensure_in_venv() -> None:
    """Warn if not running inside the project's .venv."""
    # Check if the current Python is inside our .venv
    current = Path(sys.executable).resolve()
    try:
        current.relative_to(VENV_DIR.resolve())
    except ValueError:
        log_warn("Not running inside .venv")
        log_info(f"Activate first: {_activation_cmd()}")


def _activation_cmd() -> str:
    """Return the platform-appropriate activation command."""
    if platform.system() == "Windows":
        return f"{VENV_DIR}\\Scripts\\activate"
    return f"source {VENV_DIR}/bin/activate"


# =====================================================================
# CLI argument parser
# =====================================================================


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser with ``--example`` routing."""
    parser = argparse.ArgumentParser(
        prog="util.py",
        description="Self-Improving Agent — Unified Entry Point",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Shared commands (no --example needed):
  python util.py setup                          Set up environment
  python util.py verify                         Verify everything works
  python util.py status                         Show full project inventory

Per-example commands (--example / -e required):
  python util.py -e cleanloop evaluate          Run referee
  python util.py -e cleanloop loop [--rerank]   Karpathy Loop
  python util.py -e cleanloop dashboard         Streamlit dashboard
  python util.py -e cleanloop challenge         Adversarial data
  python util.py -e cleanloop sandbox           Subprocess isolation
  python util.py -e cleanloop autonomy          Trust ladder sim
  python util.py -e cleanloop reset             Clear output & restore genome
    python util.py -e prompt_evolution catalog    List contexts and preferences
    python util.py -e prompt_evolution scenarios  List scenario cases
    python util.py -e prompt_evolution loop       Mutate instructions with Hermes + guided review
    python util.py -e prompt_evolution dashboard  Inspect trace, diffs, and LLM requests
    python util.py -e prompt_evolution reset      Clear prompt evolution outputs
    python util.py -e skill_mastery catalog       List contexts and habit seeds
    python util.py -e skill_mastery usecases      List repeatable habit demos
    python util.py -e skill_mastery loop          Learn habits + guided review
    python util.py -e skill_mastery dashboard     Inspect trace, diffs, and LLM requests
    python util.py -e skill_mastery reset         Clear Skill Mastery outputs
""",
    )

    parser.add_argument(
        "--example",
        "-e",
        choices=["cleanloop", "prompt_evolution", "skill_mastery"],
        help="Example project to operate on",
    )

    sub = parser.add_subparsers(dest="command", help="Available commands")

    # --- Shared commands (no --example needed) ---
    sub.add_parser("setup", help="Create .venv and install dependencies")
    sub.add_parser("verify", help="Check environment, credentials, LLM")
    sub.add_parser("status", help="Show project status and file inventory")

    # --- Unified per-example commands ---
    sub.add_parser("catalog", help="List example contexts, preferences, or habit seeds")
    p_evaluate = sub.add_parser("evaluate", help="Run the referee/evaluator")
    p_evaluate.add_argument(
        "--scenario",
        help="Prompt Evolution scenario slug to evaluate against",
    )
    p_evaluate.add_argument(
        "--usecase",
        help="Skill Mastery use case slug to evaluate against",
    )
    p_evaluate.add_argument(
        "--candidate",
        help="Path to a candidate reply file (markdown or text)",
    )

    p_loop = sub.add_parser("loop", help="Run the self-improving loop")
    p_loop.add_argument("--max-iterations", type=int, default=5)
    p_loop.add_argument("--rerank", action="store_true", help="Use Best-of-N")
    p_loop.add_argument("--candidates", type=int, default=3)
    p_loop.add_argument(
        "--named-instance",
        default=None,
        help="Optional CleanLoop run-instance name for saved logs, traces, and diagnostics",
    )
    p_loop.add_argument("--context", help="Example context slug")
    p_loop.add_argument("--scenario", help="Prompt Evolution scenario slug")
    p_loop.add_argument("--usecase", help="Skill Mastery use case slug")
    p_loop.add_argument(
        "--preference",
        action="append",
        default=[],
        help="Preference in axis=value form; repeat for multiple choices",
    )
    p_loop.add_argument(
        "--problem", help="Problem statement for prompt or habit composition"
    )

    sub.add_parser("dashboard", help="Launch Streamlit monitoring")
    sub.add_parser("scenarios", help="List Prompt Evolution scenario cases")
    sub.add_parser("usecases", help="List Skill Mastery use cases")

    p_challenge = sub.add_parser(
        "challenge",
        help="Generate adversarial data",
    )
    p_challenge.add_argument(
        "--levels",
        type=int,
        nargs="+",
        default=[1, 2, 3],
        help="Difficulty levels for CleanLoop challenger runs",
    )
    p_challenge.add_argument(
        "--usecase",
        help="Skill Mastery use case slug (limits variants to one use case)",
    )
    p_challenge.add_argument(
        "--scenario",
        help="Prompt Evolution scenario slug (limits variants to one scenario)",
    )

    p_sandbox = sub.add_parser(
        "sandbox",
        help="Run genome in isolated subprocess",
    )
    p_sandbox.add_argument("--timeout", type=int, default=30)
    p_sandbox.add_argument(
        "--scenario",
        help="Prompt Evolution scenario slug for sandbox round",
    )
    p_sandbox.add_argument(
        "--usecase",
        help="Skill Mastery use case slug for sandbox round",
    )
    p_sandbox.add_argument(
        "--context",
        help="Prompt Evolution context slug",
    )
    p_sandbox.add_argument(
        "--problem",
        help="Override customer problem text",
    )
    p_sandbox.add_argument(
        "--preference",
        action="append",
        default=[],
        help="Preference axis=value (repeat for multiple)",
    )

    p_autonomy = sub.add_parser(
        "autonomy",
        help="Simulate graduated trust ladder",
    )
    p_autonomy.add_argument("--rounds", type=int, default=10)
    p_autonomy.add_argument("--timeout", type=int, default=30)
    p_autonomy.add_argument(
        "--scenario",
        help="Prompt Evolution scenario slug for autonomy rounds",
    )
    p_autonomy.add_argument(
        "--usecase",
        help="Skill Mastery use case slug for autonomy rounds",
    )
    p_autonomy.add_argument(
        "--context",
        help="Prompt Evolution context slug",
    )
    p_autonomy.add_argument(
        "--problem",
        help="Override customer problem text",
    )
    p_autonomy.add_argument(
        "--preference",
        action="append",
        default=[],
        help="Preference axis=value (repeat for multiple)",
    )

    sub.add_parser("reset", help="Clear .output/ and restore genome")

    return parser


# =====================================================================
# Main
# =====================================================================

SHARED_COMMANDS: dict[str, CommandHandler] = {
    "setup": cmd_setup,
    "verify": cmd_verify,
    "status": cmd_status,
}

EXAMPLE_COMMANDS: dict[str, dict[str, CommandHandler]] = {
    "cleanloop": {
        "evaluate": cmd_evaluate,
        "loop": cmd_loop,
        "dashboard": cmd_dashboard,
        "challenge": cmd_challenge,
        "sandbox": cmd_sandbox,
        "autonomy": cmd_autonomy,
        "reset": cmd_reset_cleanloop,
    },
    "prompt_evolution": {
        "catalog": cmd_prompt_evolution_catalog,
        "scenarios": cmd_prompt_evolution_scenarios,
        "loop": cmd_prompt_evolution_loop,
        "dashboard": cmd_prompt_evolution_dashboard,
        "status": cmd_prompt_evolution_status,
        "verify": cmd_prompt_evolution_verify,
        "evaluate": cmd_prompt_evolution_evaluate,
        "sandbox": cmd_prompt_evolution_sandbox,
        "autonomy": cmd_prompt_evolution_autonomy,
        "challenge": cmd_prompt_evolution_challenge,
        "reset": cmd_reset_prompt_evolution,
    },
    "skill_mastery": {
        "catalog": cmd_skill_mastery_catalog,
        "usecases": cmd_skill_mastery_usecases,
        "loop": cmd_skill_mastery_loop,
        "dashboard": cmd_skill_mastery_dashboard,
        "evaluate": cmd_skill_mastery_evaluate,
        "sandbox": cmd_skill_mastery_sandbox,
        "autonomy": cmd_skill_mastery_autonomy,
        "challenge": cmd_skill_mastery_challenge,
        "verify": cmd_skill_mastery_verify,
        "status": cmd_skill_mastery_status,
        "reset": cmd_reset_skill_mastery,
    },
}


def main() -> None:
    """Parse arguments and dispatch to the right command."""
    if _should_bootstrap_to_venv(sys.argv):
        target_python = _get_python_path().resolve()
        log_info(f"Using project .venv interpreter: {target_python}")
        result = subprocess.run(
            [str(target_python), str(ROOT / "util.py"), *sys.argv[1:]],
            cwd=str(ROOT),
            check=False,
        )
        sys.exit(result.returncode)

    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        print(f"\n  {C.CYAN}Quick start:{C.RESET}")
        print("    python util.py setup")
        print("    python util.py verify")
        print("    python util.py -e cleanloop loop\n")
        sys.exit(0)

    # Per-example commands (preferred when --example is supplied and command is registered)
    example = getattr(args, "example", None)
    if example and args.command in EXAMPLE_COMMANDS.get(example, {}):
        sys.exit(EXAMPLE_COMMANDS[example][args.command](args))

    # Shared commands (no --example needed)
    if args.command in SHARED_COMMANDS:
        shared_handler = SHARED_COMMANDS[args.command]
        sys.exit(shared_handler(args))

    # Per-example commands
    if not example:
        print(
            f"\n  {C.RED}ERROR:{C.RESET} " f"'{args.command}' requires --example / -e\n"
        )
        print(f"  Example: python util.py -e cleanloop {args.command}")
        sys.exit(1)

    example_cmds = EXAMPLE_COMMANDS.get(example, {})
    example_handler = example_cmds.get(args.command)
    if example_handler is not None:
        sys.exit(example_handler(args))
    else:
        print(
            f"\n  {C.RED}ERROR:{C.RESET} "
            f"'{args.command}' is not available for --example {example}\n"
        )
        available = ", ".join(sorted(example_cmds.keys()))
        print(f"  Available commands: {available}")
        sys.exit(1)


if __name__ == "__main__":
    main()
