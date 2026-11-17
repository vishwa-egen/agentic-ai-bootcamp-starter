"""LangGraph starter: an explicit graph with a model node and a tool node.

    START -> model -> (tool calls?) -> tools -> model -> ... -> END

Grow your capstone from here: add nodes, branches, a checkpointer for memory,
or an interrupt for human approval.
"""

from __future__ import annotations

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from bootcamp.agents.base import SYSTEM_PROMPT, message_text
from bootcamp.config import Settings
from bootcamp.llm import make_chat_model
from bootcamp.tools import SAMPLE_TOOLS


def build_graph(settings: Settings):
    """Build and compile the agent graph."""
    model = make_chat_model(settings).bind_tools(SAMPLE_TOOLS)

    def call_model(state: MessagesState) -> dict:
        messages = [SystemMessage(SYSTEM_PROMPT), *state["messages"]]
        return {"messages": [model.invoke(messages)]}

    graph = StateGraph(MessagesState)
    graph.add_node("model", call_model)
    graph.add_node("tools", ToolNode(SAMPLE_TOOLS))
    graph.add_edge(START, "model")
    graph.add_conditional_edges("model", tools_condition)  # to "tools" or END
    graph.add_edge("tools", "model")
    return graph.compile()


def run(prompt: str, settings: Settings) -> str:
    """Run one prompt through the graph and return the final answer."""
    result = build_graph(settings).invoke({"messages": [HumanMessage(prompt)]})
    return message_text(result["messages"][-1])
