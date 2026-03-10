from .models import CustomUser, Profile
from rest_framework import serializers


class BaseCustomUserSerializer(serializers.ModelSerializer):
    """Shared config + password handling for CustomUser serializers.

    This mixin relies on DRF's auto-generated model field for `password`,
    but tweaks its behaviour via `extra_kwargs` and hashes passwords in
    create/update.
    """

    class Meta:
        model = CustomUser
        # I need to exclude groups and user_permissions (at least for now)
        # because there is no view for groups and permissions and, therefore,
        # the HyperlinkedSerializer can not generate url for those fields.
        exclude = (
            "groups",
            "user_permissions",
            "is_superuser",
            "is_staff",
            "is_active",
            "date_joined",
            "deactivated_at",
            "last_login",
            # TODO: an expanded serializer may be necessary for the account
            # management page. For now I exclude:
            "username",
            "first_name",
            "last_name",
            "created_at",
            "updated_at",
            "deleted_at",
        )
        read_only_fields = (
            "last_login",
            "date_joined",
            "last_authenticated_at",
            "deactivated_at",
            "created_at",
            "updated_at",
        )
        # Configure the auto-generated password field to be write-only and
        # rendered as a password input in the browsable API.
        extra_kwargs = {
            "password": {
                "write_only": True,
                "style": {"input_type": "password"},
            },
            "username": {
                "required": False,
                "allow_blank": True,
                "read_only": True,
            },
        }

    def create(self, validated_data: dict[str, str]) -> CustomUser:
        """Hash the password before creating the user.

        DRF's default ModelSerializer.create would store the raw password.
        """
        password = validated_data.pop("password", "")
        if not password:
            # Enforce that new users can only be created when a password
            # is provided, even if the field were made non-required.
            raise serializers.ValidationError({
                "password": "A password is required to create a user.",
            })
        email = validated_data.get("email", "")
        if not email:
            raise serializers.ValidationError({
                "email": "An email is required to create a user.",
            })
        validated_data["username"] = email
        user: CustomUser = super().create(validated_data)
        user.set_password(password)
        user.save(update_fields=["password"])
        return user

    def update(self, instance, validated_data: dict[str, str]) -> CustomUser:
        """Hash the password when it's included in an update payload."""
        password = validated_data.pop("password", None)
        user: CustomUser = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save(update_fields=["password"])
        return user


class CustomUserHyperlinkedSerializer(
        BaseCustomUserSerializer,
        serializers.HyperlinkedModelSerializer):
    class Meta(BaseCustomUserSerializer.Meta):
        pass


class CustomUserModelSerializer(
        BaseCustomUserSerializer,
        serializers.ModelSerializer):
    display_name = serializers.SerializerMethodField()
    profile_id = serializers.SerializerMethodField()

    class Meta(BaseCustomUserSerializer.Meta):
        pass

    def get_display_name(self, obj):
        profile = getattr(obj, "profile", None)
        return getattr(profile, "display_name", None)

    def get_profile_id(self, obj):
        profile = getattr(obj, "profile", None)
        if profile is None:
            return None
        return str(profile.id)


class BaseProfileSerializer:
    """Shared Meta config for Profile serializers to avoid repetition.

    Concrete serializers will inherit from this and from the
    appropriate DRF base class.
    """

    class Meta:
        model = Profile
        fields = "__all__"


class ProfileHyperlinkedSerializer(serializers.HyperlinkedModelSerializer,
                                   BaseProfileSerializer):
    class Meta(BaseProfileSerializer.Meta):
        pass


class ProfileModelSerializer(serializers.ModelSerializer,
                             BaseProfileSerializer):
    class Meta(BaseProfileSerializer.Meta):
        pass


class ProfileSummarySerializer(serializers.ModelSerializer,
                               BaseProfileSerializer):
    """Compact profile representation for nested usage in other serializers."""
    class Meta(BaseProfileSerializer.Meta):
        fields = (
            "id",
            "display_name",
        )
