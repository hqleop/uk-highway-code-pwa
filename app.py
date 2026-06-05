"""Render fallback entrypoint.

Some manually created Render Python services default to `gunicorn app:app`.
Expose the Django WSGI application under that name so the default still works.
"""
import os

from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = get_wsgi_application()
