from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from .models import (Recipe, RecipeStatus, SavedRecipe, Difficulty, Step,
                     SavedStep)
from .serializers import (RecipeSummarySerializer,
                          RecipeSummaryHyperlinkedSerializer,
                          RecipeExpandedSerializer,
                          SavedRecipeSummarySerializer,
                          SavedRecipeSummaryHyperlinkedSerializer,
                          SavedRecipeExpandedSerializer,
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
    GET /recipes/ - List with summaries
    GET /recipes/<id>/ - Detail with nested full objects
    """
    # TODO: filter published recipes and order by publication date
    queryset = Recipe.objects.filter(author__user__deleted_at__isnull=True)
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "anime_custom", "description",
                     "author__display_name"]
    ordering_fields = ["created_at", "published_at",
                       "estimated_time_minutes", "title"]
    ordering = ["-published_at", "-created_at"]
    summary_serializer_class = None
    detail_serializer_class = None

    def get_serializer_class(self):
        """Use summary serializer for list and expanded serializer for detail.
        """
        if self.action == "retrieve" and self.detail_serializer_class:
            return self.detail_serializer_class
        elif self.summary_serializer_class:
            return self.summary_serializer_class
        return super().get_serializer_class()

    def get_queryset(self):  # type: ignore[override]
        """Optimize queries for detail endpoint with nested objects."""
        queryset = Recipe.objects.all().order_by("-created_at")

        if self.action == "retrieve":
            # Detail endpoint: optimize for expanded nested data
            queryset = queryset.select_related(
                "author", "difficulty", "status"
            )
            queryset = queryset.prefetch_related(
                "steps",
                "ingredients__ingredient__allowed_unit_kinds",
                "ingredients__unit__kind",
            )

        return queryset


class RecipeModelViewSet(BaseRecipeViewSet):
    """
    API endpoint that allows recipes to be viewed or edited.

    List endpoint returns summary serializer (compact, fast).
    Detail endpoint returns expanded serializer (nested full objects).
    """
    # serializer_class = RecipeSummarySerializer
    summary_serializer_class = RecipeSummarySerializer
    detail_serializer_class = RecipeExpandedSerializer


class RecipeHyperlinkedViewSet(BaseRecipeViewSet):
    """
    API endpoint that allows recipes to be viewed or edited.
    Uses URL references instead of UUIDs.
    """
    # serializer_class = RecipeSummaryHyperlinkedSerializer
    summary_serializer_class = RecipeSummaryHyperlinkedSerializer
    detail_serializer_class = RecipeExpandedSerializer


class BaseSavedRecipeViewSet(viewsets.ModelViewSet):
    """
    Shared behavior for saved recipe viewsets.
    GET /saved-recipes/ - List with summaries
    GET /saved-recipes/<id>/ - Detail with nested full objects
    """
    queryset = SavedRecipe.objects.all()
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "anime_custom", "description",
                     "saver__display_name", "original_author__display_name"]
    ordering_fields = ["saved_at", "created_at", "published_at", "title"]
    ordering = "saved_at"
    summary_serializer_class = None
    detail_serializer_class = None

    def get_serializer_class(self):
        """Use summary serializer for list and expanded serializer for detail.
        """
        if self.action == "retrieve" and self.detail_serializer_class:
            return self.detail_serializer_class
        elif self.summary_serializer_class:
            return self.summary_serializer_class
        return super().get_serializer_class()

    def get_queryset(self):  # type: ignore[override]
        """Optimize queries for detail endpoint with nested objects."""
        queryset = SavedRecipe.objects.all().order_by("-saved_at")
        if self.action == "retrieve":
            # Detail endpoint: optimize for expanded nested data.
            # select_related: SQL JOIN (1 query) -> ForeignKey/OneToOne
            # prefetch_related: Separate queries + Python join
            # -> ManyToMany/reverse ForeignKey
            queryset = queryset.select_related("saver", "original_author",
                                               "difficulty", "status",
                                               "original_recipe")
            # prefetch_related() optimizes queries for reverse foreign key
            # relationships and many-to-many fields by performing a separate
            # query and joining results
            queryset = queryset.prefetch_related("steps")

        return queryset


class SavedRecipeModelViewSet(BaseSavedRecipeViewSet):
    """
    API endpoint that allows saved recipes to be viewed or edited.

    List endpoint returns summary serializer (compact).
    Detail endpoint returns expanded serializer (nested full objects).
    """
    # serializer_class = SavedRecipeSummarySerializer
    summary_serializer_class = SavedRecipeSummarySerializer
    detail_serializer_class = SavedRecipeExpandedSerializer


class SavedRecipeHyperlinkedViewSet(BaseSavedRecipeViewSet):
    """
    API endpoint that allows recipe ingredients to be viewed or edited.
    Uses URL references instead of scalar IDs.
    """
    # serializer_class = SavedRecipeSummaryHyperlinkedSerializer
    summary_serializer_class = SavedRecipeSummaryHyperlinkedSerializer
    detail_serializer_class = SavedRecipeExpandedSerializer


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
    queryset = Step.objects.all()
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=["post"], url_path="swap")
    def swap_number(self, request):
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

        # Swap using a temporary ancillary value to avoid the unique
        # constraint violation.  order=0 is safe because valid orders
        # start at 1 (PositiveSmallIntegerField semantics in this project).
        with transaction.atomic():
            number_a, number_b = step_a.number, step_b.number
            # Move step_a to a temporary order (0) to free its slot
            Step.objects.filter(pk=step_a.pk).update(number=0)
            # Move step_b into step_a's old slot
            Step.objects.filter(pk=step_b.pk).update(number=number_a)
            # Move step_a into step_b's old slot
            Step.objects.filter(pk=step_a.pk).update(number=number_b)

        steps = Step.objects.filter(recipe=step_a.recipe).order_by("number")
        serializer = StepModelSerializer(steps, many=True)
        return Response(serializer.data)


class StepModelViewSet(BaseStepViewSet):
    serializer_class = StepModelSerializer


class StepHyperlinkedViewSet(BaseStepViewSet):
    serializer_class = StepHyperlinkedSerializer


class BaseSavedStepViewSet(viewsets.ModelViewSet):
    queryset = SavedStep.objects.all()
    permission_classes = [permissions.AllowAny]


class SavedStepModelViewSet(BaseSavedStepViewSet):
    serializer_class = SavedStepModelSerializer


class SavedStepHyperlinkedViewSet(BaseSavedStepViewSet):
    serializer_class = SavedStepHyperlinkedSerializer
