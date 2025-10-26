"""
URL configuration for animize_eat project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static


@login_required(login_url='/api/auth/login/')
def swagger_redirect(request):
    schema_view = get_schema_view(
        openapi.Info(
            title="Animize-eat API",
            default_version='v1',
            description="API documentation",
        ),
        public=True,
        permission_classes=(permissions.IsAdminUser,),
        # (permissions.AllowAny,),
    )
    return schema_view.with_ui('swagger', cache_timeout=0)(request)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/swagger/',
         swagger_redirect,  # schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('api/auth/', include('rest_framework.urls')),
    path('api/accounts/', include('accounts.urls')),
    path('api/tokens/', include('tokens.urls')),
    # path('redoc/',
    #      schema_view.with_ui('redoc', cache_timeout=0),
    #      name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
