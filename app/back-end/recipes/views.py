from rest_framework import viewsets, permissions
from .models import Recipe, RecipeStatus, SavedRecipe, Difficulty
from .serializers import (RecipeModelSerializer,
                          RecipeHyperlinkedSerializer,
                          SavedRecipeModelSerializer,
                          SavedRecipeHyperlinkedSerializer,
                          DifficultyModelSerializer,
                          DifficultyHyperlinkedSerializer,
                          RecipeStatusModelSerializer,
                          RecipeStatusHyperlinkedSerializer)


class BaseRecipeViewSet(viewsets.ModelViewSet):
    """
    Shared behavior for recipe viewsets.
    """
    # TODO: filter published recipes and order by publication date
    queryset = Recipe.objects.all().order_by("-created_at")
    permission_classes = [permissions.AllowAny]


class RecipeModelViewSet(BaseRecipeViewSet):
    """
    API endpoint that allows recipes to be viewed or edited.
    """
    serializer_class = RecipeModelSerializer


class RecipeHyperlinkedViewSet(BaseRecipeViewSet):
    """
    API endpoint that allows recipes to be viewed or edited.
    """
    serializer_class = RecipeHyperlinkedSerializer


class BaseSavedRecipeViewSet(viewsets.ModelViewSet):
    """
    Shared behavior for saved recipe viewsets.
    """
    queryset = SavedRecipe.objects.all().order_by("-saved_at")
    permission_classes = [permissions.AllowAny]


class SavedRecipeModelViewSet(BaseSavedRecipeViewSet):
    """
    API endpoint that allows saved recipes to be viewed or edited.
    """
    serializer_class = SavedRecipeModelSerializer


class SavedRecipeHyperlinkedViewSet(BaseSavedRecipeViewSet):
    """
    API endpoint that allows recipe ingredients to be viewed or edited.
    """
    serializer_class = SavedRecipeHyperlinkedSerializer


class BaseDifficultyViewSet(viewsets.ModelViewSet):
    queryset = Difficulty.objects.all().order_by("value")
    permission_classes = [permissions.AllowAny]


class DifficultyModelViewSet(BaseDifficultyViewSet):
    serializer_class = DifficultyModelSerializer


class DifficultyHyperlinkedViewSet(BaseDifficultyViewSet):
    serializer_class = DifficultyHyperlinkedSerializer


class BaseRecipeStatusViewSet(viewsets.ModelViewSet):
    queryset = RecipeStatus.objects.all().order_by("value")
    permission_classes = [permissions.AllowAny]


class RecipeStatusModelViewSet(BaseRecipeStatusViewSet):
    serializer_class = RecipeStatusModelSerializer


class RecipeStatusHyperlinkedViewSet(BaseRecipeStatusViewSet):
    serializer_class = RecipeStatusHyperlinkedSerializer
