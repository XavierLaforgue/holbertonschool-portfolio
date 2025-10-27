from django.db import models
from django.conf import settings

# Create your models here.

import uuid
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False)
    email = models.EmailField(unique=True)


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    bio = models.TextField(blank=True, null=True, max_length=300)
    avatar = models.ImageField(
        upload_to='avatars/',
        default='avatars/default_avatar.png',
        blank=True, null=True)
    favorite_anime = models.TextField(blank=True, null=True, max_length=100)
    favorite_meal = models.TextField(blank=True, null=True, max_length=100)
    location = models.TextField(blank=True, null=True, max_length=85)
    personal_website = models.TextField(blank=True, null=True, max_length=100)
    dietary_preferences = models.TextField(blank=True, null=True,
                                           max_length=100)

    def __str__(self):
        return self.user.username
