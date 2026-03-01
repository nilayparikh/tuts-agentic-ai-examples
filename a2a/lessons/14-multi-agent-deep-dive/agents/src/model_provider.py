"""
Model Provider — Unified LLM client for GitHub Models, Azure (MicrosoftFoundry),
and Foundry Local (LocalFoundry).

Select the provider via the ``PROVIDER`` environment variable:
  - ``github``            → GitHub Models (Phi-4) — DEFAULT
  - ``MicrosoftFoundry``  → Azure AI Foundry (Kimi-K2-Thinking)
  - ``LocalFoundry``      → Foundry Local / Ollama (Qwen2.5, etc.)

All providers return an ``openai.AsyncOpenAI`` client and a model name,
so agent code is provider-agnostic.

Environment variables
---------------------
  PROVIDER                          github | MicrosoftFoundry | LocalFoundry
  GITHUB_TOKEN                      PAT for GitHub Models
  AZURE_OPENAI_ENDPOINT             Azure OpenAI resource endpoint
  AZURE_AI_API_KEY                  Azure OpenAI API key
  AZURE_AI_MODEL_DEPLOYMENT_NAME    Azure deployment name (default: Kimi-K2-Thinking)
  LOCALFOUNDRY_ENDPOINT             Local HTTP endpoint (default: http://localhost:5272/v1/)
  LOCALFOUNDRY_MODEL                Local model name (default: qwen2.5-0.5b-instruct-generic-gpu:4)
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass

from openai import AsyncOpenAI

logger = logging.getLogger("model_provider")


@dataclass(frozen=True)
class ModelConfig:
    """Resolved model configuration."""

    provider: str
    client: AsyncOpenAI
    model: str
    display_name: str


def get_model_config(override_provider: str | None = None) -> ModelConfig:
    """Build an AsyncOpenAI client for the configured provider.

    Parameters
    ----------
    override_provider
        If set, overrides the ``PROVIDER`` env var. Useful for testing.

    Returns
    -------
    ModelConfig
        A frozen dataclass with ``client``, ``model`` name, and metadata.
    """
    provider = (override_provider or os.getenv("PROVIDER", "github")).strip().lower()

    if provider in ("github", "gh"):
        return _github_config()
    if provider in ("microsoftfoundry", "azure", "microsoft"):
        return _azure_config()
    if provider in ("localfoundry", "local", "ollama"):
        return _local_config()

    logger.warning(
        "Unknown PROVIDER=%r — falling back to 'github'. "
        "Valid values: github, MicrosoftFoundry, LocalFoundry",
        provider,
    )
    return _github_config()


# ── Provider implementations ─────────────────────────────────────────────────


def _github_config() -> ModelConfig:
    """GitHub Models — gpt-4o-mini via OpenAI-compatible API."""
    token = os.getenv("GITHUB_TOKEN", "")
    if not token:
        logger.error("GITHUB_TOKEN is not set — GitHub Models provider will fail")

    model = os.getenv("GITHUB_MODEL", "openai/gpt-4o-mini")

    client = AsyncOpenAI(
        base_url="https://models.github.ai/inference",
        api_key=token,
    )
    logger.info(
        "Model provider: GitHub Models | model=%s | endpoint=models.github.ai",
        model,
    )
    return ModelConfig(
        provider="github",
        client=client,
        model=model,
        display_name=f"GitHub Models ({model})",
    )


def _azure_config() -> ModelConfig:
    """Azure AI Foundry — Kimi-K2-Thinking (or configured deployment)."""
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    api_key = os.getenv("AZURE_AI_API_KEY", "")
    model = os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME", "Kimi-K2-Thinking")

    if not endpoint or not api_key:
        logger.error(
            "AZURE_OPENAI_ENDPOINT and/or AZURE_AI_API_KEY not set — "
            "MicrosoftFoundry provider will fail"
        )

    client = AsyncOpenAI(
        base_url=f"{endpoint}/openai/deployments/{model}",
        api_key=api_key,
        default_headers={"api-key": api_key},
    )
    logger.info(
        "Model provider: MicrosoftFoundry | model=%s | endpoint=%s",
        model,
        endpoint,
    )
    return ModelConfig(
        provider="MicrosoftFoundry",
        client=client,
        model=model,
        display_name=f"Azure AI Foundry ({model})",
    )


def _local_config() -> ModelConfig:
    """Foundry Local / Ollama — local HTTP endpoint."""
    endpoint = os.getenv("LOCALFOUNDRY_ENDPOINT", "http://localhost:5272/v1/")
    model = os.getenv("LOCALFOUNDRY_MODEL", "qwen2.5-0.5b-instruct-generic-gpu:4")

    client = AsyncOpenAI(
        base_url=endpoint,
        api_key="not-needed",
    )
    logger.info(
        "Model provider: LocalFoundry | model=%s | endpoint=%s",
        model,
        endpoint,
    )
    return ModelConfig(
        provider="LocalFoundry",
        client=client,
        model=model,
        display_name=f"Foundry Local ({model})",
    )
