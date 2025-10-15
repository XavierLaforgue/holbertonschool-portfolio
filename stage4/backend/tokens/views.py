from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView
)
# Create your views here.


class CustomTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        tags=['Authentication'],
        operation_summary="Log-in",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        tags=['Authentication'],
        operation_summary='Renew \"session\"'
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomTokenVerifyView(TokenVerifyView):
    @swagger_auto_schema(
        tags=['Authentication'],
        operation_summary='Verify \"session status\"'
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomTokenBlacklistView(TokenBlacklistView):
    @swagger_auto_schema(
        tags=['Authentication'],
        operation_summary='Log-out'
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
