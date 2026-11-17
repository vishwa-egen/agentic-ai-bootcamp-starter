"""Streamlit app for the starter: check the connections and run a prompt.

    python -m bootcamp app

This page is a connection check and a demo, kept small on purpose. Build your
capstone UI in its own file, or replace this one.
"""

from __future__ import annotations

import streamlit as st

from bootcamp.agents import FRAMEWORKS, AgentResult, run_agent
from bootcamp.config import Settings, get_settings, is_placeholder, mask
from bootcamp.doctor import Check, run_checks

SAMPLE_PROMPTS = [
    "What is 17 * 23?",
    "What is the current time in UTC?",
    "In one sentence, what is an AI agent?",
]

st.set_page_config(page_title="Agentic AI Bootcamp", layout="wide")


def load() -> Settings:
    return get_settings()


def shown(value: str) -> str:
    """A setting's value for display, or "(not set)" for an empty or placeholder value."""
    return "(not set)" if is_placeholder(value) else value


def show_check(check: Check) -> None:
    box = {"ok": st.success, "warn": st.warning, "fail": st.error}[check.status]
    text = f"**{check.name}**: {check.detail}"
    if check.fix and check.status != "ok":
        text += f"\n\n{check.fix}"
    box(text)


def sidebar(settings: Settings) -> None:
    with st.sidebar:
        st.header("Configuration")
        st.caption("Read from your .env file. Keys are never shown in full.")
        st.markdown(
            f"""
| Setting | Value |
| --- | --- |
| LLM endpoint | `{settings.endpoint_host}` |
| Model | `{shown(settings.openai_model)}` |
| Judge model | `{shown(settings.judge_model)}` |
| LLM key | `{mask(settings.api_key)}` |
| Arize space | `{mask(settings.arize_space_id)}` |
| Arize key | `{mask(settings.arize_key)}` |
| Arize project | `{shown(settings.arize_project_name)}` |
| Capstone | `{shown(settings.capstone_name)}` |
| Team | `{shown(settings.team_name)}` |
"""
        )
        if st.button("Reload .env", key="reload"):
            get_settings.cache_clear()
            st.session_state.pop("checks", None)
            st.rerun()


def connections_tab(settings: Settings) -> None:
    st.subheader("Connections")
    st.write("Checks Python, the installed frameworks, the LLM endpoint and Arize.")
    if st.button("Run connection checks", type="primary", key="run_checks"):
        with st.spinner("Checking..."):
            st.session_state["checks"] = run_checks(settings)
    checks: list[Check] | None = st.session_state.get("checks")
    if checks is None:
        st.info("Press the button to test your setup.")
        return
    failures = sum(check.status == "fail" for check in checks)
    if failures:
        st.error(
            f"{failures} check(s) failed. Fix them, press Reload .env, and run the checks again."
        )
    else:
        st.success("All required checks passed. You are ready to build.")
    for check in checks:
        show_check(check)


def show_result(result: AgentResult) -> None:
    st.markdown("#### Answer")
    st.write(result.text)
    first, second, third = st.columns(3)
    first.metric("Framework", result.framework)
    second.metric("Latency", f"{result.latency_seconds:.1f} s")
    third.metric("Tool calls", len(result.tool_calls))
    if result.tool_calls:
        st.markdown("#### Tool calls")
        st.table(
            [
                {"tool": call.name, "arguments": str(call.arguments), "result": call.result}
                for call in result.tool_calls
            ]
        )
    if result.trace_id:
        st.caption(f"Trace ID: `{result.trace_id}`. Find this run in your Arize project.")
    else:
        st.caption("Tracing is off. Add ARIZE_SPACE_ID and ARIZE_API_KEY to .env to send traces.")


def prompt_tab(settings: Settings) -> None:
    st.subheader("Run a prompt")
    if not settings.llm_ready:
        missing = ", ".join(settings.missing_llm_settings())
        st.warning(f"Set {missing} in .env, then press Reload .env in the sidebar.")
        return

    keys = list(FRAMEWORKS)
    default = keys.index(settings.agent_framework) if settings.agent_framework in keys else 0
    framework = st.selectbox(
        "Agent framework",
        keys,
        index=default,
        format_func=lambda key: FRAMEWORKS[key][0],
        key="framework",
    )
    sample = st.selectbox("Sample prompt", SAMPLE_PROMPTS, key="sample")
    prompt = st.text_area("Prompt", value=sample, height=90, key=f"prompt_{sample}")
    judge = st.checkbox("Grade the answer with the LLM judge", value=True, key="judge")

    if st.button("Run", type="primary", key="run_prompt") and prompt.strip():
        st.session_state.pop("verdict", None)
        try:
            with st.spinner(f"Running with {FRAMEWORKS[framework][0]}..."):
                st.session_state["result"] = run_agent(framework, prompt.strip(), settings)
            if judge:
                from bootcamp.evals.judge import judge_answer

                with st.spinner("Judging the answer..."):
                    result = st.session_state["result"]
                    st.session_state["verdict"] = judge_answer(
                        prompt.strip(), result.text, settings=settings
                    )
        except Exception as exc:  # noqa: BLE001 - show the error on the page
            st.session_state.pop("result", None)
            st.error(f"{type(exc).__name__}: {exc}")

    result: AgentResult | None = st.session_state.get("result")
    if result is None:
        return
    show_result(result)
    verdict = st.session_state.get("verdict")
    if verdict is not None:
        st.markdown("#### LLM judge")
        box = st.success if verdict.passed else st.warning
        box(f"**{verdict.name}: {verdict.label}** (score {verdict.score})\n\n{verdict.explanation}")


def next_steps_tab() -> None:
    st.subheader("Where to go next")
    st.markdown(
        """
1. Work through `capstone/CAPSTONE.md`: problem, user journey, V1, V2 and guardrails.
2. Pick your framework and record the reasons in `specs/adr/0001-agent-framework.md`.
3. Write your first spec with the `/sdd-specify` command in Copilot or Claude Code.
4. Replace the sample tools in `src/bootcamp/tools.py` with your own.
5. Replace `evals/golden/smoke.jsonl` with your golden set and run `python -m bootcamp eval`.
"""
    )


def main() -> None:
    settings = load()
    st.title("Agentic AI Bootcamp")
    st.caption(
        "Starter app: check your connections, then run a prompt through each agent framework."
    )
    sidebar(settings)
    connections, prompt, next_steps = st.tabs(["Connections", "Run a prompt", "Next steps"])
    with connections:
        connections_tab(settings)
    with prompt:
        prompt_tab(settings)
    with next_steps:
        next_steps_tab()


main()
