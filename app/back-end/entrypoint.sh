#!/bin/sh
# =============================================================================
# Back-end entrypoint script
# =============================================================================
#
# This script runs every time the container starts (before the CMD).
# It applies any pending database migrations so the schema is always
# up-to-date when the application boots.
#
# Why a separate script instead of putting this in the Dockerfile?
#   - Migrations need a running database, which is only available at
#     runtime (not at build time).
#   - This keeps the Dockerfile focused on building the image.
# =============================================================================

set -e  # Exit immediately if any command fails

echo "Applying database migrations..."
uv run manage.py migrate --noinput

# Create the Django superuser if ADMIN_EMAIL and ADMIN_PW are set.
# DJANGO_SUPERUSER_PASSWORD is the env var Django's createsuperuser
# reads in --noinput mode. We map it from ADMIN_PW for consistency
# with the rest of our env file.
# The `|| true` ensures this doesn't fail if the user already exists
# (e.g., on subsequent container restarts).
if [ -n "$ADMIN_EMAIL" ] && [ -n "$ADMIN_PW" ]; then
    echo "Creating superuser (if not exists)..."
    DJANGO_SUPERUSER_PASSWORD="$ADMIN_PW" \
        uv run manage.py createsuperuser \
            --noinput \
            --email "$ADMIN_EMAIL" \
        || true
fi

# Populate the database with system-required data (difficulties,
# statuses, unit kinds and units).
# These commands are idempotent (they skip existing rows), so they are
# safe to run on every container start, not just the first time.
echo "Populating reference data..."
uv run manage.py create_difficulties
uv run manage.py create_recipe_statuses
uv run manage.py create_unit_kinds
uv run manage.py create_units

# Copy the static files of this image (Django admin and DRF CSS/JS) into
# the shared `backend_static` volume that Nginx serves, so a rebuilt image
# also updates them (collectstatic only copies new or changed files).
# Several back-end replicas share the volume and start at the same time:
# `flock /app/staticfiles` makes them take turns (it locks the folder
# itself, so no lock file ends up being served by Nginx).
echo "Collecting static files..."
flock /app/staticfiles uv run manage.py collectstatic --noinput

echo "Starting server..."
# Execute the CMD passed to the container (Gunicorn by default).
# `exec` replaces this shell process with Gunicorn so that signals
# (SIGTERM, SIGINT) are forwarded correctly for graceful shutdown.
exec "$@"
