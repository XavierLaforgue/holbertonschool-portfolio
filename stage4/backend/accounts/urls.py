from django.urls import path
from .views import ProfileListView, ProfileDetailView, MeView
from .views import UserListCreateView, UserDetailView, AvatarView


urlpatterns = [
    path('profiles/', ProfileListView.as_view(),
         name='profile-list-create'),
    path('profiles/<uuid:user_id>/', ProfileDetailView.as_view(),
         name='profile-detail'),
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<uuid:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('me/avatar/', AvatarView.as_view(), name='me-avatar'),
    path('me/', MeView.as_view(), name='me'),
]
