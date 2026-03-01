from django.urls import include, path
from rest_framework import routers
from .views import (DifficultyModelViewSet,
                    DifficultyHyperlinkedViewSet,
                    RecipeModelViewSet,
                    RecipeHyperlinkedViewSet,
                    SavedRecipeModelViewSet,
                    SavedRecipeHyperlinkedViewSet,
                    RecipeStatusModelViewSet,
                    RecipeStatusHyperlinkedViewSet)

router = routers.DefaultRouter()
router.register(r"recipe_models", RecipeModelViewSet,
                basename="recipe_model")
router.register(r"recipe_hyperlinks", RecipeHyperlinkedViewSet,
                basename="recipe")
router.register(r"savedrecipe_models", SavedRecipeModelViewSet,
                basename="savedrecipe_model")
router.register(r"savedrecipe_hyperlinks", SavedRecipeHyperlinkedViewSet,
                basename="savedrecipe")
router.register(r"difficulty_models", DifficultyModelViewSet,
                basename="difficulty_model")
router.register(r"difficulty_hyperlinks", DifficultyHyperlinkedViewSet,
                basename="difficulty")
router.register(r"recipestatus_models", RecipeStatusModelViewSet,
                basename="recipestatus_model")
router.register(r"recipestatus_hyperlinks", RecipeStatusHyperlinkedViewSet,
                basename="recipestatus")

urlpatterns = [
    path("", include(router.urls))
]
