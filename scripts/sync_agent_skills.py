"""Copy the agent skills to the folder each coding tool reads.

The skills are written once, in `.agents/skills/`. GitHub Copilot reads
`.github/skills/` and Claude Code reads `.claude/skills/`, so this script
mirrors the source folder to both. Edit only `.agents/skills/`.

    python scripts/sync_agent_skills.py           copy the skills
    python scripts/sync_agent_skills.py --check   fail if a copy is out of date
"""

from __future__ import annotations

import filecmp
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / ".agents" / "skills"
TARGETS = [ROOT / ".github" / "skills", ROOT / ".claude" / "skills"]


def differences(source: Path, target: Path) -> list[str]:
    """Paths that differ between the source folder and one copy."""
    if not target.is_dir():
        return [f"{target.relative_to(ROOT)} is missing"]
    problems: list[str] = []

    def walk(comparison: filecmp.dircmp) -> None:
        here = Path(comparison.right).relative_to(ROOT)
        problems.extend(f"{here / name} is missing" for name in comparison.left_only)
        problems.extend(f"{here / name} should not exist" for name in comparison.right_only)
        _, changed, errors = filecmp.cmpfiles(
            comparison.left, comparison.right, comparison.common_files, shallow=False
        )
        problems.extend(f"{here / name} is out of date" for name in [*changed, *errors])
        for sub in comparison.subdirs.values():
            walk(sub)

    walk(filecmp.dircmp(source, target))
    return problems


def main() -> int:
    check_only = "--check" in sys.argv[1:]
    problems = [problem for target in TARGETS for problem in differences(SOURCE, target)]
    if check_only:
        if problems:
            print("Agent skills are out of sync:")
            print("\n".join(f"  {problem}" for problem in problems))
            print("Run: python scripts/sync_agent_skills.py")
            return 1
        print("Agent skills are in sync.")
        return 0
    for target in TARGETS:
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(SOURCE, target)
        print(f"Copied {SOURCE.relative_to(ROOT)} -> {target.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
