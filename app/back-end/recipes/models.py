from django.db import models
from core.models import UUIDModel
from accounts.models import Profile
# TODO: Create Anime model in the anime app
# from animes.models import Anime
# from django.utils import timezone
# Create your models here.


class Difficulty(UUIDModel):
    label = models.CharField(blank=False, null=False, unique=True,
                             max_length=25)
    value = models.PositiveSmallIntegerField(blank=False, null=False,
                                             unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta(UUIDModel.Meta):
        verbose_name = "Difficulty"
        verbose_name_plural = "Degrees of difficulty"

    def __str__(self):
        return f"{self.label}"


class RecipeStatus(UUIDModel):
    value = models.CharField(blank=False, null=False, unique=True,
                             max_length=25, default="Draft")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.value}"

    class Meta(UUIDModel.Meta):
        verbose_name = "Recipe status"
        verbose_name_plural = "Recipe statuses"


class RecipeBase(UUIDModel):
    title = models.CharField(blank=False, null=False, max_length=150)
    # TODO: create Anime model (in the Animes app)
    # anime = models.ForeignKey(
    #     Anime,
    #     # TODO: figure out what to use for on_delete when I don't want the
    #     # object to be deleted but perhaps some data in it to be rewritten.
    #     on_delete=models.????
    #     null=False,
    #     blank=False
    # )
    anime_custom = models.CharField(blank=False, null=False, max_length=150)
    description = models.TextField(blank=True, null=True, max_length=500)
    difficulty = models.ForeignKey(
        Difficulty,
        on_delete=models.PROTECT,
        # Use a dynamic related_name so each concrete subclass
        # gets its own reverse accessor on Difficulty
        related_name="%(class)s_recipes",
        null=True,
    )
    portions = models.PositiveSmallIntegerField(null=False, blank=False,
                                                default=1)
    preparation_time_minutes = models.PositiveSmallIntegerField(null=False,
                                                                blank=False)
    status = models.ForeignKey(
        RecipeStatus,
        on_delete=models.PROTECT,
        # Use a dynamic related_name so each concrete subclass
        # gets its own reverse accessor on RecipeStatus
        related_name="%(class)s_recipes",
        null=True
    )
    published_at = models.DateTimeField(blank=True, null=True,
                                        default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # TODO: add RecipePhoto model

    class Meta(UUIDModel.Meta):
        abstract = True


class Recipe(RecipeBase):
    author = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="authored_recipes",  # for profile.authored_recipes.all()
        null=True
    )

    def __str__(self) -> str:
        return self.title


class SavedRecipe(RecipeBase):
    saver = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="saved_recipes",  # to do profile.saved_recipes.all()
    )
    original_recipe = models.ForeignKey(
        Recipe,
        on_delete=models.SET_NULL,  # author can delete; snapshot stays
        null=True,
        blank=True,
        related_name="saved_copies",
    )
    original_author = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="authored_recipes_saved",
        editable=False
    )
    saved_at = models.DateTimeField(auto_now_add=True)
