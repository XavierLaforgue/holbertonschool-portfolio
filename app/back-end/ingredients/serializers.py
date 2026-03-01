from .models import Ingredient, RecipeIngredient
from rest_framework import serializers


class BaseIngredientSerializer:
    class Meta:
        model = Ingredient
        fields = "__all__"


class IngredientModelSerializer(BaseIngredientSerializer,
                                serializers.ModelSerializer):
    class Meta(BaseIngredientSerializer.Meta):
        pass


class IngredientHyperlinkedSerializer(
        BaseIngredientSerializer,
        serializers.HyperlinkedModelSerializer):
    class Meta(BaseIngredientSerializer.Meta):
        pass


class BaseRecipeIngredientSerializer:
    class Meta:
        model = RecipeIngredient
        fields = "__all__"


class RecipeIngredientHyperlinkedSerializer(
        BaseRecipeIngredientSerializer,
        serializers.HyperlinkedModelSerializer):
    class Meta(BaseRecipeIngredientSerializer.Meta):
        pass


class RecipeIngredientModelSerializer(
        BaseRecipeIngredientSerializer,
        serializers.ModelSerializer):
    class Meta(BaseRecipeIngredientSerializer.Meta):
        pass
