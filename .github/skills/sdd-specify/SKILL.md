---
name: sdd-specify
description: Write a feature specification before any code. Use when someone describes a new feature or a change in behavior and no spec exists for it yet. Step 1 of spec-driven development.
argument-hint: "[what the feature should do]"
---

# Write a feature spec

You are starting spec-driven development for one feature. Your output is a
specification. Do not write or change code in this step.

The feature request is the user's message. In Claude Code it arrives as: $ARGUMENTS

## Steps

1. Read `specs/constitution.md` and `capstone/CAPSTONE.md` for the rules and the context.
   Take the problem, the user journey, the autonomy level, the metrics and the
   guardrails for this version (V1 or V2) from `CAPSTONE.md`.
2. Find the next feature number. Look at the folders in `specs/` named `NNN-...`
   and add one to the highest number.
3. Create `specs/NNN-short-name/spec.md` from `specs/templates/spec.md`. Use a
   short kebab-case name.
4. Fill in every section from the request. Describe behavior in plain language.
   Leave out implementation detail: no class names, libraries or file paths.
5. Ask the user up to five questions about anything that changes scope, users,
   guardrails or acceptance criteria. Record what stays unanswered under
   "Open questions".
6. Write acceptance criteria that can be tested. Use the form "Given, when, then".
7. Add the eval metrics, each with how it is checked (code-based, LLM judge or
   human review), and at least three eval cases with an input and the expected
   outcome. Use `docs/evals-and-guardrails.md` for ideas.
8. Show the spec and stop. Suggest `/sdd-plan` as the next step once the team approves it.

## Rules

- One feature per spec. Split a request that holds two features.
- State every guardrail the agent must never break, with its type (input,
  tool/action or output), and every action that needs human approval.
- Keep V1 at assist or augment. Propose more autonomy only in a V2 spec, with the
  evidence that justifies it.
- Use neutral examples. Never write a client name, client data or an internal URL.
- Set the status to `Draft`. Only a person changes it to `Approved`.
