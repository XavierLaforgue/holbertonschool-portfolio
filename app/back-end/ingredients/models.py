from django.db import models
from core.models import UUIDModel
from recipes.models import Recipe
# Create your models here.


class UnitKind(UUIDModel):
    label = models.CharField(max_length=10, unique=True)  # "weight",
    # "volume", "count"
    descriptive_name = models.CharField(max_length=50)    # "Weight",
    # "Volume", ...

    def __str__(self):
        return f"{self.descriptive_name}"


class Unit(UUIDModel):
    name = models.CharField(blank=False, null=False, max_length=15)
    symbol = models.CharField(blank=False, null=False, max_length=5)
    kind = models.ForeignKey(
        UnitKind,
        on_delete=models.PROTECT,  # PROTECT prevents deletion of the parent
        # (an instance of UnitKind) if any children exist
        related_name="units")

    def __str__(self):
        return f"{self.name}"


class Ingredient(UUIDModel):
    # TODO: add allowed units depending on the type of ingredient
    name = models.CharField(blank=False, null=False, max_length=50,
                            unique=True)
    allowed_unit_kinds = models.ManyToManyField(
        UnitKind,
        related_name="ingredients",
        blank=True)

    def __str__(self):
        return f"{self.name}"


class RecipeIngredient(UUIDModel):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="ingredients",  # to access the ingredient via
        # recipe.ingredients
        blank=False, null=False
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="in_recipe",
        blank=False, null=False
    )
    quantity = models.FloatField(blank=False, null=False)
    unit = models.ForeignKey(
        Unit,
        on_delete=models.PROTECT,
        related_name="recipe_ingredients",
        blank=False, null=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantity} {self.unit} of {self.ingredient}"

    def clean(self):
        """Ensure the chosen unit kind is allowed for this ingredient."""
        from django.core.exceptions import ValidationError

        if self.ingredient.id and self.unit.id:
            allowed_unit_kinds = self.ingredient.allowed_unit_kinds.all()
            # If no kinds are configured for the ingredient, treat it as
            # "all kinds allowed".
            if (
                allowed_unit_kinds.exists()
                and self.unit.kind not in allowed_unit_kinds
            ):
                raise ValidationError(
                    {"unit": "This unit kind is not allowed for the selected "
                        "ingredient."}
                )
