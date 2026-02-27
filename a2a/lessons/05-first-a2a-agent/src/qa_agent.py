"""QA Agent — Standalone agent powered by GitHub Phi-4.

This module defines the QAAgent class that answers questions about
domain-specific documents using GitHub Models' OpenAI-compatible API.

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
    """Question-answering agent backed by GitHub Phi-4.

    Args:
        knowledge_path: Path to the domain knowledge document.
        model: Model name on GitHub Models (default: Phi-4).
        temperature: Sampling temperature (lower = more deterministic).
    """

    def __init__(
        self,
        knowledge_path: str,
        model: str = "Phi-4",
        temperature: float = 0.2,
    ):
        self.client = AsyncOpenAI(
            base_url="https://models.inference.ai.azure.com",
            api_key=os.environ["GITHUB_TOKEN"],
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
        )
        return response.choices[0].message.content


# ---------------------------------------------------------------------------
# Standalone test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import asyncio

    async def main():
        agent = QAAgent("data/insurance_policy.txt")

        questions = [
            "What is the deductible for the Standard plan?",
            "How much is the monthly premium?",
            "Are cosmetic procedures covered?",
        ]

        for q in questions:
            print(f"\n❓ {q}")
            answer = await agent.query(q)
            print(f"💬 {answer}")

    asyncio.run(main())
