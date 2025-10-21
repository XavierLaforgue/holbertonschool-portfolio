from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView
)
from rest_framework import status
from django.conf import settings
import jwt


access_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
refresh_lifetime = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
max_age_access = int(access_lifetime.total_seconds())
max_age_refresh = int(refresh_lifetime.total_seconds())


class CustomTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        tags=['Authentication'],
        operation_summary="Log-in",
    )
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            data = response.data
            access_token = data.get('access')
            refresh_token = data.get('refresh')
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=False,  # set to True for https
                samesite='Lax',  # set to None to allow cookies for all
                    # cross-site requests (it requires https)
                max_age=max_age_access  # (in seconds)
            )
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=False,  # set to True for https
                samesite='Lax',  # set to None to allow cookies for all
                    # cross-site requests (it requires https)
                max_age=max_age_refresh  # (in seconds)
            )
            user_id = jwt.decode(access_token,
                                 settings.SECRET_KEY,
                                 algorithms=["HS256"]).get('user_id')
            response.data['id'] = user_id
            response.data.pop('access', None)
            response.data.pop('refresh', None)
        return response


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
