from .models import Difficulty, Recipe, SavedRecipe, RecipeStatus
from rest_framework import serializers


class BaseRecipeSerializer:
    class Meta:
        model = Recipe
        fields = "__all__"


class RecipeModelSerializer(BaseRecipeSerializer,
                            serializers.ModelSerializer):
    class Meta(BaseRecipeSerializer.Meta):
        pass


class RecipeHyperlinkedSerializer(BaseRecipeSerializer,
                                  serializers.HyperlinkedModelSerializer):
    class Meta(BaseRecipeSerializer.Meta):
        pass


class BaseSavedRecipeSerializer:
    class Meta:
        model = SavedRecipe
        fields = "__all__"


class SavedRecipeModelSerializer(BaseSavedRecipeSerializer,
                                 serializers.ModelSerializer):
    class Meta(BaseSavedRecipeSerializer.Meta):
        pass


class SavedRecipeHyperlinkedSerializer(BaseSavedRecipeSerializer,
                                       serializers.HyperlinkedModelSerializer):
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
