#!/usr/bin/env bash
# Run once: full initialization = database creation + table creation + seed data.
# Requires: .env with DB_* (or defaults: DB_DATABASE=grid_db, DB_HOST=127.0.0.1, etc.)
# Usage: ./init_once.sh   or   bash init_once.sh

set -e

apt-get update
apt install postgresql-client -y

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [ -f .env ]; then
  set -a
  source .env
  set +a
fi

# Ensure virtual env and dependencies (create_venv.sh is idempotent)
echo "[init_once] Ensuring virtual env and dependencies..."
bash "$SCRIPT_DIR/create_venv.sh"

VENV_DIR="${VENV_DIR:-.venv}"
if [ -x "$VENV_DIR/bin/python" ]; then
  PYTHON="$VENV_DIR/bin/python"
else
  PYTHON=python
fi

DB_HOST="${DB_HOST:-127.0.0.1}"
DB_PORT="${DB_PORT:-5432}"
DB_USERNAME="${DB_USERNAME:-postgres}"
DB_PASSWORD="${DB_PASSWORD:-}"
DB_DATABASE="${DB_DATABASE:-grid_db}"

# ---------------------------------------------------------------------------
# Step 1: Database creation
# ---------------------------------------------------------------------------
echo "[init_once] Step 1/3: Database creation..."
export PGPASSWORD="$DB_PASSWORD"
if psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USERNAME" -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='$DB_DATABASE'" | grep -q 1; then
  echo "[init_once]   Database $DB_DATABASE already exists."
else
  psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USERNAME" -d postgres -c "CREATE DATABASE $DB_DATABASE ENCODING 'UTF8';"
  echo "[init_once]   Created database $DB_DATABASE."
fi
unset PGPASSWORD

# ---------------------------------------------------------------------------
# Step 2: Table creation (Django migrations create grid_table, etc.)
# ---------------------------------------------------------------------------
echo "[init_once] Step 2/3: Table creation (running migrations)..."
"$PYTHON" manage.py migrate --noinput
echo "[init_once]   Tables created."

# ---------------------------------------------------------------------------
# Step 3: Seed data population (24 rows in grid_table, columns A-X)
# ---------------------------------------------------------------------------
echo "[init_once] Step 3/3: Seed data population..."
"$PYTHON" manage.py seedgrid
echo "[init_once]   Seed data loaded."

echo "[init_once] Done. All initialization steps complete. Start the app with: ./start.sh"
