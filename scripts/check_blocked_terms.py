"""Stop client names and other private words from reaching the repository.

The list of blocked terms is private. It comes from either of:

- `.blocked-terms.local` at the repository root (ignored by git), one term per line
- the `BLOCKED_TERMS` environment variable, terms separated by commas or new lines
  (set it as a repository secret to run the same check in CI)

    python scripts/check_blocked_terms.py file1 file2    check these files (pre-commit)
    python scripts/check_blocked_terms.py --all          check every tracked file
    python scripts/check_blocked_terms.py --all --mask   same, without printing the terms

With no terms configured, the check passes and says so.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCAL_LIST = ROOT / ".blocked-terms.local"
SKIP_NAMES = {".blocked-terms.local", ".blocked-terms.example"}


def load_terms() -> list[str]:
    lines: list[str] = []
    if LOCAL_LIST.is_file():
        lines += LOCAL_LIST.read_text(encoding="utf-8").splitlines()
    lines += re.split(r"[,\n]", os.environ.get("BLOCKED_TERMS", ""))
    terms = {line.strip().lower() for line in lines}
    return sorted(term for term in terms if term and not term.startswith("#"))


def tracked_files() -> list[str]:
    result = subprocess.run(  # noqa: S603
        ["git", "ls-files"],  # noqa: S607
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.splitlines()


def scan(files: list[str], terms: list[str], mask: bool) -> list[str]:
    findings = []
    for name in files:
        path = ROOT / name
        if path.name in SKIP_NAMES or not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue  # binary or unreadable file
        for number, line in enumerate(text.splitlines(), start=1):
            lowered = line.lower()
            for index, term in enumerate(terms, start=1):
                if term in lowered:
                    shown = f"blocked term #{index}" if mask else f"'{term}'"
                    findings.append(f"{name}:{number}: {shown}")
    return findings


def main(argv: list[str]) -> int:
    mask = "--mask" in argv
    check_all = "--all" in argv
    files = [arg for arg in argv if not arg.startswith("--")]

    terms = load_terms()
    if not terms:
        print("check_blocked_terms: no blocked terms configured, nothing to check.")
        print("  Copy .blocked-terms.example to .blocked-terms.local and add your terms.")
        return 0

    findings = scan(tracked_files() if check_all else files, terms, mask)
    if findings:
        print("Blocked terms found. Remove them before you commit:")
        print("\n".join(f"  {finding}" for finding in findings))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
