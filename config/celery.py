import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("highway_code")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "send-daily-reminders": {
        "task": "apps.notifications.tasks.send_daily_reminders",
        "schedule": 60.0,
    },
}
