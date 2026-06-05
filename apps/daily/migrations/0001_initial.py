from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("quiz", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="DailyChallenge",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField(unique=True)),
                ("fun_fact", models.TextField(blank=True)),
                ("question", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="quiz.question")),
            ],
            options={"ordering": ["-date"]},
        ),
        migrations.CreateModel(
            name="DailyChallengeResponse",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("session_key", models.CharField(blank=True, max_length=40)),
                ("is_correct", models.BooleanField()),
                ("answered_at", models.DateTimeField(auto_now_add=True)),
                (
                    "challenge",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="responses", to="daily.dailychallenge"),
                ),
                (
                    "chosen_answer",
                    models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to="quiz.answer"),
                ),
                (
                    "user",
                    models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={"unique_together": {("challenge", "user"), ("challenge", "session_key")}},
        ),
    ]
