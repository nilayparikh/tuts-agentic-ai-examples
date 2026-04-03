"""Regression tests for the coordinator routing example."""

import unittest
from unittest.mock import patch

import coordinator_server


class _FakeResponse:
    """Provide a minimal OpenAI-compatible response payload."""

    def __init__(self, content: str) -> None:
        """Store the mock message content."""
        message = type("Message", (), {"content": content})()
        choice = type("Choice", (), {"message": message})()
        self.choices = [choice]


class _FakeCompletions:
    """Track calls to the fake completions API."""

    def __init__(self, content: str) -> None:
        """Initialize the fake completion response."""
        self._content = content
        self.calls = 0

    def create(self, **_: object) -> _FakeResponse:
        """Return the configured fake response and track the call."""
        self.calls += 1
        return _FakeResponse(self._content)


class _FakeOpenAI:
    """Expose the same nested chat.completions surface as OpenAI."""

    def __init__(self, content: str) -> None:
        """Build the fake chat client structure."""
        self.completions = _FakeCompletions(content)
        self.chat = type("Chat", (), {"completions": self.completions})()


class CoordinatorRouterTests(unittest.TestCase):
    """Validate coordinator classification behavior."""

    def test_llm_classification_precedes_keyword_rules(self) -> None:
        """Use the LLM result before falling back to keyword rules."""
        fake_client = _FakeOpenAI("FoodAgent")

        with patch.object(coordinator_server, "OpenAI", return_value=fake_client):
            router = coordinator_server.CoordinatorRouter()

        chosen = router._classify_query(
            "How do I get around Tokyo using public transit?"
        )

        self.assertEqual(chosen, "FoodAgent")
        self.assertEqual(fake_client.completions.calls, 1)

    def test_keyword_rules_recover_when_llm_returns_empty(self) -> None:
        """Use keyword rules when the LLM response is blank."""
        fake_client = _FakeOpenAI("   ")

        with patch.object(coordinator_server, "OpenAI", return_value=fake_client):
            router = coordinator_server.CoordinatorRouter()

        chosen = router._classify_query(
            "How do I get around Tokyo using public transit?"
        )

        self.assertEqual(chosen, "TransportAgent")
        self.assertEqual(fake_client.completions.calls, 1)


if __name__ == "__main__":
    unittest.main()