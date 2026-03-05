# Json Web Token with Django

## Installation [^drf-simplejwt-install]

We can use jwt with django by installing the django rest framework jwt package:

```bash
uv add djangorestframework-simplejwt
```

## Project configuration [^drf-simplejwt-configuration]

We configure our django project to use the library by adding the authenticaiton class to the list of default authentication classes in `settings.py`:

```python
REST_FRAMEWORK = {
    ...
    'DEFAULT_AUTHENTICATION_CLASSES': (
        ...
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
    ...
}
```

The urls to obtain manage the tokens need to be added to some `urls` config file:

```python
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    ...
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # optionally, a `verify` view may be included, this simply returns 200 or 401 depending on if the token is valid or not:
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    ...
]
```

For localization/translation:

```python
INSTALLED_APPS = [
    ...
    'rest_framework_simplejwt',
    ...
]
```

## Simple JWT customization [^DRJ-simple-jwt-settings]

Some of Simple JWT’s behavior can be customized through settings variables in settings.py:

```python
from datetime import timedelta
...

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    ...
    "CHECK_USER_IS_ACTIVE": True,
}
```

## Rotating reresh tokens [^drf-simple-jwt-rotate-refresh-tokens]

If used, the refresh endpoint will return another access and refresh pair, where the new refresh token has an renewed lifetime.
The previous refresh token should be blacklisted.
This is useful to raise warnings if the wrong refresh token is used and determine if perhaps an attacker took and tried to use it.

## Blacklist token [^drf-simple-jwt-blacklist]

There is an available blacklist app that needs to be installed and its corresponding migrations performed:

```python
INSTALLED_APPS = (
    ...
    'rest_framework_simplejwt.token_blacklist',
    ...
)
```

A dedicated url may be added:

```python
from rest_framework_simplejwt.views import TokenBlacklistView

urlpatterns = [
  ...
  path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
  ...
]
```

and a management command, `flushexpiredtokens`, is made available (which should be scheduled with a `cron` job to be run daily).

## References

[^drf-simplejwt-install]: Django REST Framework third party package for JWT authentication
    [django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html#installation](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html#installation)

[^drf-simplejwt-configuration]: Django REST Framework Simple JWT project configuration
    [django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html#project-configuration](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html#project-configuration)

[^drf-simple-jwt-blacklist]: DRF blacklist app
    [django-rest-framework-simplejwt.readthedocs.io/en/latest/blacklist_app.html#blacklist-app](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/blacklist_app.html#blacklist-app)

[^drf-simple-jwt-rotate-refresh-tokens]: Django REST Framework - Rotate Refresh tokens
    [django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html#rotate-refresh-tokens](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html#rotate-refresh-tokens)
