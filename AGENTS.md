# AGENTS.md

Instructions for AI coding agents that work in this repository: GitHub Copilot,
Claude Code and any other tool that reads `AGENTS.md`. People should start with
`README.md`.

## What this repository is

A starter for building an AI agent as a bootcamp capstone. It wires up
configuration, an OpenAI-compatible LLM endpoint, three agent frameworks, Arize
tracing, LLM-as-judge evals and a small Streamlit app. It contains no business
logic. Each team adds its capstone on top.

## Commands

Always use the project's virtual environment. Never install packages globally.

| Task | macOS and Linux | Windows |
| --- | --- | --- |
| Set up | `./scripts/setup.sh` | `powershell -ExecutionPolicy Bypass -File .\scripts\setup.ps1` |
| Python in the venv | `.venv/bin/python` | `.venv\Scripts\python.exe` |

With the virtual environment active, the commands are the same everywhere:

- Tests: `python -m pytest`
- Lint: `python -m ruff check .`
- Format: `python -m ruff format .`
- Connection check: `python -m bootcamp doctor`
- Run one prompt: `python -m bootcamp ask "What is 17 * 23?"`
- Evals: `python -m bootcamp eval`
- App: `python -m bootcamp app`

Run the tests and the linter before you say a task is done.

## Project map

| Path | Purpose |
| --- | --- |
| `src/bootcamp/config.py` | All settings. Reads `.env`. |
| `src/bootcamp/llm.py` | The only place that creates LLM clients. |
| `src/bootcamp/tools.py` | Tools the agents can call. |
| `src/bootcamp/agents/` | One starter per framework: `maf_agent.py` (default), and optional `langgraph_agent.py` and `deep_agent.py`. |
| `src/bootcamp/observability.py` | Tracing to Arize. |
| `src/bootcamp/evals/` | LLM-as-judge and the golden-set runner. |
| `src/bootcamp/mock_llm.py` | Mock LLM used by every test. |
| `app/streamlit_app.py` | Demo and connection-check UI. |
| `evals/golden/` | Golden sets in JSON Lines. |
| `specs/` | Constitution, templates, decisions and one folder per feature. |
| `capstone/CAPSTONE.md` | The team's capstone brief: problem, user journey, V1 and V2, metrics, guardrails. |
| `docs/evals-and-guardrails.md` | Eval and guardrail ideas by use case, and where each goes in the code. |
| `tests/` | Tests. They never call a real endpoint. |

## How we work: spec-driven development

Every feature follows the same five steps. Each step has a skill with the same
name in Copilot and in Claude Code.

1. `/sdd-specify`: write `specs/NNN-name/spec.md`. No code.
2. `/sdd-plan`: write `plan.md` from the spec. Design, data, tools, evals.
3. `/sdd-tasks`: write `tasks.md`. Small tasks, each with a test.
4. `/sdd-implement`: build one task at a time, tests first.
5. `/sdd-review`: check the change against the spec, the plan and the constitution.

Rules:

- Read `specs/constitution.md` before you plan or write code. It overrides other guidance.
- Do not write feature code without a spec and a task for it. A typo fix or a
  small refactor needs no spec.
- When the code and the spec disagree, stop and ask. Then update the spec first.
- Keep each change small enough to review in a few minutes.

## Code conventions

- Python 3.12 or later, with type hints. Ruff formats and lints. Line length is 100.
- Read settings only through `bootcamp.config`. Do not call `os.environ` elsewhere.
- Create LLM clients only through `bootcamp.llm`: `make_openai_client`,
  `make_async_openai_client` or `make_chat_model`. Never hard-code an endpoint,
  a key or a model name.
- A tool is a plain function with type hints and a docstring. Register it in `tools.py`.
- Put hard business rules in code, with a test. A prompt can explain a rule but
  cannot enforce it.
- Every new behavior gets a test that runs against the mock LLM, and an eval
  case in the golden set when it changes what the agent says.
- To add a dependency, pin it in `requirements.txt`, run
  `python scripts/refresh_constraints.py`, and say why in the pull request.
- The agent skills live in `.agents/skills/`. Edit them there, then run
  `python scripts/sync_agent_skills.py`. Never edit the copies in
  `.claude/skills/` or `.github/skills/`.

## Security and privacy

These rules have no exceptions.

- Never read, print, log or commit `.env` or any key, token or password.
- Never put a real client name, client data, an internal URL or a person's name
  in code, specs, tests, commit messages or docs. Use neutral examples.
  The one exception is the template's own address, `https://github.com/vishwa-egen/agentic-ai-bootcamp-starter`,
  which the README links to so teams can find the template.
- Use synthetic data only.
- Any agent action that changes data outside the app needs human approval in the design.
- Do not turn off the pre-commit hooks or the tests to get a change through.

## Definition of done

- The task's acceptance criteria are met and its box in `tasks.md` is ticked.
- `python -m pytest` and `python -m ruff check .` pass.
- New behavior has a test, and an eval case where it applies.
- The spec, the plan and the docs match the code.
