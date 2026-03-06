from rest_framework import viewsets, permissions, filters
from .models import (Ingredient, RecipeIngredient, SavedRecipeIngredient,
                     Unit, UnitKind)
from .serializers import (IngredientModelSerializer,
                          IngredientHyperlinkedSerializer,
                          UnitKindModelSerializer,
                          UnitKindHyperlinkedSerializer,
                          UnitModelSerializer,
                          UnitHyperlinkedSerializer,
                          RecipeIngredientModelSerializer,
                          RecipeIngredientHyperlinkedSerializer,
                          SavedRecipeIngredientModelSerializer,
                          SavedRecipeIngredientHyperlinkedSerializer)


class UnitKindModelViewSet(viewsets.ModelViewSet):
    queryset = UnitKind.objects.all().order_by("descriptive_name")
    serializer_class = UnitKindModelSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["label", "descriptive_name"]
    ordering_fields = ["label", "descriptive_name"]
    ordering = "label"


class UnitKindHyperlinkedViewSet(viewsets.ModelViewSet):
    queryset = UnitKind.objects.all().order_by("descriptive_name")
    serializer_class = UnitKindHyperlinkedSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["label", "descriptive_name"]
    ordering_fields = ["label", "descriptive_name"]
    ordering = "label"


class UnitModelViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.select_related("kind").all().order_by("name")
    serializer_class = UnitModelSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "symbol", "kind__label", "kind__descriptive_name"]
    ordering_fields = ["name", "symbol", "kind__descriptive_name"]
    ordering = "name"


class UnitHyperlinkedViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.select_related("kind").all().order_by("name")
    serializer_class = UnitHyperlinkedSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "symbol", "kind__label", "kind__descriptive_name"]
    ordering_fields = ["name", "symbol", "kind__descriptive_name"]
    ordering = "name"


class IngredientModelViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ingredients to be viewed or edited.
    """
    queryset = Ingredient.objects.all().order_by("name")
    serializer_class = IngredientModelSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = "name"


class IngredientHyperlinkedViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ingredients to be viewed or edited.
    """
    queryset = Ingredient.objects.all().order_by("name")
    serializer_class = IngredientHyperlinkedSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = "name"


class RecipeIngredientModelViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows recipe ingredients to be viewed or edited.
    """
    queryset = RecipeIngredient.objects.all().order_by("-recipe__published_at")
    serializer_class = RecipeIngredientModelSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["ingredient__name", "recipe__title", "unit__name"]
    ordering_fields = ["created_at", "updated_at", "recipe__published_at"]
    ordering = "created_at"


class RecipeIngredientHyperlinkedViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows recipe ingredients to be viewed or edited.
    """
    queryset = RecipeIngredient.objects.all().order_by("-recipe__published_at")
    serializer_class = RecipeIngredientHyperlinkedSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["ingredient__name", "recipe__title", "unit__name"]
    ordering_fields = ["created_at", "updated_at", "recipe__published_at"]
    ordering = "created_at"


class BaseSavedRecipeIngredientViewSet(viewsets.ModelViewSet):
    queryset = SavedRecipeIngredient.objects.all()
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["ingredient__name", "recipe__title", "unit__name"]
    ordering_fields = ["created_at", "updated_at"]
    ordering = "created_at"


class SavedRecipeIngredientModelViewSet(BaseSavedRecipeIngredientViewSet):
    serializer_class = SavedRecipeIngredientModelSerializer


class SavedRecipeIngredientHyperlinkedViewSet(
        BaseSavedRecipeIngredientViewSet):
    serializer_class = SavedRecipeIngredientHyperlinkedSerializer
