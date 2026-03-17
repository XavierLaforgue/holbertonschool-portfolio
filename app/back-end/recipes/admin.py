from django.contrib import admin
from .models import Recipe, RecipePhoto, Difficulty, RecipeStatus, SavedRecipe


@admin.register(Difficulty)
class DifficultyAdmin(admin.ModelAdmin):
    list_display = ('label', 'value', 'created_at', 'updated_at')
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = (
        ('Details', {
            'fields': ('id', 'label', 'value')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(RecipeStatus)
class RecipeStatusAdmin(admin.ModelAdmin):
    list_display = ('value', 'created_at', 'updated_at')
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = (
        ('Details', {
            'fields': ('id', 'value')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


class RecipePhotoInline(admin.TabularInline):
    model = RecipePhoto
    extra = 0  # show no extra blank RecipePhoto rows initially
    readonly_fields = ('id', 'created_at', 'updated_at')
    fields = ('position', 'image', 'created_at', 'updated_at')
    ordering = ('position',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_at', 'updated_at')
    readonly_fields = ('id', 'created_at', 'updated_at')
    inlines = [RecipePhotoInline]
    fieldsets = (
        ('Details', {
            'fields': ('id', 'title', 'author', 'anime_custom', 'description')
        }),
        ('Recipe Info', {
            'fields': ('difficulty', 'portions', 'estimated_time_minutes',
                       'status', 'published_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(SavedRecipe)
class SavedRecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'saver', 'created_at', 'updated_at')
    readonly_fields = ('id', 'created_at', 'updated_at', 'original_recipe',
                       'original_author', 'saved_at')
    fieldsets = (
        ('Details', {
            'fields': ('id', 'title', 'saver', 'anime_custom', 'description')
        }),
        ('Recipe Info', {
            'fields': ('difficulty', 'portions', 'estimated_time_minutes',
                       'status', 'published_at')
        }),
        ('Original', {
            'fields': ('original_recipe', 'original_author')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'saved_at')
        }),
    )


@admin.register(RecipePhoto)
class RecipePhotoAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'position',  # 'is_main',
                    'created_at')
    list_filter = ('position',)
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = (
        ('Details', {
            'fields': ('id', 'recipe', 'image', 'position')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
