from django.urls import path
from . import views
from .views import ProfileListCreateView, ProfileDetailView
from .views import UserListCreateView, UserDetailView


urlpatterns = [
    path("", views.index, name='index'),
    path('profiles/', ProfileListCreateView.as_view(),
         name='profile-list-create'),
    path('profiles/<uuid:pk>/', ProfileDetailView.as_view(),
         name='profile-detail'),
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]
