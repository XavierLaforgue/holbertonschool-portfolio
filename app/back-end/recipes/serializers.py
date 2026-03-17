from .models import (Difficulty, Recipe, RecipePhoto, SavedRecipe,
                     RecipeStatus, Step, SavedStep)
from rest_framework import serializers
from accounts.serializers import ProfileSummarySerializer
from ingredients.models import RecipeIngredient, Ingredient, Unit, UnitKind


class DifficultyBaseSerializer:
    class Meta:
        abstract = True
        model = Difficulty
        fields = ("id", "label")


class DifficultyModelSerializer(DifficultyBaseSerializer,
                                serializers.ModelSerializer):
    class Meta(DifficultyBaseSerializer.Meta):
        pass


class DifficultyHyperlinkedSerializer(DifficultyBaseSerializer,
                                      serializers.HyperlinkedModelSerializer):
    class Meta(DifficultyBaseSerializer.Meta):
        pass


class BaseRecipeStatusSerializer:
    class Meta:
        model = RecipeStatus
        fields = "__all__"


class RecipeStatusModelSerializer(BaseRecipeStatusSerializer,
                                  serializers.ModelSerializer):
    class Meta(BaseRecipeStatusSerializer.Meta):
        model = RecipeStatus
        fields = ("id", "value")


class RecipeStatusHyperlinkedSerializer(
        BaseRecipeStatusSerializer,
        serializers.HyperlinkedModelSerializer):
    class Meta(BaseRecipeStatusSerializer.Meta):
        pass


class UnitKindSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitKind
        fields = "__all__"  # ("id", "label", "descriptive_name")


class UnitSummarySerializer(serializers.ModelSerializer):
    kind = UnitKindSummarySerializer(read_only=True)

    class Meta:
        model = Unit
        fields = "__all__"  # ("id", "name", "symbol", "kind")


class IngredientSummarySerializer(serializers.ModelSerializer):
    allowed_unit_kinds = UnitKindSummarySerializer(many=True, read_only=True)

    class Meta:
        model = Ingredient
        fields = "__all__"  # ("id", "name", "allowed_unit_kinds")


class RecipeIngredientExpandedSerializer(serializers.ModelSerializer):
    ingredient = IngredientSummarySerializer(read_only=True)
    unit = UnitSummarySerializer(read_only=True)

    class Meta:
        model = RecipeIngredient
        fields = "__all__"  # (
        #     "id",
        #     "ingredient",
        #     "quantity",
        #     "unit",
        #     "created_at",
        #     "updated_at",
        # )


class BaseRecipePhotoSerializer:
    class Meta:
        model = RecipePhoto
        fields = "__all__"


class RecipePhotoModelSerializer(BaseRecipePhotoSerializer,
                                 serializers.ModelSerializer):
    class Meta(BaseRecipePhotoSerializer.Meta):
        read_only_fields = ("recipe",)


class RecipePhotoHyperlinkedSerializer(
        BaseRecipePhotoSerializer,
        serializers.HyperlinkedModelSerializer):
    class Meta(BaseRecipePhotoSerializer.Meta):
        pass


class BaseStepSerializer:
    class Meta:
        model = Step
        fields = "__all__"


class StepModelSerializer(BaseStepSerializer,
                          serializers.ModelSerializer):
    class Meta(BaseStepSerializer.Meta):
        pass


class StepHyperlinkedSerializer(BaseStepSerializer,
                                serializers.HyperlinkedModelSerializer):
    class Meta(BaseStepSerializer.Meta):
        pass


class BaseRecipeSerializer:
    class Meta:
        model = Recipe
        fields = "__all__"


class RecipeIngredientWriteSerializer(serializers.Serializer):
    """Flat ingredient entry accepted inside a recipe write payload."""
    ingredient_name = serializers.CharField(max_length=50)
    quantity = serializers.FloatField()
    unit = serializers.PrimaryKeyRelatedField(queryset=Unit.objects.all())


class StepWriteSerializer(serializers.Serializer):
    """Flat step entry accepted inside a recipe write payload."""
    number = serializers.IntegerField(min_value=1)
    description = serializers.CharField(max_length=500)
    duration = serializers.DurationField(required=False, allow_null=True)


class RecipeWriteSerializer(serializers.ModelSerializer):
    """Accepts PKs for related fields; used for create/update."""
    difficulty = serializers.PrimaryKeyRelatedField(
        queryset=Difficulty.objects.all()
    )
    ingredients = RecipeIngredientWriteSerializer(
        many=True, required=False, write_only=True
    )
    steps = StepWriteSerializer(
        many=True, required=False, write_only=True
    )

    class Meta:
        model = Recipe
        fields = "__all__"
        read_only_fields = ("author", "status", "published_at")

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop("ingredients", None)
        steps_data = validated_data.pop("steps", None)
        instance = super().update(instance, validated_data)

        if ingredients_data is not None:
            # Replace all existing ingredients with the new set
            instance.ingredients.all().delete()
            for item in ingredients_data:
                ingredient, _created = Ingredient.objects.get_or_create(
                    name=item["ingredient_name"],
                )
                RecipeIngredient.objects.create(
                    recipe=instance,
                    ingredient=ingredient,
                    quantity=item["quantity"],
                    unit=item["unit"],
                )

        if steps_data is not None:
            # Replace all existing steps with the new set
            instance.steps.all().delete()
            for item in steps_data:
                Step.objects.create(
                    recipe=instance,
                    number=item["number"],
                    description=item["description"],
                    duration=item.get("duration"),
                )

        return instance


class RecipeSummarySerializer(BaseRecipeSerializer,
                              serializers.ModelSerializer):
    """Compact recipe response with nested author/difficulty/status objects."""
    main_photo = serializers.SerializerMethodField()
    author = ProfileSummarySerializer(read_only=True)
    difficulty = DifficultyModelSerializer(read_only=True)
    status = RecipeStatusModelSerializer(read_only=True)

    class Meta(BaseRecipeSerializer.Meta):
        pass

    def get_main_photo(self, obj):
        """Return URL of the main photo (position=1), or None."""
        if not hasattr(obj, 'photos'):
            return None
        photo = obj.photos.filter(position=1).first()
        if photo:
            # serializers have access to the request via their `context`
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(  # build the absolute URI:
                    # not just the ressource path but full url from http...
                    photo.image.url  # fallback: return relative url
                    # image is a ImageField in the model, ImageField inherits
                    # from FileField, which provides useful methos and
                    # attributes, such as .url=MEDIA_URL/path_from_re_path.
                    # .open(), .read(), and other file operations come from
                    # this.
                )
            return photo.image.url
        # The .url generation is handled by the storage backend (default:
        # FileSystemStorage, but swappable to S3 via django-storages).
        # When switching to S3, .url automatically returns the S3 URL without
        # changing the code.
        return None


class RecipeSummaryHyperlinkedSerializer(
        BaseRecipeSerializer, serializers.HyperlinkedModelSerializer
        ):
    """Compact recipe response with URL references to related objects."""
    class Meta(BaseRecipeSerializer.Meta):
        pass


class RecipeDetailsSerializer(serializers.ModelSerializer):
    """Recipe response with nested full objects for related resources."""
    author = ProfileSummarySerializer(read_only=True)
    difficulty = DifficultyModelSerializer(read_only=True)
    status = RecipeStatusModelSerializer(read_only=True)
    steps = StepModelSerializer(many=True, read_only=True)
    ingredients = RecipeIngredientExpandedSerializer(many=True,
                                                     read_only=True)
    photos = RecipePhotoModelSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        # fields = "__all__"
        exclude = ("created_at", "updated_at")


class BaseSavedRecipeSerializer:
    class Meta:
        model = SavedRecipe
        fields = "__all__"
        read_only_fields = ("saver", "original_recipe", "original_author",
                            "saved_at", "status")


class SavedRecipeSummarySerializer(BaseSavedRecipeSerializer,
                                   serializers.ModelSerializer):
    """Compact saved recipe response with scalar references to related
    objects."""
    class Meta(BaseSavedRecipeSerializer.Meta):
        pass


class SavedRecipeSummaryHyperlinkedSerializer(
        BaseSavedRecipeSerializer, serializers.HyperlinkedModelSerializer
        ):
    """Compact saved recipe response with URL references to related objects."""
    class Meta(BaseSavedRecipeSerializer.Meta):
        pass


class BaseSavedStepSerializer:
    class Meta:
        model = SavedStep
        fields = "__all__"


class SavedStepModelSerializer(BaseSavedStepSerializer,
                               serializers.ModelSerializer):
    class Meta(BaseSavedStepSerializer.Meta):
        pass


class SavedStepHyperlinkedSerializer(BaseSavedStepSerializer,
                                     serializers.HyperlinkedModelSerializer):
    class Meta(BaseSavedStepSerializer.Meta):
        pass


class SavedRecipeDetailsSerializer(serializers.ModelSerializer):
    """Saved recipe response with nested full objects for related resources."""
    saver = ProfileSummarySerializer(read_only=True)
    original_author = ProfileSummarySerializer(read_only=True)
    difficulty = DifficultyModelSerializer(read_only=True)
    status = RecipeStatusModelSerializer(read_only=True)
    steps = SavedStepModelSerializer(many=True, read_only=True)
    original_recipe_photos = serializers.SerializerMethodField()

    class Meta:
        model = SavedRecipe
        fields = "__all__"

    def get_original_recipe_photos(self, obj):
        """Return photos from the original recipe, or empty list."""
        if obj.original_recipe is None:
            return []
        photos = obj.original_recipe.photos.all()
        return RecipePhotoModelSerializer(
            photos, many=True, context=self.context
        ).data
