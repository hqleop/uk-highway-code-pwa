import os

import django
from django.core.management import call_command


_has_run = False


def run_startup_tasks():
    """Run idempotent startup tasks for Render services without a pre-deploy command."""
    global _has_run
    if _has_run:
        return
    if os.environ.get("RUN_MIGRATIONS_ON_START", "true").lower() in {"0", "false", "no"}:
        _has_run = True
        return

    django.setup()
    call_command("migrate", interactive=False, verbosity=1)
    call_command("seed_quiz", verbosity=0)
    ensure_highway_code_data()
    generate_quiz_from_rules_if_needed()
    _has_run = True


def ensure_highway_code_data():
    from apps.rules.models import RuleSection

    min_sections = int(os.environ.get("MIN_HIGHWAY_CODE_SECTIONS", "20"))
    if RuleSection.objects.count() >= min_sections:
        return

    if os.environ.get("LOAD_HIGHWAY_CODE_FIXTURES", "true").lower() not in {"0", "false", "no"}:
        call_command("loaddata", "highway_code_full", verbosity=1)
        call_command("loaddata", "highway_code_quiz", verbosity=1)
        if RuleSection.objects.count() >= min_sections:
            return

    limit = os.environ.get("IMPORT_HIGHWAY_CODE_LIMIT", "").strip()
    command_kwargs = {"verbosity": 1}
    if limit:
        command_kwargs["limit_sections"] = int(limit)
    call_command("import_highway_code", **command_kwargs)


def generate_quiz_from_rules_if_needed():
    from apps.quiz.models import Question
    from apps.rules.models import Rule

    rules_count = Rule.objects.count()
    generated_count = Question.objects.filter(rule__isnull=False).count()
    if rules_count == 0 or generated_count >= rules_count:
        return

    call_command("generate_quiz_from_rules", verbosity=1)
