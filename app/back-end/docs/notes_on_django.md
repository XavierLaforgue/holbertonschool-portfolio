# Notes on `django`
<!-- TODO: write bash script to initialize `django` project-->
Once installed `django`, e.g., with

```bash
uv add django
```

We can initialize a ne django project with

```bash
uv run django-admin startproject my_project .
```

This will generate the file tree for a basic `django` project.

The `django` server is launched with

```bash
uv run manage.py runserver
```

or

```bash
uv run manage.py runserver $port_number
```

which may require migrations, for which we would need to define them

```bash
uv run manage.py makemigrations
```

and execute them

```bash
uv run manage.py migrate
```

If successful, the new `django` server will be running on `localhost:8000` (or on `localhost:$portnumber`) and an `admin` panel will be available at its `/admin`.
However, `admin` users must be created so they may access such panel.

## Secrets

No secrets must remain in the versioned (and shared) codebase.
Therefore, we remove the hardcoded `SECRET_KEY` and replace it with one read from the environment.

We can use

```bash
openssl rand -base64 50
```

to generate the secret keys.

## Database

The default database used by `django` is sqlite.
To use `postgresql` instead we need to change `django` database settings in [settings.py](../back-end/config/settings.py).
And we need to install the driver:

```bash
uv add psycopg
```

Look at [^djangoproject-postgres].

## Admin - Superuser

To create an admin user, a user that can access the admin panel and operating directly on the models for CRUD operations, do

```bash
uv run manage.py createsuperuser --username=admin --email=admin@example.com

```

## Django apps

The Django framework uses the concept of apps to divide the reponsibilities.
According to the models I'll need, [class diagram](../../../project-reports/stage3_report.md#class-diagram), I consider the following apps:

| App           | Model(s)                                                                                     | View(s)                                                                                          |
|---------------|----------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------|
| `accounts`    | CustomUser, Profile                                                                          | LoginView, LogoutView, CheckConnectionView, UserListView, UserView, ProfileListView, ProfileView |
| `recipes`     | Recipe (with enum models: Difficulty and RecipeStatus), Step, RecipePhotos, RecipeIngredient | RecipeListView, RecipeView, StepListView, StepView, RecipePhotosView                             |
| `ingredients` | Ingredient (with enum model Unit)                                                            | IngredientListView, IngredientView                                                               |
| `animes`      | Anime, AnimeDBVersion                                                                        | AnimeListView, AnimeView                                                                         |

We start apps on `Django` with

```bash
uv run manage.py startapp accounts
```

### Installing `Django` apps

Once the apps have been created they need to be 'installed' so `django` may use them (e.g., make migrations for its models).
Apps are installed by adding their names to the list of installed apps on `django_project/settings.py`.

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'my_new_app1',
    'my_new_app2',
]
```

## `Django` shell

The `django` shell allows to test our `django` modules, models, etc. without having to import everything manually.
To launch it, execute

```bash
uv run manage.py shell [-v 2]
```

where the optional `-v 2` sets the level of verbosity.

## How to use `UUID4` instead of `int`s [^django-uuid]

```python
import uuid
from django.db import models


class MyUUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
```

When the model is then created it must be filled with key-value pairs and the id field must be omitted.

## How to modify the `User` model (the authentication model) [^django-custom-user-model]

We need to import `django`'s abstract class for the authenticating user: `AbstractUser`:

```python
from django.contrib.auth.models import AbstractUser
```

Then we define the User model inheriting from that class, we can use a different name to highlight that it is not the built-in `User` model:

```python
class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
```

As this is the model that will be used for authentication, we'll need to state it in `settings.py`.

```python
AUTH_USER_MODEL = "accounts.CustomUser"
```

And the database will have to be remade and migrations applied.

## References

[^django-custom-user-model]: Django documentation - Customizing User
    [docs.djangoproject.com/en/6.0/topics/auth/customizing/#substituting-a-custom-user-model](https://docs.djangoproject.com/en/6.0/topics/auth/customizing/#substituting-a-custom-user-model)
[^django-uuid]: Django documentation - Model field reference
    [docs.djangoproject.com/en/6.0/ref/models/fields/#uuidfield](https://docs.djangoproject.com/en/6.0/ref/models/fields/#uuidfield)

[^djangoproject-postgres]: Django documentation - postgresql notes
    [docs.djangoproject.com/en/6.0/ref/databases/#postgresql-notes](https://docs.djangoproject.com/en/6.0/ref/databases/#postgresql-notes)
