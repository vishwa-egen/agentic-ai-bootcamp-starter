# Tasks NNN: <feature name>

Spec: `spec.md`. Plan: `plan.md`.

Work top to bottom. Finish and commit one task before you start the next.
Each task names its test. Tick the box when the test passes.

## Tasks

- [ ] T1: <small change>
  - Test: <test name or eval case>
  - Covers: AC1
- [ ] T2: <small change>
  - Test: <...>
  - Covers: AC2

## Done when

- [ ] Every acceptance criterion in the spec is covered by a ticked task.
- [ ] `python -m pytest` and `python -m ruff check .` pass.
- [ ] `python -m bootcamp eval` runs and the pass rate is recorded below.

## Eval record

| Date | Framework | Golden set | Pass rate |
| --- | --- | --- | --- |
| <date> | <framework> | <file> | <rate> |
