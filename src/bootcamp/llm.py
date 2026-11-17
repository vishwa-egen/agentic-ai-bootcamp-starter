"""One place that creates LLM clients.

The endpoint is OpenAI-compatible. That covers the OpenAI API, an Azure OpenAI
deployment behind a LiteLLM proxy, and most other gateways. Every framework in
this starter gets its endpoint, key and model from here.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from openai import AsyncOpenAI, OpenAI

from bootcamp.config import Settings, get_settings

if TYPE_CHECKING:  # LangChain is imported only when a LangChain-based starter asks for it.
    from langchain_openai import ChatOpenAI


class LLMNotConfiguredError(RuntimeError):
    """Raised when `.env` is missing the LLM endpoint, key or model."""


def require_llm(settings: Settings) -> None:
    missing = settings.missing_llm_settings()
    if missing:
        raise LLMNotConfiguredError(
            f"Set {', '.join(missing)} in your .env file. See .env.example for the format."
        )


def make_openai_client(settings: Settings | None = None) -> OpenAI:
    """Return an OpenAI SDK client pointed at the configured endpoint."""
    settings = settings or get_settings()
    require_llm(settings)
    return OpenAI(
        base_url=settings.openai_base_url,
        api_key=settings.api_key,
        timeout=settings.llm_timeout_seconds,
        max_retries=2,
    )


def make_async_openai_client(settings: Settings | None = None) -> AsyncOpenAI:
    """Async OpenAI SDK client for the configured endpoint. Used by Microsoft Agent Framework."""
    settings = settings or get_settings()
    require_llm(settings)
    return AsyncOpenAI(
        base_url=settings.openai_base_url,
        api_key=settings.api_key,
        timeout=settings.llm_timeout_seconds,
        max_retries=2,
    )


def make_chat_model(settings: Settings | None = None, model: str | None = None) -> ChatOpenAI:
    """LangChain chat model for the configured endpoint. Used by LangGraph and Deep Agents."""
    settings = settings or get_settings()
    require_llm(settings)
    from langchain_openai import ChatOpenAI

    return ChatOpenAI(
        model=model or settings.openai_model,
        base_url=settings.openai_base_url,
        api_key=settings.api_key,
        timeout=settings.llm_timeout_seconds,
        max_retries=2,
    )


@dataclass
class PingResult:
    ok: bool
    model: str
    reply: str = ""
    latency_seconds: float = 0.0
    error: str = ""
    available_models: list[str] = field(default_factory=list)


def list_models(settings: Settings | None = None) -> list[str]:
    """Model names the endpoint reports. Returns an empty list if it does not say."""
    try:
        client = make_openai_client(settings)
        return sorted(model.id for model in client.models.list())
    except Exception:  # noqa: BLE001 - some gateways do not expose /models
        return []


def ping(settings: Settings | None = None) -> PingResult:
    """Send one tiny chat request and report whether the endpoint answered."""
    settings = settings or get_settings()
    try:
        client = make_openai_client(settings)
        started = time.perf_counter()
        # No temperature or token limit: some models reject one or the other.
        response = client.chat.completions.create(
            model=settings.openai_model,
            messages=[{"role": "user", "content": "Reply with the single word: pong"}],
        )
        latency = time.perf_counter() - started
        reply = (response.choices[0].message.content or "").strip()
        return PingResult(True, settings.openai_model, reply, latency)
    except Exception as exc:  # noqa: BLE001 - report every failure to the user
        return PingResult(
            False,
            settings.openai_model,
            error=f"{type(exc).__name__}: {exc}",
            available_models=list_models(settings) if settings.llm_ready else [],
        )
