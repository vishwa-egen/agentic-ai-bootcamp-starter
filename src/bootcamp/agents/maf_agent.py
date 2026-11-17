"""Microsoft Agent Framework starter: one agent with tools.

Grow your capstone from here: add more agents, connect them in a workflow,
attach MCP tools, or add middleware for approvals and guardrails.
"""

from __future__ import annotations

import asyncio

from agent_framework import Agent
from agent_framework.openai import OpenAIChatCompletionClient
from openai import AsyncOpenAI

from bootcamp.agents.base import SYSTEM_PROMPT
from bootcamp.config import Settings
from bootcamp.llm import make_async_openai_client
from bootcamp.tools import SAMPLE_TOOLS


def build_agent(settings: Settings, async_client: AsyncOpenAI) -> Agent:
    """Create the agent on top of a Chat Completions client."""
    chat_client = OpenAIChatCompletionClient(model=settings.openai_model, async_client=async_client)
    return chat_client.as_agent(
        name="bootcamp-starter-agent",
        instructions=SYSTEM_PROMPT,
        tools=SAMPLE_TOOLS,
    )


async def arun(prompt: str, settings: Settings) -> str:
    """Run one prompt and return the final answer. Agent Framework is async."""
    async with make_async_openai_client(settings) as async_client:
        response = await build_agent(settings, async_client).run(prompt)
        return response.text


def run(prompt: str, settings: Settings) -> str:
    """Synchronous wrapper so the command line and the Streamlit app can call the agent."""
    return asyncio.run(arun(prompt, settings))
