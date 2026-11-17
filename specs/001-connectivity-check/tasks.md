# Tasks 001: Connectivity check

Spec: `spec.md`. Plan: `plan.md`.

## Tasks

- [x] T1: Settings load from `.env` and report missing values
  - Test: `tests/test_config.py`
  - Covers: AC2
- [x] T2: LLM client factory and ping
  - Test: `tests/test_llm.py`
  - Covers: AC1
- [x] T3: Sample tools with a call recorder
  - Test: `tests/test_tools.py`
  - Covers: AC3
- [x] T4: One starter agent per framework
  - Test: `tests/test_agents.py`
  - Covers: AC3
- [x] T5: Tracing for all three frameworks
  - Test: `tests/test_tracing.py`
  - Covers: AC4
- [x] T6: LLM judge and golden-set runner
  - Test: `tests/test_evals.py`
  - Covers: AC5
- [x] T7: Doctor checks and command line
  - Test: `tests/test_doctor.py`
  - Covers: AC1, AC2
- [x] T8: Streamlit app
  - Test: `tests/test_app.py`
  - Covers: AC1, AC3, AC5

## Done when

- [x] Every acceptance criterion in the spec is covered by a ticked task.
- [x] `python -m pytest` and `python -m ruff check .` pass.
- [x] `python -m bootcamp eval` runs.

## Eval record

Record your own first run here after you add your keys.

| Date | Framework | Golden set | Pass rate |
| --- | --- | --- | --- |
| <date> | <framework> | `evals/golden/smoke.jsonl` | <rate> |
