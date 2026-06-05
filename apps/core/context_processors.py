from django.conf import settings


def pwa_settings(request):
    return {
        "PWA_MANIFEST_URL": settings.PWA_MANIFEST_URL,
        "VAPID_PUBLIC_KEY": settings.VAPID_PUBLIC_KEY,
    }
