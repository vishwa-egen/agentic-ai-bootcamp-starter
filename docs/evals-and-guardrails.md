# Evals and guardrails reference

Ideas to draw from when you fill in sections 4 and 5 of
[`capstone/CAPSTONE.md`](../capstone/CAPSTONE.md). They are starting points, not
a checklist. The best evals and guardrails come from one question: what would
go wrong in production that we want to catch early?

For the capstone, choose 2 or 3 metrics that tell you whether V1 works, and at
least one guardrail that says when the system stops or asks a person. If you run
a case, record the result. If not, mark it as planned.

## How to score an eval

| Method | Use it when | In this repo |
| --- | --- | --- |
| Code-based | The rule is precise: format, schema, length, or a value you can compare with a known answer | A pytest test, or a golden-set `reference` compared in code |
| LLM judge | Quality is subjective or can be phrased many ways | A rubric in `src/bootcamp/evals/judge.py`, run by `python -m bootcamp eval` |
| Human review | You need ground truth, or the case is ambiguous | A teammate labels rows in `evals/results/*.csv` |

Code-based checks are fast, deterministic and cheap. An LLM judge needs
calibration: label 10 to 20 cases by hand first, run the judge on the same
cases, and trust it only when it agrees with the people. Whichever method you
use, write a pass/fail rule that a teammate could apply to the same example and
get the same answer.

## Evals by use case

### Document review and summarization

Summaries, report review, meeting notes, narrative extraction, inconsistency flagging.

| Eval | How to check | What it asks |
| --- | --- | --- |
| Faithfulness | LLM judge | Does the output contain only facts from the source? |
| Completeness | LLM judge or code | Did it capture every important point? |
| Conciseness | Code | Is the output actually shorter than the input? |
| Coherence | LLM judge | Does it read as one logical piece of text? |

### Compliance and policy checking

Policy adherence, regulatory formatting, disclosure completeness.

| Eval | How to check | What it asks |
| --- | --- | --- |
| Detection accuracy | Code or human review | Against reviewer-labeled cases, which real issues were missed and which flags were false alarms? |
| Citation accuracy | Code or LLM judge | Does each flag point to the right rule? |
| Explanation helpfulness | LLM judge | Could a reviewer act on the explanation alone? |

### Knowledge assistants and Q&A

Help desks, documentation bots, policy assistants, platform guidance.

| Eval | How to check | What it asks |
| --- | --- | --- |
| Answer correctness | LLM judge | Is the answer right according to the source material? |
| Source attribution | Code or LLM judge | Is the cited source in the source list, and does it support the answer? |
| Boundary awareness | LLM judge | Does it say "I don't know" when it doesn't know? |
| Tone | LLM judge | Is the reply helpful rather than robotic or dismissive? |
| Actionability | LLM judge | Does the user know exactly what to do next? |
| Escalation accuracy | LLM judge | Does it route to a person when it should? |

### Workflow automation

Audit tracking, approval chains, task routing, status reporting.

| Eval | How to check | What it asks |
| --- | --- | --- |
| Status accuracy | Code | Does it report the workflow's real current state? |
| Action appropriateness | LLM judge | Is the recommended next step reasonable and safe? |
| Escalation accuracy | LLM judge | Does it hand off to a person when it should? |

### Data extraction and mapping

Document extraction, invoice processing, taxonomy mapping, form parsing.

| Eval | How to check | What it asks |
| --- | --- | --- |
| Extraction accuracy | Code or human review | Do extracted values match the reference? Normalize dates and totals in code; have a person check ambiguous fields. |
| Schema conformance | Code | Does the output have the right shape, types and required fields? |
| Handling of ambiguity | LLM judge | Does it flag uncertainty instead of guessing? |

### Change impact analysis

Cross-document dependencies, linked report updates, downstream impacts.

| Eval | How to check | What it asks |
| --- | --- | --- |
| Dependency completeness | Code or LLM judge | Did it find every affected downstream document? |
| False dependency rate | Code or LLM judge | How many flagged documents are not actually affected? |
| Impact severity | LLM judge | Does it tell material changes from cosmetic ones? |

### User onboarding and guidance

In-app assistants, onboarding flows, tutorial bots, setup wizards.

| Eval | How to check | What it asks |
| --- | --- | --- |
| Task completion | LLM judge | Would following the instructions reach the goal? |
| Clarity | LLM judge | Can someone new to the product understand it? |
| Detail level | LLM judge | Does the depth match the user's expertise? |
| Tone | LLM judge | Is it welcoming rather than a dry manual? |

### Risk flagging and anomaly detection

Anomaly detection, fraud flagging, spend monitoring, data quality checks.

| Eval | How to check | What it asks |
| --- | --- | --- |
| Detection accuracy | Code or human review | Against known outcomes, how many real anomalies were caught and how many alerts were false alarms? |
| Explanation quality | LLM judge | Can a reviewer act on the explanation? |
| Threshold calibration | Code | Is the definition of "anomalous" statistically reasonable? |
| Alarm level | LLM judge | Does it tell "take a quick look" from "stop everything"? |

## Guardrails

Guardrails are checks the application runs while it works. Put each one in code
and cover it with a test (constitution rule 5). Pick the ones that matter for
your use case and ask what would go wrong without them.

### Input guardrails

They run before the user's message reaches the model.

| Guardrail | What it does | Ways to build it |
| --- | --- | --- |
| PII detection and redaction | Masks sensitive data such as ID or card numbers before the model sees it | Regex for structured formats; a library such as Microsoft Presidio for names and addresses |
| Prompt injection detection | Catches attempts to override the instructions ("ignore your previous instructions") | Pattern matching as a baseline; a dedicated classifier model or service |
| Jailbreak detection | Catches manipulation through role play, encoding tricks or many small steps | A safety classifier; regex alone misses most of these |
| Sensitive data blocking | Keeps keys, credentials and internal documents out of the model's context | Regex for key formats; an allowlist of data that is safe to process |
| Scope filtering | Rejects off-topic requests before they use model time | A small classifier, or a short yes/no LLM call |
| Input sanitization | Strips markup, scripts and obfuscation characters | Code: sanitization libraries, regex, `unicodedata.normalize` |
| Data classification gating | Blocks content above an allowed sensitivity level | Source metadata tags plus a classifier for untagged content |
| Sensitive topic detection | Flags topics the system must not engage with | A content moderation API, or a small topic classifier |

### Tool and action guardrails

They run before the application executes a tool call the model proposed.
In this starter, put them inside the tool function in `src/bootcamp/tools.py`,
so no prompt can skip them.

| Guardrail | What it does | Ways to build it |
| --- | --- | --- |
| Tool call validation | Checks the requested tool and its arguments | Allow only the tools this workflow step permits; validate the arguments against the tool's types |
| Action boundary enforcement | Blocks an action unless the caller has permission and every approval is in place | Check permission and approval for this exact item first; if either fails, stop and route to a reviewer |

### Output guardrails

They run after the model answers and before the user sees the answer.

| Guardrail | What it does | Ways to build it |
| --- | --- | --- |
| Groundedness check | Confirms the answer is supported by the source documents | An LLM judge that compares the answer with the retrieved context |
| PII leakage detection | Stops sensitive data, including other users' data, from appearing in the answer | The same tools as input PII detection, run on the output |
| Action confirmation | Makes sure a claim such as "I sent it" matches what happened | Report success only when the tool returned success; otherwise report its real status |
| Escalation routing | Forces a hand-off to a person for high-risk, sensitive or ambiguous cases | Rule-based triggers, or a small classifier trained on examples that needed escalation |
| Toxicity and tone filtering | Flags harmful, offensive or off-brand language | A moderation API; an LLM judge with a tone rubric for brand voice |
| Domain boundary check | Replaces answers that drift out of scope | A topic classifier or LLM judge, with a safe fallback such as "I can only help with X" |
| Relevance validation | Checks that the answer addresses the question | An LLM judge; embedding similarity as a fast proxy |
| Compliance disclaimers | Adds required disclaimers on regulated topics | Detect trigger topics by keyword or classifier, then append a fixed disclaimer |
| Output schema validation | Rejects malformed structured output before anything uses it | Code: a JSON schema or Pydantic model |
| Confidence thresholds | Routes to a person when the system is not confident enough | A calibrated confidence score with a threshold, below which the reply hands off |
| Citation validation | Confirms cited sources exist and support the claim | Code to check the source exists; an LLM judge to check it supports the claim |
| URL validation | Checks generated links are real and allowed | Code: an allowlist of domains, and a request that confirms the link resolves |
| Logical consistency | Catches answers that contradict themselves | An LLM judge |
| Competitor mention blocking | Screens out unintended references to competitors | A keyword blocklist |
| Gibberish detection | Catches garbled or repetitive output | Repetition checks in code, or a small classifier |
| Refusal mechanism | Declines gracefully with a helpful redirect | Fixed fallback replies triggered by scope or confidence checks |

## Turning a choice into work in the repo

| You chose | Put it in | Prove it with |
| --- | --- | --- |
| A code-based metric | A pytest test, or a golden-set case with a `reference` | `python -m pytest` |
| An LLM-judge metric | A rubric in `src/bootcamp/evals/judge.py` and cases in `evals/golden/` | `python -m bootcamp eval`, compared with your human labels |
| An input or output guardrail | A function that runs before or after `run_agent`, with a test | A test that sends a bad input or a bad output and expects the block |
| A tool or action guardrail | The tool function in `src/bootcamp/tools.py` | A test that calls the tool without approval and expects a refusal |
| A hand-off to a person | The design in `plan.md`, naming who approves and what happens on a rejection | A test, plus an eval case where escalation is the right answer |
