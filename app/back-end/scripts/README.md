# Back-end scripts

Helper scripts for development and testing. They are **not** part of the
application: the Docker image does not contain them (see `../.dockerignore`)
and nothing runs them automatically.

Run them from the `back-end/` directory.

## `destroy_initialize_postgres.sh`: (re-)create the local dev database

**⚠️ DESTRUCTIVE:** drops the local development database (the one named in
`.env.dev`), with all its data.

```bash
bash scripts/destroy_initialize_postgres.sh
```

It:

1. drops the database `DB_NAME` if it exists
2. creates the role `DB_USER` (password `DB_PW`) if it does not exist
3. creates the database `DB_NAME`, owned by `DB_USER`
4. applies the migrations
5. adds the reference data (difficulties, statuses, unit kinds, units)
6. creates the superuser: from `ADMIN_EMAIL`/`ADMIN_PW` if both are set
   in `.env.dev`, otherwise interactively

Use it for the first local setup or to start again from an empty database.
It only concerns local development; the Docker setup initializes its own
database (see `INSTALLATION.md`).

**Requirements:** a local PostgreSQL server, `sudo` rights (the script acts
as the `postgres` superuser), `uv`, and a `.env.dev` file.
