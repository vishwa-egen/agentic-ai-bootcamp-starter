# Specs

This folder is the source of truth for what the project builds and why. Code
follows the specs. When they disagree, fix the spec first.

| Path | What it holds |
| --- | --- |
| `constitution.md` | The team's standing rules. Every plan and review checks against it. |
| `templates/` | Blank spec, plan, tasks and decision templates. |
| `adr/` | Architecture decision records, one file per decision. |
| `NNN-short-name/` | One folder per feature: `spec.md`, `plan.md`, `tasks.md`. |

## The loop

| Step | Skill | Output | Who decides |
| --- | --- | --- | --- |
| 1. Specify | `/sdd-specify` | `spec.md`: users, behavior, acceptance criteria, guardrails, eval cases | The team |
| 2. Plan | `/sdd-plan` | `plan.md`: design, data, tools, eval plan | The team |
| 3. Tasks | `/sdd-tasks` | `tasks.md`: small ordered tasks, each with a test | The team |
| 4. Implement | `/sdd-implement` | Code and tests for one task at a time | The engineer |
| 5. Review | `/sdd-review` | Findings against the spec, plan and constitution | A teammate |

The coding agent drafts each document and writes the code. People make the
product and design decisions and approve every step.

`001-connectivity-check/` is a finished example. It describes the starter itself.

The folder layout matches GitHub Spec Kit, so a team can adopt Spec Kit later
without moving files.
