"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    # TODO: check if it is worthwhile to implement the blacklist app
    # TokenBlacklistView,
)
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def api_root(request, format=None):
    return Response({
        "accounts": request.build_absolute_uri("/api/accounts/"),
        "ingredients": request.build_absolute_uri("/api/ingredients/"),
        "recipes": request.build_absolute_uri("/api/recipes/"),
        "token_obtain_pair": request.build_absolute_uri("/api/token/"),
        "token_refresh": request.build_absolute_uri("/api/token/refresh/"),
        "token_verify": request.build_absolute_uri("/api/token/verify/"),
        # "token_blacklist": request.build_absolute_uri(
        #     "/api/token/blacklist/"),
    })


urlpatterns = [
    # admin endpoint:
    path('admin/', admin.site.urls),
    # REST API endpoints:
    path("api/", api_root, name="api-root"),
    path('api/accounts/', include('accounts.urls')),
    path('api/ingredients/', include('ingredients.urls')),
    path('api/recipes/', include('recipes.urls')),
    # JWT authentication endpoints:
    # TODO: switch to httponly cookie tokens
    path('api/token/', include([
        path("", TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('verify/', TokenVerifyView.as_view(), name='token_verify'),
        # path('blacklist/', TokenBlacklistView.as_view(),
        #      name='token_blacklist')
        ])
    )
]
