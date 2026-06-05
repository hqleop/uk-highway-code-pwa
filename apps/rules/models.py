from django.db import models


class RuleSection(models.Model):
    """Highway Code section, for example 'Rules for pedestrians'."""

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    order = models.PositiveIntegerField(default=0)
    icon = models.CharField(max_length=50, blank=True)
    source_url = models.URLField()

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class Rule(models.Model):
    """Individual Highway Code rule or article."""

    section = models.ForeignKey(RuleSection, on_delete=models.CASCADE, related_name="rules")
    rule_number = models.CharField(max_length=10, blank=True)
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField()
    has_image = models.BooleanField(default=False)
    image = models.ImageField(upload_to="rules/", blank=True, null=True)
    source_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["section__order", "rule_number", "id"]

    def __str__(self):
        label = f"Rule {self.rule_number}" if self.rule_number else self.title
        return label or f"Rule #{self.pk}"
