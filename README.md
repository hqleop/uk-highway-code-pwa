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
