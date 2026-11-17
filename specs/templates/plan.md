# Plan NNN: <feature name>

Spec: `spec.md`
Status: Draft | Approved

## Approach

<Two or three paragraphs: how the feature works and why this design. Name the simpler option you rejected and why.>

## Constitution check

| Rule | How this plan meets it |
| --- | --- |
| People approve actions | <...> |
| Rules live in code | <...> |
| Evals are part of the feature | <...> |

## Agent design

- Framework: <LangGraph | Microsoft Agent Framework | Deep Agents>, see `specs/adr/0001-agent-framework.md`
- Agents or graph nodes: <name and one-line job for each>
- State and memory: <what is kept between steps and where>
- Human approval: <where the run pauses and how it resumes>

## Tools

| Tool | Reads or writes | Input | Output | Data source |
| --- | --- | --- | --- | --- |
| <name> | <read> | <args> | <result> | <where the data lives> |

## Data

<Tables, files or APIs the feature needs. All synthetic.>

## Files to change

| File | Change |
| --- | --- |
| `src/bootcamp/...` | <what changes> |

## Test and eval plan

- Unit tests: <what they cover>
- Golden set: <which cases, which judge, target pass rate>

## Risks

- <risk and how the plan limits it>
