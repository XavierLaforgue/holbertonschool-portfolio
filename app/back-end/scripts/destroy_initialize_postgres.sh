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
DB_HOST=$(env_value DB_HOST)
DB_PORT=$(env_value DB_PORT)

# Drop the database:
echo -e "Dropping postgres database ${DB_NAME}..."
echo -e "Database owner password (${DB_USER}) will be requested."
dropdb -U $DB_USER -h $DB_HOST -p $DB_PORT $DB_NAME 

# Create database and assign the Django user as its owner.
# This uses the postgres user which is the default user of postresql
# databases and has no password, but needs to match with the user
# executing the command (hence the `sudo -u postgres`).
echo -e "Creating database $DB_NAME with owner $DB_USER..."
sudo -u postgres createdb --owner=$DB_USER $DB_NAME

# Create the tables from the migration files. They are committed with
# the code (never deleted or regenerated here), so every machine creates
# exactly the same tables.
echo "Applying migrations..."
uv run manage.py migrate

# Use details of the superuser from the environment file:
ADMIN_USER=$(env_value ADMIN_USER)
ADMIN_EMAIL=$(env_value ADMIN_EMAIL)
# Create a superuser (admin user) for the django server
echo "Creating superuser '$ADMIN_USER' with email '${ADMIN_EMAIL}'..."
echo "Password for the new superuser will be requested:" 
# uv run manage.py createsuperuser --username=$ADMIN_USER
# --email=$ADMIN_EMAIL
uv run manage.py createsuperuser --email=$ADMIN_EMAIL
uv run manage.py create_difficulties
uv run manage.py create_recipe_statuses
uv run manage.py create_unit_kinds
uv run manage.py create_units
