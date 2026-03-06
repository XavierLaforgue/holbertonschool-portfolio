from .models import (Difficulty, Recipe, SavedRecipe, RecipeStatus,
                     Step, SavedStep)
from rest_framework import serializers
from accounts.serializers import ProfileSummarySerializer
from ingredients.models import RecipeIngredient, Ingredient, Unit, UnitKind


class BaseRecipeSerializer:
    class Meta:
        model = Recipe
        fields = "__all__"


class RecipeSummarySerializer(BaseRecipeSerializer,
                              serializers.ModelSerializer):
    """Compact recipe response with scalar references to related objects."""
    class Meta(BaseRecipeSerializer.Meta):
        pass


class RecipeSummaryHyperlinkedSerializer(
        BaseRecipeSerializer, serializers.HyperlinkedModelSerializer
        ):
    """Compact recipe response with URL references to related objects."""
    class Meta(BaseRecipeSerializer.Meta):
        pass


class BaseSavedRecipeSerializer:
    class Meta:
        model = SavedRecipe
        fields = "__all__"


class SavedRecipeSummarySerializer(BaseSavedRecipeSerializer,
                                   serializers.ModelSerializer):
    """Compact saved recipe response with scalar references to related
    objects."""
    class Meta(BaseSavedRecipeSerializer.Meta):
        pass


class SavedRecipeSummaryHyperlinkedSerializer(
        BaseSavedRecipeSerializer, serializers.HyperlinkedModelSerializer
        ):
    """Compact saved recipe response with URL references to related objects."""
    class Meta(BaseSavedRecipeSerializer.Meta):
        pass


class BaseDifficultySerializer:
    class Meta:
        model = Difficulty
        fields = "__all__"


class DifficultyModelSerializer(BaseDifficultySerializer,
                                serializers.ModelSerializer):
    class Meta(BaseDifficultySerializer.Meta):
        pass


class DifficultyHyperlinkedSerializer(BaseDifficultySerializer,
                                      serializers.HyperlinkedModelSerializer):
    class Meta(BaseDifficultySerializer.Meta):
        pass


class BaseRecipeStatusSerializer:
    class Meta:
        model = RecipeStatus
        fields = "__all__"


class RecipeStatusModelSerializer(BaseRecipeStatusSerializer,
                                  serializers.ModelSerializer):
    class Meta(BaseRecipeStatusSerializer.Meta):
        pass


class RecipeStatusHyperlinkedSerializer(
        BaseRecipeStatusSerializer,
        serializers.HyperlinkedModelSerializer):
    class Meta(BaseRecipeStatusSerializer.Meta):
        pass


class BaseStepSerializer:
    class Meta:
        model = Step
        fields = "__all__"


class StepModelSerializer(BaseStepSerializer,
                          serializers.ModelSerializer):
    class Meta(BaseStepSerializer.Meta):
        pass


class StepHyperlinkedSerializer(BaseStepSerializer,
                                serializers.HyperlinkedModelSerializer):
    class Meta(BaseStepSerializer.Meta):
        pass


class BaseSavedStepSerializer:
    class Meta:
        model = SavedStep
        fields = "__all__"


class SavedStepModelSerializer(BaseSavedStepSerializer,
                               serializers.ModelSerializer):
    class Meta(BaseSavedStepSerializer.Meta):
        pass


class SavedStepHyperlinkedSerializer(BaseSavedStepSerializer,
                                     serializers.HyperlinkedModelSerializer):
    class Meta(BaseSavedStepSerializer.Meta):
        pass


class UnitKindSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitKind
        fields = ("id", "label", "descriptive_name")


class UnitSummarySerializer(serializers.ModelSerializer):
    kind = UnitKindSummarySerializer(read_only=True)

    class Meta:
        model = Unit
        fields = ("id", "name", "symbol", "kind")


class IngredientSummarySerializer(serializers.ModelSerializer):
    allowed_unit_kinds = UnitKindSummarySerializer(many=True, read_only=True)

    class Meta:
        model = Ingredient
        fields = ("id", "name", "allowed_unit_kinds")


class RecipeIngredientExpandedSerializer(serializers.ModelSerializer):
    ingredient = IngredientSummarySerializer(read_only=True)
    unit = UnitSummarySerializer(read_only=True)

    class Meta:
        model = RecipeIngredient
        fields = (
            "id",
            "ingredient",
            "quantity",
            "unit",
            "created_at",
            "updated_at",
        )


class RecipeExpandedSerializer(serializers.ModelSerializer):
    """Recipe response with nested full objects for related resources."""
    author = ProfileSummarySerializer(read_only=True)
    difficulty = DifficultyModelSerializer(read_only=True)
    status = RecipeStatusModelSerializer(read_only=True)
    steps = StepModelSerializer(many=True, read_only=True)
    ingredients = RecipeIngredientExpandedSerializer(many=True,
                                                     read_only=True)

    class Meta:
        model = Recipe
        fields = "__all__"


class SavedRecipeExpandedSerializer(serializers.ModelSerializer):
    """Saved recipe response with nested full objects for related resources."""
    saver = ProfileSummarySerializer(read_only=True)
    original_author = ProfileSummarySerializer(read_only=True)
    difficulty = DifficultyModelSerializer(read_only=True)
    status = RecipeStatusModelSerializer(read_only=True)
    steps = SavedStepModelSerializer(many=True, read_only=True)

    class Meta:
        model = SavedRecipe
        fields = "__all__"
