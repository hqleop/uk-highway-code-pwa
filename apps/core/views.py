from django.conf import settings
from django.http import FileResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_control

from apps.daily.models import DailyChallenge
from apps.quiz.models import Question
from apps.rules.models import Rule, RuleSection


def home(request):
    sections = RuleSection.objects.prefetch_related("rules")[:6]
    question_count = Question.objects.filter(is_active=True).count()
    rule_count = Rule.objects.count()
    daily = DailyChallenge.objects.select_related("question").first()
    return render(
        request,
        "core/home.html",
        {
            "sections": sections,
            "question_count": question_count,
            "rule_count": rule_count,
            "daily": daily,
        },
    )


def offline(request):
    return render(request, "core/offline.html")


@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
def serve_service_worker(request):
    return FileResponse(open(settings.BASE_DIR / "static" / "sw.js", "rb"), content_type="application/javascript")
