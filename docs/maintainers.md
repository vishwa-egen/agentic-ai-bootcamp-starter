# Maintainer notes

For the people who own the template repository.

## One-time repository settings

1. **Make it a template.** On GitHub, open **Settings**, then select
   **Template repository**. Teams then see the **Use this template** button.
2. **Protect `main`.** Require a pull request and a passing CI run before merging.
3. **Turn on secret scanning and push protection** under
   **Settings > Code security**. GitHub then blocks pushes that contain known key formats.
4. **Add the blocked terms as a secret.** Create a repository secret named
   `BLOCKED_TERMS` with your private words, separated by commas. CI then fails
   when one appears, and the log shows the file and line without the word.
5. **Add a license** if the organization wants one. The template ships without a license file.

Teams that create a private repository from the template should repeat steps 2 to 4 there.

## What must never be in this repository

The template is public. Before every merge, check that the change holds:

- no client name, project code name or internal system name
- no real endpoint URL, key or account ID
- no real data, including sample rows copied from a real system
- no person's name or email address (the one exception is the template's own
  address, `https://github.com/vishwa-egen/agentic-ai-bootcamp-starter`, linked from the README)

Keep your own `.blocked-terms.local` current so the commit check catches these.

## Upgrading libraries

Upgrade on purpose, one library family at a time.

1. Change the version in `requirements.txt` or `requirements-dev.txt`.
2. Run `python scripts/refresh_constraints.py`. It rebuilds `constraints.txt`.
3. Run the setup script again to install the new set.
4. Run `python -m pytest`, then `python -m bootcamp doctor` and the app against a real endpoint.
5. Read the release notes of anything below version 1.0. Deep Agents and the
   Arize and OpenInference packages can change their APIs between releases.
6. Update the version table in `README.md`.

The files most likely to need a change after an upgrade:

| Library | File |
| --- | --- |
| Microsoft Agent Framework | `src/bootcamp/agents/maf_agent.py`, `src/bootcamp/observability.py` |
| LangGraph, LangChain | `src/bootcamp/agents/langgraph_agent.py` |
| Deep Agents | `src/bootcamp/agents/deep_agent.py` |
| Arize, OpenInference | `src/bootcamp/observability.py` |
| Phoenix evals | `src/bootcamp/evals/judge.py` |
| Streamlit | `app/streamlit_app.py` |

## Python versions

The pinned set installs on Python 3.12, 3.13 and 3.14. CI runs on 3.12. To add
a version, install with it locally, run the tests, then widen `requires-python`
in `pyproject.toml`, the checks in `scripts/setup.sh` and `scripts/setup.ps1`,
and `SUPPORTED_PYTHON` in `src/bootcamp/doctor.py`.

## Changing the agent skills

Edit the files in `.agents/skills/`, then run `python scripts/sync_agent_skills.py`
and commit the three folders together. CI and the commit check fail when the
copies differ from the source.

## Known limits

- `scripts/setup.ps1` follows the same steps as `scripts/setup.sh`. Run it on a
  Windows laptop after any change to either script.
- The tests use the mock LLM. They prove the wiring and do not measure answer
  quality. Use `python -m bootcamp eval` with a real model for that.
