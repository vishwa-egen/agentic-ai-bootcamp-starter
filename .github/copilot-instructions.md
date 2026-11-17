# Copilot instructions

The full instructions for this repository are in `AGENTS.md` at the repository
root. Read that file and follow it. The short version:

- Work spec first. Use the skills `/sdd-specify`, `/sdd-plan`, `/sdd-tasks`,
  `/sdd-implement` and `/sdd-review`. Read `specs/constitution.md` before you plan or code.
- Use the virtual environment in `.venv`. Run `python -m pytest` and
  `python -m ruff check .` before you call a task done.
- Read settings through `bootcamp.config` and create LLM clients through `bootcamp.llm`.
- Never read, print or commit `.env` or any secret.
- Never write a real client name, client data or an internal URL anywhere in the repository.
