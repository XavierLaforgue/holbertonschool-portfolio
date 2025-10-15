from django.urls import path
from .views import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    CustomTokenVerifyView,
    CustomTokenBlacklistView
)

urlpatterns = [
    path('', CustomTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('refresh/', CustomTokenRefreshView.as_view(),
         name='token_refresh'),
    path('verify/', CustomTokenVerifyView.as_view(),
         name='token_verify'),
    path('blacklist/', CustomTokenBlacklistView.as_view(),
         name='token_blacklist'),
]
