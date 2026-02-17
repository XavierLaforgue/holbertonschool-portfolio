from django.db import models
from core.models import UUIDModel
from accounts.models import Profile
# TODO: Create Anime model in the anime app
# from animes.models import Anime
from django.utils import timezone
# Create your models here.


class Difficulty(UUIDModel):
    label = models.TextField(blank=False, null=False, unique=True,
                             max_length=25)
    value = models.PositiveSmallIntegerField(blank=False, null=False,
                                             unique=True)


class Recipe_Status(UUIDModel):
    value = models.TextField(blank=False, null=False, unique=True,
                             max_length=25, default="Draft")


class Recipe(UUIDModel):
    owner = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="recipes",  # to do profile.recipes.all()
    )
    # anime = models.ForeignKey(
    #     Anime,
    #     # TODO: figure out what to use for on_delete when I don't want the
    #     # object to be deleted but perhaps some data in it to be rewritten.
    #     on_delete=models.????
    #     null=False,
    #     blank=False
    # )
    anime_custom = models.TextField(blank=False, null=False, max_length=150)
    title = models.TextField(blank=False, null=False, max_length=150)
    description = models.TextField(blank=False, null=False, max_length=500)
    # TODO: Figure out what to do in case of delete
    # on_delete=models.???,
    # difficulty = models.ForeignKey(
    #     Difficulty,
    #     # related_name="recipes",
    # )
    portions = models.PositiveSmallIntegerField(null=False, blank=False,
                                                default=1)
    preparation_time_minutes = models.PositiveSmallIntegerField(null=False,
                                                                blank=False)
    published_at = models.DateTimeField(blank=True, null=True,
                                        default=timezone.now())
