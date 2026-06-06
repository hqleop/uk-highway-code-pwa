import os

from django.core.wsgi import get_wsgi_application

from .startup import run_startup_tasks


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
run_startup_tasks()
application = get_wsgi_application()
