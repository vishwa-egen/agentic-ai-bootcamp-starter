"""Checks on the repository itself: placeholders, skills and ignored files."""

import subprocess
import sys
from pathlib import Path

from bootcamp.config import PLACEHOLDER, Settings

ROOT = Path(__file__).resolve().parents[1]


def test_env_example_covers_every_setting():
    example = (ROOT / ".env.example").read_text(encoding="utf-8")
    names = {
        line.split("=", 1)[0] for line in example.splitlines() if "=" in line and line[0] != "#"
    }
    for field in Settings.model_fields:
        if field != "llm_timeout_seconds":
            assert field.upper() in names, f"{field.upper()} is missing from .env.example"


def test_env_example_holds_only_placeholders():
    example = (ROOT / ".env.example").read_text(encoding="utf-8")
    for line in example.splitlines():
        if line.startswith(("OPENAI_API_KEY=", "ARIZE_API_KEY=", "ARIZE_SPACE_ID=")):
            assert line.split("=", 1)[1] == PLACEHOLDER


def test_env_files_are_ignored_by_git():
    ignore = (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
    assert ".env" in ignore and ".blocked-terms.local" in ignore


def test_agent_skills_are_in_sync():
    script = ROOT / "scripts" / "sync_agent_skills.py"
    result = subprocess.run(
        [sys.executable, str(script), "--check"], capture_output=True, text=True
    )
    assert result.returncode == 0, result.stdout


def test_every_skill_has_a_name_that_matches_its_folder():
    for skill in (ROOT / ".agents" / "skills").iterdir():
        text = (skill / "SKILL.md").read_text(encoding="utf-8")
        assert f"name: {skill.name}\n" in text
        assert "description: " in text
