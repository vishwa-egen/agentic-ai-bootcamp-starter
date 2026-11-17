---
name: sdd-plan
description: Turn an approved feature spec into a technical plan covering design, tools, data and evals. Use after a spec exists and before any code. Step 2 of spec-driven development.
argument-hint: "[spec folder, for example 002-my-feature]"
---

# Write the technical plan

Your output is `plan.md` for one feature. Do not write or change code in this step.

The spec to plan is named in the user's message. In Claude Code it arrives as: $ARGUMENTS
If none is named, use the newest folder in `specs/` that has a `spec.md` and no `plan.md`.

## Steps

1. Read the feature's `spec.md`, `specs/constitution.md`, `capstone/CAPSTONE.md`
   and `specs/adr/0001-agent-framework.md`.
2. If the spec has open questions that block the design, ask them and stop.
3. Read the code the feature will touch. Start with `AGENTS.md` for the project map.
4. Create `plan.md` in the feature folder from `specs/templates/plan.md`.
5. Fill in the approach, the agent design, the tools, the data, the files to
   change, and the test and eval plan.
6. Complete the constitution check table. If the plan breaks a rule, change the plan.
7. Record any decision that affects more than this feature as a new file in
   `specs/adr/`, from `specs/templates/adr.md`.
8. Show the plan and stop. Suggest `/sdd-tasks` as the next step once the team approves it.

## Rules

- Choose the simplest design that meets the spec. Name the simpler option you rejected and why.
- Every tool has a typed input, a typed output and a named data source.
- Every write action has a human approval step.
- Hard business rules and every guardrail in the spec are enforced in code, with a test.
  Put tool and action guardrails inside the tool function.
- Each LLM-judge metric names the human-labeled cases used to calibrate it.
- Reuse `bootcamp.config` for settings and `bootcamp.llm` for model clients.
- Each acceptance criterion maps to a test or an eval case.
