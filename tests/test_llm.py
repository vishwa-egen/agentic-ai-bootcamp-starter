import pytest

from bootcamp.config import Settings
from bootcamp.llm import LLMNotConfiguredError, list_models, make_openai_client, ping
from bootcamp.mock_llm import MOCK_MODEL


def test_ping_reaches_the_endpoint(settings):
    result = ping(settings)
    assert result.ok and result.reply == "pong"


def test_models_are_listed(settings):
    assert list_models(settings) == [MOCK_MODEL]


def test_ping_reports_a_bad_endpoint():
    settings = Settings(
        _env_file=None,
        openai_base_url="http://127.0.0.1:9/v1",
        openai_api_key="x",
        openai_model="m",
        llm_timeout_seconds=2,
    )
    result = ping(settings)
    assert not result.ok and result.error


def test_missing_settings_raise_a_clear_error(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "")
    with pytest.raises(LLMNotConfiguredError, match="OPENAI_API_KEY"):
        make_openai_client(Settings(_env_file=None))


def test_async_client_uses_the_configured_endpoint(settings):
    from bootcamp.llm import make_async_openai_client

    assert str(make_async_openai_client(settings).base_url).rstrip("/") == settings.openai_base_url


def test_chat_model_uses_the_configured_endpoint(settings):
    pytest.importorskip("langchain_openai", reason="LangGraph and Deep Agents were removed")
    from bootcamp.llm import make_chat_model

    chat = make_chat_model(settings)
    assert chat.model_name == MOCK_MODEL
    assert str(chat.openai_api_base) == settings.openai_base_url
    assert make_chat_model(settings, model="judge-model").model_name == "judge-model"


def test_framework_clients_need_the_llm_settings(monkeypatch):
    from bootcamp.llm import make_async_openai_client, make_chat_model

    monkeypatch.setenv("OPENAI_MODEL", "")
    for factory in (make_chat_model, make_async_openai_client):
        with pytest.raises(LLMNotConfiguredError, match="OPENAI_MODEL"):
            factory(Settings(_env_file=None))
