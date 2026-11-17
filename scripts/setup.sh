#!/usr/bin/env bash
# One-time setup for macOS and Linux. Safe to run again.
#   ./scripts/setup.sh
set -euo pipefail
cd "$(dirname "$0")/.."

# 1. Find a supported Python (3.12 to 3.14). Python 3.12 is the tested default.
PYTHON=""
for candidate in python3.12 python3.13 python3.14 python3 python; do
  if command -v "$candidate" >/dev/null 2>&1 &&
    "$candidate" -c 'import sys; sys.exit(0 if (3, 12) <= sys.version_info[:2] <= (3, 14) else 1)' 2>/dev/null; then
    PYTHON="$candidate"
    break
  fi
done
if [ -z "$PYTHON" ]; then
  echo "No supported Python found. Install Python 3.12 and run this script again."
  echo "  macOS:  brew install python@3.12"
  echo "  Ubuntu: sudo apt install python3.12 python3.12-venv"
  exit 1
fi
echo "==> Using $("$PYTHON" --version) ($(command -v "$PYTHON"))"

# 2. Create the virtual environment. Everything installs into .venv, not your system.
if [ ! -d .venv ]; then
  echo "==> Creating the virtual environment in .venv"
  "$PYTHON" -m venv .venv
fi
VENV_PYTHON=".venv/bin/python"

# 3. Install the pinned libraries.
echo "==> Installing libraries (a few minutes on the first run)"
"$VENV_PYTHON" -m pip install --quiet --upgrade pip
"$VENV_PYTHON" -m pip install --quiet -e ".[dev]" -c constraints.txt

# 4. Create your private settings file.
if [ ! -f .env ]; then
  cp .env.example .env
  echo "==> Created .env from .env.example"
fi

# 5. Install the commit checks.
if [ -d .git ]; then
  .venv/bin/pre-commit install >/dev/null
  echo "==> Installed the pre-commit checks"
fi

cat <<'NEXT'

Setup complete. Next steps:

  1. Open .env and replace every REPLACE_ME value.
  2. Activate the environment:   source .venv/bin/activate
  3. Check your connections:     python -m bootcamp doctor
  4. Open the app:               python -m bootcamp app
NEXT
