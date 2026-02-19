#!/usr/bin/bash

# To be executed from the Django-project directory (back-end/), e.g.,
# ```bash
# bash ./scripts/destroy_initialize_postgres.sh
# ```

# Add details of the database to the local environment from an
# environment file:
export $(grep '^DB_USER=' .env.dev)
export $(grep '^DB_HOST=' .env.dev)
export $(grep '^DB_PORT=' .env.dev)
export $(grep '^DB_NAME=' .env.dev)

# Drop the database:
echo -e "Dropping postgres database ${DB_NAME}..."
echo -e "Database owner password (${DB_USER}) will be requested."
dropdb -U $DB_USER -h $DB_HOST -p $DB_PORT $DB_NAME 

# Remove all files with '.py' file extension in a 'migrations/'
# directory two levels below the project directory, i.e.,
# `back-end/*/migrations/`, except those that start with an underscore
# (_). The --force option is so no error is thrown if there are no
# files to delete.
echo "Removing migrations files..."
rm --verbose --force */migrations/[!_]*.py 

# Create database and assign the Django user as its owner.
# This uses the postgres user which is the default user of postresql
# databases and has no password, but needs to match with the user
# executing the command (hence the `sudo -u postgres`).
echo -e "Creating database $DB_NAME with owner $DB_USER..."
sudo -u postgres createdb --owner=$DB_USER $DB_NAME

# Create initial migrations for the models defined in the project:
echo "Creating migration files..."
uv run manage.py makemigrations
# Perform said migrations:
echo "Migrating models to database schema..."
uv run manage.py migrate

# Use details of the superuser from the environment file:
export $(grep '^ADMIN_USER=' .env.dev)
export $(grep '^ADMIN_EMAIL=' .env.dev)
# Create a superuser (admin user) for the django server
echo "Creating superuser '$ADMIN_USER' with email '${ADMIN_EMAIL}'..."
echo "Password for the new superuser will be requested:" 
uv run manage.py createsuperuser --username=$ADMIN_USER --email=$ADMIN_EMAIL
