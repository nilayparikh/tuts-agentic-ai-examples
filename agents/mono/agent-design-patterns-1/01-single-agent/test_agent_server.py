"""Regression tests for the single-agent example."""

import unittest
from unittest.mock import patch

import agent_server


class _FakeResponse:
    """Provide the smallest OpenAI-compatible response object for tests."""

    def __init__(self, content: str, finish_reason: str = "stop") -> None:
        """Build a completion response with configurable content."""
        message = type("Message", (), {"content": content, "tool_calls": None})()
        choice = type("Choice", (), {"message": message, "finish_reason": finish_reason})()
        self.choices = [choice]


class _FakeCompletions:
    """Return a preconfigured completion response."""

    def __init__(self, content: str, finish_reason: str = "stop") -> None:
        """Store the response payload to emit."""
        self._content = content
        self._finish_reason = finish_reason

    def create(self, **_: object) -> _FakeResponse:
        """Return the configured fake response."""
        return _FakeResponse(self._content, self._finish_reason)


class _FakeOpenAI:
    """Expose the nested chat.completions surface expected by the agent."""

    def __init__(self, content: str, finish_reason: str = "stop") -> None:
        """Build a deterministic fake chat client."""
        completions = _FakeCompletions(content, finish_reason)
        self.chat = type("Chat", (), {"completions": completions})()


class TripPlannerAgentTests(unittest.TestCase):
    """Validate single-agent fallback behavior."""

    def test_process_replaces_raw_tool_text_with_grounded_fallback_plan(self) -> None:
        """Execute fallback tools when the model emits tool syntax as plain text."""
        fake_client = _FakeOpenAI(
            "search_attractions{city:<|\"|>San Francisco<|\"|>}\n"
            "search_restaurants{city:<|\"|>San Francisco<|\"|>}\n"
            "get_weather{city:<|\"|>San Francisco<|\"|>}"
        )

        with patch.object(agent_server, "OpenAI", return_value=fake_client):
            planner = agent_server.TripPlannerAgent()

        result = planner.process(
            "Plan a weekend trip to San Francisco. Include attractions, restaurants, and weather."
        )

        self.assertNotIn("search_attractions", result)
        self.assertIn("Golden Gate Bridge", result)
        self.assertIn("Tartine Bakery", result)
        self.assertIn("62F", result)


if __name__ == "__main__":
    unittest.main()