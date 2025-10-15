from django.http import HttpResponse
from rest_framework import generics, response, status
from .models import Profile, CustomUser
from .serializers import ProfileSerializer
from .serializers import UserCreateSerializer, UserReadSerializer
from django.utils.crypto import get_random_string
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import (
    IsAuthenticated, IsAdminUser, AllowAny, BasePermission
)


# Create your views here.
def index(request):
    return HttpResponse('Hello accounts world. Here I should manage '
                        'registered accounts')


class IsNotTokenAuthentication(BasePermission):
    def has_permission(self, request, view):
        return not request.auth


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
        if not user or not user.is_authenticated:
            return False
        # Only access is_staff and id for authenticated users
        return obj.id == getattr(user, 'id', None)


class IsSelfOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            IsSelf().has_object_permission(request, view, obj)
            or getattr(request.user, 'is_staff', False)
        )


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserReadSerializer
    permission_classes = [IsSelfOrAdmin]

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
        return response.Response(
            {'detail': 'User has been permanently deleted.'},
            status=204)


class ProfileListCreateView(generics.ListAPIView):
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

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsSelfOrAdmin()]

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
