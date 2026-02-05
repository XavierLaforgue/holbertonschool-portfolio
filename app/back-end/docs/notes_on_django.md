# Notes on `django`
<!-- TODO: write bash script to initialize `django` project-->
Once installed `django`, e.g., with
```
uv add django
```
We can initialize a ne django project with
```
uv run django-admin startproject my_project .
```
This will generate the file tree for a basic `django` project.

The `django` server is launched with
```
uv run manage.py runserver
```
which may require migrations, i.e.,
```
uv run manage.py migrate
```

If successful, the new `django` server will be running on `localhost:8000` and an `admin` panel will be available at `localhost:8000/admin`.
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
