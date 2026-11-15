# Back-end scripts

Helper scripts for development and testing. They are **not** part of the
application: the Docker image does not contain them (see `../.dockerignore`)
and nothing runs them automatically.

Run them from the `back-end/` directory.

## `seed_data.py`: fill the app with test data

A fresh installation has an empty database: only the reference data
(difficulties, statuses, unit kinds and units) and the admin user are
created. To try the app without creating everything by hand, this script
adds test users and recipes **through the REST API**, like the front-end
does, so all API validation applies (publishing rules, authorship, ...).

It only needs Python 3.10+ (standard library only, no `uv sync`) and a
running app:

```bash
# Docker setup (Nginx on http://localhost)
python3 scripts/seed_data.py

# Local development (Django dev server)
python3 scripts/seed_data.py --base-url http://localhost:8000
```

It creates:

- 4 users, `seed.user1@animize.example` to `seed.user4@animize.example`,
  all with the password `Itadakimasu-2026!`, with a filled-in profile
- 2 published recipes per user, with ingredients and steps
- 1 draft recipe per user
- 2 saved copies per user, of other users' recipes

It skips whatever already exists (users by email, recipes and saved copies
by title), so running it twice does not duplicate anything. To remove the
test data, reset the database (see `INSTALLATION.md`).

> The seed password is public. Never run this script against a deployment
> that is reachable from the internet.

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
