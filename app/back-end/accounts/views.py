from rest_framework import viewsets, permissions
from .models import CustomUser, Profile
from .permissions import IsAccountOwnerOrAdmin
from .views_auth import clear_auth_cookies
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

    def destroy(self, request, *args, **kwargs):
        """Delete the account for good (RGPD: right to erasure).

        The database deletes, by cascade (on_delete=CASCADE), the profile,
        the recipes with their steps, ingredients and photos (the image
        files too, see recipes/models.py), and the user's saved copies.
        Copies that other users saved of this user's recipes stay, without
        their link to the deleted author (on_delete=SET_NULL).
        """
        deleting_myself = self.get_object() == request.user
        response = super().destroy(request, *args, **kwargs)
        if deleting_myself:
            # The account no longer exists: log this browser out.
            clear_auth_cookies(response)
        return response


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
