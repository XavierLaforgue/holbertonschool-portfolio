from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404

from .models import Recipe, Ingredient, Step
from .serializers import (
    RecipeListSerializer,
    RecipeDetailSerializer,
    RecipeCreateUpdateSerializer,
    IngredientSerializer,
    StepSerializer
)


class IsRecipeAuthor(BasePermission):
    """Permission class to check if user is the recipe author"""

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for published recipes
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return obj.is_published or obj.author == request.user
        # Write permissions only for recipe author
        return obj.author == request.user


class RecipeListCreateView(generics.ListCreateAPIView):
    """
    List all published recipes or create a new recipe.
    GET: List all published recipes (public)
    POST: Create a new recipe (authenticated users only)
    """
    queryset = Recipe.objects.filter(is_published=True).order_by('-created_at')
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RecipeCreateUpdateSerializer
        return RecipeListSerializer

    @swagger_auto_schema(
        tags=['Recipes'],
        operation_summary='List all published recipes'
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Recipes'],
        operation_summary='Create a new recipe',
        request_body=RecipeCreateUpdateSerializer
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Set the author to the current user when creating a recipe"""
        serializer.save(author=self.request.user)


class RecipeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a recipe.
    GET: Get recipe details (public if published)
    PUT/PATCH: Update recipe (author only)
    DELETE: Delete recipe (author only)
    """
    queryset = Recipe.objects.all()
    lookup_field = 'pk'
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get_permissions(self):
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return [AllowAny()]
        return [IsAuthenticated(), IsRecipeAuthor()]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return RecipeCreateUpdateSerializer
        return RecipeDetailSerializer

    @swagger_auto_schema(
        tags=['Recipes'],
        operation_summary='Get recipe details'
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Recipes'],
        operation_summary='Update recipe (full update)',
        request_body=RecipeCreateUpdateSerializer
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Recipes'],
        operation_summary='Partial update recipe',
        request_body=RecipeCreateUpdateSerializer
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Recipes'],
        operation_summary='Delete recipe'
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class RecipeIngredientListCreateView(generics.ListCreateAPIView):
    """
    List ingredients for a recipe or add a new ingredient.
    GET: List all ingredients for a recipe
    POST: Add a new ingredient to a recipe
    """
    serializer_class = IngredientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Get ingredients for a specific recipe"""
        recipe_id = self.kwargs.get('recipe_id')
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        return recipe.ingredients.all()

    @swagger_auto_schema(
        tags=['Recipe Ingredients'],
        operation_summary='List ingredients for a recipe'
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Recipe Ingredients'],
        operation_summary='Add ingredient to recipe',
        request_body=IngredientSerializer
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Add ingredient to the recipe"""
        recipe_id = self.kwargs.get('recipe_id')
        recipe = get_object_or_404(Recipe, pk=recipe_id)

        # Check if user is the recipe author
        if recipe.author != self.request.user:
            raise PermissionError("You don't have permission to modify this recipe")

        # Create or get ingredient
        ingredient = serializer.save()
        recipe.ingredients.add(ingredient)


class RecipeIngredientDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or remove an ingredient from a recipe.
    GET: Get ingredient details
    PUT/PATCH: Update ingredient
    DELETE: Remove ingredient from recipe
    """
    serializer_class = IngredientSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
    lookup_url_kwarg = 'ingredient_id'

    def get_queryset(self):
        """Get ingredients for a specific recipe"""
        recipe_id = self.kwargs.get('recipe_id')
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        return recipe.ingredients.all()

    @swagger_auto_schema(
        tags=['Recipe Ingredients'],
        operation_summary='Get ingredient details'
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Recipe Ingredients'],
        operation_summary='Update ingredient',
        request_body=IngredientSerializer
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Recipe Ingredients'],
        operation_summary='Partial update ingredient',
        request_body=IngredientSerializer
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Recipe Ingredients'],
        operation_summary='Remove ingredient from recipe'
    )
    def delete(self, request, *args, **kwargs):
        """Remove ingredient from the recipe"""
        recipe_id = self.kwargs.get('recipe_id')
        recipe = get_object_or_404(Recipe, pk=recipe_id)

        # Check if user is the recipe author
        if recipe.author != self.request.user:
            return Response(
                {"detail": "You don't have permission to modify this recipe"},
                status=status.HTTP_403_FORBIDDEN
            )

        ingredient = self.get_object()
        recipe.ingredients.remove(ingredient)

        return Response(
            {"detail": "Ingredient removed from recipe"},
            status=status.HTTP_204_NO_CONTENT
        )


class RecipeStepListCreateView(generics.ListCreateAPIView):
    """
    List steps for a recipe or add a new step.
    GET: List all steps for a recipe (ordered)
    POST: Add a new step to a recipe
    """
    serializer_class = StepSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Get steps for a specific recipe, ordered by step number"""
        recipe_id = self.kwargs.get('recipe_id')
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        return recipe.steps.all().order_by('order')

    @swagger_auto_schema(
        tags=['Recipe Steps'],
        operation_summary='List steps for a recipe'
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Recipe Steps'],
        operation_summary='Add step to recipe',
        request_body=StepSerializer
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Add step to the recipe"""
        recipe_id = self.kwargs.get('recipe_id')
        recipe = get_object_or_404(Recipe, pk=recipe_id)

        # Check if user is the recipe author
        if recipe.author != self.request.user:
            raise PermissionError("You don't have permission to modify this recipe")

        # Create step and add to recipe
        step = serializer.save()
        recipe.steps.add(step)


class RecipeStepDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or remove a step from a recipe.
    GET: Get step details
    PUT/PATCH: Update step
    DELETE: Remove step from recipe
    """
    serializer_class = StepSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
    lookup_url_kwarg = 'step_id'

    def get_queryset(self):
        """Get steps for a specific recipe"""
        recipe_id = self.kwargs.get('recipe_id')
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        return recipe.steps.all()

    @swagger_auto_schema(
        tags=['Recipe Steps'],
        operation_summary='Get step details'
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Recipe Steps'],
        operation_summary='Update step',
        request_body=StepSerializer
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Recipe Steps'],
        operation_summary='Partial update step',
        request_body=StepSerializer
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Recipe Steps'],
        operation_summary='Remove step from recipe'
    )
    def delete(self, request, *args, **kwargs):
        """Remove step from the recipe"""
        recipe_id = self.kwargs.get('recipe_id')
        recipe = get_object_or_404(Recipe, pk=recipe_id)

        # Check if user is the recipe author
        if recipe.author != self.request.user:
            return Response(
                {"detail": "You don't have permission to modify this recipe"},
                status=status.HTTP_403_FORBIDDEN
            )

        step = self.get_object()
        recipe.steps.remove(step)

        return Response(
            {"detail": "Step removed from recipe"},
            status=status.HTTP_204_NO_CONTENT
        )
