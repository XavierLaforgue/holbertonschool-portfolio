from rest_framework import viewsets, permissions
from .models import Ingredient, RecipeIngredient, SavedRecipeIngredient
from .serializers import (IngredientModelSerializer,
                          IngredientHyperlinkedSerializer,
                          RecipeIngredientModelSerializer,
                          RecipeIngredientHyperlinkedSerializer,
                          SavedRecipeIngredientModelSerializer,
                          SavedRecipeIngredientHyperlinkedSerializer)


class IngredientModelViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ingredients to be viewed or edited.
    """
    queryset = Ingredient.objects.all().order_by("name")
    serializer_class = IngredientModelSerializer
    permission_classes = [permissions.AllowAny]


class IngredientHyperlinkedViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ingredients to be viewed or edited.
    """
    queryset = Ingredient.objects.all().order_by("name")
    serializer_class = IngredientHyperlinkedSerializer
    permission_classes = [permissions.AllowAny]


class RecipeIngredientModelViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows recipe ingredients to be viewed or edited.
    """
    queryset = RecipeIngredient.objects.all().order_by("-recipe__published_at")
    serializer_class = RecipeIngredientModelSerializer
    permission_classes = [permissions.AllowAny]


class RecipeIngredientHyperlinkedViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows recipe ingredients to be viewed or edited.
    """
    queryset = RecipeIngredient.objects.all().order_by("-recipe__published_at")
    serializer_class = RecipeIngredientHyperlinkedSerializer
    permission_classes = [permissions.AllowAny]


class BaseSavedRecipeIngredientViewSet(viewsets.ModelViewSet):
    queryset = SavedRecipeIngredient.objects.all()
    permission_classes = [permissions.AllowAny]


class SavedRecipeIngredientModelViewSet(BaseSavedRecipeIngredientViewSet):
    serializer_class = SavedRecipeIngredientModelSerializer


class SavedRecipeIngredientHyperlinkedViewSet(
        BaseSavedRecipeIngredientViewSet):
    serializer_class = SavedRecipeIngredientHyperlinkedSerializer
