from django.contrib import admin
from .models import Recipe, Difficulty, RecipeStatus, SavedRecipe
# Register your models here.

admin.site.register([
    Recipe,
    Difficulty,
    RecipeStatus,
    SavedRecipe
])
