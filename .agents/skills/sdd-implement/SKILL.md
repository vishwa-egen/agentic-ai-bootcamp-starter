---
name: sdd-implement
description: Implement the next unchecked task from a feature's tasks.md, test first. Use when the spec, plan and tasks are approved and it is time to write code. Step 4 of spec-driven development.
argument-hint: "[spec folder and optional task ID, for example 002-my-feature T3]"
---

# Implement one task

Your output is working, tested code for exactly one task.

The feature and task are named in the user's message. In Claude Code they arrive as: $ARGUMENTS
If no task is named, take the first unchecked task in the feature's `tasks.md`.

## Steps

1. Read the feature's `spec.md`, `plan.md` and `tasks.md`, and `specs/constitution.md`.
2. State which task you are implementing and which acceptance criteria it covers.
3. Write the test first. Run it and confirm that it fails for the right reason.
4. Write the smallest change that makes the test pass.
5. Run the checks with the project's virtual environment:
   - `python -m pytest`
   - `python -m ruff check .`
   - `python -m ruff format .`
6. If the task changes what the agent says, add or update cases in the golden
   set and run `python -m bootcamp eval`.
7. Tick the task's box in `tasks.md`.
8. Summarize what changed and stop. Do not start the next task without being asked.

## Rules

- Stay inside the task. Note other problems you find and leave them alone.
- If the plan turns out to be wrong, stop and say so. Update the plan before the code.
- Tests run against the mock LLM. Never call a real endpoint from a test.
- Read settings through `bootcamp.config`. Create model clients through `bootcamp.llm`.
- Never read or print `.env`. Never write a client name, client data or an internal URL.
- Do not weaken a test, a lint rule or a pre-commit hook to get the task through.
