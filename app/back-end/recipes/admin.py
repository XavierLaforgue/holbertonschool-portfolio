from django.contrib import admin
from .models import Recipe, Difficulty, RecipeStatus
# Register your models here.

admin.site.register(Recipe)
admin.site.register(Difficulty)
admin.site.register(RecipeStatus)
