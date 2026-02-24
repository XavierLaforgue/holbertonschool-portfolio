from django.contrib import admin
from .models import UnitKind, Unit, Ingredient, RecipeIngredient
# Register your models here.

admin.site.register([
    UnitKind,
    Unit,
    Ingredient,
    RecipeIngredient
    ])
