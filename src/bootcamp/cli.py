"""Command line for the starter.

python -m bootcamp doctor      check Python, packages, the LLM endpoint and Arize
python -m bootcamp ask "..."   run one prompt through an agent
python -m bootcamp eval        run the golden set with the LLM judge
python -m bootcamp app         open the Streamlit app
python -m bootcamp mock-llm    start a local mock LLM (no key needed)
"""

from __future__ import annotations

import argparse
import sys

from bootcamp import __version__
from bootcamp.agents import FRAMEWORKS
from bootcamp.config import find_project_root, get_settings

#: The frameworks still listed in `bootcamp.agents.FRAMEWORKS`.
FRAMEWORK_CHOICES = list(FRAMEWORKS)


def _doctor(args: argparse.Namespace) -> int:
    from bootcamp.doctor import format_checks, run_checks

    checks = run_checks(network=not args.offline)
    print(format_checks(checks))
    return 1 if any(check.status == "fail" for check in checks) else 0


def _ask(args: argparse.Namespace) -> int:
    from bootcamp.agents import run_agent
    from bootcamp.observability import flush_traces

    settings = get_settings()
    framework = args.framework or settings.agent_framework
    result = run_agent(framework, args.prompt, settings)
    print(f"\n{result.text}\n")
    for call in result.tool_calls:
        print(f"  tool: {call.name}({call.arguments}) -> {call.result}")
    print(
        f"  framework: {result.framework} | model: {result.model} | {result.latency_seconds:.1f}s"
    )
    if result.trace_id:
        print(f"  trace id: {result.trace_id}")
    if args.judge:
        from bootcamp.evals.judge import judge_answer

        verdict = judge_answer(args.prompt, result.text, settings=settings)
        print(f"  judge ({verdict.name}): {verdict.label} | {verdict.explanation}")
    flush_traces()
    return 0


def _eval(args: argparse.Namespace) -> int:
    from bootcamp.evals.run import run_eval

    settings = get_settings()
    framework = args.framework or settings.agent_framework
    summary = run_eval(framework, args.dataset, settings, limit=args.limit)
    columns = [
        c for c in ("id", "label", "score", "tools", "output", "error") if c in summary.results
    ]
    print(summary.results[columns].to_string(index=False, max_colwidth=60))
    print(f"\nPass rate: {summary.pass_rate:.0%} ({framework})")
    if summary.output_file:
        print(f"Results saved to {summary.output_file}")
    if summary.pass_rate < args.min_pass_rate:
        print(f"Below the required pass rate of {args.min_pass_rate:.0%}.")
        return 1
    return 0


def _app(args: argparse.Namespace) -> int:
    """Run Streamlit in this process, so Ctrl+C stops the app cleanly."""
    from streamlit.web import cli as streamlit_cli

    app_file = find_project_root() / "app" / "streamlit_app.py"
    sys.argv = ["streamlit", "run", str(app_file), *args.streamlit_args]
    streamlit_cli.main()
    return 0


def _mock_llm(args: argparse.Namespace) -> int:
    from bootcamp.mock_llm import serve_forever

    serve_forever(args.port)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="bootcamp", description=__doc__, formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("--version", action="version", version=f"bootcamp {__version__}")
    commands = parser.add_subparsers(dest="command", required=True)

    doctor = commands.add_parser("doctor", help="check the setup and the connections")
    doctor.add_argument(
        "--offline", action="store_true", help="skip the calls to the LLM and Arize"
    )
    doctor.set_defaults(func=_doctor)

    ask = commands.add_parser("ask", help="run one prompt through an agent")
    ask.add_argument("prompt")
    ask.add_argument(
        "--framework", choices=FRAMEWORK_CHOICES, help="default: AGENT_FRAMEWORK in .env"
    )
    ask.add_argument("--judge", action="store_true", help="grade the answer with the LLM judge")
    ask.set_defaults(func=_ask)

    evals = commands.add_parser("eval", help="run a golden set with the LLM judge")
    evals.add_argument(
        "--framework", choices=FRAMEWORK_CHOICES, help="default: AGENT_FRAMEWORK in .env"
    )
    evals.add_argument("--dataset", default="evals/golden/smoke.jsonl")
    evals.add_argument("--limit", type=int, default=None, help="run only the first N rows")
    evals.add_argument(
        "--min-pass-rate", type=float, default=0.0, help="exit with an error below this rate"
    )
    evals.set_defaults(func=_eval)

    app = commands.add_parser(
        "app", help="open the Streamlit app (extra options go to streamlit run)"
    )
    app.set_defaults(func=_app)

    mock = commands.add_parser(
        "mock-llm", help="start a local mock LLM for trying the starter without a key"
    )
    mock.add_argument("--port", type=int, default=4010)
    mock.set_defaults(func=_mock_llm)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args, extra = parser.parse_known_args(argv)
    if extra and args.command != "app":
        parser.error(f"unrecognized arguments: {' '.join(extra)}")
    args.streamlit_args = extra
    try:
        return args.func(args)
    except Exception as exc:  # noqa: BLE001 - show a short message, not a stack trace
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
