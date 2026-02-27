"""QAAgent Executor — A2A protocol adapter for QAAgent.

Wraps the standalone QAAgent with the A2A SDK's AgentExecutor interface,
bridging agent logic to the A2A protocol via EventQueue.
"""

import os
import sys
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

# Load .env from nearest parent directory (searches up to _examples/.env)
load_dotenv(find_dotenv(raise_error_if_not_found=False))

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message

# ---------------------------------------------------------------------------
# Add lesson 05 to path so we can import QAAgent
# ---------------------------------------------------------------------------
LESSON_05_DIR = Path(__file__).resolve().parent.parent.parent / "05-first-a2a-agent" / "src"
sys.path.insert(0, str(LESSON_05_DIR))

from qa_agent import QAAgent  # noqa: E402


# ---------------------------------------------------------------------------
# AgentExecutor implementation
# ---------------------------------------------------------------------------


class QAAgentExecutor(AgentExecutor):
    """Wraps QAAgent with the A2A AgentExecutor interface.

    The execute method:
    1. Extracts the user message from the RequestContext
    2. Calls QAAgent.query() to get the answer
    3. Emits the answer as an agent text message via EventQueue
    """

    def __init__(self, knowledge_path: str = "data/insurance_policy.txt"):
        self.agent = QAAgent(knowledge_path)

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """Execute the agent for an incoming A2A request."""
        # Extract user message text from the request context
        question = context.get_user_input()

        # Call the underlying QA agent
        answer = await self.agent.query(question)

        # Emit the response as a properly formatted A2A event
        await event_queue.enqueue_event(new_agent_text_message(answer))

    async def cancel(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """Handle task cancellation."""
        raise Exception("cancel not supported")
