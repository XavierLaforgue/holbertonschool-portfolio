# Installation instructions

## Cloning repository

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
```
