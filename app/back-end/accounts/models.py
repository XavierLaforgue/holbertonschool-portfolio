from django.db import models
# to to use the abstract model with uuid instead
from core.models import UUIDModel
# from core.models import UUIDPkMixin
# to create a CustomUser with UUID4 as identifier instead of an int:
from django.contrib.auth.models import AbstractUser
# to link models to the model used for authentication:
from django.conf import settings
import uuid

from .validators import person_name_validator

# Create your models here.


class CustomUser(
                 # UUIDPkMixin,
                 AbstractUser,
                 ):
    # TODO: Try again using the UUIDPkMixin with a clean database and no
    # migration files
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    username = models.TextField(unique=True, blank=False, null=False,
                                max_length=150)
    email = models.EmailField(unique=True, blank=False, null=False,
                              max_length=150)
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
    # TODO: make sure this is updated each time the user requests an
    # authentication token, e.g.,
    #     user.last_auth_time = timezone.now()
    #     user.save(update_fields=["last_auth_time"])
    last_authenticated_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deactivated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return self.username


class Profile(UUIDModel):
    # TODO: make it so it is created when the associated user is created. This
    # will be included in the user creation logic.
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4,
    #                      editable=False)
    # TODO: add automatic numbering to unnamed users display names and add
    # unique constraint.
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                null=False,
                                blank=False)
    birth_date = models.DateField(blank=True, null=True, default=None)
    display_name = models.TextField(blank=False, null=False,
                                    default="unnamed_user_#",
                                    max_length=150,
                                    # unique=True
                                    )
    bio = models.TextField(blank=True, null=True, default=None,
                           max_length=500)
    # TODO: add avatar image field, perhaps with:
    # avatar = models.ImageField(
    #     upload_to='avatars/',
    #     default='avatars/default_avatar.png',
    #     blank=True, null=True)
    favorite_anime_custom = models.TextField(blank=True, null=True,
                                             max_length=150)
    # TODO: Create a relationship with an anime entity that is replaced by a
    # simple text (the title of the anime it was related to) on delete
    # favorite_anime = models.OneToOneField(Anime, on_delete=???)
    favorite_meal = models.TextField(blank=True, null=True, max_length=150)
    location = models.TextField(blank=True, null=True, max_length=150)
    myAnimeList_profile = models.URLField(blank=True, null=True,
                                          max_length=200)
    dietary_preferences = models.TextField(blank=True, null=True,
                                           max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cleared_at = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return self.user.username
