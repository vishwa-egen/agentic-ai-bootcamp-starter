"""Deep Agents starter: a planning agent built on LangGraph.

`create_deep_agent` adds a to-do planner, a working file system and sub-agents
on top of your tools. Use it when the agent must plan long, open-ended work.
Give sub-agents their own prompts and tools through the `subagents` argument.
"""

from __future__ import annotations

from deepagents import create_deep_agent

from bootcamp.agents.base import SYSTEM_PROMPT, message_text
from bootcamp.config import Settings
from bootcamp.llm import make_chat_model
from bootcamp.tools import SAMPLE_TOOLS


def build_agent(settings: Settings):
    """Create the deep agent. It returns a compiled LangGraph graph."""
    return create_deep_agent(
        model=make_chat_model(settings),
        tools=SAMPLE_TOOLS,
        system_prompt=SYSTEM_PROMPT,
    )


def run(prompt: str, settings: Settings) -> str:
    """Run one prompt through the deep agent and return the final answer."""
    result = build_agent(settings).invoke({"messages": [{"role": "user", "content": prompt}]})
    return message_text(result["messages"][-1])
