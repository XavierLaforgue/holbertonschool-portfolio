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
from django.conf import settings
# from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve
from rest_framework_simplejwt.views import (
    # TokenObtainPairView,
    # TokenRefreshView,
    TokenVerifyView,
    # TODO: check if it is worthwhile to implement the blacklist app
    # TokenBlacklistView,
)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from accounts.views_auth import (
    CookieTokenObtainPairView,
    CookieTokenRefreshView,
    LogoutView,
    MeView,
)
from recipes.views import MyRecipesGroupedAPIView


@api_view(["GET"])
def api_root(request, format=None):
    return Response({
        "accounts": request.build_absolute_uri("/api/accounts/"),
        "ingredients": request.build_absolute_uri("/api/ingredients/"),
        "recipes": request.build_absolute_uri("/api/recipes/"),
        "token_obtain_pair": request.build_absolute_uri("/api/token/"),
        "token_refresh": request.build_absolute_uri("/api/token/refresh/"),
        "token_verify": request.build_absolute_uri("/api/token/verify/"),
        "token_logout": request.build_absolute_uri("/api/token/logout/"),
        "me": request.build_absolute_uri("/api/accounts/me/"),
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
    # JWT authentication endpoints (tokens set via cookies):
    # TODO: migrate to httpOnly Cookies tokens
    path('api/token/', include([
        path("", CookieTokenObtainPairView.as_view(),
             name='token_obtain_pair'),
        path('refresh/', CookieTokenRefreshView.as_view(),
             name='token_refresh'),
        # path("", TokenObtainPairView.as_view(),
        #      name='token_obtain_pair'),
        # path('refresh/', TokenRefreshView.as_view(),
        #      name='token_refresh'),
        path('verify/', TokenVerifyView.as_view(), name='token_verify'),
        path('logout/', LogoutView.as_view(), name='token_logout'),
        # path('blacklist/', TokenBlacklistView.as_view(),
        #      name='token_blacklist')
        ])
    ),
    # Current-user shortcut:
    path('api/me/', MeView.as_view(), name='me'),
    path('api/me/recipes/', MyRecipesGroupedAPIView.as_view(),
         name='me-recipes'),
]

# To serve static media files via Django we would typically do:
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)
# since this is practiced typically only on dev and not in production.
# To remove the conditional is not enough since static() checks for DEBUG
# internally.
# TODO: Use this DEBUG configuration once the need for a pseudo prod
# environment passes.

# TODO: replace with Nginx or S3 in production (see config/settings.py):
# To have a pseudo prod environment up asap, use `re_path` + `serve` directly
# instead because static() and no DEBUG=False check.
urlpatterns += [
    re_path(                      # Django's regex-based URL routing function.
        r"^media/(?P<path>.*)$",  # URL must start with `media/`, followed by
                                  # a path of any length all the way
                                  # to the end of the URL.
        serve,                    # View function called when pattern matches.
        {"document_root": settings.MEDIA_ROOT},  # file local root directory.
        # `serve` will serve a media file if its path, made by the
        # concatenetaion of `MEDIA_ROOT` + `media/<path>`
    ),
]
