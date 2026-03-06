from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from .models import (Recipe, RecipeStatus, SavedRecipe, Difficulty, Step,
                     SavedStep)
from .serializers import (RecipeModelSerializer,
                          RecipeHyperlinkedSerializer,
                          SavedRecipeModelSerializer,
                          SavedRecipeHyperlinkedSerializer,
                          DifficultyModelSerializer,
                          DifficultyHyperlinkedSerializer,
                          RecipeStatusModelSerializer,
                          RecipeStatusHyperlinkedSerializer,
                          StepModelSerializer,
                          StepHyperlinkedSerializer,
                          SavedStepModelSerializer,
                          SavedStepHyperlinkedSerializer)


class BaseRecipeViewSet(viewsets.ModelViewSet):
    """
    Shared behavior for recipe viewsets.
    """
    # TODO: filter published recipes and order by publication date
    queryset = Recipe.objects.all().order_by("-created_at")
    permission_classes = [permissions.AllowAny]


class RecipeModelViewSet(BaseRecipeViewSet):
    """
    API endpoint that allows recipes to be viewed or edited.
    """
    serializer_class = RecipeModelSerializer


class RecipeHyperlinkedViewSet(BaseRecipeViewSet):
    """
    API endpoint that allows recipes to be viewed or edited.
    """
    serializer_class = RecipeHyperlinkedSerializer


class BaseSavedRecipeViewSet(viewsets.ModelViewSet):
    """
    Shared behavior for saved recipe viewsets.
    """
    queryset = SavedRecipe.objects.all().order_by("-saved_at")
    permission_classes = [permissions.AllowAny]


class SavedRecipeModelViewSet(BaseSavedRecipeViewSet):
    """
    API endpoint that allows saved recipes to be viewed or edited.
    """
    serializer_class = SavedRecipeModelSerializer


class SavedRecipeHyperlinkedViewSet(BaseSavedRecipeViewSet):
    """
    API endpoint that allows recipe ingredients to be viewed or edited.
    """
    serializer_class = SavedRecipeHyperlinkedSerializer


class BaseDifficultyViewSet(viewsets.ModelViewSet):
    queryset = Difficulty.objects.all().order_by("value")
    permission_classes = [permissions.AllowAny]


class DifficultyModelViewSet(BaseDifficultyViewSet):
    serializer_class = DifficultyModelSerializer


class DifficultyHyperlinkedViewSet(BaseDifficultyViewSet):
    serializer_class = DifficultyHyperlinkedSerializer


class BaseRecipeStatusViewSet(viewsets.ModelViewSet):
    queryset = RecipeStatus.objects.all().order_by("value")
    permission_classes = [permissions.AllowAny]


class RecipeStatusModelViewSet(BaseRecipeStatusViewSet):
    serializer_class = RecipeStatusModelSerializer


class RecipeStatusHyperlinkedViewSet(BaseRecipeStatusViewSet):
    serializer_class = RecipeStatusHyperlinkedSerializer


class BaseStepViewSet(viewsets.ModelViewSet):
    queryset = Step.objects.all().order_by("order")
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=["post"], url_path="swap")
    def swap_order(self, request):
        """
        Swap the order of two steps belonging to the same recipe.

        Expects JSON: {"step_a": "<uuid>", "step_b": "<uuid>"}
        Returns the updated list of steps for that recipe.
        """
        step_a_id = request.data.get("step_a")
        step_b_id = request.data.get("step_b")

        if not step_a_id or not step_b_id:
            return Response(
                {"detail": "Both 'step_a' and 'step_b' UUIDs are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if step_a_id == step_b_id:
            return Response(
                {"detail": "The two step UUIDs must be different."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            step_a = Step.objects.get(pk=step_a_id)
            step_b = Step.objects.get(pk=step_b_id)
        except Step.DoesNotExist:
            return Response(
                {"detail": "One or both steps not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if step_a.recipe != step_b.recipe:
            return Response(
                {"detail": "Both steps must belong to the same recipe."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Swap using a temporary sentinel value to avoid the unique
        # constraint violation.  order=0 is safe because valid orders
        # start at 1 (PositiveSmallIntegerField semantics in this project).
        with transaction.atomic():
            order_a, order_b = step_a.order, step_b.order
            # Move step_a to a temporary order (0) to free its slot
            Step.objects.filter(pk=step_a.pk).update(order=0)
            # Move step_b into step_a's old slot
            Step.objects.filter(pk=step_b.pk).update(order=order_a)
            # Move step_a into step_b's old slot
            Step.objects.filter(pk=step_a.pk).update(order=order_b)

        steps = Step.objects.filter(recipe=step_a.recipe).order_by("order")
        serializer = StepModelSerializer(steps, many=True)
        return Response(serializer.data)


class StepModelViewSet(BaseStepViewSet):
    serializer_class = StepModelSerializer


class StepHyperlinkedViewSet(BaseStepViewSet):
    serializer_class = StepHyperlinkedSerializer


class BaseSavedStepViewSet(viewsets.ModelViewSet):
    queryset = SavedStep.objects.all().order_by("order")
    permission_classes = [permissions.AllowAny]


class SavedStepModelViewSet(BaseSavedStepViewSet):
    serializer_class = SavedStepModelSerializer


class SavedStepHyperlinkedViewSet(BaseSavedStepViewSet):
    serializer_class = SavedStepHyperlinkedSerializer
