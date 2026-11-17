"""Tracing to Arize AX with OpenTelemetry and OpenInference.

`setup_tracing()` runs once per process. After that, every agent run sends a
trace to your Arize project, whichever framework you use:

- LangGraph and Deep Agents are traced by the OpenInference LangChain instrumentor.
- Microsoft Agent Framework emits its own OpenTelemetry spans. A span processor
  converts them to the OpenInference format that Arize reads.

Tracing stays off until ARIZE_SPACE_ID and ARIZE_API_KEY are set in `.env`.
"""

from __future__ import annotations

import logging
import threading
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass

from opentelemetry import trace
from opentelemetry.sdk.trace import SpanProcessor, TracerProvider

from bootcamp.config import Settings, get_settings

_lock = threading.Lock()
_status: TracingStatus | None = None
_provider: TracerProvider | None = None


@dataclass
class TracingStatus:
    enabled: bool
    project: str = ""
    detail: str = ""


#: The HTTP exporter needs the full URL, including the /v1/traces path.
ARIZE_HTTP_TRACES_URL = "https://otlp.arize.com/v1/traces"


def _arize_exporter_settings(settings: Settings) -> tuple[dict, object]:
    """Keyword arguments and transport for the Arize exporters.

    gRPC is Arize's default. HTTP is the fallback for networks that block gRPC.
    """
    from arize.otel import Transport

    arguments: dict = {"space_id": settings.arize_space_id, "api_key": settings.arize_key}
    if settings.arize_transport == "http":
        arguments["endpoint"] = settings.arize_endpoint or ARIZE_HTTP_TRACES_URL
        return arguments, Transport.HTTP
    if settings.arize_endpoint:
        arguments["endpoint"] = settings.arize_endpoint
    return arguments, Transport.GRPC


def _agent_framework_converter() -> SpanProcessor | None:
    """Span processor that converts Agent Framework spans to OpenInference.

    The stock processor rewrites every span it sees. LangChain spans are already
    in OpenInference format, so this subclass leaves those untouched. Returns
    None when the team has removed the Agent Framework packages.
    """
    try:
        from openinference.instrumentation.agent_framework import (
            AgentFrameworkToOpenInferenceProcessor,
        )
    except ImportError:
        return None

    class AgentFrameworkOnlyProcessor(AgentFrameworkToOpenInferenceProcessor):
        def on_end(self, span) -> None:
            attributes = span.attributes or {}
            if "openinference.span.kind" not in attributes:
                super().on_end(span)

    return AgentFrameworkOnlyProcessor()


def build_tracer_provider(
    settings: Settings, extra_processors: list[SpanProcessor] | None = None
) -> TracerProvider:
    """Create the tracer provider and its span processors, without making it global."""
    from arize.otel import PROJECT_NAME, Resource

    resource = Resource.create({PROJECT_NAME: settings.arize_project_name})
    provider = TracerProvider(resource=resource)
    # Order matters: convert Agent Framework spans first, then export.
    converter = _agent_framework_converter()
    if converter is not None:
        provider.add_span_processor(converter)
    if settings.arize_ready:
        from arize.otel import BatchSpanProcessor

        arguments, transport = _arize_exporter_settings(settings)
        provider.add_span_processor(BatchSpanProcessor(**arguments, transport=transport))
    for processor in extra_processors or []:
        provider.add_span_processor(processor)
    return provider


def _instrument_frameworks(provider: TracerProvider) -> None:
    """Hook tracing into each installed framework. A removed framework is skipped."""
    try:
        from agent_framework.observability import enable_sensitive_telemetry
    except ImportError:
        pass
    else:
        # Capture prompts and answers on Agent Framework spans.
        enable_sensitive_telemetry()

    try:
        from openinference.instrumentation.langchain import LangChainInstrumentor
    except ImportError:
        return
    # Trace LangChain, LangGraph and Deep Agents.
    instrumentor = LangChainInstrumentor()
    if not instrumentor.is_instrumented_by_opentelemetry:
        instrumentor.instrument(tracer_provider=provider)


def setup_tracing(
    settings: Settings | None = None,
    extra_processors: list[SpanProcessor] | None = None,
) -> TracingStatus:
    """Turn tracing on once. Safe to call many times (Streamlit reruns the script).

    While tracing is off, each call checks the settings again, so adding the
    Arize keys to `.env` and reloading the settings turns tracing on without a
    restart. Once on, it stays on for the life of the process.

    `extra_processors` lets tests capture spans in memory without Arize.
    """
    global _status, _provider
    settings = settings or get_settings()
    with _lock:
        if _status is not None and _status.enabled:
            return _status
        if not settings.arize_ready and not extra_processors:
            missing = ", ".join(settings.missing_arize_settings())
            _status = TracingStatus(
                False, detail=f"Tracing is off. Set {missing} in .env to turn it on."
            )
            return _status

        _provider = build_tracer_provider(settings, extra_processors)
        trace.set_tracer_provider(_provider)
        _instrument_frameworks(_provider)

        _status = TracingStatus(
            True,
            project=settings.arize_project_name,
            detail=f"Sending traces to Arize project '{settings.arize_project_name}'.",
        )
        return _status


def flush_traces(timeout_seconds: float = 10.0) -> None:
    """Send any buffered spans now. Call before a short script exits."""
    if _provider is not None:
        _provider.force_flush(int(timeout_seconds * 1000))


def reset_tracing_for_tests() -> None:
    """Forget the cached status so a test can set tracing up again."""
    global _status, _provider
    with _lock:
        _status = None
        _provider = None


class _RunSpan:
    """Small wrapper so callers can set the output and read the trace ID."""

    def __init__(self, span: trace.Span) -> None:
        self._span = span
        context = span.get_span_context()
        self.trace_id = f"{context.trace_id:032x}" if context.is_valid else ""

    def set_output(self, text: str) -> None:
        self._span.set_attribute("output.value", text)


@contextmanager
def agent_run_span(framework: str, prompt: str) -> Iterator[_RunSpan]:
    """Wrap one agent run in a root span so the whole run is a single trace."""
    tracer = trace.get_tracer("bootcamp")
    attributes = {
        "openinference.span.kind": "CHAIN",
        "input.value": prompt,
        "bootcamp.framework": framework,
    }
    with tracer.start_as_current_span("bootcamp.agent_run", attributes=attributes) as span:
        yield _RunSpan(span)


class _LogCapture(logging.Handler):
    """Collects the exporter's warnings so the check can show the real reason."""

    def __init__(self) -> None:
        super().__init__(level=logging.WARNING)
        self.messages: list[str] = []

    def emit(self, record: logging.LogRecord) -> None:
        self.messages.append(record.getMessage())


def check_arize_connection(
    settings: Settings | None = None, timeout_seconds: float = 10.0
) -> tuple[bool, str]:
    """Export one test span to Arize and report whether Arize accepted it."""
    settings = settings or get_settings()
    if not settings.arize_ready:
        return False, f"Not configured. Set {', '.join(settings.missing_arize_settings())} in .env."

    capture = _LogCapture()
    exporter_logger = logging.getLogger("opentelemetry.exporter")
    previous_propagate = exporter_logger.propagate
    exporter_logger.addHandler(capture)
    exporter_logger.propagate = False  # keep retries out of the terminal during the check
    try:
        from arize.otel import PROJECT_NAME, GRPCSpanExporter, HTTPSpanExporter, Resource, Transport
        from opentelemetry.sdk.trace.export import SimpleSpanProcessor, SpanExportResult
        from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

        memory = InMemorySpanExporter()
        resource = Resource.create({PROJECT_NAME: settings.arize_project_name})
        provider = TracerProvider(resource=resource)
        provider.add_span_processor(SimpleSpanProcessor(memory))
        tracer = provider.get_tracer("bootcamp.doctor")
        with tracer.start_as_current_span("bootcamp.connection_check") as span:
            span.set_attribute("openinference.span.kind", "CHAIN")
            span.set_attribute("input.value", "connection check from python -m bootcamp doctor")
            span.set_attribute("output.value", "ok")

        arguments, transport = _arize_exporter_settings(settings)
        exporter_class = HTTPSpanExporter if transport is Transport.HTTP else GRPCSpanExporter
        exporter = exporter_class(**arguments, timeout=timeout_seconds)
        result = exporter.export(memory.get_finished_spans())
        exporter.shutdown()
        if result is SpanExportResult.SUCCESS:
            project = settings.arize_project_name
            return True, f"Arize accepted a test span for project '{project}' ({transport.value})."
        reason = capture.messages[-1] if capture.messages else "no reason given"
        return False, f"Arize did not accept the test span ({transport.value}): {reason[:300]}"
    except Exception as exc:  # noqa: BLE001 - report every failure to the user
        return False, f"{type(exc).__name__}: {exc}"
    finally:
        exporter_logger.removeHandler(capture)
        exporter_logger.propagate = previous_propagate
