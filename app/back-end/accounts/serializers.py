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
        }

    def create(self, validated_data: dict[str, str]) -> CustomUser:
        """Hash the password before creating the user.

        DRF's default ModelSerializer.create would store the raw password.
        """
        password = validated_data.pop("password", None)
        if not password:
            # Enforce that new users can only be created when a password
            # is provided, even if the field were made non-required.
            raise serializers.ValidationError({
                "password": "A password is required to create a user.",
            })

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
    class Meta(BaseCustomUserSerializer.Meta):
        pass


class BaseProfileSerializer:
    """Shared Meta config for Profile serializers to avoid repetition.

    Concrete serializers will inherit from this and from the
    appropriate DRF base class.
    """

    class Meta:
        model = Profile
        exclude = ("cleared_at",)


class ProfileHyperlinkedSerializer(serializers.HyperlinkedModelSerializer,
                                   BaseProfileSerializer):
    class Meta(BaseProfileSerializer.Meta):
        pass


class ProfileModelSerializer(serializers.ModelSerializer,
                             BaseProfileSerializer):
    class Meta(BaseProfileSerializer.Meta):
        pass
