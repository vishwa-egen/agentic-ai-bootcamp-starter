from bootcamp.agents import FRAMEWORKS
from bootcamp.evals.judge import CORRECTNESS_CHOICES, RELEVANCE_CHOICES, judge_answer
from bootcamp.evals.run import load_golden_set, run_eval


def test_relevance_judge_returns_a_label(settings):
    verdict = judge_answer("What is 2 + 2?", "4", settings=settings)
    assert verdict.name == "relevance"
    assert verdict.label in RELEVANCE_CHOICES
    assert verdict.explanation


def test_correctness_judge_runs_when_a_reference_is_given(settings):
    verdict = judge_answer("What is 2 + 2?", "4", reference="4", settings=settings)
    assert verdict.name == "correctness"
    assert verdict.label in CORRECTNESS_CHOICES


def test_golden_set_loads(tmp_path):
    file = tmp_path / "set.jsonl"
    file.write_text('# comment\n{"input": "hi"}\n\n{"id": "b", "input": "yo", "reference": "x"}\n')
    rows = load_golden_set(file)
    assert [row["id"] for row in rows] == ["row-2", "b"]


def test_eval_run_grades_every_row(settings):
    summary = run_eval(next(iter(FRAMEWORKS)), settings=settings, limit=2, save=False)
    assert len(summary.results) == 2
    assert set(summary.results["label"]) <= set(CORRECTNESS_CHOICES) | set(RELEVANCE_CHOICES)
    assert 0.0 <= summary.pass_rate <= 1.0
