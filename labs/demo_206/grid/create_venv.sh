#!/usr/bin/env bash
# Create a Python virtual environment and install dependencies.
# Run once per machine. Usage: ./create_venv.sh

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

VENV_DIR="${VENV_DIR:-.venv}"

if [ -d "$VENV_DIR" ]; then
  echo "[create_venv] Virtual env already exists at $VENV_DIR"
else
  echo "[create_venv] Creating virtual env at $VENV_DIR ..."
  python3 -m venv "$VENV_DIR"
  echo "[create_venv] Done."
fi

echo "[create_venv] Installing dependencies from requirements.txt ..."
"$VENV_DIR/bin/pip" install -r requirements.txt

echo "[create_venv] Compiling translation messages (en, ja, zh) ..."
"$VENV_DIR/bin/python" manage.py compilemessages 2>/dev/null || true

echo "[create_venv] Ready. Activate with:"
echo "  source $VENV_DIR/bin/activate   # Linux/macOS"
echo "  $VENV_DIR\\Scripts\\activate     # Windows"
