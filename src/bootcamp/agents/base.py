"""Types and prompt shared by the three framework starters."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

#: Replace this with your capstone's instructions.
SYSTEM_PROMPT = (
    "You are the starter agent for the Agentic AI Bootcamp. "
    "Use a tool when it gives a more reliable answer than you can from memory: "
    "the calculator for arithmetic and get_current_time for dates and times. "
    "Keep answers short and state the result directly."
)


@dataclass
class ToolCall:
    name: str
    arguments: Any
    result: str


@dataclass
class AgentResult:
    """What every starter returns, whichever framework ran the prompt."""

    framework: str
    model: str
    prompt: str
    text: str
    tool_calls: list[ToolCall] = field(default_factory=list)
    latency_seconds: float = 0.0
    trace_id: str = ""


def message_text(message: Any) -> str:
    """A LangChain message's content as plain text (content can be a list of parts)."""
    content = message.content
    if isinstance(content, str):
        return content
    return "".join(part.get("text", "") for part in content if isinstance(part, dict))
