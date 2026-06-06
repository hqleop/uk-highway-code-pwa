"""Render fallback entrypoint.

Some manually created Render Python services default to `gunicorn app:app`.
Expose the Django WSGI application under that name so the default still works.
"""
import os

import django
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

if os.environ.get("RUN_MIGRATIONS_ON_START", "true").lower() not in {"0", "false", "no"}:
    django.setup()
    call_command("migrate", interactive=False, verbosity=1)
    call_command("seed_quiz", verbosity=0)

app = get_wsgi_application()
