from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, response
from .models import Profile, CustomUser
from .serializers import ProfileSerializer
from django.contrib.auth.models import User
from .serializers import UserCreateSerializer, UserReadSerializer
from django.utils.crypto import get_random_string
from drf_yasg.utils import swagger_auto_schema


# Create your views here.


def index(request):
    return HttpResponse('Hello accounts world. Here I should manage '
                        'registered accounts')


class UserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()

    @swagger_auto_schema(tags=['Users'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Users'])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserReadSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserReadSerializer

    @swagger_auto_schema(tags=['User ID'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=['User ID'])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(tags=['User ID'])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(tags=['User ID'])
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


class ProfileListCreateView(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    @swagger_auto_schema(tags=['Profiles'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Profiles'])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    @swagger_auto_schema(tags=['Profile ID'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Profile ID'])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Profile ID'])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Profile ID'])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
