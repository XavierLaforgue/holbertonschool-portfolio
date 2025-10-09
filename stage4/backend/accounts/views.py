from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
from .models import Profile
from .serializers import ProfileSerializer
from django.contrib.auth.models import User
from .serializers import UserSerializer

# Create your views here.


def index(request):
    return HttpResponse('Hello accounts world. Here I should manage '
                        'registered accounts')


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileListCreateView(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
