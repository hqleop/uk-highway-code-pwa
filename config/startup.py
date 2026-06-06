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
    _has_run = True
