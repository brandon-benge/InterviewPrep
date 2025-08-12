#!/usr/bin/env bash
# Activate local virtual environment and run a Python module or script.
# Usage: ./scripts/run_venv.sh generate_quiz.py --ollama --ollama-model mistral --count 5
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${SCRIPT_DIR%/scripts}"
VENV_DIR="$PROJECT_ROOT/.venv"
if [ ! -d "$VENV_DIR" ]; then
  echo "[info] Creating virtual environment at .venv" >&2
  python3 -m venv "$VENV_DIR"
fi
# shellcheck source=/dev/null
source "$VENV_DIR/bin/activate"
if ! python -c "import openai" >/dev/null 2>&1; then
  echo "[info] Installing dependencies (scripts/requirements.txt)" >&2
  python -m pip install --upgrade pip >/dev/null 2>&1 || true
  if [ -f "$PROJECT_ROOT/scripts/requirements.txt" ]; then
    python -m pip install -r "$PROJECT_ROOT/scripts/requirements.txt" >/dev/null 2>&1 || true
  elif [ -f "$PROJECT_ROOT/requirements.txt" ]; then
    # Fallback for backward compatibility
    python -m pip install -r "$PROJECT_ROOT/requirements.txt" >/dev/null 2>&1 || true
  fi
fi
exec python "$@"
