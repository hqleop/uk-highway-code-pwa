from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    push_notifications_enabled = models.BooleanField(default=False)
    reminder_time = models.TimeField(default="19:00")
    streak_days = models.PositiveIntegerField(default=0)
    last_activity_date = models.DateField(null=True, blank=True)
    avatar_initial = models.CharField(max_length=2, blank=True)

    def __str__(self):
        return f"{self.user} profile"


class UserNote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rule = models.ForeignKey("rules.Rule", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"Note by {self.user} on {self.rule}"


class UserProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    section = models.ForeignKey("rules.RuleSection", on_delete=models.CASCADE)
    rules_read = models.ManyToManyField("rules.Rule", blank=True)
    completed = models.BooleanField(default=False)
    last_read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ["user", "section"]

    def __str__(self):
        return f"{self.user} - {self.section}"
