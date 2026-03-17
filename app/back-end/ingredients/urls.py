from django.urls import include, path
from rest_framework import routers
from .views import (IngredientModelViewSet,
                    IngredientHyperlinkedViewSet,
                    UnitKindModelViewSet,
                    UnitKindHyperlinkedViewSet,
                    UnitModelViewSet,
                    UnitHyperlinkedViewSet,
                    RecipeIngredientModelViewSet,
                    RecipeIngredientHyperlinkedViewSet,
                    SavedRecipeIngredientModelViewSet,
                    SavedRecipeIngredientHyperlinkedViewSet)

router = routers.DefaultRouter()
router.register(r"unitkind_models", UnitKindModelViewSet,
                basename="unitkind_model")
router.register(r"unitkind_hyperlinks", UnitKindHyperlinkedViewSet,
                basename="unitkind")
router.register(r"unit_models", UnitModelViewSet,
                basename="unit_model")
router.register(r"unit_hyperlinks", UnitHyperlinkedViewSet,
                basename="unit")
router.register(r"ingredient_models", IngredientModelViewSet,
                basename="ingredient_model")
router.register(r"ingredient_hyperlinks", IngredientHyperlinkedViewSet,
                basename="ingredient")
router.register(r"recipeingredient_models", RecipeIngredientModelViewSet,
                basename="recipeingredient_model")
router.register(r"recipeingredient_hyperlinks",
                RecipeIngredientHyperlinkedViewSet,
                basename="recipeingredient")
router.register(r"savedrecipeingredient_models",
                SavedRecipeIngredientModelViewSet,
                basename="savedrecipeingredient_model")
router.register(r"savedrecipeingredient_hyperlinks",
                SavedRecipeIngredientHyperlinkedViewSet,
                basename="savedrecipeingredient")

urlpatterns = [
    path("", include(router.urls))
]
