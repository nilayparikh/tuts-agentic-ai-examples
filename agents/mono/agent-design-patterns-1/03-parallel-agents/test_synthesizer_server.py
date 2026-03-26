"""Regression tests for the parallel synthesizer Ollama integration."""

import unittest

from synthesizer_server import SynthesizerAgent


class _FakeResponse:
    """Provide a minimal OpenAI-compatible response object."""

    def __init__(self, content: str) -> None:
        """Store the content returned by the fake model."""
        self.choices = [
            type(
                "Choice",
                (),
                {"message": type("Message", (), {"content": content})()},
            )()
        ]


class _FakeCompletions:
    """Expose the subset of the completions API used by the synthesizer."""

    def __init__(self, behavior) -> None:
        """Store the callable that simulates the model response."""
        self._behavior = behavior

    def create(self, **kwargs):
        """Return the fake response or raise an injected exception."""
        return self._behavior(**kwargs)


class _FakeChat:
    """Expose a fake chat endpoint."""

    def __init__(self, behavior) -> None:
        """Initialize the fake completions client."""
        self.completions = _FakeCompletions(behavior)


class _FakeClient:
    """Expose the subset of the OpenAI client used by the agent."""

    def __init__(self, behavior) -> None:
        """Initialize the fake chat client."""
        self.chat = _FakeChat(behavior)


class SynthesizerAgentTests(unittest.TestCase):
    """Cover the Ollama-backed synthesis behavior."""

    def test_process_uses_ollama_response_when_available(self) -> None:
        """Return the cleaned model output when Ollama responds successfully."""
        payload = (
            '{"original_query": "Plan a day in Tokyo", "results": {'
            '"MuseumFinder": {"items": [{"name": "Tokyo National Museum", '
            '"type": "Japanese art", "area": "Ueno"}], '
            '"note": "Start with culture."}, '
            '"RestaurantFinder": {"items": [{"name": "Ichiran Ramen", '
            '"cuisine": "Ramen", "area": "Shibuya"}], '
            '"note": "Lunch near Shibuya."}, '
            '"ConcertFinder": {"items": [{"name": "Blue Note Tokyo", '
            '"genre": "Jazz", "venue": "Blue Note Tokyo"}], '
            '"note": "Evening music."}}}'
        )
        fake_client = _FakeClient(
            lambda **kwargs: _FakeResponse(
                "<think>internal</think>Morning: Tokyo National Museum. "
                "Lunch: Ichiran Ramen. Evening: Blue Note Tokyo."
            )
        )
        agent = SynthesizerAgent(client=fake_client)

        result = agent.process(payload)

        self.assertEqual(
            result,
            "Morning: Tokyo National Museum. Lunch: Ichiran Ramen. Evening: Blue Note Tokyo.",
        )

    def test_process_falls_back_when_ollama_fails(self) -> None:
        """Return a deterministic plan when the model call raises."""
        payload = (
            '{"original_query": "Plan a day in San Francisco", "results": {'
            '"MuseumFinder": {"items": [{"name": "SFMOMA", '
            '"type": "Modern art", "area": "SoMa"}], '
            '"note": "Morning stop."}, '
            '"RestaurantFinder": {"items": [{"name": "Tartine Bakery", '
            '"cuisine": "French bakery", "area": "Mission"}], '
            '"note": "Lunch stop."}, '
            '"ConcertFinder": {"items": [{"name": "The Fillmore", '
            '"genre": "Jazz", "venue": "The Fillmore"}], '
            '"note": "Evening stop."}}}'
        )
        fake_client = _FakeClient(lambda **kwargs: (_ for _ in ()).throw(RuntimeError("Ollama offline")))
        agent = SynthesizerAgent(client=fake_client)

        result = agent.process(payload)

        self.assertIn("Day plan:", result)
        self.assertIn("SFMOMA", result)
        self.assertIn("Tartine Bakery", result)
        self.assertIn("The Fillmore", result)


if __name__ == "__main__":
    unittest.main()