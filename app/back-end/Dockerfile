# =============================================================================
# Back-end Dockerfile: Django REST API using Gunicorn
# =============================================================================
#
# This Dockerfile builds the production image for the Django back-end.
#
#   - Gunicorn           Production-grade WSGI server (Django's runserver is
#                        for development only).
#
# Build from: ./back-end
# =============================================================================

# ---------- base image ----------
# The Python version is passed as a build argument so it stays in sync
# with the `requires-python` field in pyproject.toml.
# Set in compose.prod.yml -> build -> args -> PYTHON_VERSION.
ARG PYTHON_VERSION=3.13
FROM python:${PYTHON_VERSION}-slim
# Slim Debian image: small footprint but still has the system libraries
# that psycopg (PostgreSQL driver) and Pillow (image processing) need.

# Prevent Python from writing .pyc files and enable unbuffered output
# so logs appear immediately in `docker logs`.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies required by:
#   - psycopg: libpq-dev (PostgreSQL client library headers)
#   - Pillow:  libjpeg-dev, zlib1g-dev (JPEG and PNG support)
#   - build:   gcc (needed for packages that require C extensions)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        # gcc 
        libpq-dev libjpeg-dev zlib1g-dev && \
    rm -rf /var/lib/apt/lists/*
    # delete APT package index cache

# ---------- install uv (Python package manager) ----------
# Using the official method: copy the binary from the uv Docker image.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# ---------- set working directory ----------
WORKDIR /app

# ---------- install Python dependencies ----------
# Copy only dependency files first so Docker can cache this layer.
# The layer is rebuilt only when pyproject.toml or uv.lock change,
# NOT when application code changes; this speeds up rebuilds.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# ---------- copy application code ----------
COPY . .

# ---------- collect Django static files ----------
# Django's collectstatic gathers all static assets (admin CSS/JS, app
# static files) into STATIC_ROOT so Nginx can serve them directly
# instead of Django handling every static file request.
# SECRET_KEY is needed by Django to start, but collectstatic does not
# use it. We pass a dummy value since the real one is injected at runtime.
RUN DJANGO_ENV=prod SECRET_KEY=dummy-build-key \
    uv run manage.py collectstatic --noinput

# ---------- create non-root user ----------
RUN addgroup --system app && \
    adduser --system --ingroup app app
# Security best practice: the app runs as an unprivileged user so a
# container escape would not grant root access on the host.

# Give the app user ownership of directories it needs to write to:
#   - media/       : user-uploaded files (recipe photos)
#   - staticfiles/ : collected static assets
RUN mkdir -p /app/media && chown -R app:app /app/media
# create directory if it doesn't exist and recursively change ownership
# to the user and group app. Syntax: `chown user:group /path/to/directory`
RUN chown -R app:app /app/staticfiles
# recursively change ownership of the static files to the user and
# group app.

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Switch to the non-root user for runtime
USER app

# ---------- entrypoint ----------
# The entrypoint script runs migrations and seeds reference data,
# then hands off to the CMD (Gunicorn).
ENTRYPOINT ["/app/entrypoint.sh"]

# ---------- default command ----------
# Gunicorn configuration:
#   --bind 0.0.0.0:8000 : listen on all interfaces inside the container
#   --workers 2          : suitable for a small MVP (general rule: 2*CPU+1,
#                          but we keep it low for a single-server deployment)
CMD ["uv", "run", "gunicorn", "config.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "2"]
