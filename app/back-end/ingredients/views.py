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


class UnitKindBaseViewSet(viewsets.ModelViewSet):
    queryset = UnitKind.objects.all()
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["label", "descriptive_name"]
    ordering_fields = ["label", "descriptive_name"]
    ordering = "label"


class UnitKindModelViewSet(UnitKindBaseViewSet):
    serializer_class = UnitKindModelSerializer


class UnitKindHyperlinkedViewSet(UnitKindBaseViewSet):
    serializer_class = UnitKindHyperlinkedSerializer


class UnitBaseViewSet(viewsets.ModelViewSet):
    # sectec_related perfomrs a JOIN with the related table
    queryset = Unit.objects.select_related("kind").all()
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "symbol", "kind__label", "kind__descriptive_name"]
    ordering_fields = ["name", "symbol", "kind__descriptive_name"]
    ordering = "name"


class UnitModelViewSet(UnitBaseViewSet):
    serializer_class = UnitModelSerializer


class UnitHyperlinkedViewSet(viewsets.ModelViewSet):
    serializer_class = UnitHyperlinkedSerializer


class IngredientBaseViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = "name"

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class IngredientModelViewSet(IngredientBaseViewSet):
    """
    API endpoint that allows ingredients to be viewed or edited.
    """
    serializer_class = IngredientModelSerializer


class IngredientHyperlinkedViewSet(IngredientBaseViewSet):
    """
    API endpoint that allows ingredients to be viewed or edited.
    """
    serializer_class = IngredientHyperlinkedSerializer


class RecipeIngredientBaseViewSet(viewsets.ModelViewSet):
    queryset = RecipeIngredient.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["ingredient__name", "recipe__title", "unit__name"]
    ordering_fields = ["created_at", "updated_at", "recipe__published_at"]
    ordering = ["-recipe__published_at", "-created_at"]

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class RecipeIngredientModelViewSet(RecipeIngredientBaseViewSet):
    """
    API endpoint that allows recipe ingredients to be viewed or edited.
    """
    serializer_class = RecipeIngredientModelSerializer


class RecipeIngredientHyperlinkedViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows recipe ingredients to be viewed or edited.
    """
    serializer_class = RecipeIngredientHyperlinkedSerializer


class BaseSavedRecipeIngredientViewSet(viewsets.ModelViewSet):
    queryset = SavedRecipeIngredient.objects.all()
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["ingredient__name", "recipe__title", "unit__name"]
    ordering_fields = ["created_at", "updated_at", "recipe__saved_at"]
    ordering = ["-recipe__saved_at", "-created_at"]


class SavedRecipeIngredientModelViewSet(BaseSavedRecipeIngredientViewSet):
    serializer_class = SavedRecipeIngredientModelSerializer


class SavedRecipeIngredientHyperlinkedViewSet(
        BaseSavedRecipeIngredientViewSet):
    serializer_class = SavedRecipeIngredientHyperlinkedSerializer
