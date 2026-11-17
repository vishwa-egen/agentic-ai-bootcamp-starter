# Agentic AI Bootcamp Starter

Template repository: [github.com/vishwa-egen/agentic-ai-bootcamp-starter](https://github.com/vishwa-egen/agentic-ai-bootcamp-starter)

A ready-to-run starting point for building an AI agent. It gives you the setup
every agent project needs and none of the business logic, so your team can
spend the bootcamp on the capstone itself.

| You get | Where |
| --- | --- |
| One place for keys and settings | `.env`, read by `src/bootcamp/config.py` |
| A client for any OpenAI-compatible endpoint, such as a LiteLLM proxy | `src/bootcamp/llm.py` |
| A working starter agent in Microsoft Agent Framework (the default), plus optional LangGraph and Deep Agents starters | `src/bootcamp/agents/` |
| Tracing of every agent run to Arize | `src/bootcamp/observability.py` |
| LLM-as-judge evals with a golden set | `src/bootcamp/evals/`, `evals/golden/` |
| A Streamlit app that checks your connections and runs a prompt | `app/streamlit_app.py` |
| Spec-driven development that works the same in GitHub Copilot and Claude Code | `AGENTS.md`, `specs/`, `.agents/skills/` |
| Commit checks that keep keys and client names out of git | `.pre-commit-config.yaml` |

You do not need earlier Python or VS Code experience. Follow the steps in order.

## Contents

1. [What you need before you start](#1-what-you-need-before-you-start)
2. [Install the software](#2-install-the-software)
3. [Create your team's repository](#3-create-your-teams-repository)
4. [Set up the project](#4-set-up-the-project)
5. [Add your keys](#5-add-your-keys)
6. [Check your connections](#6-check-your-connections)
7. [Run the app](#7-run-the-app)
8. [Everyday commands](#8-everyday-commands)
9. [Build your capstone](#9-build-your-capstone)
10. [Work with Copilot or Claude Code](#10-work-with-copilot-or-claude-code)
11. [Keep keys and client names out of git](#11-keep-keys-and-client-names-out-of-git)
12. [Repository tour](#12-repository-tour)
13. [Library versions](#13-library-versions)
14. [Troubleshooting](#14-troubleshooting)

## 1. What you need before you start

Ask your bootcamp lead for these values. You will paste them into a private file in step 5.

| Value | What it is |
| --- | --- |
| LLM endpoint URL | The address of the OpenAI-compatible endpoint, for example a LiteLLM proxy. It usually ends in `/v1`. |
| LLM API key | Your personal key for that endpoint. |
| Model name | The model name or alias the endpoint expects. |
| Arize space ID and API key | From your Arize space settings. Used for tracing and evals. |

You also need a GitHub account with access to your organization, and a license
for GitHub Copilot or Claude Code.

## 2. Install the software

You need Git, Python 3.12 and Visual Studio Code. Python 3.13 and 3.14 also
work. Python 3.11 and earlier do not.

### macOS

Open the Terminal app and run these commands. They use [Homebrew](https://brew.sh).
Install Homebrew first if the `brew` command is not found.

```bash
brew install git python@3.12
brew install --cask visual-studio-code
```

### Windows

Open PowerShell and run:

```powershell
winget install -e --id Git.Git
winget install -e --id Python.Python.3.12
winget install -e --id Microsoft.VisualStudioCode
```

Close PowerShell and open it again so the new commands are found.

### Check the installs

| Check | macOS | Windows |
| --- | --- | --- |
| Git | `git --version` | `git --version` |
| Python | `python3.12 --version` | `py -3.12 --version` |
| VS Code | `code --version` | `code --version` |

Each command prints a version number. If one fails, see [Troubleshooting](#14-troubleshooting).

### VS Code extensions

When you open the project, VS Code offers to install the recommended
extensions. Choose **Install All**. The list is in `.vscode/extensions.json`.

| Extension | ID | Why |
| --- | --- | --- |
| Python | `ms-python.python` | Runs and tests Python and finds the virtual environment |
| Pylance | `ms-python.vscode-pylance` | Code completion and type checking |
| Python Debugger | `ms-python.debugpy` | Breakpoints and step-through debugging |
| Ruff | `charliermarsh.ruff` | Formats and lints on save |
| GitHub Copilot Chat | `github.copilot-chat` | Copilot chat, agent mode and code completion |
| Claude Code | `anthropic.claude-code` | Claude Code inside VS Code |
| GitHub Pull Requests | `github.vscode-pull-request-github` | Review and merge pull requests in the editor |
| Even Better TOML | `tamasfe.even-better-toml` | Syntax help for `pyproject.toml` |

Install Copilot Chat, Claude Code, or both. The project works the same with either.

## 3. Create your team's repository

This repository is a template. Each team makes its own private copy.

1. Open the template repository on GitHub: <https://github.com/vishwa-egen/agentic-ai-bootcamp-starter>.
2. Click **Use this template**, then **Create a new repository**.
3. Choose your organization as the owner and name the repository, for example `capstone-team-name`.
4. Select **Private**.
5. Click **Create repository**.

Do not fork this repository. A fork of a public repository is always public,
and capstone work must stay private.

Now copy your new repository to your laptop. Use the address of your team's new
repository, not the template's address.

```bash
git clone https://github.com/<your-org>/<your-repo>.git
cd <your-repo>
code .
```

`code .` opens the folder in VS Code. Accept the prompt to trust the folder, and
install the recommended extensions when VS Code asks.

## 4. Set up the project

Open a terminal inside VS Code with **Terminal > New Terminal**. Run the setup
script for your system from the project folder.

macOS and Linux:

```bash
./scripts/setup.sh
```

Windows:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup.ps1
```

The script does four things:

1. Creates a virtual environment in the `.venv` folder. Every library installs
   there, so nothing on your laptop changes outside this folder.
2. Installs the pinned libraries with `pip`. The first run takes a few minutes.
3. Copies `.env.example` to `.env`, your private settings file.
4. Installs the commit checks.

Then activate the virtual environment. Do this in every new terminal.

| System | Command |
| --- | --- |
| macOS and Linux | `source .venv/bin/activate` |
| Windows PowerShell | `.\.venv\Scripts\Activate.ps1` |
| Windows Command Prompt | `.venv\Scripts\activate.bat` |

Your prompt now starts with `(.venv)`.

Last, tell VS Code to use the same environment. Press `Cmd+Shift+P` on macOS or
`Ctrl+Shift+P` on Windows, run **Python: Select Interpreter**, and pick the entry
that shows `.venv`. New VS Code terminals then activate it for you.

<details>
<summary>Manual setup, if you prefer to run each command yourself</summary>

macOS and Linux:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]" -c constraints.txt
cp .env.example .env
pre-commit install
```

Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]" -c constraints.txt
Copy-Item .env.example .env
pre-commit install
```

</details>

## 5. Add your keys

Open the `.env` file in VS Code and replace every `REPLACE_ME` value.

| Variable | What to enter |
| --- | --- |
| `OPENAI_BASE_URL` | Your LLM endpoint URL, ending in `/v1` |
| `OPENAI_API_KEY` | Your LLM API key |
| `OPENAI_MODEL` | The model name or alias your endpoint expects |
| `OPENAI_JUDGE_MODEL` | Optional. A different model for the LLM judge. Empty reuses `OPENAI_MODEL`. |
| `ARIZE_SPACE_ID` | Your Arize space ID |
| `ARIZE_API_KEY` | Your Arize API key |
| `ARIZE_PROJECT_NAME` | The project your traces appear under in Arize, for example `bootcamp-team-name` |
| `CAPSTONE_NAME`, `TEAM_NAME` | Your capstone and team names |
| `AGENT_FRAMEWORK` | Your default framework: `maf` (the default), `langgraph` or `deepagents` |

Git ignores `.env`, so your keys stay on your laptop. Never commit a key, and
never paste one into a chat tool.

No key yet? Skip to [Try it without a key](#try-it-without-a-key) and come back later.

## 6. Check your connections

```bash
python -m bootcamp doctor
```

The command checks your Python version, the installed frameworks, the LLM
endpoint and Arize. A healthy setup looks like this:

```text
[ OK ] Python version: Python 3.12.x
[ OK ] Virtual environment: Active: .../.venv
[ OK ] .env file: Found .../.env
[ OK ] Microsoft Agent Framework: agent-framework-core 1.26.0
[ OK ] LangGraph: langgraph 1.2.22
[ OK ] Deep Agents: deepagents 0.7.39
[ OK ] Arize tracing (arize-otel): arize-otel 0.14.1
[ OK ] Arize Phoenix evals: arize-phoenix-evals 3.10.0
[ OK ] LLM endpoint: your-endpoint, model 'your-model', key ...abcd. Replied 'pong' in 0.8s.
[ OK ] Arize tracing: Arize accepted a test span for project 'bootcamp-team-name' (grpc).

All required checks passed.
```

A line marked `[FAIL]` is followed by the fix. If the model name is wrong, the
message lists the models your endpoint offers.

## 7. Run the app

```bash
python -m bootcamp app
```

Your browser opens `http://localhost:8501`. The app has three tabs:

- **Connections** runs the same checks as `doctor` and shows the results.
- **Run a prompt** sends a prompt through the framework you pick. It shows the
  answer, the tools the agent called, the time taken, the trace ID and the LLM
  judge's verdict.
- **Next steps** lists what to do first for your capstone.

Try the sample prompt `What is 17 * 23?` in each framework. The agent calls the
calculator tool and answers 391. Then open your project in Arize to see the trace.

Press `Ctrl+C` in the terminal to stop the app.

### Try it without a key

The starter includes a mock LLM, so you can run everything before your key
arrives. Open a second terminal, activate the environment, and run:

```bash
python -m bootcamp mock-llm
```

Put the three lines it prints into `.env`, then run `doctor` and the app again.
The mock returns canned answers. It proves that your setup works, and it is not
a real model.

## 8. Everyday commands

Run these from the project folder with the virtual environment active.

| Command | What it does |
| --- | --- |
| `python -m bootcamp doctor` | Checks the setup and every connection |
| `python -m bootcamp app` | Opens the Streamlit app |
| `python -m bootcamp ask "What is 17 * 23?"` | Runs one prompt in the terminal |
| `python -m bootcamp ask "..." --framework maf --judge` | Picks a framework and grades the answer |
| `python -m bootcamp eval` | Runs the golden set through the agent and the LLM judge |
| `python -m bootcamp mock-llm` | Starts the local mock LLM |
| `python -m pytest` | Runs the tests. They use the mock LLM and need no key. |
| `python -m ruff check .` | Lints the code |
| `python -m ruff format .` | Formats the code |

The same actions are in VS Code under **Terminal > Run Task**, and the debugger
has ready-made launch entries for the app and for a single prompt.

## 9. Build your capstone

Work in this order.

1. **Describe the capstone.** Work through `capstone/CAPSTONE.md` as a team: roles,
   problem, user journey, a low-autonomy V1, a V2 with guardrails, and the showcase.
   Coding agents read it for context. Metric and guardrail ideas are in
   [docs/evals-and-guardrails.md](docs/evals-and-guardrails.md).
2. **Confirm the framework.** Microsoft Agent Framework is the default. LangGraph
   and Deep Agents are optional: run the same prompt in each, read the starter
   files in `src/bootcamp/agents/`, and record your choice in
   `specs/adr/0001-agent-framework.md`. To drop a starter you do not need, delete
   its module and its line in `FRAMEWORKS` in `src/bootcamp/agents/__init__.py`.
3. **Write a spec before code.** In Copilot Chat or Claude Code, type
   `/sdd-specify` followed by what the feature should do. Review the spec as a team.
4. **Plan, split into tasks, implement, review.** Use `/sdd-plan`, `/sdd-tasks`,
   `/sdd-implement` and `/sdd-review`. Each step is explained in
   [docs/agentic-sdlc.md](docs/agentic-sdlc.md).
5. **Replace the sample tools.** Add your own functions to `src/bootcamp/tools.py`.
   A tool is a plain Python function with type hints and a docstring.
6. **Replace the golden set.** Put your cases in `evals/golden/` and run
   `python -m bootcamp eval`. Write judges for your rubric in `src/bootcamp/evals/judge.py`.
7. **Grow the UI.** Keep `app/streamlit_app.py` as a connection check, or build your demo on it.

How the pieces fit together is in [docs/architecture.md](docs/architecture.md).

## 10. Work with Copilot or Claude Code

The repository is set up so both tools follow the same rules and offer the same commands.

| File | GitHub Copilot | Claude Code |
| --- | --- | --- |
| `AGENTS.md` | Reads it as project instructions | Reads it through `CLAUDE.md` |
| `CLAUDE.md` | Not used | Reads it. The file imports `AGENTS.md`. |
| `.github/copilot-instructions.md` | Reads it. A short pointer to `AGENTS.md`. | Not used |
| `.github/skills/` | Loads the skills | Not used |
| `.claude/skills/` | Not used | Loads the skills |
| `.claude/settings.json` | Not used | Blocks the agent from reading `.env` |

`AGENTS.md` is the single source of the rules. The skills are written once in
`.agents/skills/` and copied to both tool folders by
`python scripts/sync_agent_skills.py`. Edit the source, run the script, and
commit all three folders.

The skills appear as slash commands in the chat box of either tool:

| Command | Step |
| --- | --- |
| `/sdd-specify <what the feature should do>` | Write the spec |
| `/sdd-plan` | Write the technical plan |
| `/sdd-tasks` | Break the plan into tasks |
| `/sdd-implement` | Build the next task, test first |
| `/sdd-review` | Review the change against the spec |

## 11. Keep keys and client names out of git

Three checks run on every commit:

- **Secret scan.** `detect-secrets` and the linter block most things that look like a key or a password.
- **No `.env`.** A staged `.env` file stops the commit.
- **Blocked terms.** Words you list are rejected anywhere in the code, specs or docs.

Set up the blocked terms once per laptop:

```bash
cp .blocked-terms.example .blocked-terms.local
```

Open `.blocked-terms.local` and list your client's name, project code names and
internal system names, one per line. Git ignores this file, so the list stays private.

Use neutral names and synthetic data everywhere in the project.

## 12. Repository tour

```text
.
├── README.md                  this guide
├── AGENTS.md                  rules for coding agents (Copilot, Claude Code, others)
├── CLAUDE.md                  imports AGENTS.md for Claude Code
├── .env.example               template for your private .env
├── requirements.txt           pinned libraries
├── requirements-dev.txt       pinned developer tools
├── constraints.txt            exact version of every package
├── pyproject.toml             package, lint and test settings
├── app/
│   └── streamlit_app.py       connection check and demo UI
├── src/bootcamp/
│   ├── config.py              settings from .env
│   ├── llm.py                 the one place that creates LLM clients, for every framework
│   ├── tools.py               sample tools: replace with yours
│   ├── agents/
│   │   ├── maf_agent.py       Microsoft Agent Framework starter (default)
│   │   ├── langgraph_agent.py LangGraph starter (optional)
│   │   └── deep_agent.py      Deep Agents starter (optional)
│   ├── observability.py       tracing to Arize
│   ├── evals/
│   │   ├── judge.py           LLM-as-judge rubrics
│   │   └── run.py             golden-set runner
│   ├── doctor.py              connection checks
│   ├── cli.py                 the `python -m bootcamp` commands
│   └── mock_llm.py            mock LLM for tests and keyless runs
├── evals/golden/              golden sets (JSON Lines)
├── tests/                     tests, all against the mock LLM
├── specs/                     constitution, templates, decisions, one folder per feature
├── capstone/CAPSTONE.md       your capstone brief: problem, V1, V2, evals, guardrails
├── docs/                      architecture, workflow, evals and guardrails, troubleshooting, maintainer notes
├── scripts/                   setup, constraints refresh, skill sync, blocked-term check
├── .agents/skills/            the spec-driven skills (source)
├── .claude/                   Claude Code settings and skill copies
├── .github/                   Copilot instructions, skill copies, CI
└── .vscode/                   recommended extensions, settings, tasks, debug entries
```

## 13. Library versions

Every version is pinned in `requirements.txt`, and `constraints.txt` pins every
package those libraries pull in. The set was installed and tested together on
Python 3.12, 3.13 and 3.14.

| Library | Version | Role |
| --- | --- | --- |
| `agent-framework-core`, `agent-framework-openai` | 1.26.0, 1.18.2 | Microsoft Agent Framework |
| `langgraph` | 1.2.22 | LangGraph |
| `langchain`, `langchain-openai` | 1.5.0, 1.8.0 | Model and tool layer for LangGraph and Deep Agents |
| `deepagents` | 0.7.39 | Deep Agents |
| `openai` | 3.52.0 | Client for the OpenAI-compatible endpoint |
| `arize-otel` | 0.14.1 | Sends traces to Arize |
| `arize-phoenix-evals` | 3.10.0 | LLM-as-judge evaluators |
| `openinference-instrumentation-langchain` | 0.1.87 | Traces LangGraph and Deep Agents |
| `openinference-instrumentation-agent-framework` | 0.1.17 | Traces Microsoft Agent Framework |
| `streamlit` | 1.67.0 | The app |
| `pydantic-settings` | 2.16.3 | Settings from `.env` |

Deep Agents and the Arize and OpenInference packages are still below version
1.0, so their APIs can change between releases. Upgrade on purpose, one library
at a time. The steps are in [docs/maintainers.md](docs/maintainers.md).

## 14. Troubleshooting

| Problem | Fix |
| --- | --- |
| `python3.12` or `py -3.12` is not found | Install Python 3.12 (step 2), then open a new terminal. |
| PowerShell says running scripts is disabled | Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, or use Command Prompt with `.venv\Scripts\activate.bat`. |
| `No module named bootcamp` | The virtual environment is not active. Activate it (step 4), or run the setup script again. |
| `doctor` fails on the LLM endpoint with 401 | The key is wrong or expired. Check `OPENAI_API_KEY`. |
| `doctor` fails with a model error | `OPENAI_MODEL` does not match a model on the endpoint. The message lists the valid names. |
| `doctor` fails with a connection error | Check `OPENAI_BASE_URL` and your VPN or network. |
| Arize check fails | Check `ARIZE_SPACE_ID` and `ARIZE_API_KEY`. On a restricted network, set `ARIZE_TRANSPORT=http` or ask for access to `otlp.arize.com`. |
| The commit is rejected | Read the message. It names the file and the check. Fix the file and commit again. |

More cases are in [docs/troubleshooting.md](docs/troubleshooting.md).
