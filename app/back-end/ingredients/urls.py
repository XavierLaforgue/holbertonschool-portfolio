from django.urls import include, path
from rest_framework import routers
from .views import (IngredientModelViewSet,
                    IngredientHyperlinkedViewSet,
                    RecipeIngredientModelViewSet,
                    RecipeIngredientHyperlinkedViewSet)

router = routers.DefaultRouter()
router.register(r"ingredient_models", IngredientModelViewSet,
                basename="ingredient_model")
router.register(r"ingredient_hyperlinks", IngredientHyperlinkedViewSet,
                basename="ingredient")
router.register(r"recipeingredient_models", RecipeIngredientModelViewSet,
                basename="recipeingredient_model")
router.register(r"recipeingredient_hyperlinks",
                RecipeIngredientHyperlinkedViewSet,
                basename="recipeingredient")

urlpatterns = [
    path("", include(router.urls))
]
