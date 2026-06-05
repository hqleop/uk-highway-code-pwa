import uuid

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("rules", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Question",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("theory", "Theory"),
                            ("hazard", "Hazard Perception"),
                            ("signs", "Road Signs"),
                            ("rules", "Highway Code"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "difficulty",
                    models.CharField(
                        choices=[("easy", "Easy"), ("medium", "Medium"), ("hard", "Hard")],
                        default="medium",
                        max_length=10,
                    ),
                ),
                ("question_text", models.TextField()),
                ("image", models.ImageField(blank=True, null=True, upload_to="questions/")),
                ("explanation", models.TextField(blank=True)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "rule",
                    models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="rules.rule"),
                ),
            ],
            options={"ordering": ["category", "difficulty", "id"]},
        ),
        migrations.CreateModel(
            name="QuizSession",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("session_key", models.CharField(blank=True, max_length=40)),
                ("category", models.CharField(blank=True, max_length=20)),
                ("total_questions", models.PositiveIntegerField()),
                ("correct_answers", models.PositiveIntegerField(default=0)),
                ("completed", models.BooleanField(default=False)),
                ("started_at", models.DateTimeField(auto_now_add=True)),
                ("finished_at", models.DateTimeField(blank=True, null=True)),
                (
                    "user",
                    models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Answer",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("text", models.CharField(max_length=500)),
                ("is_correct", models.BooleanField(default=False)),
                (
                    "question",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="answers", to="quiz.question"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="QuizAnswer",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("is_correct", models.BooleanField()),
                ("answered_at", models.DateTimeField(auto_now_add=True)),
                (
                    "chosen_answer",
                    models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to="quiz.answer"),
                ),
                (
                    "question",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="quiz.question"),
                ),
                (
                    "session",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="responses", to="quiz.quizsession"),
                ),
            ],
            options={"unique_together": {("session", "question")}},
        ),
    ]
