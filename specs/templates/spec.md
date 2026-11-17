# Spec NNN: <feature name>

Status: Draft | Approved | Done
Version: V1 | V2 (see `capstone/CAPSTONE.md`)
Autonomy: Assist | Augment | Automate
Owner: <name>
Date: <YYYY-MM-DD>

## Problem

<Who has the problem, what they do today, and why that falls short. Three to five sentences.>

## Users and outcome

| User | What they need | How we know it worked |
| --- | --- | --- |
| <role> | <need> | <measure> |

## Behavior

<What the agent does, step by step, in plain language. No implementation detail.>

1. <step>
2. <step>

## Out of scope

- <what this feature does not do>

## Guardrails

Ideas by type are in `docs/evals-and-guardrails.md`. Each guardrail is enforced in code.

| Risk or failure mode | Guardrail | Type |
| --- | --- | --- |
| <what could go wrong> | <the check> | Input, tool/action or output |

Human approval: <which actions need a person's approval, who approves, and what happens on a rejection>

## Acceptance criteria

Each criterion is testable. Each one becomes a test or an eval case.

- [ ] AC1: Given <context>, when <action>, then <result>.
- [ ] AC2: ...

## Eval metrics

The 2 or 3 metrics from `capstone/CAPSTONE.md` that this feature must move.

| Metric | How it is checked | What "good" looks like |
| --- | --- | --- |
| <name> | Code-based, LLM judge or human review | <target> |

## Eval cases

At least three examples for the golden set.

| ID | Input | Expected outcome |
| --- | --- | --- |
| <id> | <input> | <what a correct answer contains> |

## Open questions

- <question, and who can answer it>
