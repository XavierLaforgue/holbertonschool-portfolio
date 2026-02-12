from django.db import models
# to to use the abstract model with uuid instead
from core.models import UUIDModel
# to create a CustomUser with UUID4 as identifier instead of an int:
from django.contrib.auth.models import AbstractUser
# to add datetime information to model fields:
from django.utils import timezone
# to use uuid as identifier for the models:
import uuid
# to link models to the model used for authentication:
from django.conf import settings

# Create your models here.


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False)
    email = models.EmailField(unique=True, blank=False, null=False,
                              max_length=150)
    username = models.TextField(unique=True, blank=False, null=False,
                                max_length=150)
    # TODO: make sure this is updated each time the user requests an
    # authentication token, e.g.,
    #     user.last_auth_time = timezone.now()
    #     user.save(update_fields=["last_auth_time"])
    last_auth_time = models.DateTimeField(blank=True, null=True)
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # TODO: add avatar image field, perhaps with:
    # avatar = models.ImageField(
    #     upload_to='avatars/',
    #     default='avatars/default_avatar.png',
    #     blank=True, null=True)
    favorite_anime = models.TextField(blank=True, null=True, max_length=150)
    favorite_meal = models.TextField(blank=True, null=True, max_length=150)
    location = models.TextField(blank=True, null=True, max_length=150)
    my_anime_list_profile = models.URLField(blank=True, null=True,
                                            max_length=200)
    dietary_preferences = models.TextField(blank=True, null=True,
                                           max_length=100)

    def __str__(self) -> str:
        return self.user.username
