---
name: sdd-tasks
description: Break an approved plan into small, ordered, testable tasks. Use after plan.md exists and before implementation. Step 3 of spec-driven development.
argument-hint: "[spec folder, for example 002-my-feature]"
---

# Write the task list

Your output is `tasks.md` for one feature. Do not write or change code in this step.

The feature is named in the user's message. In Claude Code it arrives as: $ARGUMENTS
If none is named, use the newest folder in `specs/` that has a `plan.md` and no `tasks.md`.

## Steps

1. Read the feature's `spec.md` and `plan.md`.
2. Create `tasks.md` in the feature folder from `specs/templates/tasks.md`.
3. List the tasks in the order they should be built. Put shared groundwork
   first: data, then tools, then agent logic, then UI.
4. For each task, name the test that proves it and the acceptance criteria it covers.
5. Check that every acceptance criterion in the spec is covered by at least one task.
6. Show the task list and stop. Suggest `/sdd-implement` as the next step.

## Rules

- A task is one reviewable change: one behavior, a handful of files, under an hour of work.
- Every task has a test. A task that only adds an eval case names that case.
- Add a task for the golden set whenever the feature changes what the agent says.
- Do not add tasks the spec does not ask for.
