import uuid

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from core.models import UUIDModel
from accounts.models import Profile
from recipes.validators import (validate_image_file_size,
                                validate_image_file_type)
# TODO: Create Anime model in the anime app
# from animes.models import Anime
# from django.utils import timezone


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
    estimated_time_minutes = models.PositiveSmallIntegerField(null=False,
                                                              blank=False)
    status = models.ForeignKey(
        RecipeStatus,
        on_delete=models.PROTECT,
        # Use a dynamic related_name so each concrete subclass
        # gets its own reverse accessor on RecipeStatus
        related_name="%(class)s_recipes",
        # null=True
    )
    published_at = models.DateTimeField(blank=True, null=True,
                                        default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta(UUIDModel.Meta):
        abstract = True


class Recipe(RecipeBase):
    author = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="authored_recipes",  # for profile.authored_recipes.all()
        # null=True
    )

    def __str__(self) -> str:
        return self.title


class SavedRecipe(RecipeBase):
    saver = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="saved_recipes",  # to do profile.saved_recipes.all()
        null=False,
        blank=False,
    )
    original_recipe = models.ForeignKey(
        Recipe,
        on_delete=models.SET_NULL,  # author can delete; snapshot stays
        null=True,
        blank=False,
        related_name="saved_copies",
        editable=False
    )
    original_author = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="authored_recipes_saved",
        editable=False
    )
    saved_at = models.DateTimeField(auto_now_add=True)


class StepBase(UUIDModel):
    number = models.PositiveSmallIntegerField(blank=False, null=False)
    description = models.TextField(blank=False, null=False, max_length=500)
    duration = models.DurationField(blank=True, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta(UUIDModel.Meta):
        abstract = True
        # default order_by() for all querysets: order with respect to recipe
        # and then to the step order
        ordering = ["recipe", "number"]


class Step(StepBase):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="steps",   # → recipe.steps.all()
    )

    class Meta(StepBase.Meta):
        verbose_name = "Step"
        verbose_name_plural = "Steps"
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "number"],
                name="unique_step_number_per_recipe",
            )
        ]

    def __str__(self):
        return f"{self.recipe.title}: step {self.number}"


class SavedStep(StepBase):
    recipe = models.ForeignKey(
        SavedRecipe,
        on_delete=models.CASCADE,
        related_name="steps",   # → recipe.steps.all()
    )

    class Meta(StepBase.Meta):
        verbose_name = "Saved step"
        verbose_name_plural = "Saved steps"
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "number"],
                name="unique_savedstep_order_per_savedrecipe",
            )
        ]

    def __str__(self):
        return f"{self.recipe.title}: step {self.number}"


def recipe_photo_upload_path(instance, filename):
    """Build upload path: recipes/<recipe_uuid>/<random_uuid>.<ext>

    Uses UUIDs for both directory and filename to:
    - avoid issues from user-provided names
    - keep a clean structure that maps directly to S3 key prefixes
    """
    import os
    ext = os.path.splitext(filename)[1].lower()
    # As it is not stored in the database the uuid of reference must be
    # created manually.
    return f"recipes/{instance.recipe_id}/{uuid.uuid4()}{ext}"


class RecipePhoto(UUIDModel):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="photos",
    )
    image = models.ImageField(
        upload_to=recipe_photo_upload_path,
        validators=[validate_image_file_size, validate_image_file_type],
    )
    position = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="1 = main image shown on card/feed; 2-5 = gallery images.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta(UUIDModel.Meta):
        ordering = ["recipe", "position"]
        verbose_name = "Recipe photo"
        verbose_name_plural = "Recipe photos"
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "position"],
                name="unique_photo_position_per_recipe",
            ),
            models.CheckConstraint(
                condition=models.Q(position__gte=1, position__lte=5),
                name="photo_position_between_1_and_5",
            ),
        ]

    # @property
    # def is_main(self):
    #     return self.position == 1

    def __str__(self):
        # label = "main" if self.is_main else f"#{self.position}"
        label = "main" if self.position == 1 else f"#{self.position}"
        return f"{self.recipe.title}: photo {label}"
