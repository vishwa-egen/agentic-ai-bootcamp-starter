# ADR 0001: Agent framework

Status: Proposed
Date: <YYYY-MM-DD>
Deciders: <team members>

## Context

The starter ships one working example for each of three frameworks. Microsoft
Agent Framework is the default. LangGraph and Deep Agents are optional. A
capstone uses one. The team confirms it before writing agent code and records
the reasons here.

## Options

| Option | Strengths | Choose it when |
| --- | --- | --- |
| Microsoft Agent Framework (default) | Agents, workflows, MCP tools and agent-to-agent calls in one library. Python and .NET. | The team wants several agents that hand work to each other, or builds in .NET. |
| LangGraph | An explicit state graph, checkpoints for durable runs, and interrupts for human approval. | The team wants fine control over state, branching and resuming after an approval. |
| Deep Agents (on LangGraph) | A planner, sub-agents and a working file system for long, open-ended tasks. | The agent must plan its own multi-step work and delegate to sub-agents. |

## Decision

<Framework chosen and the two or three reasons that decided it.>

## Consequences

- Delete the starter modules the team will not use from `src/bootcamp/agents/`
  and remove them from `FRAMEWORKS` in `src/bootcamp/agents/__init__.py`.
- Set `AGENT_FRAMEWORK` in `.env` to the chosen framework. The default is `maf`.
- <anything else the team expects>
