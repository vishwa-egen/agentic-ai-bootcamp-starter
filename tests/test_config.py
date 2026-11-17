from bootcamp.config import PLACEHOLDER, Settings, is_placeholder, mask


def make(**values) -> Settings:
    return Settings(_env_file=None, **values)


def test_placeholders_count_as_missing(monkeypatch):
    for name in ("OPENAI_BASE_URL", "OPENAI_API_KEY", "OPENAI_MODEL"):
        monkeypatch.setenv(name, PLACEHOLDER)
    settings = make()
    assert settings.missing_llm_settings() == ["OPENAI_BASE_URL", "OPENAI_API_KEY", "OPENAI_MODEL"]
    assert not settings.llm_ready


def test_ready_when_all_llm_values_are_set(settings):
    assert settings.llm_ready
    assert settings.judge_model == settings.openai_model


def test_base_url_is_cleaned():
    settings = make(openai_base_url="  https://llm.example.com/v1/  ")
    assert settings.openai_base_url == "https://llm.example.com/v1"
    assert settings.endpoint_host == "llm.example.com"


def test_secrets_never_appear_in_repr():
    settings = make(openai_api_key="sk-super-secret-value", arize_api_key="ak-another-secret")
    assert "super-secret" not in repr(settings)
    assert "another-secret" not in repr(settings)
    assert mask(settings.api_key) == "...alue"


def test_arize_is_optional(settings):
    assert not settings.arize_ready
    assert settings.missing_arize_settings() == ["ARIZE_SPACE_ID", "ARIZE_API_KEY"]


def test_is_placeholder():
    assert (
        is_placeholder("") and is_placeholder(None) and is_placeholder(f"https://{PLACEHOLDER}/v1")
    )
    assert not is_placeholder("gpt-4.1")
