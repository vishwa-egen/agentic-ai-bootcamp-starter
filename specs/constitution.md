# Constitution

The standing rules for this project. Every spec, plan, task and review checks
against them. Change this file only by team agreement, in its own pull request.

## 1. Spec before code

A feature starts with a spec that people have read and approved. Code follows
the spec. When they disagree, the spec changes first.

## 2. Small, tested steps

Work lands as small tasks. Each task has a test that fails before the change
and passes after it. The test suite runs against the mock LLM and needs no
network.

## 3. Evals are part of the feature

A change to what the agent says or does comes with eval cases in the golden
set. The pass rate is recorded before and after the change.

## 4. People approve actions

The agent may read and propose. Any action that changes data outside the app
waits for a person's approval. The design names who approves and what happens
on a rejection.

## 5. Rules live in code

A hard business rule is enforced in code and covered by a test. Prompts explain
rules. They do not enforce them.

## 6. One way to reach the model

Settings come from `bootcamp.config`. LLM clients come from `bootcamp.llm`. No
endpoint, key or model name is written anywhere else.

## 7. Every run leaves a trace

Agent runs are traced end to end. A failure can be found and replayed from its
trace ID.

## 8. No secrets and no client data

Keys stay in `.env`. Real client names, client data and internal URLs never
enter the repository. All data is synthetic.

## 9. Keep it simple

Choose the simplest design that meets the spec. Add a framework feature, an
agent or a dependency only when a spec needs it.

## Team additions

Add your own rules below, for example a latency budget or a required reviewer.

- _None yet._
