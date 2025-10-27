from django.urls import path
from .views import (
    RecipeListCreateView,
    RecipeDetailView,
    RecipeIngredientListCreateView,
    RecipeIngredientDetailView,
    RecipeStepListCreateView,
    RecipeStepDetailView
)


urlpatterns = [
    # Recipe endpoints
    path('recipes/', RecipeListCreateView.as_view(),
         name='recipes-list-create'),
    path('recipes/<uuid:pk>/', RecipeDetailView.as_view(),
         name='recipes-detail'),

    # Recipe ingredients endpoints
    path('recipes/<uuid:recipe_id>/ingredients/',
         RecipeIngredientListCreateView.as_view(),
         name='recipe-ingredients-list-create'),
    path('recipes/<uuid:recipe_id>/ingredients/<int:ingredient_id>/',
         RecipeIngredientDetailView.as_view(),
         name='recipe-ingredients-detail'),

    # Recipe steps endpoints
    path('recipes/<uuid:recipe_id>/steps/',
         RecipeStepListCreateView.as_view(),
         name='recipe-steps-list-create'),
    path('recipes/<uuid:recipe_id>/steps/<uuid:step_id>/',
         RecipeStepDetailView.as_view(),
         name='recipe-steps-detail'),
]
