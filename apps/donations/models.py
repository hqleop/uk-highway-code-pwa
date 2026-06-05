from django.db import models


class Charity(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "charities"

    def __str__(self):
        return self.name
