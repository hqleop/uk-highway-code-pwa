# UK Highway Code PWA

Django PWA for studying the official UK Highway Code from `gov.uk`.

## Quick Start

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py import_highway_code --limit-sections 4
python manage.py seed_quiz
python manage.py runserver
```

Open <http://127.0.0.1:8000/>.

## Production Notes

- Set `DATABASE_URL` to PostgreSQL.
- Set `REDIS_URL` for Celery and cache.
- Set VAPID keys before enabling Web Push.
- Serve over HTTPS for PWA installability and Web Push.

## Render

This repository includes `render.yaml`, so Render can create the web service and PostgreSQL database from the repo.

1. Push the latest `main` branch to GitHub.
2. In Render, choose **New +** -> **Blueprint** and connect `hqleop/uk-highway-code-pwa`.
3. Confirm the generated web service and database.
4. After the first deploy, open the Render shell and run:

```bash
python manage.py import_highway_code
```

The deploy runs `migrate`, `seed_quiz`, and imports Highway Code content if the rules table is empty. By default Render imports the first 8 official gov.uk sections via `IMPORT_HIGHWAY_CODE_LIMIT=8`.

If you create a Render Web Service manually instead of using Blueprint, set:

```bash
Build Command: bash ./build.sh
Pre-Deploy Command: python manage.py migrate && python manage.py seed_quiz
Start Command: gunicorn config.wsgi:application
```

If Render tries to run `gunicorn app:app`, the Start Command is still set to Render's default Flask-style command and must be changed.

For a manually created Render service, add a PostgreSQL database and set the web service `DATABASE_URL` env var to its internal connection string. Without `DATABASE_URL`, Django falls back to SQLite, which is not persistent on Render.

To import the full official Highway Code after deploy, open Render Shell and run:

```bash
python manage.py import_highway_code --flush
```
