from django.contrib import admin

from .models import Rule, RuleSection


@admin.register(RuleSection)
class RuleSectionAdmin(admin.ModelAdmin):
    list_display = ["order", "title", "slug", "source_url"]
    prepopulated_fields = {"slug": ("title",)}
    ordering = ["order"]


@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    list_display = ["rule_number", "title", "section", "updated_at"]
    list_filter = ["section"]
    search_fields = ["rule_number", "title", "content"]
