#!/usr/bin/env bash
# Start the Django web application (reused for every run).
# Loads .env if present, runs migrations, then runserver.
# Usage: ./start.sh   or   bash start.sh

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

VENV_DIR="${VENV_DIR:-.venv}"
if [ -x "$VENV_DIR/bin/python" ]; then
  PYTHON="$VENV_DIR/bin/python"
else
  PYTHON=python
fi

if [ -f .env ]; then
  set -a
  source .env
  set +a
fi

echo "[start] Applying migrations (if any)..."
"$PYTHON" manage.py migrate --noinput

echo "[start] Starting server at http://0.0.0.0:8000"
exec "$PYTHON" manage.py runserver 0.0.0.0:8000
