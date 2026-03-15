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
        if "HTTP_AUTHORIZATION" in request.META:
            return None  # DRF treats `None` as "no authentication was done" 
        token = request.COOKIES.get("access_token")
        if token is None:
            return None
        # partially use logic from the parent class:
        # validated_token = self.get_validated_token(token)
        # user = self.get_user(validated_token)
        # return (user, validated_token)
        # ---------------------------------------
        # fully use logic from parent class:
        request.META["HTTP_AUTHORIZATION"] = f"Bearer {token}"
        return super().authenticate(request)
