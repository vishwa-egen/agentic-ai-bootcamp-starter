# Capstone brief

Fill this in as a team on day one, section by section. It replaces the team
scratchpad, so your thinking lives next to your code. Coding agents read this
file for context before they write a spec, so keep it current.

Use neutral terms. Do not name a client, a client system or a real person's data.

| Section | Time | Owner | Feeds |
| --- | --- | --- | --- |
| [1. Team and roles](#1-team-and-roles) | 5 min | Everyone | This file |
| [2. Problem scoping](#2-problem-scoping) | 10 min | Strategy lead | `specs/NNN-*/spec.md` (Problem) |
| [3. User journey](#3-user-journey) | 10 min | Writer/designer | Spec (Behavior) |
| [4. V1: low autonomy](#4-v1-low-autonomy) | 15 min | Strategy and eval leads | Spec 002, `evals/golden/`, `src/bootcamp/evals/judge.py` |
| [5. V2: next iteration](#5-v2-next-iteration) | 15 min | Eval lead | Spec 003, guardrails in code |
| [6. Showcase](#6-showcase) | 10 min | Presenters | Your deck and demo |

For metric and guardrail ideas by use case, see
[docs/evals-and-guardrails.md](../docs/evals-and-guardrails.md).

## 1. Team and roles

| Field | Value |
| --- | --- |
| Capstone name | <name, also `CAPSTONE_NAME` in `.env`> |
| Team name | <name, also `TEAM_NAME` in `.env`> |
| Repository | <link to your private repository> |

Everyone can contribute across areas. Name one owner for each role.

| Role | What they own | Who |
| --- | --- | --- |
| Writer/designer | Documents the ideas and sketches the user journey | <name> |
| Strategy lead | Shapes the problem framing and the iteration plan | <name> |
| Eval lead | Defines the metrics, the guardrails and what "good" looks like | <name> |
| Presenter(s) | Gives the 8 to 9 minute showcase and takes 5 minutes of questions | <name> |

## 2. Problem scoping

**Problem statement.** Fill in every blank.

> Users currently spend <time> doing <task>. This results in <errors, delays,
> frustration>. AI can solve this by <approach>. We will know it is working when
> <measurable outcome>. If the AI is wrong, the risk is <consequence>.

**Why this is a good fit for generative AI** (1 to 2 lines; use GIFT from the
workshop to name the type of problem):

<answer>

**What the AI needs to do the job** (context engineering):

| Context | What it is for this capstone | Where it lives in the repo |
| --- | --- | --- |
| Instructions | <role, rules, tone> | `SYSTEM_PROMPT` in `src/bootcamp/agents/base.py` |
| External knowledge | <documents, policies, reference data, all synthetic> | A folder you add, such as `data/`, and a tool that reads it |
| Tools | <lookups and actions the agent can call> | `src/bootcamp/tools.py` |

## 3. User journey

**Current workflow, without AI:**

| Step | What happens | Who does it | Time or effort |
| --- | --- | --- | --- |
| 1 | <step> | <role> | <minutes> |
| 2 | <step> | <role> | <minutes> |
| 3 | <step> | <role> | <minutes> |
| 4 | <step> | <role> | <minutes> |

**Where AI fits in.** For each step above where AI can help, say how much it does.

| Step | AI role (assist, augment or automate) | Why |
| --- | --- | --- |
| <n> | <role> | <reason> |

- **Assist:** AI drafts or suggests. The person does the step.
- **Augment:** AI does most of the step. The person reviews and approves.
- **Automate:** AI does the step without review. Save this for V2 or later, with evidence.

## 4. V1: low autonomy

V1 keeps the person in control. AI assists or augments, and the user reviews
and approves before anything is final. Build V1 first and get it working end to end.

| | V1 |
| --- | --- |
| Autonomy level | <Assist or Augment> |
| What AI does | <...> |
| What the user still controls | <...> |
| Why this autonomy level | <...> |

**Flow:** inputs -> AI processing -> user review -> output

| Stage | Your V1 |
| --- | --- |
| Inputs | <what goes into the system> |
| AI processing | <what the agent does with it, and which tools it calls> |
| User review | <what the user checks before approving> |
| Output | <what the final output looks like> |

**Evaluation metrics for V1.** Pick 2 or 3. Evals are checks you run on
examples to see how well the system does its task. Write a pass/fail rule that a
teammate could apply to the same example.

| Metric | What it measures | How you check it | What "good" looks like | Status |
| --- | --- | --- | --- | --- |
| <name> | <...> | <Code-based, LLM judge or human review> | <target, for example 9 of 10 cases> | <planned or result> |
| <name> | <...> | <...> | <...> | <...> |

How each kind of check maps to the repo:

- **Code-based:** a pytest test, or a golden-set case whose `reference` the code compares exactly.
- **LLM judge:** a rubric in `src/bootcamp/evals/judge.py`, run with `python -m bootcamp eval`.
  Label 10 to 20 cases by hand first and check that the judge agrees before you trust it.
- **Human review:** a teammate labels outputs from `evals/results/` and records the pass rate.

## 5. V2: next iteration

Use what you learned from V1 to design the next version. If V2 adds autonomy,
name the evidence that justifies it.

| | V1 | V2 |
| --- | --- | --- |
| Autonomy level | <...> | <...> |
| What AI now handles that the user used to | <...> | <...> |
| What the user still controls | <...> | <...> |

**Justification.** <What V1 results support the change? If V1 has not run yet,
what would you test, and what pass rate would convince you?>

**Guardrails for V2.** Guardrails are checks the application runs while it
works: on the input, before a tool acts, or on the output before the user sees
it. Enforce each one in code, with a test. A prompt can explain a rule but
cannot enforce it.

| Risk or failure mode | Guardrail | Type | Where it runs in the code |
| --- | --- | --- | --- |
| <what could go wrong> | <the check> | <Input, tool/action or output> | <for example, inside the tool in `tools.py`> |
| <...> | <...> | <...> | <...> |

Name at least one point where the system stops and asks a person. Any action
that changes data outside the app needs human approval (constitution rule 4).

**Updated evaluation.** Do the V1 metrics still apply? Add metrics for what V2 adds.

| New or updated metric | What it measures | How you check it | What "good" looks like |
| --- | --- | --- | --- |
| <name> | <...> | <...> | <...> |

## 6. Showcase

Present in 8 to 9 minutes, then take 5 minutes of questions. A short demo of V1
or V2 is an optional bonus: `python -m bootcamp app`, a terminal run, or a trace
in Arize all count.

1. **Problem and user journey.** The problem, who feels it, and the current workflow.
2. **V1: low autonomy.** Where AI steps in, what it does, what the user still
   controls, and the eval results for this version.
3. **V2: next iteration.** What changed and why, and the guardrails in place. Add
   a diagram if it helps.

## From this brief to code

1. Record the framework choice in `specs/adr/0001-agent-framework.md`.
   Microsoft Agent Framework is the default.
2. Run `/sdd-specify` for V1. Give it sections 2 to 4 of this file.
3. Run `/sdd-plan`, `/sdd-tasks` and `/sdd-implement` to build V1.
4. Put the V1 eval cases in `evals/golden/` and record the pass rate in the feature's `tasks.md`.
5. Repeat with a new spec for V2, using section 5.
