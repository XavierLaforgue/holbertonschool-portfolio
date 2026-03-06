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

In the shell we can create instances of objects, retrieve them from and store them in the database,

```python
# create an instance of CustomUser
new_user = CustomUser(username='new_user1', email='new_user_1@example.com', password='visible_password')
# retrieve `CustomUser` objects from the database
stored_users = CustomUser.objects.all()
# store new user in the database
new_user.save()
```

## How to use `UUID4` as default `id` instead of `int` in the base model [^django-uuid] [^django-abstract]

Create a new app (e.g., `core`), as one of its models, the abstract class that overwrites the id field in the base model:

```python
import uuid
from django.db import models

class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    class Meta:
        abstract = True
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

And the database will have to be remade, the superuser recreated, and migrations made and applied.

### Adding relationships to `CustomUser`

To add the `CustomUser` in a relationship use, instead of `CustomUser` directly,

```python
user = models.ForeignKey(settings.AUTH_USER_MODEL,
                         on_delete=models.CASCADE)
```

<!-- #### Signals sent by the `CustomUser` model [^django-user-signal]

When connecting to signals sent by the user model, we need to specify the custom model using the AUTH_USER_MODEL setting. For example:

```python
from django.conf import settings
from django.db.models.signals import post_save

def post_save_receiver(sender, instance, created, **kwargs):
    pass

post_save.connect(post_save_receiver, sender=settings.AUTH_USER_MODEL)
``` -->

## Django models and validation of fields/attributes

## Django choices

In Django `choices` is always an iterable of 2‑tuples: `(value_stored_in_DB, human_readable_label)`.

The first element is what gets saved in the database.
For example, in

```python
class Unit(UUIDModel):
    WEIGHT = "weight"
    KIND_CHOICES = [(WEIGHT, "Weight")]
    kind = models.CharField(choices=KIND_CHOICES)
```

what you compare in code is

```python
if unit.kind == Unit.WEIGHT: 
    ...
```

The second element (`"Weight"`) is what Django shows in forms/admin/HTML as the label.

## Django `CharField` vs `TextField`

- `CharField`:

You must give `max_length`.
Stored as something like `VARCHAR(max_length)` in the DB.
Slightly more efficient and usually indexed; good for short strings (names, titles, codes, choices).
Often rendered as a single‑line `<input>` in forms.

- `TextField`:

No `max_length` requirement (can still be added for validation).
Stored as a large `TEXT/CLOB` type in the DB.
Used for long, free‑form text (descriptions, notes, comments).
Usually rendered as a multi‑line `<textarea>` in forms.
Rule of thumb: "short, structured, maybe used in filters or choices" -> `CharField`; "long, free text" -> `TextField`.

## Django REST Framework

### Installation

- Install the dependance.

```bash
uv add djangorestframework
```

- Install it as a django app.

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    ...
]
```

### Additions of the DRF

The DRF uses serializers, urls, and viewsets (instead of regular Django views).

#### Serializers
<!-- TODO: Describe how to use serializers taking advantage of DRF extensions -->
#### URLs
<!-- TODO: Describe how to use url_patterns taking advantage of the DRF Router extension -->
#### Viewsets
<!-- TODO: Describe how to use views taking advantage of DRF viewsets extensions -->

## CORS (Cros-Origin Resource Sharing)

Requests from other origins are blocked by default for security.
However, we need to allow the front-end application to query the API.
For this, we need to setup CORS headers.

### CORS installation for django [^django-cors-freecodecamp]

To install the dependency:

```bash
uv add django-cors-headers
```

The app also needs to be installed into django:

```python
INSTALLED_APPS = [
    ...
    'corsheaders',
]
```

and its middleware added:

```python
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
]
```

### CORS allowed origins

We need to include a list of allowed origins that will pass CORS.

```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
]
```

The list should not be hardcoded though, it should be kept in the environment.

### CORS credentials

When using authentication credentials such as tokens or cookies, we also need:

```python
CORS_ALLOW_CREDENTIALS = True
```

## CSRF (Cross-Site Request Forgery)

It is a type of vulnerability that is addressed with their own tokens.
When implemented, the server also needs to have a list of origins that are trusted to perform requests.

```python
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
]
```

The list should not be hardcoded though, it should be kept in the environment.

## Further topics to research

### Checks

`django`'s management utility has a `check` command, research what it is for.

```bash
uv run manage.py checks
```

## Search/Filtering

Se can implement search/fitering on the backend by offering query-parameter--based requests to the front-end.
The DRF facilitates this by supplying the filters module, which offers several filtering "backends" and it's implemented by just adding them to the viewsets.
It should be noted that these query-parameters--augmentation of endpoints is only applied to list endpoints (`/recipes/`), not to details endpoints (`/recipes/{recipe_id}`).

`SearchFilter` and `SortingFilter` are two common filters.

`SearchFilter` offers text-based search to the viewset.
The corresponding viewset field `search_fields` sets the fields of the view on which text search will be applied.

`OrderingFilter` offers results sorting (ordering).
The corresponding viewset field `ordering_fields` set the fields of the view according to which the results will be ordered and `ordering`  allows to set the default ordering field.

An example implementation:

```python
class RecipeViewSet(rest_framework.viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "anime"]
    ordering_fields = ["published_at", "estimated_time_minutes"]
    ordering = "published_at"
```

```python
    search_fields = ["ingredient__name", "recipe__title", "unit__name"]
    ordering_fields = ["created_at", "updated_at", "recipe__published_at"]
    ordering = "created_at"
```

## References

[^django-custom-user-model]: Django documentation - Customizing User
    [docs.djangoproject.com/en/6.0/topics/auth/customizing/#substituting-a-custom-user-model](https://docs.djangoproject.com/en/6.0/topics/auth/customizing/#substituting-a-custom-user-model)

[^django-uuid]: Django documentation - Model field reference
    [docs.djangoproject.com/en/6.0/ref/models/fields/#uuidfield](https://docs.djangoproject.com/en/6.0/ref/models/fields/#uuidfield)

[^django-abstract]: Django documentation - Modifying base model
    [docs.djangoproject.com/en/6.0/topics/db/models/#abstract-base-classes](https://docs.djangoproject.com/en/6.0/topics/db/models/#abstract-base-classes)

[^djangoproject-postgres]: Django documentation - postgresql notes
    [docs.djangoproject.com/en/6.0/ref/databases/#postgresql-notes](https://docs.djangoproject.com/en/6.0/ref/databases/#postgresql-notes)

[^django-cors-freecodecamp]: Django CORS policy - freeCodeCamp
    [freecodecamp.org/news/how-to-enable-cors-in-django/](https://www.freecodecamp.org/news/how-to-enable-cors-in-django/)
<!-- [^django-user-signal]: Django documentation - signals
    [docs.djangoproject.com/en/6.0/topics/signals/](https://docs.djangoproject.com/en/6.0/topics/signals/) -->
