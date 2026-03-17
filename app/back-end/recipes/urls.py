from django.urls import include, path
from rest_framework import routers
from .views import (DifficultyModelViewSet,
                    DifficultyHyperlinkedViewSet,
                    RecipeModelViewSet,
                    RecipeHyperlinkedViewSet,
                    RecipePhotoListCreateAPIView,
                    RecipePhotoDetailAPIView,
                    RecipeStepListCreateSwapAPIView,
                    RecipeStepDetailAPIView,
                    SavedRecipeModelViewSet,
                    SavedRecipeHyperlinkedViewSet,
                    RecipeStatusModelViewSet,
                    RecipeStatusHyperlinkedViewSet,
                    StepModelViewSet,
                    StepHyperlinkedViewSet,
                    SavedStepModelViewSet,
                    SavedStepHyperlinkedViewSet)

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
router.register(r"step_models", StepModelViewSet,
                basename="step_model")
router.register(r"step_hyperlinks", StepHyperlinkedViewSet,
                basename="step")
router.register(r"savedstep_models", SavedStepModelViewSet,
                basename="savedstep_model")
router.register(r"savedstep_hyperlinks", SavedStepHyperlinkedViewSet,
                basename="savedstep")

urlpatterns = [
    path("<uuid:recipe_id>/steps/", RecipeStepListCreateSwapAPIView.as_view(),
         name="recipe-steps-list"),
    path("<uuid:recipe_id>/steps/<uuid:step_id>/",
         RecipeStepDetailAPIView.as_view(), name="recipe-steps-detail"),
    path("<uuid:recipe_id>/photos/",
         RecipePhotoListCreateAPIView.as_view(),
         name="recipe-photos-list"),
    path("<uuid:recipe_id>/photos/<uuid:photo_id>/",
         RecipePhotoDetailAPIView.as_view(),
         name="recipe-photos-detail"),
    path("", include(router.urls))
]
