"""Shared fixtures. Every test talks to the local mock LLM, never to a real endpoint."""

from __future__ import annotations

import pytest
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

from bootcamp import observability
from bootcamp.agents import FRAMEWORKS
from bootcamp.config import Settings, get_settings, load_settings
from bootcamp.mock_llm import MOCK_MODEL, start_mock_server

#: Tests use whichever starters the team kept, so deleting one does not break them.
FIRST_FRAMEWORK = next(iter(FRAMEWORKS))


@pytest.fixture(scope="session")
def mock_llm_url():
    server, url = start_mock_server()
    yield url
    server.shutdown()


@pytest.fixture(autouse=True)
def mock_environment(monkeypatch, mock_llm_url):
    """Point every setting at the mock, whatever is in the developer's own .env."""
    values = {
        "OPENAI_BASE_URL": mock_llm_url,
        "OPENAI_API_KEY": "mock-key-for-tests",  # pragma: allowlist secret
        "OPENAI_MODEL": MOCK_MODEL,
        "OPENAI_JUDGE_MODEL": "",
        "ARIZE_SPACE_ID": "",
        "ARIZE_API_KEY": "",
        "ARIZE_PROJECT_NAME": "bootcamp-tests",
        "AGENT_FRAMEWORK": FIRST_FRAMEWORK,
    }
    for name, value in values.items():
        monkeypatch.setenv(name, value)
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest.fixture
def settings() -> Settings:
    return load_settings()


@pytest.fixture(scope="session", autouse=True)
def span_exporter(mock_llm_url):
    """Capture spans in memory for the whole test session instead of sending them to Arize."""
    exporter = InMemorySpanExporter()
    observability.reset_tracing_for_tests()
    probe = Settings(_env_file=None, arize_project_name="bootcamp-tests")
    observability.setup_tracing(probe, extra_processors=[SimpleSpanProcessor(exporter)])
    return exporter


@pytest.fixture
def spans(span_exporter):
    span_exporter.clear()
    return span_exporter
