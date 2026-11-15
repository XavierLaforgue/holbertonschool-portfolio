# `animize_eat` installation guide

This guide explains how to run the application with Docker.

It starts with an **empty database**: only the reference data the app
needs (difficulties, statuses, unit kinds, units) and an admin user are
created.

The instructions were written for and tested on `Ubuntu 22.04` (on WSL2);
they are expected to work on any Unix-based system. Unless stated
otherwise, every command is run from the `app/` directory.

## Get the code

```bash
git clone --branch main https://github.com/XavierLaforgue/holbertonschool-portfolio.git ./desired-directory
cd desired-directory/app
```

---

## A. Docker (production-like)

### Prerequisites

The Docker engine and the Docker Compose plugin (V2 or later). Both
commands must print a version:

```bash
docker --version
docker compose version
```

Otherwise install Docker first (e.g., [docs.docker.com/get-started/](https://docs.docker.com/get-started/)).
On Windows with WSL, start Docker Desktop and enable its WSL integration.

Tested with `Docker version 29.9.2` and `Docker Compose version v5.6.1`.

Port `80` of your machine must be free.

> **Tip:** every Compose command below needs `-f compose.prod.yml`. To avoid
> typing it, run `export COMPOSE_FILE=compose.prod.yml` once per terminal
> and drop the `-f compose.prod.yml` part.

### First start (from scratch)

#### 1. Create the environment file

All the configuration (Django, database, admin user) comes from
`back-end/.env.prod`, which is private (git-ignored). Create it from the
template:

```bash
cp back-end/.env.prod.example back-end/.env.prod
```

Then edit `back-end/.env.prod`:

- **`SECRET_KEY`**: a long random string Django uses for all cryptographic
  needs (sessions, cookies, tokens, ...). Generate one, e.g.:

  ```bash
  python3 -c "import secrets; print(secrets.token_urlsafe(50))"
  # or
  openssl rand -base64 50
  ```

- **Database**: choose a strong password and write it in both `DB_PW`
  (used by Django) and `POSTGRES_PASSWORD` (used by the PostgreSQL
  container to create the database). Likewise, `DB_NAME` must equal
  `POSTGRES_DB` and `DB_USER` must equal `POSTGRES_USER`. Keep
  `DB_HOST=db` (the name of the database service in `compose.prod.yml`) and
  `DB_PORT=5432`.
  If a value contains a dollar sign (`$`), write it twice (`$$`): Docker
  Compose would otherwise treat it as a variable.
- **Admin user**: `ADMIN_EMAIL` and `ADMIN_PW` are the credentials of the
  Django superuser created on the first start (you log in to the admin
  site and to the app with the email). Leave one of them empty to skip it
  and [create the superuser by hand](#create-a-superuser-by-hand) later.
- **Hosts** (`DJANGO_ALLOWED_HOSTS`, `DJANGO_CORS_ALLOWED_ORIGINS`,
  `DJANGO_CSRF_TRUSTED_ORIGINS`): the defaults work for
  `http://localhost`. On a server, add its domain name (and `https://` URL).

No front-end environment file is needed: the front-end image gets its only
setting (`VITE_API_BASE_URL`) from `compose.prod.yml`.

> PostgreSQL only reads `POSTGRES_*` the very first time it starts, when
> its data volume is empty. Changing them afterwards does not change the
> existing database (see [Reset everything](#reset-everything)).

#### 2. Build and start

```bash
docker compose -f compose.prod.yml up --build -d
```

```bash
docker compose  # Docker Compose CLI
-f compose.prod.yml  # use compose.prod.yml as the config file instead of the default
up  # create and start all services defined in that file
--build  # build the images from the Dockerfiles before starting
-d  # detached mode: run the containers in the background
```

The first build takes a few minutes. Then, on start:

1. `db` initializes the PostgreSQL database (first start only).
2. `back-end` waits for `db` to be ready, applies the migrations, creates
   the superuser (if `ADMIN_EMAIL` and `ADMIN_PW` are set), adds the
   reference data, copies Django's static files (admin CSS/JS) into a
   shared volume and starts Gunicorn. This runs on every start and
   skips whatever already exists (on later starts, the log shows
   `CommandError: Error: That email is already taken.` for the
   superuser: this is expected and harmless).
3. `front-end` copies the built React app into a shared volume (on every
   start, so a rebuild always replaces the previous files).
4. `nginx` serves the app on port 80.

#### 3. Check that it works

```bash
docker compose -f compose.prod.yml ps                # all 4 services "Up" (front-end only idles, to keep its volume mounted)
docker compose -f compose.prod.yml logs -f back-end  # wait for "Starting server..." and "Listening at", then Ctrl+C
```

Then open:

- the app: [http://localhost](http://localhost) (sign up to create a regular user)
- the Django admin: [http://localhost/admin/](http://localhost/admin/) (log in with `ADMIN_EMAIL` / `ADMIN_PW`)

### Daily use (after the first build)

| To | Run |
| --- | --- |
| Start the app (no rebuild) | `docker compose -f compose.prod.yml up -d` |
| Stop the app (keeps the containers) | `docker compose -f compose.prod.yml stop` |
| Stop and remove the containers (keeps the data) | `docker compose -f compose.prod.yml down` |
| See the status | `docker compose -f compose.prod.yml ps` |
| Follow the logs (all services, or one) | `docker compose -f compose.prod.yml logs -f [back-end]` |
| Open a Django shell | `docker compose -f compose.prod.yml exec back-end uv run manage.py shell` |

The database, uploaded photos and static files live in named Docker
volumes, so they survive `stop`, `down` and rebuilds (but not `down -v`).

#### Apply code changes (e.g., after `git pull`)

Rebuild the images and restart the services:

```bash
docker compose -f compose.prod.yml up --build -d
```

When they start, `front-end` and `back-end` copy the new front-end build
and static files into their volumes, and `back-end` applies the new
migrations. The data (database, uploaded photos) is kept.

#### Run several back-end instances

Nginx distributes the API requests between all `back-end` containers
(round-robin):

```bash
docker compose -f compose.prod.yml up -d --scale back-end=3
docker compose -f compose.prod.yml restart nginx
```

Nginx looks up the `back-end` containers when it starts, hence the restart
after changing the number of instances.

#### Create a superuser by hand

```bash
docker compose -f compose.prod.yml exec back-end uv run manage.py createsuperuser
```

#### Reset everything

⚠️ **Deletes all data** (database, uploaded photos):

```bash
docker compose -f compose.prod.yml down -v
docker compose -f compose.prod.yml up --build -d
```

`-v` removes the named volumes, so the next start creates a new, empty
database from the current `back-end/.env.prod`.

---

## `uv` project setup

```python
```

## Environment variables

Create `.env` file and replace the default (insecure) data.
Password may not be provided since they need to be input when prompted anyway.

## Initialize database

```bash
./scripts/destroy_initialize_postgres.sh
```

## Add model data

```python
uv run manage.py create_difficulties
uv run manage.py create_recipe_statuses
uv run manage.py create_unit_kinds
uv run manage.py create_units
```
