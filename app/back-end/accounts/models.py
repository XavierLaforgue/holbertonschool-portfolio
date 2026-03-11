from django.db import models
# to to use the abstract model with uuid instead
from core.models import UUIDModel
# from core.models import UUIDPkMixin
# to create a CustomUser with UUID4 as identifier instead of an int:
from django.contrib.auth.models import AbstractUser
# to link models to the model used for authentication:
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .validators import person_name_validator


# TODO: build a customuser manager to enforce constraints at all levels
# (admin, API, shell)


class CustomUser(
                 UUIDModel,
                 AbstractUser,
                 ):
    class Meta(UUIDModel.Meta):
        verbose_name = "user"
        verbose_name_plural = "users"
        constraints = [
            models.UniqueConstraint(
                fields=["email"],
                condition=models.Q(deleted_at__isnull=True),
                name="unique_active_email"
            )
        ]

    username = models.CharField(unique=True, blank=False, null=False,
                                max_length=150)
    email = models.EmailField(unique=True, blank=False, null=False,
                              max_length=150)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # for createsuperuser: only email + password
    # Optional, but when provided must look like a person name.
    first_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        validators=[person_name_validator],
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        validators=[person_name_validator],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deactivated_at = models.DateTimeField(blank=False, null=True,
                                          default=None)
    deleted_at = models.DateTimeField(blank=False, null=True, default=None)

    def __str__(self) -> str:
        return self.email


def default_display_name():
    n = 1
    while True:
        display_name = f"unnamed_user_{n}"
        if not Profile.objects.filter(display_name=display_name).first():
            return display_name
        n += 1


class Profile(UUIDModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                null=False,
                                blank=False)
    birth_date = models.DateField(blank=True, null=True, default=None)
    # TODO: make `display_name` nullable and let front-end replace other
    # user's `display_name` for `unnamed` and own's `display_name` for `email`
    display_name = models.CharField(blank=False, null=False,
                                    default=default_display_name,
                                    max_length=150,
                                    unique=True
                                    )
    bio = models.TextField(blank=True, null=True, default=None,
                           max_length=500)
    # TODO: add avatar image field, perhaps with:
    # avatar = models.ImageField(
    #     upload_to='avatars/',
    #     default='avatars/default_avatar.png',
    #     blank=True, null=True)
    favorite_anime_custom = models.CharField(blank=True, null=True,
                                             max_length=150)
    # TODO: Create a relationship with an anime entity that is replaced by a
    # simple text (the title of the anime it was related to) on delete
    # favorite_anime = models.ForeignKey(
    #   Anime,
    #   on_delete=models.PROTECT,
    #   related_name="favorites"
    # )
    favorite_meal = models.CharField(blank=True, null=True, max_length=150)
    location = models.CharField(blank=True, null=True, max_length=150)
    myAnimeList_profile = models.URLField(blank=True, null=True,
                                          max_length=200)
    dietary_preferences = models.TextField(blank=True, null=True,
                                           max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cleared_at = models.DateTimeField(blank=False, null=True, default=None)

    def __str__(self) -> str:
        return self.user.email


# receive signals of events of `CustomUser` instance being saved and create a
# profile for that new user
@receiver(post_save, sender=CustomUser)
def create_profile_for_new_user(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
