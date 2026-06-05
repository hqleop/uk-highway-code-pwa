import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from pywebpush import WebPushException, webpush

from .models import PushSubscription


@login_required
@require_POST
def subscribe(request):
    data = json.loads(request.body or "{}")
    PushSubscription.objects.update_or_create(
        endpoint=data["endpoint"],
        defaults={
            "user": request.user,
            "p256dh": data["keys"]["p256dh"],
            "auth": data["keys"]["auth"],
            "is_active": True,
        },
    )
    request.user.userprofile.push_notifications_enabled = True
    request.user.userprofile.save(update_fields=["push_notifications_enabled"])
    return JsonResponse({"status": "subscribed"})


@login_required
@require_POST
def unsubscribe(request):
    data = json.loads(request.body or "{}")
    endpoint = data.get("endpoint")
    if endpoint:
        PushSubscription.objects.filter(user=request.user, endpoint=endpoint).update(is_active=False)
    return JsonResponse({"status": "unsubscribed"})


def send_push_notification(subscription, title, body, url="/daily/"):
    if not settings.VAPID_PRIVATE_KEY:
        return False
    try:
        webpush(
            subscription_info={
                "endpoint": subscription.endpoint,
                "keys": {"p256dh": subscription.p256dh, "auth": subscription.auth},
            },
            data=json.dumps({"title": title, "body": body, "url": url}),
            vapid_private_key=settings.VAPID_PRIVATE_KEY,
            vapid_claims={"sub": f"mailto:{settings.VAPID_EMAIL}"},
        )
        return True
    except WebPushException as exc:
        if "410" in str(exc):
            subscription.is_active = False
            subscription.save(update_fields=["is_active"])
        return False
