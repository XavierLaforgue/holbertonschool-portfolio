"""Cookie-based JWT views and `/me` endpoint.

* `CookieTokenObtainPairView`: authenticates and sets
  `access_token` / `refresh_token` cookies.
* `CookieTokenRefreshView`: reads the refresh token from its cookie,
  creates a new access token, and sets the updated cookie.
* `LogoutView`: clears both token cookies (with a commented-out
  draft for further implementation of token blacklisting).
* `MeView`: returns the currently authenticated user.
"""
from django.conf import settings
from rest_framework import permissions, status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from accounts.authentication import CookieJWTAuthentication
from .serializers import CustomUserModelSerializer

# ---------------- /me -----------------------------------------


class MeView(RetrieveAPIView):
    """Return the currently authenticated user."""
    serializer_class = CustomUserModelSerializer
    permission_classes = [permissions.IsAuthenticated]
    # `IsAuthenticated` checks for authentication in the order it is declared
    # in default authentication classes, i.e., CookieJWT, body JWT, SessionID,
    # and uses the first successful class.
    # To limit the authentication classes for this view:
    authentication_classes = [
        CookieJWTAuthentication,
        # JWTAuthentication,
        # SessionAuthentication,
    ]

    def get_object(self):  # type: ignore[override]
        return self.request.user


# ── Cookie configuration ────────────────────────────────────

ACCESS_COOKIE = "access_token"
REFRESH_COOKIE = "refresh_token"

COOKIE_DEFAULTS: dict = {
    # httponly=True,
    # TODO: once the httpOnly will be working properly, the frontend will no
    # longer need a client-side fallback for cookie deletion.
    "httponly": False,
    "secure": settings.AUTH_COOKIE_SECURE,
    "samesite": settings.AUTH_COOKIE_SAMESITE,
    "path": "/",
}


def set_auth_cookies(
    response: Response,
    access: str,
    refresh: str | None = None,
) -> None:
    """Attach JWT cookies to response."""
    response.set_cookie(
        ACCESS_COOKIE,
        access,
        max_age=int(
            settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()
        ),
        **COOKIE_DEFAULTS,
    )
    if refresh is not None:
        response.set_cookie(
            REFRESH_COOKIE,
            refresh,
            max_age=int(
                settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()
            ),
            **COOKIE_DEFAULTS,
        )


def clear_auth_cookies(response: Response) -> None:
    """Delete JWT cookies from response."""
    response.delete_cookie(ACCESS_COOKIE, path="/")
    response.delete_cookie(REFRESH_COOKIE, path="/")


# -------------- Token views -------------------------------

class CookieTokenObtainPairView(TokenObtainPairView):
    """POST email + password -> set token cookies, return JSON message."""

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        tokens = serializer.validated_data  # {"access": ..., "refresh": ...}
        response = Response(
            {"detail": "Login successful."},
            status=status.HTTP_200_OK,
        )
        set_auth_cookies(response, tokens["access"], tokens["refresh"])
        return response


class CookieTokenRefreshView(TokenRefreshView):
    """Read refresh token from cookie, issue new access cookie."""

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get(REFRESH_COOKIE)
        if not refresh_token:
            return Response(
                {"detail": "Refresh cookie missing."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = self.get_serializer(data={"refresh": refresh_token})
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        # e.args[0] is the error message of the `Exception`

        response = Response(
            {"detail": "Token refreshed."},
            status=status.HTTP_200_OK,
        )
        set_auth_cookies(response, serializer.validated_data["access"])
        return response


# ------------- Logout ------------------------------

class LogoutView(APIView):
    """Clear token cookies (and potentially blacklist the refresh token)."""
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        # TODO: blacklist logic here
        response = Response(
            {"detail": "Logged out."},
            status=status.HTTP_200_OK,
        )
        clear_auth_cookies(response)
        return response
