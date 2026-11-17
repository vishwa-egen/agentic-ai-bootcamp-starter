"""Settings for the starter, loaded from environment variables and the `.env` file.

Copy `.env.example` to `.env` and fill in the values. `.env` is ignored by git,
so keys never reach the repository.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Literal
from urllib.parse import urlparse

from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

Framework = Literal["maf", "langgraph", "deepagents"]

PLACEHOLDER = "REPLACE_ME"


def find_project_root(start: Path | None = None) -> Path:
    """Return the nearest folder at or above `start` that holds `pyproject.toml`."""
    here = (start or Path.cwd()).resolve()
    for folder in (here, *here.parents):
        if (folder / "pyproject.toml").is_file():
            return folder
    return here


def is_placeholder(value: str | None) -> bool:
    """True when a setting is empty or still holds the `.env.example` placeholder."""
    return not value or not value.strip() or PLACEHOLDER in value


class Settings(BaseSettings):
    """All configuration in one place. Field names match the variables in `.env`."""

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # --- LLM: any OpenAI-compatible endpoint, for example a LiteLLM proxy ---
    openai_base_url: str = ""
    openai_api_key: SecretStr = SecretStr("")
    openai_model: str = ""
    openai_judge_model: str = ""
    llm_timeout_seconds: float = 60.0

    # --- Arize AX: tracing and evaluation ---
    arize_space_id: str = ""
    arize_api_key: SecretStr = SecretStr("")
    arize_project_name: str = "agentic-ai-bootcamp-starter"
    arize_transport: Literal["grpc", "http"] = "grpc"
    arize_endpoint: str = ""

    # --- Capstone ---
    capstone_name: str = ""
    team_name: str = ""
    agent_framework: Framework = "maf"

    @field_validator("openai_base_url", "arize_endpoint", mode="before")
    @classmethod
    def _strip_url(cls, value: object) -> object:
        return value.strip().rstrip("/") if isinstance(value, str) else value

    @field_validator("openai_model", "openai_judge_model", "arize_space_id", mode="before")
    @classmethod
    def _strip_text(cls, value: object) -> object:
        return value.strip() if isinstance(value, str) else value

    # ---- LLM helpers ----
    @property
    def api_key(self) -> str:
        return self.openai_api_key.get_secret_value().strip()

    @property
    def judge_model(self) -> str:
        """The model used for LLM-as-judge. Falls back to the main model."""
        return (
            self.openai_model
            if is_placeholder(self.openai_judge_model)
            else self.openai_judge_model
        )

    def missing_llm_settings(self) -> list[str]:
        """Names of the LLM variables that still need a value in `.env`."""
        checks = {
            "OPENAI_BASE_URL": self.openai_base_url,
            "OPENAI_API_KEY": self.api_key,
            "OPENAI_MODEL": self.openai_model,
        }
        return [name for name, value in checks.items() if is_placeholder(value)]

    @property
    def llm_ready(self) -> bool:
        return not self.missing_llm_settings()

    @property
    def endpoint_host(self) -> str:
        """Host of the LLM endpoint, safe to show on screen."""
        return urlparse(self.openai_base_url).netloc or "(not set)"

    # ---- Arize helpers ----
    @property
    def arize_key(self) -> str:
        return self.arize_api_key.get_secret_value().strip()

    def missing_arize_settings(self) -> list[str]:
        checks = {"ARIZE_SPACE_ID": self.arize_space_id, "ARIZE_API_KEY": self.arize_key}
        return [name for name, value in checks.items() if is_placeholder(value)]

    @property
    def arize_ready(self) -> bool:
        return not self.missing_arize_settings()


def mask(secret: str) -> str:
    """Show only the last four characters of a secret."""
    if is_placeholder(secret):
        return "(not set)"
    return f"...{secret[-4:]}" if len(secret) > 8 else "(set)"


def load_settings(env_file: Path | str | None = None) -> Settings:
    """Read settings from the environment, then from `.env` at the project root."""
    path = Path(env_file) if env_file else find_project_root() / ".env"
    return Settings(_env_file=path if path.is_file() else None)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Cached settings for normal use. Call `get_settings.cache_clear()` after edits."""
    return load_settings()
