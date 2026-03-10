"""Cookie-based JWT authentication for DRF.

Reads the access token from the `access_token` cookie instead of the
`Authorization` header.
The browser handles the token transport automatically via `credentials:
'include'`, keeping the frontend free of any token manipulation and
facilitating migration to httpOnly.
"""

from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthentication(JWTAuthentication):
    """Authenticate using the `access_token` cookie."""

    def authenticate(self, request):
        """Returns None if no token in cookies, returns tuple with user and
        token otherwise"""
        raw_token = request.COOKIES.get("access_token")
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token
