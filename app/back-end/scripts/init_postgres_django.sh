#!/usr/bin/bash

export $(grep '^DB_USER=' .env.dev)
export $(grep '^DB_NAME=' .env.dev)
sudo -u postgres createdb --owner=$DB_USER $DB_NAME

uv run manage.py makemigrations
uv run manage.py migrate

uv run manage.py createsuperuser --username=admin --email=admin@example.com
