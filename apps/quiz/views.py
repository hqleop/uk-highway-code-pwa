import json

from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Answer, Question, QuizAnswer, QuizSession


def quiz_home(request):
    categories = (
        Question.objects.filter(is_active=True)
        .values("category")
        .annotate(total=Count("id"))
        .order_by("category")
    )
    return render(request, "quiz/home.html", {"categories": categories})


@require_POST
def start(request):
    category = request.POST.get("category", "")
    total = int(request.POST.get("total_questions") or 10)
    total = max(1, min(total, 50))
    questions = Question.objects.filter(is_active=True)
    if category:
        questions = questions.filter(category=category)
    selected_ids = list(questions.order_by("?").values_list("id", flat=True)[:total])
    if not selected_ids:
        return JsonResponse({"ok": False, "error": "No active questions are available."}, status=400)

    quiz = QuizSession.objects.create(
        user=request.user if request.user.is_authenticated else None,
        session_key=request.session.session_key,
        category=category,
        total_questions=len(selected_ids),
    )
    request.session[f"quiz_questions_{quiz.id}"] = selected_ids
    first = serialize_question(Question.objects.get(pk=selected_ids[0]))
    return JsonResponse(
        {"ok": True, "session_id": str(quiz.id), "redirect_url": f"/quiz/session/{quiz.id}/", "question": first}
    )


def session(request, session_id):
    quiz = get_object_or_404(QuizSession, pk=session_id)
    question_ids = request.session.get(f"quiz_questions_{quiz.id}", [])
    answered_ids = set(quiz.responses.values_list("question_id", flat=True))
    next_id = next((qid for qid in question_ids if qid not in answered_ids), None)
    question = Question.objects.prefetch_related("answers").filter(pk=next_id).first() if next_id else None
    if question is None and not quiz.completed:
        quiz.completed = True
        quiz.finished_at = timezone.now()
        quiz.save(update_fields=["completed", "finished_at"])
    return render(request, "quiz/session.html", {"quiz": quiz, "question": question})


@require_POST
def answer(request):
    data = request.POST or json.loads(request.body or "{}")
    quiz = get_object_or_404(QuizSession, pk=data.get("session_id"))
    question = get_object_or_404(Question, pk=data.get("question_id"))
    chosen = get_object_or_404(Answer, pk=data.get("answer_id"), question=question)

    response, created = QuizAnswer.objects.get_or_create(
        session=quiz,
        question=question,
        defaults={"chosen_answer": chosen, "is_correct": chosen.is_correct},
    )
    if created and chosen.is_correct:
        quiz.correct_answers += 1
        quiz.save(update_fields=["correct_answers"])

    question_ids = request.session.get(f"quiz_questions_{quiz.id}", [])
    answered_ids = set(quiz.responses.values_list("question_id", flat=True))
    next_id = next((qid for qid in question_ids if qid not in answered_ids), None)
    if next_id is None:
        quiz.completed = True
        quiz.finished_at = timezone.now()
        quiz.save(update_fields=["completed", "finished_at"])

    correct = question.answers.filter(is_correct=True).first()
    return JsonResponse(
        {
            "ok": True,
            "is_correct": response.is_correct,
            "correct_answer": correct.text if correct else "",
            "explanation": question.explanation,
            "completed": quiz.completed,
            "results_url": f"/quiz/results/{quiz.id}/",
            "next_question": serialize_question(Question.objects.get(pk=next_id)) if next_id else None,
        }
    )


def results(request, session_id):
    quiz = get_object_or_404(QuizSession, pk=session_id)
    responses = quiz.responses.select_related("question", "chosen_answer")
    score = round((quiz.correct_answers / quiz.total_questions) * 100) if quiz.total_questions else 0
    return render(request, "quiz/results.html", {"quiz": quiz, "responses": responses, "score": score})


def serialize_question(question):
    return {
        "id": question.id,
        "text": question.question_text,
        "category": question.category,
        "difficulty": question.difficulty,
        "answers": [{"id": answer.id, "text": answer.text} for answer in question.answers.all()],
    }
