# Plan 001: Connectivity check

Spec: `spec.md`
Status: Approved

## Approach

One settings object reads `.env`. One module creates LLM clients for an
OpenAI-compatible endpoint. Each framework gets a small module with the same
`run(prompt, settings)` function, so the command line, the app and the eval
runner can call any of them the same way.

A local mock LLM stands in for the endpoint in tests. The suite needs no key
and no network. The rejected option was to record real responses, which would
tie the tests to one model.

## Constitution check

| Rule | How this plan meets it |
| --- | --- |
| People approve actions | The starter only reads. It has no write actions. |
| Rules live in code | The calculator evaluates arithmetic in code and rejects anything else. |
| Evals are part of the feature | `evals/golden/smoke.jsonl` runs through the judge. |

## Agent design

- Framework: all three, one module each
- Agents or graph nodes: one agent with two tools
- State and memory: none between runs
- Human approval: not needed, no write actions

## Tools

| Tool | Reads or writes | Input | Output | Data source |
| --- | --- | --- | --- | --- |
| `get_current_time` | Reads | timezone | Date and time | System clock |
| `calculator` | Reads | expression | Result | None |

## Data

None.

## Files to change

| File | Change |
| --- | --- |
| `src/bootcamp/config.py` | Settings from `.env` |
| `src/bootcamp/llm.py` | Client factory and ping |
| `src/bootcamp/agents/` | One starter per framework |
| `src/bootcamp/observability.py` | Tracing setup |
| `src/bootcamp/evals/` | Judge and golden-set runner |
| `src/bootcamp/doctor.py`, `cli.py` | Checks and commands |
| `app/streamlit_app.py` | UI |

## Test and eval plan

- Unit tests: settings, tools, each framework, tracing, judge, checks and the app, all against the mock LLM
- Golden set: `evals/golden/smoke.jsonl`, correctness and relevance judges

## Risks

- A framework release changes its API. Versions are pinned and tested together.
