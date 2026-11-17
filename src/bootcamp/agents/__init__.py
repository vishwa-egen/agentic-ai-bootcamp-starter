"""Run a prompt through any of the three framework starters.

    from bootcamp.agents import run_agent
    result = run_agent("maf", "What is 17 * 23?")

Microsoft Agent Framework is the default. LangGraph and Deep Agents are
optional. Each framework lives in its own module and is imported only when
used, so a team can delete the starters it does not need.
"""

from __future__ import annotations

import importlib
import time

from bootcamp.agents.base import SYSTEM_PROMPT, AgentResult, ToolCall
from bootcamp.config import Settings, get_settings
from bootcamp.llm import require_llm
from bootcamp.observability import agent_run_span, setup_tracing
from bootcamp.tools import record_tool_calls

#: key -> (display name, module with a `run(prompt, settings)` function).
#: Microsoft Agent Framework is the default. LangGraph and Deep Agents are optional:
#: to drop one, delete its module and its line here.
FRAMEWORKS: dict[str, tuple[str, str]] = {
    "maf": ("Microsoft Agent Framework", "bootcamp.agents.maf_agent"),
    "langgraph": ("LangGraph", "bootcamp.agents.langgraph_agent"),
    "deepagents": ("Deep Agents", "bootcamp.agents.deep_agent"),
}


def framework_label(key: str) -> str:
    return FRAMEWORKS[key][0]


def run_agent(framework: str, prompt: str, settings: Settings | None = None) -> AgentResult:
    """Run `prompt` through the chosen framework and return a uniform result."""
    settings = settings or get_settings()
    if framework not in FRAMEWORKS:
        raise ValueError(
            f"Unknown framework '{framework}'. Choose one of: {', '.join(FRAMEWORKS)}. "
            "Set AGENT_FRAMEWORK in .env to the framework your team kept."
        )
    require_llm(settings)
    setup_tracing(settings)

    label, module_name = FRAMEWORKS[framework]
    module = importlib.import_module(module_name)

    started = time.perf_counter()
    with agent_run_span(framework, prompt) as span, record_tool_calls() as calls:
        text = module.run(prompt, settings)
        span.set_output(text)
    return AgentResult(
        framework=label,
        model=settings.openai_model,
        prompt=prompt,
        text=text,
        tool_calls=[ToolCall(**call) for call in calls],
        latency_seconds=time.perf_counter() - started,
        trace_id=span.trace_id,
    )


__all__ = ["FRAMEWORKS", "SYSTEM_PROMPT", "AgentResult", "ToolCall", "framework_label", "run_agent"]
