"""Regression tests for the loop-and-critique example."""

import unittest
from unittest.mock import patch

import critic_server
import generator_server
import loop_server


class _FakeResponse:
    """Provide the smallest response object needed by generator tests."""

    def __init__(self, content: str) -> None:
        """Build a message with the given content."""
        message = type("Message", (), {"content": content})()
        choice = type("Choice", (), {"message": message})()
        self.choices = [choice]


class _FakeCompletions:
    """Return a preconfigured completion payload."""

    def __init__(self, content: str) -> None:
        """Store the content to return from create."""
        self._content = content

    def create(self, **_: object) -> _FakeResponse:
        """Return the configured fake response."""
        return _FakeResponse(self._content)


class _FakeOpenAI:
    """Expose the nested chat.completions shape used by the generator."""

    def __init__(self, content: str) -> None:
        """Build a fake chat client for deterministic unit tests."""
        completions = _FakeCompletions(content)
        self.chat = type("Chat", (), {"completions": completions})()


class GeneratorAgentTests(unittest.TestCase):
    """Validate model output normalization for the generator."""

    def test_process_strips_think_tags_from_model_output(self) -> None:
        """Return only the visible plan text when Ollama includes reasoning tags."""
        fake_client = _FakeOpenAI("<think>hidden</think>Visible plan")

        with patch.object(generator_server, "OpenAI", return_value=fake_client):
            agent = generator_server.GeneratorAgent()

        result = agent.process("Plan a weekend trip")

        self.assertEqual(result, "Visible plan")


class CriticAgentTests(unittest.TestCase):
    """Validate the critic's deterministic quality gate."""

    def test_process_returns_pass_for_complete_plan(self) -> None:
        """Approve plans that include all required trip elements."""
        agent = critic_server.CriticAgent()

        result = agent.process(
            "Hotel: Fairmont. Attractions: bridge and park. Dining: dinner at a restaurant. "
            "Transport: use train and walk."
        )

        self.assertEqual(result, "PASS")

    def test_process_returns_targeted_feedback_for_missing_sections(self) -> None:
        """List the missing trip-plan requirements when the draft is incomplete."""
        agent = critic_server.CriticAgent()

        result = agent.process("Visit one museum and then relax.")

        self.assertIn("hotel or accommodation", result.lower())
        self.assertIn("at least two attractions", result.lower())
        self.assertIn("dining", result.lower())
        self.assertIn("transport", result.lower())


class LoopOrchestratorTests(unittest.IsolatedAsyncioTestCase):
    """Validate loop control for approve and retry paths."""

    async def test_process_stops_when_critic_passes(self) -> None:
        """Return the approved plan immediately once the critic says PASS."""
        orchestrator = loop_server.LoopOrchestrator()

        with patch.object(
            loop_server,
            "call_agent",
            side_effect=["Draft plan", "PASS"],
        ) as mock_call_agent:
            result = await orchestrator.process("Plan a weekend trip")

        self.assertIn("approved on iteration 1", result)
        self.assertIn("Draft plan", result)
        self.assertEqual(mock_call_agent.await_count, 2)

    async def test_process_returns_last_plan_after_max_iterations(self) -> None:
        """Surface the last plan and feedback after the retry budget is exhausted."""
        orchestrator = loop_server.LoopOrchestrator()

        with patch.object(
            loop_server,
            "call_agent",
            side_effect=[
                "Plan 1", "Need hotel",
                "Plan 2", "Need dining",
                "Plan 3", "Need transport",
            ],
        ) as mock_call_agent:
            result = await orchestrator.process("Plan a weekend trip")

        self.assertIn("max 3 iterations reached", result)
        self.assertIn("Last plan:\nPlan 3", result)
        self.assertIn("Last feedback:\nNeed transport", result)
        self.assertEqual(mock_call_agent.await_count, 6)


if __name__ == "__main__":
    unittest.main()