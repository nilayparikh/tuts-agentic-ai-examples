"""Example-local environment and AutoGen client helpers for CleanLoop."""

from __future__ import annotations

import importlib
import os
from pathlib import Path
from typing import Any

ENV_FILE = Path(__file__).resolve().parent / ".env"
FALLBACK_ENV_FILE = Path(__file__).resolve().parent.parent / ".env"
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
    if os.getenv("LLM_ENDPOINT"):
        endpoint_var = "LLM_ENDPOINT"
    elif os.getenv("AZURE_OPENAI_ENDPOINT"):
        endpoint_var = "AZURE_OPENAI_ENDPOINT"
    elif os.getenv("OPENAI_BASE_URL"):
        endpoint_var = "OPENAI_BASE_URL"
    else:
        endpoint_var = "AZURE_ENDPOINT"

    if os.getenv("LLM_API_KEY"):
        api_key_var = "LLM_API_KEY"
    elif os.getenv("AZURE_OPENAI_API_KEY"):
        api_key_var = "AZURE_OPENAI_API_KEY"
    elif os.getenv("OPENAI_API_KEY"):
        api_key_var = "OPENAI_API_KEY"
    elif os.getenv("GITHUB_TOKEN"):
        api_key_var = "GITHUB_TOKEN"
    else:
        api_key_var = "AZURE_API_KEY"

    endpoint = (
        os.getenv("LLM_ENDPOINT")
        or os.getenv("AZURE_OPENAI_ENDPOINT")
        or os.getenv("OPENAI_BASE_URL")
        or os.getenv("AZURE_ENDPOINT")
        or ""
    )
    api_key = (
        os.getenv("LLM_API_KEY")
        or os.getenv("AZURE_OPENAI_API_KEY")
        or os.getenv("OPENAI_API_KEY")
        or os.getenv("AZURE_API_KEY")
        or os.getenv("GITHUB_TOKEN")
        or ""
    )
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
        if _is_github_models_endpoint(endpoint):
            client_kwargs["model_info"] = _default_model_info()
        elif not endpoint.rstrip("/").endswith("/v1"):
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
    if _is_capacity_error(exc):
        return (
            "Endpoint busy (429 capacity): "
            f"{exc}. The provider rejected the request before the model completed."
        )
    return f"LLM call failed: {exc}"


def format_llm_exception(exc: Exception) -> str:
    """Convert provider errors into clearer learner-facing messages."""
    return _format_llm_exception(exc)


def create_text_completion(
    client: Any,
    *,
    system_prompt: str | None,
    user_prompt: str,
    max_tokens: int,
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

    create_args: dict[str, object] = {"max_tokens": max_tokens}
    if temperature is not None:
        create_args["temperature"] = temperature

    response = _run_coro(
        client.create(messages=messages, extra_create_args=create_args)
    )
    content = getattr(response, "content", "")
    if isinstance(content, str):
        return content.strip()
    raise RuntimeError(f"Expected a text response, received {type(content).__name__}.")


def _run_coro(coro: Any) -> Any:
    """Run a coroutine from the synchronous lesson modules."""
    import asyncio

    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)
    raise RuntimeError(
        "CleanLoop sync helpers cannot run inside an existing event loop."
    )
