#!/usr/bin/bash
set -euo pipefail
# flags breakdown:
# - set -e: exit immediately if any command returns a non‑zero status.
# - set -u: treat use of unset variables as an error.
# - set -o pipefail: make pipelines fail if any part fails.

# To be executed from the Django-project directory (back-end/), e.g.,
# ```bash
# bash ./scripts/destroy_initialize_postgres.sh
# ```

ENV_FILE=.env.dev
if [ ! -f "$ENV_FILE" ]; then
    echo "No ${ENV_FILE} found. Run this script from back-end/ after" \
         "copying .env.dev.example to .env.dev." >&2
    exit 1
fi

# Read one variable from the environment file.
# `export $(grep ...)` would break on lines with an inline comment, like
# `DB_PORT=5432  # default PostgreSQL port`, so instead: keep what follows
# the first `=`, then remove an inline comment (whitespace + `#`), trailing
# whitespace and surrounding quotes. (Values must therefore not contain
# " #".)
env_value() {
    grep -E "^$1=" "$ENV_FILE" | tail -n 1 | cut -d '=' -f 2- \
        | sed -E -e 's/[[:space:]]+#.*$//' -e 's/[[:space:]]+$//' \
                 -e 's/^"(.*)"$/\1/' -e "s/^'(.*)'$/\1/"
}

DB_NAME=$(env_value DB_NAME)
DB_USER=$(env_value DB_USER)
DB_PW=$(env_value DB_PW)
# Optional: without them, the admin user is created interactively.
# (`|| true` because grep fails, and so would the script, when the
# variable is missing.)
ADMIN_EMAIL=$(env_value ADMIN_EMAIL || true)
ADMIN_PW=$(env_value ADMIN_PW || true)

# Run a command as the `postgres` superuser. It is the default admin role
# of PostgreSQL and has no password: it uses "peer" authentication, i.e.
# the Linux user running the command must have the same name (hence
# `sudo -u postgres`). The `cd /` avoids a harmless "could not change
# directory" warning, since `postgres` cannot read our home directory.
as_postgres() {
    (cd / && sudo -u postgres "$@")
}

# Drop the database (no error if it does not exist yet).
echo "Dropping database ${DB_NAME} (if it exists)..."
as_postgres dropdb --if-exists "$DB_NAME"

# Create the role Django connects with, unless it already exists.
# The SQL is read from stdin (heredoc) so psql can substitute its
# variables safely: :"user" is quoted as an identifier and :'pw' as a
# string literal (psql does not substitute variables in `-c` commands).
# CREATEDB lets Django create its temporary database when running tests.
role_exists=$(as_postgres psql -tA -v user="$DB_USER" <<'SQL'
SELECT 1 FROM pg_roles WHERE rolname = :'user';
SQL
)
if [ "$role_exists" = "1" ]; then
    echo "Role ${DB_USER} already exists (its password is left unchanged)."
else
    echo "Creating role ${DB_USER} with the password DB_PW from ${ENV_FILE}..."
    as_postgres psql -q -v ON_ERROR_STOP=1 -v user="$DB_USER" \
        -v pw="$DB_PW" <<'SQL'
CREATE ROLE :"user" LOGIN CREATEDB PASSWORD :'pw';
SQL
fi

# Create the database and make the Django role its owner.
echo "Creating database ${DB_NAME} with owner ${DB_USER}..."
as_postgres createdb --owner="$DB_USER" "$DB_NAME"

# Create the tables from the migration files. They are committed with
# the code (never deleted or regenerated here), so every machine creates
# exactly the same tables.
echo "Applying migrations..."
uv run manage.py migrate

# Reference data the app needs to work (idempotent commands).
echo "Adding reference data..."
uv run manage.py create_difficulties
uv run manage.py create_recipe_statuses
uv run manage.py create_unit_kinds
uv run manage.py create_units

# Create a superuser (admin user) for the Django admin, the same way the
# Docker entrypoint does: non-interactively from ADMIN_EMAIL/ADMIN_PW
# when both are set, otherwise by asking for them.
if [ -n "$ADMIN_EMAIL" ] && [ -n "$ADMIN_PW" ]; then
    echo "Creating superuser '${ADMIN_EMAIL}'..."
    DJANGO_SUPERUSER_PASSWORD="$ADMIN_PW" \
        uv run manage.py createsuperuser --noinput --email "$ADMIN_EMAIL"
else
    echo "Creating superuser (you will be asked for its details)..."
    uv run manage.py createsuperuser
fi
