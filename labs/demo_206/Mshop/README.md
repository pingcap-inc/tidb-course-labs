# Mshop (demo_206) – Django

This is the **Django** port of the demo_205 Laravel bookstore app. Logic and behavior match demo_205; only the web framework is different.

## Stack

- **Framework:** Django 4.2+
- **Database:** MySQL / TiDB (same as Laravel demo_205)
- **Python:** 3.10+

## Setup

1. **Create a virtualenv and install dependencies:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # or .venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

2. **Configure environment (optional `.env` or export):**

   - `DB_HOST` (default: 127.0.0.1)
   - `DB_PORT` (default: 4000 for TiDB)
   - `DB_DATABASE` (default: shop)
   - `DB_USERNAME` (default: root)
   - `DB_PASSWORD`
   - `URL_PREFIX` – set when behind a reverse proxy (e.g. `/vscode/proxy/8000`)
   - `DEBUG` – set to `True` for development

3. **Create database and run migrations:**

   ```bash
   # Ensure MySQL/TiDB is running and database "shop" exists
   python manage.py migrate
   ```

4. **Load initial data (optional):**

   Use the same `initshop.sql` as demo_205 for users, `pay_type`, `product_type`, and `products`. Adjust table names if your Laravel migrations use different names (e.g. `users` from Laravel vs Django’s `auth_user`). For a quick start you can run the SQL that inserts into `product_type`, `pay_type`, and `products`; create Django superusers for users if needed.

5. **Run the dev server:**

   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

   With `URL_PREFIX` set, pagination and links respect the prefix.

## Routes (same intent as demo_205)

- `/` → product list
- `/products/` – list products (for sale)
- `/products/create/` – create product (redirects to edit)
- `/products/manage/` – manage products (paginated)
- `/products/<id>/` – product detail and buy form
- `/products/<id>/edit/` – edit product form
- `/products/<id>/update/` – POST to update product
- `/products/<id>/delete/` – POST to soft-delete (status D)
- `/products/<id>/buy/` – POST to purchase
- `/transactions/` – all transactions (paginated, by date then id)
- `/transactions/<id>/` – transaction detail
- `/transactions/<user_id>/user/` – user’s orders (paginated)

## Differences from Laravel

- Auth: uses Django’s `auth.User`; purchase uses a hardcoded user id (e.g. 1) like Laravel.
- i18n: locale strings are in `shop/locale_strings.py` (same keys as Laravel’s `shop.php`).
- Pagination: uses `request.build_absolute_uri()` so links respect `URL_PREFIX`.
- Static/media: product photos under `media/assets/images/`; optional `URL_PREFIX` for correct URLs behind a proxy.
