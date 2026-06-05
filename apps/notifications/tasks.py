from celery import shared_task
from django.utils import timezone

from apps.daily.models import DailyChallenge

from .models import PushSubscription
from .views import send_push_notification


@shared_task
def send_daily_reminders():
    now = timezone.localtime()
    minute_start = max(now.minute - 2, 0)
    minute_end = min(now.minute + 2, 59)
    subscriptions = PushSubscription.objects.filter(
        is_active=True,
        user__userprofile__push_notifications_enabled=True,
        user__userprofile__reminder_time__hour=now.hour,
        user__userprofile__reminder_time__minute__range=(minute_start, minute_end),
    ).select_related("user")

    daily = DailyChallenge.objects.filter(date=now.date()).first()
    if daily is None:
        return 0

    sent = 0
    for subscription in subscriptions:
        sent += int(
            send_push_notification(
                subscription,
                title="Daily Highway Code Challenge",
                body="A new question is waiting for you. Keep your streak going.",
                url="/daily/",
            )
        )
    return sent
