import pytest

from bootcamp.agents import FRAMEWORKS, run_agent

KIND = "openinference.span.kind"


@pytest.mark.parametrize("framework", list(FRAMEWORKS))
def test_each_run_is_one_trace_with_llm_and_tool_spans(framework, settings, spans):
    result = run_agent(framework, "What is 17 * 23?", settings)
    finished = spans.get_finished_spans()

    trace_ids = {f"{span.context.trace_id:032x}" for span in finished}
    assert trace_ids == {result.trace_id}

    kinds = {span.attributes.get(KIND) for span in finished}
    assert {"CHAIN", "LLM", "TOOL"} <= kinds

    root = next(span for span in finished if span.name == "bootcamp.agent_run")
    assert root.attributes["input.value"] == "What is 17 * 23?"
    assert "391" in root.attributes["output.value"]


def test_grpc_is_the_default_transport():
    from arize.otel import Transport

    from bootcamp.config import Settings
    from bootcamp.observability import _arize_exporter_settings

    settings = Settings(_env_file=None, arize_space_id="space", arize_api_key="key")
    arguments, transport = _arize_exporter_settings(settings)
    assert transport is Transport.GRPC
    assert "endpoint" not in arguments


def test_http_transport_uses_the_full_traces_url(monkeypatch):
    from arize.otel import Transport

    from bootcamp.config import Settings
    from bootcamp.observability import ARIZE_HTTP_TRACES_URL, _arize_exporter_settings

    monkeypatch.setenv("ARIZE_TRANSPORT", "http")
    settings = Settings(_env_file=None, arize_space_id="space", arize_api_key="key")
    arguments, transport = _arize_exporter_settings(settings)
    assert transport is Transport.HTTP
    assert arguments["endpoint"] == ARIZE_HTTP_TRACES_URL
    assert arguments["endpoint"].endswith("/v1/traces")


def test_tracing_turns_on_after_the_arize_keys_are_added(monkeypatch):
    """Adding the keys and pressing Reload .env must turn tracing on without a restart."""
    from bootcamp import observability
    from bootcamp.config import Settings

    monkeypatch.setattr(observability, "_status", None)
    monkeypatch.setattr(observability, "_provider", None)
    built = []
    monkeypatch.setattr(
        observability, "build_tracer_provider", lambda settings, extra: built.append(settings)
    )
    monkeypatch.setattr(observability.trace, "set_tracer_provider", lambda provider: None)
    monkeypatch.setattr(observability, "_instrument_frameworks", lambda provider: None)

    off = observability.setup_tracing(Settings(_env_file=None))
    assert not off.enabled and not built

    ready = Settings(_env_file=None, arize_space_id="space", arize_api_key="key")
    on = observability.setup_tracing(ready)
    assert on.enabled and len(built) == 1
    assert observability.setup_tracing(ready) is on and len(built) == 1
