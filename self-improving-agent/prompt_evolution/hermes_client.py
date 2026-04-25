"""Hermes Agent adapter for prompt evolution loops."""

from __future__ import annotations

import importlib
import io
import os
from contextlib import redirect_stderr, redirect_stdout
from dataclasses import dataclass
from typing import Any

import util


def _is_azure_openai_endpoint(endpoint: str) -> bool:
    """Return whether the endpoint targets an Azure OpenAI resource."""
    return ".openai.azure.com" in endpoint.lower()


def _normalize_endpoint(endpoint: str | None) -> str | None:
    """Normalize OpenAI-compatible endpoints for Hermes."""
    if not endpoint:
        return None
    normalized = endpoint.rstrip("/")
    if _is_azure_openai_endpoint(normalized) and "/openai/v1" not in normalized:
        return f"{normalized}/openai/v1"
    return normalized


def _infer_provider(base_url: str | None) -> str | None:
    """Infer the Hermes provider name from the configured base URL."""
    if not base_url:
        return None
    lowered = base_url.lower()
    if "openrouter.ai" in lowered:
        return "openrouter"
    return "custom"


@dataclass(frozen=True)
class HermesResponse:
    """Small wrapper around Hermes' run_conversation result payload."""

    text: str
    messages: list[dict[str, Any]]
    task_id: str | None
    raw_output: str = ""


class HermesAgentRunner:
    """Create one quiet, locked-down Hermes agent per prompt-evolution task."""

    def __init__(
        self,
        *,
        model: str,
        base_url: str | None,
        api_key: str | None,
        max_iterations: int = 8,
    ) -> None:
        self.model = model
        self.base_url = base_url
        self.api_key = api_key
        self.max_iterations = max_iterations
        self.provider = _infer_provider(base_url)

    @classmethod
    def from_env(cls) -> "HermesAgentRunner":
        """Build a runner from the shared example environment variables."""
        config = util.resolve_llm_env()
        return cls(
            model=config["model"],
            base_url=_normalize_endpoint(config["endpoint"]),
            api_key=config["api_key"],
        )

    def _build_agent(self):
        """Construct a fresh Hermes AIAgent instance for one conversation."""
        if self.base_url and not os.getenv("OPENAI_BASE_URL"):
            os.environ["OPENAI_BASE_URL"] = self.base_url
        if self.api_key and not os.getenv("OPENAI_API_KEY"):
            os.environ["OPENAI_API_KEY"] = self.api_key

        try:
            module = importlib.import_module("run_agent")
        except ImportError as exc:
            raise RuntimeError(
                "Hermes Agent is not installed. Run `python util.py setup` first."
            ) from exc

        agent_class = getattr(module, "AIAgent")
        return agent_class(
            model=self.model,
            base_url=self.base_url,
            api_key=self.api_key,
            provider=self.provider,
            quiet_mode=True,
            max_iterations=self.max_iterations,
            skip_context_files=True,
            skip_memory=True,
            disabled_toolsets=["*"],
        )

    def run_text(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        task_id: str | None = None,
    ) -> HermesResponse:
        """Run one Hermes conversation and return only the text we need."""
        agent = self._build_agent()
        stdout_buffer = io.StringIO()
        stderr_buffer = io.StringIO()
        with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
            result = agent.run_conversation(
                user_message=user_prompt,
                system_message=system_prompt,
                task_id=task_id,
            )
        text = str(result.get("final_response", "")).strip()
        if not text:
            raise RuntimeError("Hermes returned an empty response.")
        messages = result.get("messages", [])
        if not isinstance(messages, list):
            messages = []
        raw_output = "\n".join(
            chunk.strip()
            for chunk in (stdout_buffer.getvalue(), stderr_buffer.getvalue())
            if chunk.strip()
        )
        return HermesResponse(
            text=text,
            messages=messages,
            task_id=task_id,
            raw_output=raw_output,
        )
