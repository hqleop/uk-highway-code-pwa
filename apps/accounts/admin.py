from django.contrib import admin

from .models import UserNote, UserProfile, UserProgress


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "push_notifications_enabled", "reminder_time", "streak_days"]
    list_filter = ["push_notifications_enabled"]


@admin.register(UserNote)
class UserNoteAdmin(admin.ModelAdmin):
    list_display = ["user", "rule", "updated_at"]
    search_fields = ["content", "rule__title", "rule__rule_number"]


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ["user", "section", "completed", "last_read_at"]
    list_filter = ["completed", "section"]
