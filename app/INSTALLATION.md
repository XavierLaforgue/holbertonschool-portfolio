# `animize_eat` installation guide

This application has been dockerized.
The setup instructions provided below have been written for and tested on `Ubuntu-22.04`, but they are expected to work on any Unix-based system.

## Prerequisites

To install/run `animize-eat` you need the docker engine and CLI, i.e., the following terminal commands should return the installed version.

```bash
docker --version
docker compose version
```

If anything other than the program version is output then install docker (e.g., [docker.com/get-started/](https://docs.docker.com/get-started/)) before resuming this guide.

The application has been tested with:

```bash
Docker version 29.32.1, build a5c7197
Docker Compose version v5.1.0
```

and it is known to require `Docker Compose V2+`.

## Start guide

### 1. Clone repository

Clone the repository to the desired directory:

```bash
git clone --branch main https://github.com/XavierLaforgue/holbertonschool-portfolio.git ./desired-directory
cd desired-directory/app
```

### 2. Provide environment file (back-end)

Use the provided `back-end/.env.dev.example` to create a private `back-end/.env.dev` file the backend (Django) will actually use.

#### 2.1. Secret key

Provide a secret key for Django to use for all cryptographic needs (secure sessions, cookies, tokens, etc).
A random key could be generated, e.g.,

- using Python:

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

- or openSSL:

```bash
openssl rand -base64 50
```

#### 2.2. Database configuration

Provide the desired database configuration.

### 3. Provide environment file (front-end)

Use the provided `front-end/animize_eat/.env.dev.example` to create a private `front-end/animize_eat/.env.dev` file the front-end (`React`) will actually use.

<!-- ### 4. Import media files

No image broker (object storage, e.g., `S3`) has been implemented yet, Django is still in charge of delivering them.
As to not upload the media files to `GitHub`, they are provided in the google drive: [drive.google.com/drive/folders/](https://drive.google.com/drive/folders/1tCYiEiYwLagJAN0OKQOdKivf30HSud_F?usp=sharing).
Download the media directory into the back-end directory so the resulting structure is:

```bash
|_backend/
    |-accounts/
    |_...
    |-config/
    |_...
    |-media/
    |   |_avatars/
    |       |_...
    |_ .env.dev, Dockerfile.dev, manage.py, download_media.sh, ...
```

Alternatively, use the provided bash script: `download_media.sh` making sure it has execution permissions (still from `app/`):

```bash
cd back-end
chmod +x download_media.sh
./download_media.sh
cd ..
```

**Warning**: the script is slow and will not work if the folder contains more than 50 files. -->

<!-- Drafted below -->

### 5. Build and start services

```bash
docker compose -f compose.prod.yml up --build -d --scale back-end=3
```

```bash
docker compose  # Docker Compose CLI
-f compose.prod.yml  # use compose.prod.yml as the config file instead of the default
up  # create and start all services defined in that file
--build  # rebuild images from Dockerfiles before starting
-d  # detached mode: runs containers in the background
--scale back-end=3  # launch 3 instances of the back-end service
```

To build image and launch container with the composed app run:

```bash
docker compose --env-file .env.combined.dev -f compose.dev.yaml up --build
```

**Note:** the variables provided by `--env-file .env.combined.dev` are only available to docker-compose itself (for variable substitution in the compose file), but they are now also passed into the backend container via the `environment` section in compose.dev.yaml.

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
