from django.http import HttpResponse
from rest_framework import generics
from rest_framework import status as drf_status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Profile, CustomUser
from .serializers import ProfileSerializer, AvatarOnlySerializer
from .serializers import UserCreateSerializer, UserReadSerializer
from django.utils.crypto import get_random_string
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import (
    IsAuthenticated, IsAdminUser, AllowAny, BasePermission
)
from rest_framework_simplejwt.backends import TokenBackend
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework.parsers import MultiPartParser, FormParser


class IsNotTokenAuthentication(BasePermission):
    def has_permission(self, request, view):
        return not request.auth


class IsTokenAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return getattr(request, 'auth', False)


class UserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsNotTokenAuthentication()]
        return [IsAdminUser()]

    @swagger_auto_schema(
        tags=['User accounts'],
        operation_summary='List signed-up users'
    )
    def get(self, request, *args, **kwargs):
        # return response.Response({'detail': 'GET not allowed.'},
        #                          status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['User accounts'],
        operation_summary='Sign-up'
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserReadSerializer


class IsSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not getattr(user, 'is_authenticated', False):
            return False
        # Only access is_staff and id for authenticated users
        return obj.id == getattr(user, 'id', None)


class IsSelfOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            IsSelf().has_object_permission(request, view, obj)
            or getattr(request.user, 'is_staff', False)
        )


class IsProfileOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not getattr(user, 'is_authenticated', False):
            return False
        return (
            getattr(obj, 'user', False) and (
                getattr(obj.user, 'id', None) == getattr(user, 'id', None)
            )
        )


class IsProfileOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            IsProfileOwner().has_object_permission(request, view, obj)
            or getattr(request.user, 'is_staff', False)
        )


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserReadSerializer
    permission_classes = [IsSelf]  # [IsSelfOrAdmin]

    @swagger_auto_schema(tags=['Account details'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Account details'])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Account details'])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['User accounts'],
        operation_summary='Delete account')
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Find the next available integer for deleted user
        count = (
            CustomUser.objects
            .filter(username__startswith='deleteduser').count() + 1
        )
        instance.username = f'deleteduser{count}'
        instance.email = f'deleteduser{count}@email.com'
        instance.is_active = False
        random_password = get_random_string(
            length=12,
            allowed_chars=(
                'abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'
                '!@#$%^&*()'
            )
        )
        instance.set_password(random_password)
        instance.save()
        return Response(
            {'detail': 'User has been permanently deleted.'},
            status=204)


class ProfileListView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        tags=['Profiles'],
        operation_summary='Get list of profiles')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'user__id'  # refers to traversing the relation: using the
    # id of the user to search
    lookup_url_kwarg = 'user_id'  # refers to the key in the path parameter
    # that will be used to get the value that needs to match the lookup_field

    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsProfileOwner()]  # [IsProfileOwnerOrAdmin()]

    @swagger_auto_schema(
        tags=['Profile details'],
        operation_summary=''
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Profile details'],
        operation_summary=''
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Profile details'],
        operation_summary=''
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class MeView(APIView):
    permission_classes = [IsTokenAuthenticated]

    @swagger_auto_schema(
        tags=['Current user details'],
        operation_summary='user id, username, avatar URL'
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        if not user or not user.is_authenticated:
            return Response(
                {'detail': 'Authentication credentials were not provided.'},
                status=drf_status.HTTP_401_UNAUTHORIZED,
            )
        profile = getattr(user, 'profile')
        serializer = AvatarOnlySerializer(
            profile, context={'request': request})
        return Response({
            'id': str(user.id),
            'username': user.username,
            **serializer.data,
        })


class AvatarView(APIView):
    permission_classes = [IsTokenAuthenticated]

    @swagger_auto_schema(
        tags=['Current user details'],
        operation_summary='Avatar URL'
    )
    def get(self, request, *args, **kwargs):
        profile = getattr(request.user, 'profile', None)
        if not profile:
            return Response({'avatar_url': None})
        serializer = AvatarOnlySerializer(
            profile, context={'request': request})
        return Response(serializer.data)


