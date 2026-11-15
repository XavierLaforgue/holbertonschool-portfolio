from django.utils import timezone
from rest_framework import viewsets, permissions
from .models import CustomUser, Profile
from .permissions import IsAccountOwnerOrAdmin
from .serializers import (CustomUserModelSerializer,
                          CustomUserHyperlinkedSerializer,
                          ProfileModelSerializer,
                          ProfileHyperlinkedSerializer)


class BaseCustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.filter(deleted_at__isnull=True)\
        .order_by("-created_at")

    def get_permissions(self):
        # Signing up (POST) is open to everyone.
        if self.action == "create":
            return [permissions.AllowAny()]
        # The list of every account (with their emails): administrators only.
        if self.action == "list":
            return [permissions.IsAdminUser()]
        # Reading, changing or deleting one account: its owner or an admin.
        return [permissions.IsAuthenticated(), IsAccountOwnerOrAdmin()]

    def perform_destroy(self, instance):
        """Soft-delete a user instead of removing it from the database.

        Marks the user as inactive and records when it was deactivated.
        """
        instance.is_active = False
        instance.deactivated_at = timezone.now()
        instance.deleted_at = timezone.now()
        instance.save(update_fields=["is_active",
                                     "deactivated_at",
                                     "deleted_at"])


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
    queryset = Profile.objects.filter(user__deleted_at__isnull=True)\
        .order_by("-updated_at")
    # forbid post (because a profile is created automatically when the user
    # is created) and delete (it is deleted with its account):
    http_method_names = ["get", "head", "options", "put", "patch"]

    def get_permissions(self):
        # The list of every profile: administrators only.
        if self.action == "list":
            return [permissions.IsAdminUser()]
        # Reading or changing one profile: its owner or an admin.
        return [permissions.IsAuthenticated(), IsAccountOwnerOrAdmin()]


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
