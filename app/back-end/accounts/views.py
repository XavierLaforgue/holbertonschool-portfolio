from django.utils import timezone
from rest_framework import viewsets, permissions
from .models import CustomUser, Profile
from .serializers import (CustomUserModelSerializer,
                          CustomUserHyperlinkedSerializer,
                          ProfileModelSerializer,
                          ProfileHyperlinkedSerializer)


class BaseCustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.filter(is_active=True)\
        .order_by("-date_joined")
    permission_classes = [permissions.AllowAny]

    def perform_destroy(self, instance):
        """Soft-delete a user instead of removing it from the database.

        Marks the user as inactive and records when it was deactivated.
        """
        instance.is_active = False
        instance.deactivated_at = timezone.now()
        instance.save(update_fields=["is_active", "deactivated_at"])


class CustomUserModelViewSet(BaseCustomUserViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = CustomUserModelSerializer


class CustomUserHyperlinkedViewSet(BaseCustomUserViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = CustomUserHyperlinkedSerializer


class BaseProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.filter(user__is_active=True)\
        .order_by("-updated_at")
    permission_classes = [permissions.AllowAny]
    http_method_names = ["get", "head", "options", "put", "patch", "delete"]


class ProfileModelViewSet(BaseProfileViewSet):
    """
    API endpoint that allows user profiles to be viewed or edited.
    """
    serializer_class = ProfileModelSerializer


class ProfileHyperlinkedViewSet(BaseProfileViewSet):
    """
    API endpoint that allows user profiles to be viewed or edited.
    """
    serializer_class = ProfileHyperlinkedSerializer
