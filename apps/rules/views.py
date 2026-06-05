from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render

from apps.accounts.models import UserNote, UserProgress

from .models import Rule, RuleSection


def section_list(request):
    sections = RuleSection.objects.annotate(rule_total=Count("rules"))
    return render(request, "rules/section_list.html", {"sections": sections})


def section_detail(request, section_slug):
    section = get_object_or_404(RuleSection, slug=section_slug)
    rules = section.rules.all()
    progress = None
    read_ids = set()
    if request.user.is_authenticated:
        progress, _ = UserProgress.objects.get_or_create(user=request.user, section=section)
        read_ids = set(progress.rules_read.values_list("id", flat=True))
    return render(
        request,
        "rules/section_detail.html",
        {"section": section, "rules": rules, "progress": progress, "read_ids": read_ids},
    )


def rule_detail(request, section_slug, rule_number):
    rules = Rule.objects.select_related("section").filter(section__slug=section_slug)
    rule = rules.filter(rule_number=rule_number).first()
    if rule is None and str(rule_number).isdigit():
        rule = rules.filter(pk=rule_number).first()
    if rule is None:
        rule = get_object_or_404(rules, rule_number=rule_number)
    notes = []
    if request.user.is_authenticated:
        progress, _ = UserProgress.objects.get_or_create(user=request.user, section=rule.section)
        progress.rules_read.add(rule)
        progress.last_read_at = rule.updated_at
        progress.completed = progress.rules_read.count() >= rule.section.rules.count()
        progress.save(update_fields=["last_read_at", "completed"])
        notes = UserNote.objects.filter(user=request.user, rule=rule)
    return render(request, "rules/rule_detail.html", {"rule": rule, "notes": notes})


def search(request):
    query = request.GET.get("q", "").strip()
    results = Rule.objects.none()
    if query:
        results = Rule.objects.select_related("section").filter(
            Q(rule_number__icontains=query)
            | Q(title__icontains=query)
            | Q(content__icontains=query)
            | Q(section__title__icontains=query)
        )[:50]
    return render(request, "rules/search.html", {"query": query, "results": results})


@login_required
def my_notes(request):
    notes = UserNote.objects.filter(user=request.user).select_related("rule", "rule__section")
    return render(request, "rules/my_notes.html", {"notes": notes})
