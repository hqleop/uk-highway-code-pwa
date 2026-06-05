from django.contrib import admin

from .models import Answer, Question, QuizAnswer, QuizSession


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4
    min_num = 2


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["question_text_short", "category", "difficulty", "is_active"]
    list_filter = ["category", "difficulty", "is_active"]
    search_fields = ["question_text"]
    inlines = [AnswerInline]

    def question_text_short(self, obj):
        return obj.question_text[:80]


@admin.register(QuizSession)
class QuizSessionAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "category", "total_questions", "correct_answers", "completed"]
    list_filter = ["category", "completed"]


@admin.register(QuizAnswer)
class QuizAnswerAdmin(admin.ModelAdmin):
    list_display = ["session", "question", "chosen_answer", "is_correct", "answered_at"]
    list_filter = ["is_correct"]
