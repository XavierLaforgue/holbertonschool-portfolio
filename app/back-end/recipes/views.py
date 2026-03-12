from rest_framework import viewsets, permissions, status, filters, generics
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.utils import timezone
from .models import (Recipe, RecipePhoto, RecipeStatus, SavedRecipe,
                     Difficulty, Step, SavedStep)
from .serializers import (RecipeSummarySerializer,
                          RecipeSummaryHyperlinkedSerializer,
                          RecipeDetailsSerializer,
                          SavedRecipeSummarySerializer,
                          SavedRecipeSummaryHyperlinkedSerializer,
                          SavedRecipeDetailsSerializer,
                          DifficultyModelSerializer,
                          DifficultyHyperlinkedSerializer,
                          RecipeStatusModelSerializer,
                          RecipeStatusHyperlinkedSerializer,
                          RecipePhotoModelSerializer,
                          StepModelSerializer,
                          StepHyperlinkedSerializer,
                          SavedStepModelSerializer,
                          SavedStepHyperlinkedSerializer)


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """Allow read to anyone; write only to authenticated users."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated


class BaseRecipeViewSet(viewsets.ModelViewSet):
    """
    Shared behavior for recipe viewsets.
    GET /recipes/ - List with summaries (Published only)
    GET /recipes/<id>/ - Detail (author sees all statuses; others see
    Published)
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
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
        if self.action in ("retrieve", "status") \
                and self.detail_serializer_class:
            return self.detail_serializer_class
        elif self.summary_serializer_class:
            return self.summary_serializer_class
        return super().get_serializer_class()

    def _get_base_queryset(self):
        return Recipe.objects.filter(author__user__deleted_at__isnull=True)

    def get_queryset(self):  # type: ignore[override]
        """Filter by status depending on the action and requester."""
        if self.action == "list":
            # Public feed: Published only
            queryset = self._get_base_queryset().filter(
                status__value="Published"
            ).order_by("-published_at", "-created_at")
            queryset = queryset.prefetch_related(
                Prefetch(
                    "photos",
                    queryset=RecipePhoto.objects.filter(position=1),
                ),
            )
            return queryset

        if self.action == "retrieve":
            # Detail: author can see their own drafts/ready; others only
            # Published
            queryset = self._get_base_queryset()
            # Authenticated users see: all Published recipes + their own
            # recipes (any status). The "|" is a queryset union; distinct()
            # removes duplicates when an author views their own published
            # recipe.
            if self.request.user.is_authenticated:
                published = queryset.filter(status__value="Published")
                own = self._get_base_queryset().filter(
                    author__user=self.request.user
                )
                queryset = (published | own).distinct()
            else:
                queryset = queryset.filter(status__value="Published")
            queryset = queryset.select_related(
                "author", "difficulty", "status"
            ).prefetch_related(
                "steps",
                "photos",
                "ingredients__ingredient__allowed_unit_kinds",
                "ingredients__unit__kind",
            )
            return queryset

        # For update, partial_update, destroy, status action: unfiltered
        return self._get_base_queryset().select_related(
            "author", "difficulty", "status"
        )

    def _require_author(self, recipe):
        """Raise 403 if the current user is not the recipe's author."""
        if recipe.author.user != self.request.user:
            raise PermissionDenied(
                "You do not have permission to modify this recipe."
            )

    @action(detail=True, methods=["patch"], url_path="status",
            permission_classes=[permissions.IsAuthenticated])
    def set_status(self, request, pk=None):
        """
        PATCH /api/recipes/recipe_models/{id}/status/
        Body: { "value": "Draft" | "Ready" | "Published" }

        Transitions:
          any -> Draft   : always allowed for author
          any -> Ready   : always allowed for author
          Ready -> Published : requires non-empty title, anime_custom,
                               >=1 ingredient, >=1 step
          Published -> Ready : clears published_at (retract)
        """
        recipe = get_object_or_404(Recipe, pk=pk)
        self._require_author(recipe)

        new_value = request.data.get("value")
        if new_value not in ("Draft", "Ready", "Published"):
            return Response(
                {"detail": "Invalid status value. Use Draft, Ready, or "
                    "Published."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        current_value = recipe.status.value

        # Validate publish transition
        if new_value == "Published":
            if current_value != "Ready":
                return Response(
                    {"detail": "Only a Ready recipe can be published."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            errors = []
            if not recipe.title.strip():
                errors.append("Recipe must have a title.")
            if not recipe.anime_custom.strip():
                errors.append("Recipe must have an anime source.")
            if not recipe.ingredients.exists():  # type: ignore
                errors.append("Recipe must have at least one ingredient.")
            if not recipe.steps.exists():  # type: ignore
                errors.append("Recipe must have at least one step.")
            if errors:
                return Response(
                    {"detail": errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        new_status = get_object_or_404(RecipeStatus, value=new_value)
        recipe.status = new_status

        if new_value == "Published":
            recipe.published_at = timezone.now()
        elif current_value == "Published" and new_value != "Published":
            # Retract: clear published_at
            recipe.published_at = None

        recipe.save(update_fields=["status", "published_at"])

        serializer = self.get_serializer(recipe)  # serializer chosen by view/
        # action
        return Response(serializer.data)


class RecipeModelViewSet(BaseRecipeViewSet):
    """
    API endpoint that allows recipes to be viewed or edited.

    List endpoint returns summary serializer (compact, fast).
    Detail endpoint returns expanded serializer (nested full objects).
    """
    summary_serializer_class = RecipeSummarySerializer
    detail_serializer_class = RecipeDetailsSerializer

    def perform_create(self, serializer):
        """Create a blank draft recipe owned by the current user."""
        draft_status = get_object_or_404(RecipeStatus, value="Draft")
        serializer.save(
            author=self.request.user.profile,
            status=draft_status,
        )

    def perform_update(self, serializer):
        """Only the author may update their recipe."""
        self._require_author(serializer.instance)
        serializer.save()

    def perform_destroy(self, instance):
        """Only the author may delete their recipe."""
        self._require_author(instance)
        instance.delete()


class RecipeHyperlinkedViewSet(BaseRecipeViewSet):
    """
    API endpoint that allows recipes to be viewed or edited.
    Uses URL references instead of UUIDs.
    """
    summary_serializer_class = RecipeSummaryHyperlinkedSerializer
    detail_serializer_class = RecipeDetailsSerializer


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
    summary_serializer_class = SavedRecipeSummarySerializer
    detail_serializer_class = SavedRecipeDetailsSerializer


class SavedRecipeHyperlinkedViewSet(BaseSavedRecipeViewSet):
    """
    API endpoint that allows recipe ingredients to be viewed or edited.
    Uses URL references instead of scalar IDs.
    """
    summary_serializer_class = SavedRecipeSummaryHyperlinkedSerializer
    detail_serializer_class = SavedRecipeDetailsSerializer


class DifficultyBaseViewSet(viewsets.ModelViewSet):
    queryset = Difficulty.objects.all().order_by("value")
    permission_classes = [permissions.AllowAny]


class DifficultyModelViewSet(DifficultyBaseViewSet):
    serializer_class = DifficultyModelSerializer


class DifficultyHyperlinkedViewSet(DifficultyBaseViewSet):
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

    @staticmethod
    def _swap_step_numbers(step_a, step_b):
        """Swap two step numbers atomically without violating uniqueness."""
        # Use a temporary value to free one slot before assigning the target.
        with transaction.atomic():
            number_a, number_b = step_a.number, step_b.number
            Step.objects.filter(pk=step_a.pk).update(number=0)
            Step.objects.filter(pk=step_b.pk).update(number=number_a)
            Step.objects.filter(pk=step_a.pk).update(number=number_b)

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

        self._swap_step_numbers(step_a, step_b)

        steps = Step.objects.filter(recipe=step_a.recipe).order_by("number")
        serializer = StepModelSerializer(steps, many=True)
        return Response(serializer.data)


class RecipeStepListCreateSwapAPIView(generics.ListCreateAPIView):
    """Nested step endpoint for a specific recipe collection."""
    serializer_class = StepModelSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):  # type: ignore[override]
        recipe_id = self.kwargs["recipe_id"]
        return Step.objects.filter(recipe_id=recipe_id).order_by("number")

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe, pk=self.kwargs["recipe_id"])
        serializer.save(recipe=recipe)

    def patch(self, request, *args, **kwargs):
        """Swap two steps via payload: {"swap": [{"id", "number"}, ...]}."""
        recipe = get_object_or_404(Recipe, pk=self.kwargs["recipe_id"])
        swap_payload = request.data.get("swap")

        if not isinstance(swap_payload, list) or len(swap_payload) != 2:
            return Response(
                {"detail": "'swap' must be a list with exactly 2 entries."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        step_ids = []
        for item in swap_payload:
            if not isinstance(item, dict):
                return Response(
                    {"detail": "Each 'swap' entry must be an object."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if "id" not in item or "number" not in item:
                return Response(
                    {
                        "detail": (
                            "Each 'swap' entry requires 'id' and 'number'."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            step_ids.append(item["id"])

        if step_ids[0] == step_ids[1]:
            return Response(
                {"detail": "The two step IDs must be different."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        steps = list(Step.objects.filter(
            recipe=recipe,
            pk__in=step_ids,
        ).order_by("number"))
        if len(steps) != 2:
            return Response(
                {
                    "detail": (
                        "One or both steps were not found for this recipe."
                    )
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        BaseStepViewSet._swap_step_numbers(steps[0], steps[1])
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RecipeStepDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Nested step endpoint for a specific recipe step resource."""
    serializer_class = StepModelSerializer
    lookup_url_kwarg = "step_id"

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):  # type: ignore[override]
        recipe_id = self.kwargs["recipe_id"]
        return Step.objects.filter(recipe_id=recipe_id)

    def perform_update(self, serializer):
        recipe = get_object_or_404(Recipe, pk=self.kwargs["recipe_id"])
        serializer.save(recipe=recipe)


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


MAX_PHOTOS_PER_RECIPE = 5


class RecipePhotoListCreateAPIView(generics.ListCreateAPIView):
    """Nested photo endpoint for a specific recipe's photo collection."""
    serializer_class = RecipePhotoModelSerializer
    parser_classes = [MultiPartParser, FormParser]

    # MultiPartParser: Parses multipart/form-data requests (standard HTML form
    # for file uploads). Handles the image file in the request body and makes
    # it available as request.data['image'].
    # FormParser: Parses application/x-www-form-urlencoded requests (standard
    # HTML form submissions without files). Included as a fallback so text
    # fields like position can be submitted either way (which would be useful
    # to swap position of photos).

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):  # type: ignore[override]
        recipe_id = self.kwargs["recipe_id"]
        return RecipePhoto.objects.filter(
            recipe_id=recipe_id
        ).order_by("position")

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe, pk=self.kwargs["recipe_id"])
        current_count = RecipePhoto.objects.filter(recipe=recipe).count()
        if current_count >= MAX_PHOTOS_PER_RECIPE:
            from rest_framework.exceptions import ValidationError
            raise ValidationError(
                {"detail": f"A recipe can have at most "
                 f"{MAX_PHOTOS_PER_RECIPE} photos."}
            )
        serializer.save(recipe=recipe)


class RecipePhotoDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Nested endpoint for a specific recipe photo resource."""
    serializer_class = RecipePhotoModelSerializer
    parser_classes = [MultiPartParser, FormParser]


class MyRecipesGroupedAPIView(APIView):
    """Return the current user's recipes grouped by status + saved recipes."""
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def _with_summary_relations(queryset):
        return queryset.select_related(
            "author",
            "difficulty",
            "status",
        ).prefetch_related(
            Prefetch(
                "photos",
                queryset=RecipePhoto.objects.filter(position=1),
            ),
        )

    def get(self, request):
        profile = request.user.profile

        authored_base = self._with_summary_relations(
            Recipe.objects.filter(author=profile)
        )

        saved_base = self._with_summary_relations(
            Recipe.objects.filter(
                saved_copies__saver=profile,
                author__user__deleted_at__isnull=True,
                status__value="Published",
            ).distinct()
        )

        data = {
            "draft": RecipeSummarySerializer(
                authored_base.filter(status__value="Draft")
                .order_by("-updated_at", "-created_at"),
                many=True,
                context={"request": request},
            ).data,
            "ready": RecipeSummarySerializer(
                authored_base.filter(status__value="Ready")
                .order_by("-updated_at", "-created_at"),
                many=True,
                context={"request": request},
            ).data,
            "published": RecipeSummarySerializer(
                authored_base.filter(status__value="Published")
                .order_by("-published_at", "-created_at"),
                many=True,
                context={"request": request},
            ).data,
            "saved": RecipeSummarySerializer(
                saved_base.order_by("-published_at", "-created_at"),
                many=True,
                context={"request": request},
            ).data,
        }

        return Response(data, status=status.HTTP_200_OK)
    lookup_url_kwarg = "photo_id"

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):  # type: ignore[override]
        recipe_id = self.kwargs["recipe_id"]
        return RecipePhoto.objects.filter(recipe_id=recipe_id)

    def perform_update(self, serializer):
        recipe = get_object_or_404(Recipe, pk=self.kwargs["recipe_id"])
        serializer.save(recipe=recipe)
