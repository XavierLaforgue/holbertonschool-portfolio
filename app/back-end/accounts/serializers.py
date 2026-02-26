from .models import CustomUser, Profile
from rest_framework import serializers


class CustomUserHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"
        # Use `fields` and a list to choose the fields I actually want to
        # serialize:
        # fields = [
        #     "url",
        #     "id",
        #     "username",
        #     "email",
        #     "first_name",
        #     "last_name",
        # ]
        # Or use `exclude` to exclude some fields from the whole for
        # serialization:
        # exclude = (
        #     "deactivated_at",
        #     "updated_at",
        #     "created_at",
        #     "last_authenticated_at"
        # )
        # `fields` and `exclude` can not be used together.


class CustomUserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"
        # fields = [
        #     "id",
        #     "username",
        #     "email",
        #     "first_name",
        #     "last_name",
        # ]


class ProfileHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Profile
        fields = "__all__"
        # fields = [
        #     "url",
        #     "id",
        #     "user",
        #     "display_name",
        #     "birth_date",
        #     "bio",
        #     "favorite_anime_custom",
        #     "favorite_meal",
        #     "location",
        #     "myAnimeList_profile",
        #     "dietary_preferences",
        # ]


class ProfileModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
        # fields = [
        #     "id",
        #     "user",
        #     "display_name",
        #     "birth_date",
        #     "bio",
        #     "favorite_anime_custom",
        #     "favorite_meal",
        #     "location",
        #     "myAnimeList_profile",
        #     "dietary_preferences",
        # ]
