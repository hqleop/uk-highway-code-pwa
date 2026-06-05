import json

from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.http import require_POST

from apps.accounts.models import UserProfile
from apps.quiz.models import Answer, Question

from .models import DailyChallenge, DailyChallengeResponse


def today(request):
    challenge = get_or_create_today_challenge()
    existing = existing_response(request, challenge) if challenge else None
    return render(request, "daily/today.html", {"challenge": challenge, "existing": existing})


@require_POST
def answer(request):
    data = request.POST or json.loads(request.body or "{}")
    challenge = get_or_create_today_challenge()
    if challenge is None:
        return JsonResponse({"ok": False, "error": "No active questions are available."}, status=400)
    if existing_response(request, challenge):
        return JsonResponse({"ok": False, "error": "You have already answered today's challenge."}, status=409)

    chosen = Answer.objects.get(pk=data.get("answer_id"), question=challenge.question)
    response = DailyChallengeResponse.objects.create(
        challenge=challenge,
        user=request.user if request.user.is_authenticated else None,
        session_key=request.session.session_key,
        chosen_answer=chosen,
        is_correct=chosen.is_correct,
    )
    if request.user.is_authenticated:
        update_streak(request.user.userprofile)
    correct = challenge.question.answers.filter(is_correct=True).first()
    return JsonResponse(
        {
            "ok": True,
            "is_correct": response.is_correct,
            "correct_answer": correct.text if correct else "",
            "explanation": challenge.question.explanation,
            "fun_fact": challenge.fun_fact,
        }
    )


def get_or_create_today_challenge():
    today_date = timezone.localdate()
    challenge = DailyChallenge.objects.select_related("question").filter(date=today_date).first()
    if challenge:
        return challenge
    question = Question.objects.filter(is_active=True).order_by("?").first()
    if question is None:
        return None
    return DailyChallenge.objects.create(
        date=today_date,
        question=question,
        fun_fact="A few minutes of daily practice builds stronger road-rule recall.",
    )


def existing_response(request, challenge):
    query = DailyChallengeResponse.objects.filter(challenge=challenge)
    if request.user.is_authenticated:
        return query.filter(user=request.user).first()
    return query.filter(session_key=request.session.session_key).first()


def update_streak(profile: UserProfile):
    today_date = timezone.localdate()
    if profile.last_activity_date == today_date:
        return
    if profile.last_activity_date and (today_date - profile.last_activity_date).days == 1:
        profile.streak_days += 1
    else:
        profile.streak_days = 1
    profile.last_activity_date = today_date
    profile.save(update_fields=["streak_days", "last_activity_date"])
