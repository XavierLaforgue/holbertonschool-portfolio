from django.urls import include, path
from rest_framework import routers
from .views import (CustomUserModelViewSet,
                    CustomUserHyperlinkedViewSet,
                    ProfileModelViewSet,
                    ProfileHyperlinkedViewSet)

router = routers.DefaultRouter()
router.register(r"user_models", CustomUserModelViewSet,
                basename="customuser_model")
router.register(r"user_hyperlinks", CustomUserHyperlinkedViewSet,
                basename="customuser")
router.register(r"profile_models", ProfileModelViewSet,
                basename="profile_model")
router.register(r"profile_hyperlinks", ProfileHyperlinkedViewSet,
                basename="profile")

urlpatterns = [
    path("", include(router.urls)),
    # path("auth/", include("rest_framework.urls",
    # namespace="rest_framework")),
]
