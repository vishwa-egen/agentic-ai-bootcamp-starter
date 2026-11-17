# Agentic SDLC: spec-driven development with a coding agent

This is how the team builds features in this repository. A coding agent
(GitHub Copilot or Claude Code) drafts the documents and writes the code.
People decide what to build and approve every step.

## Why work this way

A coding agent writes code fast. It does not know what your team decided unless
that decision is written down where the agent can read it. Specs, plans and
tasks in the repository give the agent that context, give reviewers something
to check the code against, and let a new team member catch up by reading.

## The five steps

| Step | Command | The agent produces | People do |
| --- | --- | --- | --- |
| 1. Specify | `/sdd-specify <what the feature should do>` | `specs/NNN-name/spec.md` | Answer the agent's questions. Approve the spec. |
| 2. Plan | `/sdd-plan` | `plan.md` | Check the design against the constitution. Approve the plan. |
| 3. Tasks | `/sdd-tasks` | `tasks.md` | Check that each task is small and has a test. |
| 4. Implement | `/sdd-implement` | Code and tests for one task | Read the diff. Run the app. Commit. |
| 5. Review | `/sdd-review` | Findings against the spec and plan | Fix blockers. A teammate approves the pull request. |

Repeat step 4 for each task. One task is one commit.

## A worked example

```text
You:    /sdd-specify An agent that answers "where is my order?" from the order
        status tool and asks for the order number when it is missing.

Agent:  Asks three questions: who the users are, what happens for an unknown
        order number, and whether the agent may cancel orders.
        Writes specs/002-order-status/spec.md with acceptance criteria and eval cases.

You:    Review the spec with the team. Change Status to Approved.

You:    /sdd-plan

Agent:  Writes plan.md: one new tool, changes to the agent module, test and eval plan.

You:    /sdd-tasks

Agent:  Writes tasks.md with five tasks.

You:    /sdd-implement

Agent:  Writes a failing test for T1, makes it pass, runs pytest and ruff,
        ticks T1, and stops.

You:    Review, commit, and run /sdd-implement again for T2.

You:    /sdd-review     (before you open the pull request)
```

## Branches and pull requests

1. Create a branch for each feature: `git switch -c 002-order-status`.
2. Commit the spec, the plan and the tasks first, then one commit per task.
3. Open a pull request. The template asks for the spec folder and the checks.
4. CI runs the linter, the tests, the secret scan and the skill sync check.
5. A teammate reviews against the spec. Merge when CI is green.

## Where people decide

The agent never decides these. A person does.

- What the feature is for, and what is out of scope
- Guardrails and which actions need approval
- The framework and other decisions recorded in `specs/adr/`
- Whether a spec, a plan or a pull request is approved
- The target pass rate for the evals

## Evals in the loop

Tests show that the code works. Evals show that the agent behaves well. For any
change to what the agent says or does:

1. Add cases to the golden set in the same pull request.
2. Run `python -m bootcamp eval` and record the pass rate in `tasks.md`.
3. Open a few traces in Arize for the failed cases and read what the agent did.

## What keeps this setup portable

| Choice | Why it lasts |
| --- | --- |
| Rules in `AGENTS.md` | An open format that many coding tools read. Claude Code loads it through `CLAUDE.md`. |
| Workflow steps as Agent Skills | An open format (`SKILL.md`) supported by Copilot, Claude Code and other tools. One source in `.agents/skills/`, copied to each tool's folder. |
| Specs as Markdown in the repository | Readable by people and by any tool. Versioned with the code. |
| A folder layout that matches GitHub Spec Kit | A team can adopt Spec Kit later without moving files. |
| Settings and the LLM endpoint in one place | A change of model, gateway or framework touches one file. |

## Tips for working with a coding agent

- Give it the spec folder name. It finds the rest.
- Ask for one task at a time. Small changes are easier to review and to undo.
- When the agent goes wrong, fix the spec or the plan, then ask again.
- Read every diff. You own the code you commit.
- Never paste a key or client data into the chat.
