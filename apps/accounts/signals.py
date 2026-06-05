from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserProfile


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        initials = (instance.first_name[:1] or instance.username[:1] or "U").upper()
        UserProfile.objects.create(user=instance, avatar_initial=initials)
