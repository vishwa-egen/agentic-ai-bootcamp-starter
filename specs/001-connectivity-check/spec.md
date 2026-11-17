# Spec 001: Connectivity check

Status: Done
Owner: Bootcamp starter
Date: 2026-11-16

This is the worked example. It describes what the starter does out of the box.

## Problem

A developer new to the project needs to know that the laptop, the LLM endpoint
and the tracing account all work before writing any agent code. Without one
clear check, a wrong key or model name shows up later as a confusing framework error.

## Users and outcome

| User | What they need | How we know it worked |
| --- | --- | --- |
| Developer | Proof that setup is complete | One command reports every connection as OK |
| Developer | A first agent run in each framework | The same prompt returns an answer from all three |

## Behavior

1. The developer runs `python -m bootcamp doctor` or opens the app.
2. The check reports the Python version, the virtual environment, the `.env`
   file and the installed frameworks.
3. The check sends one small request to the LLM endpoint and reports the reply.
4. The check sends one test span to Arize and reports whether Arize accepted it.
5. The developer runs a prompt through a chosen framework and sees the answer,
   the tool calls and a judge's verdict.

## Out of scope

- Any business logic.
- Deployment.

## Guardrails

- A key is never printed in full.
- A missing setting produces a message that names the variable to fix.

## Acceptance criteria

- [x] AC1: Given a complete `.env`, when the developer runs `doctor`, then every required check reports OK.
- [x] AC2: Given a missing LLM setting, when the developer runs any command, then the message names the missing variable.
- [x] AC3: Given the prompt "What is 17 * 23?", when it runs in each framework, then the agent calls the calculator and answers 391.
- [x] AC4: Given tracing is on, when an agent runs, then the run is one trace with LLM and tool spans.
- [x] AC5: Given an answer, when the judge runs, then it returns a label and an explanation.

## Eval cases

| ID | Input | Expected outcome |
| --- | --- | --- |
| calc-1 | What is 17 * 23? | 391 |
| calc-2 | What is (125 + 75) / 8? | 25 |
| time-1 | What is the current time in UTC? | A current UTC time from the tool |

## Open questions

- None.
