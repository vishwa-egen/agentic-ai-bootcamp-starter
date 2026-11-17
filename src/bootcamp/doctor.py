"""Connection and setup checks, used by `python -m bootcamp doctor` and the Streamlit app."""

from __future__ import annotations

import importlib.metadata
import sys
from dataclasses import dataclass
from typing import Literal

from bootcamp.config import Settings, find_project_root, get_settings, is_placeholder, mask
from bootcamp.llm import list_models, ping
from bootcamp.observability import check_arize_connection

Status = Literal["ok", "warn", "fail"]

#: Framework key in `bootcamp.agents.FRAMEWORKS` -> the PyPI package that proves it is installed.
#: Only the frameworks still listed in FRAMEWORKS are checked, so a team can delete the others.
FRAMEWORK_PACKAGES = {
    "maf": "agent-framework-core",
    "langgraph": "langgraph",
    "deepagents": "deepagents",
}

#: Display name -> package that every team needs, whichever framework it keeps.
REQUIRED_PACKAGES = {
    "Arize tracing (arize-otel)": "arize-otel",
    "Arize Phoenix evals": "arize-phoenix-evals",
}

SUPPORTED_PYTHON = ((3, 12), (3, 14))


@dataclass
class Check:
    name: str
    status: Status
    detail: str
    fix: str = ""


def check_python() -> Check:
    version = sys.version_info
    text = f"Python {version.major}.{version.minor}.{version.micro}"
    low, high = SUPPORTED_PYTHON
    if not (low <= (version.major, version.minor) <= high):
        return Check(
            "Python version", "fail", text, "Install Python 3.12 and recreate the .venv folder."
        )
    return Check("Python version", "ok", text)


def check_virtualenv() -> Check:
    if sys.prefix != sys.base_prefix:
        return Check("Virtual environment", "ok", f"Active: {sys.prefix}")
    return Check(
        "Virtual environment",
        "warn",
        "No virtual environment is active.",
        "Activate .venv first (see README, step 4).",
    )


def check_env_file() -> Check:
    path = find_project_root() / ".env"
    if path.is_file():
        return Check(".env file", "ok", f"Found {path}")
    return Check(".env file", "fail", "No .env file.", "Copy .env.example to .env and fill it in.")


def check_packages() -> list[Check]:
    from bootcamp.agents import FRAMEWORKS

    wanted = {
        label: FRAMEWORK_PACKAGES[key]
        for key, (label, _module) in FRAMEWORKS.items()
        if key in FRAMEWORK_PACKAGES
    } | REQUIRED_PACKAGES
    checks = []
    for label, package in wanted.items():
        try:
            checks.append(Check(label, "ok", f"{package} {importlib.metadata.version(package)}"))
        except importlib.metadata.PackageNotFoundError:
            checks.append(
                Check(label, "fail", f"{package} is not installed.", "Run the setup script again.")
            )
    return checks


def check_llm(settings: Settings) -> Check:
    missing = settings.missing_llm_settings()
    if missing:
        return Check(
            "LLM endpoint", "fail", f"Missing: {', '.join(missing)}", "Fill these in .env."
        )
    result = ping(settings)
    where = (
        f"{settings.endpoint_host}, model '{settings.openai_model}', key {mask(settings.api_key)}"
    )
    if result.ok:
        return Check(
            "LLM endpoint",
            "ok",
            f"{where}. Replied '{result.reply}' in {result.latency_seconds:.1f}s.",
        )
    fix = "Check OPENAI_BASE_URL, OPENAI_API_KEY and OPENAI_MODEL in .env."
    if result.available_models:
        fix += f" Models this endpoint offers: {', '.join(result.available_models[:15])}."
    return Check("LLM endpoint", "fail", f"{where}. {result.error}", fix)


def check_model_listed(settings: Settings) -> Check | None:
    """Warn when the endpoint lists its models and the configured one is absent."""
    if not settings.llm_ready:
        return None
    models = list_models(settings)
    if not models or settings.openai_model in models:
        return None
    return Check(
        "Model name",
        "warn",
        f"'{settings.openai_model}' is not in the endpoint's model list.",
        f"Available: {', '.join(models[:15])}",
    )


def check_arize(settings: Settings) -> Check:
    missing = settings.missing_arize_settings()
    if missing:
        return Check(
            "Arize tracing",
            "warn",
            f"Off. Missing: {', '.join(missing)}",
            "Optional for a first run. Add the values to .env to see traces in Arize.",
        )
    ok, detail = check_arize_connection(settings)
    if ok and is_placeholder(settings.arize_project_name):
        return Check(
            "Arize tracing",
            "warn",
            detail,
            "Set ARIZE_PROJECT_NAME in .env to your team's project name.",
        )
    if ok:
        return Check("Arize tracing", "ok", detail)
    if settings.arize_transport == "grpc":
        fix = "Check ARIZE_SPACE_ID and ARIZE_API_KEY. Network blocked? Set ARIZE_TRANSPORT=http."
    else:
        fix = "Check ARIZE_SPACE_ID and ARIZE_API_KEY, and your network access to Arize."
    return Check("Arize tracing", "fail", detail, fix)


def run_checks(settings: Settings | None = None, network: bool = True) -> list[Check]:
    """Run every check. `network=False` skips the calls to the LLM and Arize."""
    settings = settings or get_settings()
    checks = [check_python(), check_virtualenv(), check_env_file(), *check_packages()]
    if network:
        checks.append(check_llm(settings))
        listed = check_model_listed(settings) if checks[-1].status == "ok" else None
        if listed:
            checks.append(listed)
        checks.append(check_arize(settings))
    return checks


def format_checks(checks: list[Check]) -> str:
    """Plain-text report that prints cleanly in any terminal."""
    marks = {"ok": "[ OK ]", "warn": "[WARN]", "fail": "[FAIL]"}
    lines = []
    for check in checks:
        lines.append(f"{marks[check.status]} {check.name}: {check.detail}")
        if check.fix and check.status != "ok":
            lines.append(f"       -> {check.fix}")
    failures = sum(check.status == "fail" for check in checks)
    lines.append("")
    lines.append("All required checks passed." if not failures else f"{failures} check(s) failed.")
    return "\n".join(lines)
