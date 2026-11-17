"""Run a golden set through an agent and grade every answer with an LLM judge.

    python -m bootcamp eval
    python -m bootcamp eval --framework maf --dataset evals/golden/smoke.jsonl

A golden set is a JSON Lines file. Each line has:
    {"id": "calc-1", "input": "What is 17 * 23?", "reference": "391"}

`reference` is optional. With a reference the `correctness` judge runs,
without one the `relevance` judge runs. Results go to `evals/results/`.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

from bootcamp.agents import run_agent
from bootcamp.config import Settings, find_project_root, get_settings
from bootcamp.evals.judge import judge_answer
from bootcamp.observability import flush_traces

DEFAULT_DATASET = "evals/golden/smoke.jsonl"


@dataclass
class EvalSummary:
    results: pd.DataFrame
    pass_rate: float
    output_file: Path | None


def load_golden_set(path: Path) -> list[dict]:
    """Read a JSON Lines golden set. Blank lines and lines starting with # are skipped."""
    rows = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        row = json.loads(line)
        if "input" not in row:
            raise ValueError(f"{path}:{number} needs an 'input' field")
        row.setdefault("id", f"row-{number}")
        rows.append(row)
    return rows


def run_eval(
    framework: str,
    dataset: Path | str = DEFAULT_DATASET,
    settings: Settings | None = None,
    limit: int | None = None,
    save: bool = True,
) -> EvalSummary:
    """Run every row of the golden set and return the graded results."""
    settings = settings or get_settings()
    root = find_project_root()
    dataset_path = Path(dataset) if Path(dataset).is_absolute() else root / dataset
    rows = load_golden_set(dataset_path)[:limit]

    records = []
    for row in rows:
        record = {"id": row["id"], "input": row["input"], "reference": row.get("reference", "")}
        try:
            result = run_agent(framework, row["input"], settings)
            verdict = judge_answer(row["input"], result.text, row.get("reference"), settings)
            record |= {
                "output": result.text,
                "tools": ", ".join(call.name for call in result.tool_calls),
                "judge": verdict.name,
                "label": verdict.label,
                "score": verdict.score,
                "explanation": verdict.explanation,
                "latency_seconds": round(result.latency_seconds, 2),
                "trace_id": result.trace_id,
                "error": "",
            }
        except Exception as exc:  # noqa: BLE001 - one bad row must not stop the run
            record |= {
                "output": "",
                "label": "error",
                "score": 0.0,
                "error": f"{type(exc).__name__}: {exc}",
            }
        records.append(record)

    results = pd.DataFrame.from_records(records)
    pass_rate = float((results["score"] >= 1.0).mean()) if len(results) else 0.0

    output_file = None
    if save and len(results):
        folder = root / "evals" / "results"
        folder.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(UTC).strftime("%Y%m%d-%H%M%S")
        output_file = folder / f"{dataset_path.stem}-{framework}-{stamp}.csv"
        results.to_csv(output_file, index=False)

    flush_traces()
    return EvalSummary(results, pass_rate, output_file)
