---
name: sdd-review
description: Review a change against its spec, plan and the project constitution, and report findings. Use before merging a feature branch or when asked to review work. Step 5 of spec-driven development.
argument-hint: "[spec folder, for example 002-my-feature]"
---

# Review a change

Your output is a list of findings. Do not change code in this step unless asked.

The feature is named in the user's message. In Claude Code it arrives as: $ARGUMENTS
If none is named, infer it from the files changed on the current branch.

## Steps

1. Read the feature's `spec.md`, `plan.md` and `tasks.md`, and `specs/constitution.md`.
2. Read the change: `git diff main...HEAD`, or the files the user points to.
3. Run `python -m pytest` and `python -m ruff check .` and note the results.
4. Check each item below and collect findings.
5. Report the findings in the format at the end.

## Checklist

- Spec: is every acceptance criterion met and covered by a test or an eval case?
- Plan: does the code follow the plan? Is any difference recorded in the plan?
- Scope: does the change stay inside its tasks?
- Constitution: does the change keep every rule? Check human approval for
  actions, rules in code, one way to reach the model, and tracing.
- Tests: do they run against the mock LLM and fail when the behavior breaks?
- Evals: were golden-set cases added for new agent behavior? Is the pass rate recorded?
- Safety: no secrets, no client names, no client data, no internal URLs, synthetic data only.
- Clarity: would a new team member understand the change from the spec and the code?

## Report format

Start with one line: `Ready to merge` or `Changes needed`.

Then list findings, most serious first:

- `[blocker | should fix | note]` `path/to/file.py:line`: what is wrong and what to do instead.

Finish with what you checked and what you could not check.
