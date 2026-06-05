from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="RuleSection",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=255)),
                ("slug", models.SlugField(unique=True)),
                ("order", models.PositiveIntegerField(default=0)),
                ("icon", models.CharField(blank=True, max_length=50)),
                ("source_url", models.URLField()),
            ],
            options={"ordering": ["order"]},
        ),
        migrations.CreateModel(
            name="Rule",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("rule_number", models.CharField(blank=True, max_length=10)),
                ("title", models.CharField(blank=True, max_length=255)),
                ("content", models.TextField()),
                ("has_image", models.BooleanField(default=False)),
                ("image", models.ImageField(blank=True, null=True, upload_to="rules/")),
                ("source_url", models.URLField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "section",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="rules", to="rules.rulesection"),
                ),
            ],
            options={"ordering": ["section__order", "rule_number", "id"]},
        ),
    ]
