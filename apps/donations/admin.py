from django.contrib import admin

from .models import Charity


@admin.register(Charity)
class CharityAdmin(admin.ModelAdmin):
    list_display = ["order", "name", "url", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name", "description"]
