# `animize_eat` installation guide

There are two ways to run the application:

| | [A. Docker](#a-docker-production-like) | [B. Local development](#b-local-development) |
| --- | --- | --- |
| Use it to | run the app as it runs in production | work on the code (hot reload) |
| You install | Docker only | Python/`uv`, Node.js, PostgreSQL |
| Services | PostgreSQL, Django + Gunicorn, React build, Nginx, all in containers | Django dev server and Vite dev server on your machine |
| App URL | `http://localhost` | `http://localhost:5173` |

Both start with an **empty database**: only the reference data the app
needs (difficulties, statuses, unit kinds, units) and an admin user are
created. To try the app with some content, add test data with the
[seed script](#test-data-optional).

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

Port `80` of your machine must be free (see
[Troubleshooting](#port-80-is-already-in-use) otherwise).

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

## B. Local development

### Prerequisites

- [`uv`](https://docs.astral.sh/uv/getting-started/installation/): Python
  package manager. It installs the right Python version (3.13) by itself.
- [Node.js](https://nodejs.org/) `20.19+` or `22.12+` (required by Vite 7)
  and `npm`.
- A local [PostgreSQL](https://www.postgresql.org/download/) server and
  `sudo` rights (to create the database).

Tested with `uv 0.12.5`, Node.js `20.19.3` and PostgreSQL `18`.

### First setup

#### 1. Back-end (`back-end/`)

```bash
cd back-end
cp .env.dev.example .env.dev
```

Edit `back-end/.env.dev`:

- `SECRET_KEY`: generate one as in [Docker step 1](#1-create-the-environment-file).
- `DB_NAME`, `DB_USER`, `DB_PW`: the database, role and password to
  create. Keep `DB_HOST=localhost` and `DB_PORT=5432`.
- `ADMIN_EMAIL`, `ADMIN_PW`: the superuser to create (leave one empty to
  be asked for it instead).

Install the dependencies, then create the database:

```bash
uv sync
bash scripts/destroy_initialize_postgres.sh
```

The script asks for your `sudo` password, creates the role and the
database, applies the migrations, adds the reference data and creates the
superuser (details in [`scripts/README.md`](back-end/scripts/README.md)).

#### 2. Front-end (`front-end/`)

```bash
cd ../front-end
cp .env.dev.example .env.development
npm ci
```

`npm ci` ("clean install") is a standard `npm` command: it installs exactly
the versions recorded in `package-lock.json`, so everybody gets the same
dependencies. It deletes `node_modules/` first and stops with an error if
`package.json` and `package-lock.json` disagree. (`npm install`, by
contrast, may update `package-lock.json`: use it only to add or upgrade a
dependency.)

`npm run dev` loads `.env.development` automatically. Its default
`VITE_API_BASE_URL=http://localhost:8000` points to the Django dev server.

### Run

Use two terminals:

```bash
# Terminal 1, in back-end/
uv run manage.py runserver   # API on http://localhost:8000/api/, admin on http://localhost:8000/admin/

# Terminal 2, in front-end/
npm run dev                  # app on http://localhost:5173
```

Open [http://localhost:5173](http://localhost:5173). Stop the servers with
`Ctrl+C`.

### After pulling changes

```bash
cd back-end && uv sync && uv run manage.py migrate
cd ../front-end && npm ci
```

### Change the models

```bash
uv run manage.py makemigrations   # creates files in <app>/migrations/
uv run manage.py migrate
```

Commit the new migration files with the model changes: the Docker
`back-end` and other developers need them to create the same tables.

### Reset the database

Run `bash scripts/destroy_initialize_postgres.sh` again from `back-end/`
(⚠️ deletes all local data).

---

## Test data (optional)

`back-end/scripts/seed_data.py` creates 4 test users with recipes, drafts
and saved recipes, through the API, so the app has some content to try.
It only needs `python3` and a running app (A or B), and can be run several
times:

```bash
cd back-end
python3 scripts/seed_data.py                                   # Docker
python3 scripts/seed_data.py --base-url http://localhost:8000  # local development
```

Then log in with e.g. `seed.user1@animize.example` / `Itadakimasu-2026!`.
See [`scripts/README.md`](back-end/scripts/README.md) for details. To
remove the test data, reset the database.

---

## Automated tests

The back-end has API tests (`recipes/tests.py`, `accounts/tests.py`): the
test cases of the recipe publication, the access rules and the account
deletion. Django creates an empty test database, runs the tests, then
deletes it: your data is not touched.

```bash
# Docker, from app/ (the app must be running)
docker compose -f compose.prod.yml exec back-end uv run manage.py test

# Local development, from back-end/
uv run manage.py test
```

Locally, the database user needs the right to create a database. The
reset script gives it to a user it creates; for an older user, give it
once with `sudo -u postgres psql -c 'ALTER ROLE "<DB_USER>" CREATEDB;'`
(`<DB_USER>`: the value in `back-end/.env.dev`). Without it, the tests
stop with `permission denied to create database`.

---

## Troubleshooting

### Port 80 is already in use

`up` fails with "port is already allocated" or "address already in use".
Either stop the program using port 80, or use another port: in
`compose.prod.yml`, change `"80:80"` to e.g. `"8080:80"`, add
`http://localhost:8080` to `DJANGO_CSRF_TRUSTED_ORIGINS` in
`back-end/.env.prod` (needed to log in to the admin site), run
`up -d` again and open `http://localhost:8080`.

### `env file .../back-end/.env.prod not found`

Create it (see [Docker step 1](#1-create-the-environment-file)). Run the
Compose commands from `app/`.

### `back-end` keeps restarting

Look at its logs: `docker compose -f compose.prod.yml logs back-end`.

- `password authentication failed`: `DB_*` and `POSTGRES_*` do not match,
  or `POSTGRES_*` were changed after the first start. Fix `.env.prod`,
  then [reset everything](#reset-everything) (or set the old values back).
- Missing variable / `SECRET_KEY` errors: check `.env.prod` against
  `.env.prod.example`.

### `Cannot reach http://localhost` (seed script)

The app is not running, or runs elsewhere: start it, or pass the right
`--base-url` (`http://localhost:8000` for local development,
`http://localhost:8080` if you changed the Docker port).
