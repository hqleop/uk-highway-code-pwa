from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from apps.core.views import serve_service_worker


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls")),
    path("rules/", include("apps.rules.urls")),
    path("quiz/", include("apps.quiz.urls")),
    path("daily/", include("apps.daily.urls")),
    path("accounts/", include("apps.accounts.urls")),
    path("notifications/", include("apps.notifications.urls")),
    path("donate/", include("apps.donations.urls")),
    path("sw.js", serve_service_worker, name="service-worker"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
