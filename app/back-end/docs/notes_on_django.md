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
uv run manage.py createsuperuser

```

## Django apps

The Django framework uses the concept of apps to divide the reponsibilities.
According to the models I'll need, [class diagram](../../../project-reports/stage3_report.md#class-diagram), I consider the following apps:

| App         | Model(s)                                                                                     | View(s)                                                                                          |
|-------------|----------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------|
| Accounts    | CustomUser, Profile                                                                          | LoginView, LogoutView, CheckConnectionView, UserListView, UserView, ProfileListView, ProfileView |
| Recipes     | Recipe (with enum models: Difficulty and RecipeStatus), Step, RecipePhotos, RecipeIngredient | RecipeListView, RecipeView, StepListView, StepView, RecipePhotosView                             |
| Ingredients | Ingredient (with enum model Unit)                                                            | IngredientListView, IngredientView                                                               |
| Anime       | Anime, AnimeDBVersion                                                                        | AnimeListView, AnimeView                                                                         |

We start apps on `Django` with

```bash
uv run django-admin startapp accounts
```

## References

[^djangoproject-postgres]: Django documentation - postgresql notes
[docs.djangoproject.com/en/6.0/ref/databases/#postgresql-notes](https://docs.djangoproject.com/en/6.0/ref/databases/#postgresql-notes)
