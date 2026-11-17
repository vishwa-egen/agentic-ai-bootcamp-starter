"""LLM-as-judge evaluators built with the Arize Phoenix evals library.

A judge is a second LLM call that grades an agent's answer against a rubric.
Two judges ship with the starter:

- `relevance`: does the answer address the question? Needs no reference answer.
- `correctness`: does the answer agree with a reference answer from a golden set?

Write your capstone's judges the same way: a prompt template with placeholders,
a set of labels, and a score for each label.
"""

from __future__ import annotations

from dataclasses import dataclass

from phoenix.evals import LLM, ClassificationEvaluator, create_classifier

from bootcamp.config import Settings, get_settings
from bootcamp.llm import require_llm

RELEVANCE_TEMPLATE = """\
You are grading an AI assistant. Decide whether the answer addresses the question.

Question:
{input}

Answer:
{output}

Choose "relevant" if the answer responds to what was asked, even if it is brief.
Choose "irrelevant" if it ignores the question, refuses without reason, or is off topic.
"""

CORRECTNESS_TEMPLATE = """\
You are grading an AI assistant against a reference answer written by a person.

Question:
{input}

Reference answer:
{reference}

Assistant's answer:
{output}

Choose "correct" if the assistant's answer agrees with the reference on every key fact.
Choose "partially_correct" if it agrees on some key facts and misses or contradicts others.
Choose "incorrect" if it contradicts the reference or does not answer the question.
Wording and length do not matter. Facts do.
"""

RELEVANCE_CHOICES = {"relevant": 1.0, "irrelevant": 0.0}
CORRECTNESS_CHOICES = {"correct": 1.0, "partially_correct": 0.5, "incorrect": 0.0}


@dataclass
class JudgeResult:
    name: str
    label: str
    score: float | None
    explanation: str

    @property
    def passed(self) -> bool:
        return self.score is not None and self.score >= 1.0


def make_judge_llm(settings: Settings | None = None) -> LLM:
    """The judge model, served by the same OpenAI-compatible endpoint as the agent."""
    settings = settings or get_settings()
    require_llm(settings)
    return LLM(
        provider="openai",
        model=settings.judge_model,
        api_key=settings.api_key,
        base_url=settings.openai_base_url,
    )


def relevance_judge(settings: Settings | None = None) -> ClassificationEvaluator:
    return create_classifier(
        name="relevance",
        prompt_template=RELEVANCE_TEMPLATE,
        llm=make_judge_llm(settings),
        choices=RELEVANCE_CHOICES,
    )


def correctness_judge(settings: Settings | None = None) -> ClassificationEvaluator:
    return create_classifier(
        name="correctness",
        prompt_template=CORRECTNESS_TEMPLATE,
        llm=make_judge_llm(settings),
        choices=CORRECTNESS_CHOICES,
    )


def judge_answer(
    question: str,
    answer: str,
    reference: str | None = None,
    settings: Settings | None = None,
) -> JudgeResult:
    """Grade one answer. Uses `correctness` when a reference is given, else `relevance`."""
    if reference:
        evaluator = correctness_judge(settings)
        scores = evaluator.evaluate({"input": question, "output": answer, "reference": reference})
    else:
        evaluator = relevance_judge(settings)
        scores = evaluator.evaluate({"input": question, "output": answer})
    score = scores[0]
    return JudgeResult(
        name=score.name or evaluator.name,
        label=str(score.label),
        score=score.score,
        explanation=score.explanation or "",
    )
