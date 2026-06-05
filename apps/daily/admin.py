from django.contrib import admin

from .models import DailyChallenge, DailyChallengeResponse


@admin.register(DailyChallenge)
class DailyChallengeAdmin(admin.ModelAdmin):
    list_display = ["date", "question", "fun_fact"]
    date_hierarchy = "date"


@admin.register(DailyChallengeResponse)
class DailyChallengeResponseAdmin(admin.ModelAdmin):
    list_display = ["challenge", "user", "session_key", "chosen_answer", "is_correct", "answered_at"]
    list_filter = ["is_correct", "challenge__date"]
