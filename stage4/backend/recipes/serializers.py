from rest_framework import serializers
from .models import Recipe, Ingredient, Step, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredients with name, amount, and units"""

    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'amount', 'units']
        read_only_fields = ['id']

    def validate_name(self, value):
        """Ensure ingredient name is not empty"""
        if not value or not value.strip():
            raise serializers.ValidationError("Ingredient name cannot be empty")
        return value.strip()


class StepSerializer(serializers.ModelSerializer):
    """Serializer for recipe steps with description and order"""

    class Meta:
        model = Step
        fields = ['id', 'description', 'order']
        read_only_fields = ['id']

    def validate_description(self, value):
        """Ensure step description is not empty"""
        if not value or not value.strip():
            raise serializers.ValidationError("Step description cannot be empty")
        return value.strip()


class RecipeListSerializer(serializers.ModelSerializer):
    """Simplified serializer for recipe lists"""
    author_username = serializers.CharField(source='author.username', read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description', 'image', 'rating',
            'author', 'author_username', 'anime', 'difficulty',
            'preparation_time', 'dietary_class', 'servings',
            'tags', 'created_at', 'is_published'
        ]
        read_only_fields = ['id', 'author', 'rating', 'created_at']


class RecipeDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for individual recipes with ingredients and steps"""
    author_username = serializers.CharField(source='author.username', read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)
    steps = StepSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description', 'image', 'rating',
            'author', 'author_username', 'ingredients', 'steps',
            'anime', 'difficulty', 'preparation_time', 'dietary_class',
            'servings', 'tags', 'created_at', 'updated_at', 'is_published'
        ]
        read_only_fields = ['id', 'author', 'rating', 'created_at', 'updated_at']


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating recipes"""

    class Meta:
        model = Recipe
        fields = [
            'title', 'description', 'image', 'anime', 'difficulty',
            'preparation_time', 'dietary_class', 'servings', 'is_published'
        ]

    def validate_title(self, value):
        """Validate title if provided"""
        if value and len(value.strip()) == 0:
            raise serializers.ValidationError("Title cannot be empty")
        return value
