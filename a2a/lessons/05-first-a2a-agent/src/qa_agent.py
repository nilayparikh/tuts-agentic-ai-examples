"""QA Agent — Standalone question-answering agent.

Supports two model providers selected via the PROVIDER env var:

  PROVIDER=github       — GitHub Models (free, needs GITHUB_TOKEN in .env)
                          https://github.com/settings/tokens
  PROVIDER=localfoundry — AI Toolkit LocalFoundry (local, no token needed)
                          VS Code AI Toolkit → Models → Load a model → Run

If PROVIDER is not set, defaults to "github".

Usage:
    from qa_agent import QAAgent

    agent = QAAgent("data/insurance_policy.txt")
    answer = await agent.query("What is the deductible?")
"""

import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from openai import AsyncOpenAI

# Load .env from nearest parent directory (searches up to _examples/.env)
load_dotenv(find_dotenv(raise_error_if_not_found=False))

# ---------------------------------------------------------------------------
# Provider configuration
# ---------------------------------------------------------------------------
# Set PROVIDER=localfoundry in your environment (or .env) to use a local model.
# Default is "github".

PROVIDER = os.environ.get("PROVIDER", "github").lower()

if PROVIDER == "github":
    _ENDPOINT = "https://models.inference.ai.azure.com"
    _API_KEY = os.environ.get("GITHUB_TOKEN", "")
    _MODEL = "Phi-4"
elif PROVIDER == "localfoundry":
    _ENDPOINT = os.environ.get("LOCALFOUNDRY_ENDPOINT", "http://localhost:5272/v1/")
    _API_KEY = "unused"  # LocalFoundry ignores the key
    _MODEL = os.environ.get("LOCALFOUNDRY_MODEL", "qwen2.5-0.5b-instruct-generic-gpu:4")
else:
    raise ValueError(
        f"Unknown PROVIDER: {PROVIDER!r}. "
        "Set PROVIDER to 'github' or 'localfoundry'."
    )

# ---------------------------------------------------------------------------
# System prompt template — injects domain knowledge at runtime
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """\
You are a helpful insurance policy assistant.
Use the following policy document to answer questions accurately.
If the answer is not in the document, say so clearly.
Always cite the relevant section when possible.

--- POLICY DOCUMENT ---
{policy_text}
--- END DOCUMENT ---
"""


def load_knowledge(path: str) -> str:
    """Load a knowledge document from disk."""
    return Path(path).read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# QAAgent — async class pattern for A2A compatibility
# ---------------------------------------------------------------------------


class QAAgent:
    """Question-answering agent using an OpenAI-compatible backend.

    Reads provider settings from module-level constants (PROVIDER, _ENDPOINT,
    _API_KEY, _MODEL) which are resolved from environment variables on import.
    Override endpoint/api_key/model to use a different provider at call-site.

    Args:
        knowledge_path: Path to the domain knowledge document.
        model: Model identifier (defaults to provider default from env).
        endpoint: API base URL (defaults to provider endpoint from env).
        api_key: API key or token (defaults to provider key from env).
        temperature: Sampling temperature (lower = more deterministic).
    """

    def __init__(
        self,
        knowledge_path: str,
        model: str = _MODEL,
        endpoint: str = _ENDPOINT,
        api_key: str = _API_KEY,
        temperature: float = 0.2,
    ):
        self.client = AsyncOpenAI(
            base_url=endpoint,
            api_key=api_key,
        )
        self.model = model
        self.temperature = temperature
        self.knowledge = load_knowledge(knowledge_path)
        self.system_prompt = SYSTEM_PROMPT.format(policy_text=self.knowledge)

    async def query(self, question: str) -> str:
        """Send a question to the model and return the answer.

        Args:
            question: The user's question about the knowledge domain.

        Returns:
            The model's answer as a string.
        """
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": question},
            ],
            temperature=self.temperature,
            max_tokens=2048,  # required by GitHub Models free-tier (4 000 out limit)
        )
        return response.choices[0].message.content


# ---------------------------------------------------------------------------
# Standalone test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import asyncio
    import sys

    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows safe

    print(f"Provider : {PROVIDER}")
    print(f"Endpoint : {_ENDPOINT}")
    print(f"Model    : {_MODEL}")
    print()

    async def main():
        """Run a quick smoke-test against the insurance policy document."""
        agent = QAAgent("data/insurance_policy.txt")

        questions = [
            "What is the deductible for the Standard plan?",
            "How much is the monthly premium?",
            "Are cosmetic procedures covered?",
        ]

        for q in questions:
            print(f"Q: {q}")
            answer = await agent.query(q)
            print(f"A: {answer}")
            print()

    asyncio.run(main())
