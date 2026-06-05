from django.conf import settings
from django.db import models


class DailyChallenge(models.Model):
    question = models.ForeignKey("quiz.Question", on_delete=models.CASCADE)
    date = models.DateField(unique=True)
    fun_fact = models.TextField(blank=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"Daily challenge {self.date}"


class DailyChallengeResponse(models.Model):
    challenge = models.ForeignKey(DailyChallenge, on_delete=models.CASCADE, related_name="responses")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, blank=True)
    chosen_answer = models.ForeignKey("quiz.Answer", on_delete=models.SET_NULL, null=True)
    is_correct = models.BooleanField()
    answered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [
            ["challenge", "user"],
            ["challenge", "session_key"],
        ]
