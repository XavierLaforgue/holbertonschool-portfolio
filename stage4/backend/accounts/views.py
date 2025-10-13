from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, response
from .models import Profile, CustomUser
from .serializers import ProfileSerializer
from django.contrib.auth.models import User
from .serializers import UserCreateSerializer, UserReadSerializer
from django.utils.crypto import get_random_string


# Create your views here.


def index(request):
    return HttpResponse('Hello accounts world. Here I should manage '
                        'registered accounts')


class UserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserReadSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserReadSerializer

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


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
