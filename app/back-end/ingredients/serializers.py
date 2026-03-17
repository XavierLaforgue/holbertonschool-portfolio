from .models import (Ingredient, RecipeIngredient, SavedRecipeIngredient,
                     Unit, UnitKind)
from rest_framework import serializers


class BaseUnitKindSerializer:
    class Meta:
        model = UnitKind
        fields = "__all__"


class UnitKindModelSerializer(BaseUnitKindSerializer,
                              serializers.ModelSerializer):
    class Meta(BaseUnitKindSerializer.Meta):
        pass


class UnitKindHyperlinkedSerializer(
        BaseUnitKindSerializer,
        serializers.HyperlinkedModelSerializer):
    class Meta(BaseUnitKindSerializer.Meta):
        pass


class BaseUnitSerializer:
    class Meta:
        model = Unit
        fields = "__all__"


class UnitModelSerializer(BaseUnitSerializer,
                          serializers.ModelSerializer):
    class Meta(BaseUnitSerializer.Meta):
        pass


class UnitHyperlinkedSerializer(
        BaseUnitSerializer,
        serializers.HyperlinkedModelSerializer):
    class Meta(BaseUnitSerializer.Meta):
        pass


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


class BaseSavedRecipeIngredientSerializer:
    class Meta:
        model = SavedRecipeIngredient
        fields = "__all__"


class SavedRecipeIngredientModelSerializer(
        BaseSavedRecipeIngredientSerializer,
        serializers.ModelSerializer):
    class Meta(BaseSavedRecipeIngredientSerializer.Meta):
        pass


class SavedRecipeIngredientHyperlinkedSerializer(
        BaseSavedRecipeIngredientSerializer,
        serializers.HyperlinkedModelSerializer):
    class Meta(BaseSavedRecipeIngredientSerializer.Meta):
        pass
