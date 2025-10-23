from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Profile, CustomUser
from django.contrib.auth.models import User
import re


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, min_length=8
    )
    email = serializers.EmailField(
        required=True,
        # validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A user with this email already exists."
            )
        return value

    def validate_password(self, value):
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError(
                "Password must contain an uppercase letter.")
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError(
                "Password must contain a lowercase letter.")
        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError("Password must contain a digit.")
        if not re.search(r'[^A-Za-z0-9]', value):
            raise serializers.ValidationError(
                "Password must contain a special character.")
        return value

    class Meta:  # type: ignore[reportIncompatibleVariableOverride]
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserReadSerializer(serializers.ModelSerializer):
    class Meta:  # type: ignore[reportIncompatibleVariableOverride]
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        extra_kwargs = {
            'email': {
                'validators': [UniqueValidator(
                    queryset=CustomUser.objects.all())],
                'required': True
            }
        }


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:  # type: ignore[reportIncompatibleVariableOverride]
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'password']


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:  # type: ignore[reportIncompatibleVariableOverride]
        model = Profile
        fields = ['username', 'bio', 'avatar', 'favorite_anime',
                  'favorite_meal', 'location', 'personal_website',
                  'dietary_preferences']


class AvatarOnlySerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    class Meta:  # type: ignore[reportIncompatibleVariableOverride]
        model = Profile
        fields = ['avatar_url']

    def get_avatar_url(self, obj):
        request = self.context.get('request')
        if obj.avatar and request:
            return request.build_absolute_uri(obj.avatar.url)
        return None
