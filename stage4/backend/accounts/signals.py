from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, CustomUser


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    # Don't auto-create profile during fixture loading (loaddata)
    if kwargs.get('raw', False):
        return

    if created:
        Profile.objects.create(user=instance)
