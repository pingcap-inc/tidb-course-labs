# demo_206 — 24×24 Color Grid (Django)

Single-page Django app: one public page showing a **24×24 color table** stored in PostgreSQL. Sci‑fi style UI. No authentication.

## Stack

- **Framework:** Django 4.2+
- **Database:** PostgreSQL
- **Python:** 3.10+

## Environment variables (runtime .env)

The app loads a **runtime .env file** from the project root (via python-dotenv in `manage.py` / `wsgi` / `asgi`). Use the same variable names as the sample below so links and static URLs work behind a reverse proxy.

| Variable | Purpose |
|----------|--------|
| `APP_NAME` | Application name (default: grid) |
| `APP_ENV` | Environment (e.g. local) |
| `APP_KEY` | Secret key (Django `SECRET_KEY`) |
| `APP_DEBUG` | `true` / `false` — debug mode |
| `APP_URL` | Base URL (e.g. `http://127.0.0.1:8000`); used for `ALLOWED_HOSTS` |
| **`URL_PREFIX`** | **Required behind reverse proxy** (e.g. `/vscode/proxy/8000`). All generated URLs and static paths are prefixed with this. |
| `APP_LOCALE` | Default UI language: `en`, `ja`, or `zh` (default: en). Users can switch via the in-page language switcher. |
| `DB_CONNECTION` | `pgsql` / `postgres` / `postgresql` (default: pgsql) |
| `DB_HOST`, `DB_PORT`, `DB_DATABASE`, `DB_USERNAME`, `DB_PASSWORD` | PostgreSQL connection |

Example `.env` (e.g. behind VS Code proxy):

```env
APP_NAME=grid
APP_ENV=local
APP_KEY=base64:...
APP_DEBUG=true
APP_URL=http://127.0.0.1:8000
URL_PREFIX=/vscode/proxy/8000
APP_LOCALE=en
DB_CONNECTION=pgsql
DB_PORT=5432
DB_HOST=postgres
DB_USERNAME=lab
DB_PASSWORD=labpass
DB_DATABASE=your_database
```

## Create virtual environment (run once per machine)

```bash
cd labs/demo_206/grid
./create_venv.sh
```

Creates `.venv`, installs dependencies from `requirements.txt`, and prints how to activate. `start.sh` and `init_once.sh` will use `.venv` automatically if it exists.

## Run once: database and table initialization

Creates the database, runs migrations, and seeds the 24×24 grid with random colors.

```bash
cd labs/demo_206/grid
# optional: copy .env with DB_* and other vars
./init_once.sh
```

**Table initialization** (schema: 24 rows × columns A–X, see `misc/schema_design.sql`):

- **`init_tables.sql`** — raw SQL that creates the `grid_table` table (RID + A–X, CHAR(6) per cell).
- **`grid/migrations/0002_gridtable_replace_gridcell.py`** — Django migration that creates `grid_table` (used by `init_once.sh` via `manage.py migrate`).

Or manually: run `init_db.sql` to create the database, then load `init_tables.sql` and `python manage.py migrate --fake grid 0002` + `python manage.py seedgrid`, or run `python manage.py migrate` and `python manage.py seedgrid`.

## Start the web application (reused every time)

```bash
cd labs/demo_206/grid
./start.sh
```

Then open the app at **APP_URL** (e.g. `http://127.0.0.1:8000` or, behind a proxy, `http://host/vscode/proxy/8000/`). The single page shows the 24×24 colored grid from the database.

## Languages (en, ja, zh)

The UI supports **English**, **Japanese**, and **Chinese (Simplified)**. Set default via `APP_LOCALE=en|ja|zh` in `.env`. Users can switch language with the header buttons (session-stored). Translation files: `grid/locale/{en,ja,zh_Hans}/LC_MESSAGES/django.po`. After editing `.po` files, run `python manage.py compilemessages` to build `.mo` files.

## Project layout

- `config/` — Django project settings and URLs
- `grid/` — app: model `GridTable` (RID, A–X), one view, one template, locale (en/ja/zh)
- `create_venv.sh` — create Python venv and install dependencies (run once per machine)
- `init_db.sql` — SQL to create the database only
- `misc/schema_design.sql` — schema reference: `grid_table` (RID, A–X)
- `init_tables.sql` — SQL to create the `grid_table` table (table initialization routine)
- `grid/migrations/0002_gridtable_replace_gridcell.py` — Django migration that creates `grid_table`
- `init_once.sh` — run-once script: create DB, migrate (creates table), seed
- `start.sh` — start script: load .env, migrate, runserver
