from rest_framework import viewsets, permissions
from .models import CustomUser, Profile
from .serializers import (CustomUserModelSerializer,
                          CustomUserHyperlinkedSerializer,
                          ProfileModelSerializer,
                          ProfileHyperlinkedSerializer)


class CustomUserModelViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CustomUser.objects.all().order_by("-date_joined")
    serializer_class = CustomUserModelSerializer
    permission_classes = [permissions.AllowAny]


class CustomUserHyperlinkedViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CustomUser.objects.all().order_by("-date_joined")
    serializer_class = CustomUserHyperlinkedSerializer
    permission_classes = [permissions.AllowAny]


class ProfileModelViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows user profiles to be viewed or edited.
    """
    queryset = Profile.objects.all().order_by("-updated_at")
    serializer_class = ProfileModelSerializer
    permission_classes = [permissions.AllowAny]


class ProfileHyperlinkedViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows user profiles to be viewed or edited.
    """
    queryset = Profile.objects.all().order_by("-updated_at")
    serializer_class = ProfileHyperlinkedSerializer
    permission_classes = [permissions.AllowAny]
