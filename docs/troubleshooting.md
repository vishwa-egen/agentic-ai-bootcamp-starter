# Troubleshooting

Start with `python -m bootcamp doctor`. It names the failing check and the fix.

## Install and setup

| Problem | Cause and fix |
| --- | --- |
| `python3.12: command not found` (macOS) | Python 3.12 is not installed. Run `brew install python@3.12` and open a new terminal. |
| `py : The term 'py' is not recognized` (Windows) | Python is not installed, or the terminal is stale. Run `winget install -e --id Python.Python.3.12` and open a new PowerShell. |
| `git: command not found`, or a prompt to install developer tools (macOS) | Run `xcode-select --install`, then `brew install git`. |
| `running scripts is disabled on this system` (Windows) | Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once. Or use Command Prompt and `.venv\Scripts\activate.bat`. |
| The setup script says no supported Python was found | Install Python 3.12. Versions 3.11 and earlier are too old for the pinned libraries. |
| `pip` fails with an SSL or certificate error | Your network inspects HTTPS traffic. Try again off the VPN, or ask IT for the company root certificate and run `pip config set global.cert <path-to-certificate>`. |
| `pip` fails with a dependency conflict | You are on an unsupported Python version, or `requirements.txt` changed without `constraints.txt`. Run `python scripts/refresh_constraints.py`. |
| You want to start over | Delete the `.venv` folder and run the setup script again. |

## Running commands

| Problem | Cause and fix |
| --- | --- |
| `No module named bootcamp` | The virtual environment is not active. Activate it, or run the setup script again. |
| `python` runs the wrong version | The environment is not active. Your prompt should start with `(.venv)`. |
| VS Code shows import errors or runs the wrong Python | Run **Python: Select Interpreter** and pick the `.venv` entry. |
| The app says a port is in use | Another copy is running. Stop it, or run `python -m bootcamp app --server.port 8502`. |
| The browser does not open | Open `http://localhost:8501` yourself. |
| Changes to `.env` have no effect in the app | Press **Reload .env** in the sidebar, or restart the app. |

## LLM endpoint

| Problem | Cause and fix |
| --- | --- |
| `AuthenticationError` or 401 | `OPENAI_API_KEY` is wrong, expired or has extra spaces. |
| `NotFoundError` or a message about the model | `OPENAI_MODEL` does not match a model on the endpoint. `doctor` lists the valid names. |
| `APIConnectionError` or a timeout | Check `OPENAI_BASE_URL`, your VPN and your network. The URL usually ends in `/v1`. |
| 429 or a rate-limit message | You hit the endpoint's limit. Wait and retry, or ask for a higher limit. |
| The judge fails and the agent works | The judge needs a model that supports structured output. Set `OPENAI_JUDGE_MODEL` to one that does. |
| The agent answers without calling a tool | Some smaller models skip tools. Use a model with reliable tool calling. |

## Arize

| Problem | Cause and fix |
| --- | --- |
| `doctor` says Arize did not accept the test span, with an authentication message | `ARIZE_SPACE_ID` or `ARIZE_API_KEY` is wrong. Copy both again from your Arize space settings. |
| `doctor` says Arize did not accept the test span, with a connection or proxy message | Your network blocks gRPC. Set `ARIZE_TRANSPORT=http` in `.env`, or ask for access to `otlp.arize.com` on port 443. |
| No traces appear in Arize | Wait a minute, check the project name in `ARIZE_PROJECT_NAME`, and widen the time filter. |
| Your space is in another region | Set `ARIZE_ENDPOINT` to that region's OTLP address. With `ARIZE_TRANSPORT=http`, give the full URL ending in `/v1/traces`. |

## Git and commit checks

| Problem | Cause and fix |
| --- | --- |
| The commit is blocked by `detect-secrets` | The file holds something that looks like a key. Remove it. For a false positive, run `detect-secrets scan --baseline .secrets.baseline` and commit the baseline. |
| The commit is blocked by `blocked-terms` | A private word is in the file named in the message. Replace it with a neutral term. |
| The commit is blocked by `agent skills are in sync` | Run `python scripts/sync_agent_skills.py` and add the changed files. |
| `pre-commit: command not found` | Activate the virtual environment, or run `.venv/bin/pre-commit` directly. |
| You committed a key by mistake | Tell your lead at once and rotate the key. Removing it in a later commit is not enough, because it stays in the history. |
