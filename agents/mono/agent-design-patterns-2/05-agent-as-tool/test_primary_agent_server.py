"""Regression tests for the agent-as-tool example."""

import unittest
from unittest.mock import AsyncMock
from unittest.mock import patch

import primary_agent_server


class _FakeOpenAI:
    """Minimal placeholder for PrimaryAgent client construction."""

    def __init__(self) -> None:
        """Expose the nested chat.completions shape expected by the agent."""
        completions = type("Completions", (), {})()
        self.chat = type("Chat", (), {"completions": completions})()


class PrimaryAgentTests(unittest.IsolatedAsyncioTestCase):
    """Validate fallback and synthesis flow for the primary agent."""

    async def test_process_falls_back_to_direct_calls_when_llm_skips_tools(self) -> None:
        """Call all sub-agents directly when the LLM returns no tool results."""
        with patch.object(primary_agent_server, "OpenAI", return_value=_FakeOpenAI()):
            agent = primary_agent_server.PrimaryAgent()

        fallback_results = {
            "find_food": "food-json",
            "find_transport": "transport-json",
            "find_nearby": "nearby-json",
        }
        agent._try_llm_tools = AsyncMock(return_value={})
        agent._call_all_agents = AsyncMock(return_value=fallback_results)
        agent._synthesize = AsyncMock(return_value="final plan")

        result = await agent.process("Plan a day trip to San Francisco")

        self.assertEqual(result, "final plan")
        agent._try_llm_tools.assert_awaited_once()
        agent._call_all_agents.assert_awaited_once_with("Plan a day trip to San Francisco")
        agent._synthesize.assert_awaited_once_with(
            "Plan a day trip to San Francisco", fallback_results
        )

    async def test_process_uses_llm_tool_results_without_direct_fallback(self) -> None:
        """Skip the direct sub-agent sweep when tool results are already available."""
        with patch.object(primary_agent_server, "OpenAI", return_value=_FakeOpenAI()):
            agent = primary_agent_server.PrimaryAgent()

        tool_results = {"find_food": "food-json"}
        agent._try_llm_tools = AsyncMock(return_value=tool_results)
        agent._call_all_agents = AsyncMock()
        agent._synthesize = AsyncMock(return_value="final plan")

        result = await agent.process("Find food in San Francisco")

        self.assertEqual(result, "final plan")
        agent._try_llm_tools.assert_awaited_once()
        agent._call_all_agents.assert_not_called()
        agent._synthesize.assert_awaited_once_with("Find food in San Francisco", tool_results)


if __name__ == "__main__":
    unittest.main()