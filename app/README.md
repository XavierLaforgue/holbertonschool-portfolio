# animize_eat — Developer Guide

Technical documentation for developers who want to understand, run, or contribute to the project.

## Quick Start

1. Clone the repository
2. Follow the [Installation Guide](INSTALLATION.md)
3. Open `http://localhost` in your browser

## Project Structure

```text
app/
├── back-end/          # Django 6 + DRF REST API
├── front-end/         # React 19 + Vite SPA
├── nginx/             # Reverse proxy configuration
├── docs/              # Diagrams and reference notes
├── compose.prod.yml   # Docker Compose production config
└── INSTALLATION.md    # Setup instructions
```

## Architecture

Nginx is the single entry point. It serves the React SPA, proxies API requests to scalable Django/Gunicorn replicas (round-robin), and serves static/media files directly from shared Docker volumes.

See the [Production Architecture diagram](docs/diagrams.md#production-architecture) and [Development Architecture diagram](docs/diagrams.md#development-architecture).

### Frontend

- **Router:** React Router DOM with `createBrowserRouter`
- **Auth state:** React Context (`AuthProvider`) — no external state library
- **API layer:** Centralized fetch wrapper (`src/lib/api.ts`) with automatic 401 refresh/retry
- **Components:** Feature-based folders under `src/components/`
- **Path alias:** `@` maps to `src/`
- **Styling:** Tailwind CSS 4

### Backend

- **Django apps:** `core` (UUID base model), `accounts` (auth/users), `recipes` (recipes/steps/photos), `ingredients` (ingredients/units), `animes` (stub)
- **Custom user model:** `CustomUser` with UUID PK and email as `USERNAME_FIELD`, plus a one-to-one `Profile`
- **Auth:** `CookieJWTAuthentication` — access token (5 min), refresh token (1 day), stored in cookies
- **Snapshot pattern:** Abstract base models (`RecipeBase`, `StepBase`, `RecipeIngredientBase`) allow creating both mutable recipes and immutable saved copies
- **Validation:** Ingredient unit validation ensures the unit's kind matches the ingredient's `allowed_unit_kinds`

## Data Model

The database uses UUID primary keys throughout (via `core.UUIDModel`). Recipes have a status workflow (Draft → Ready → Published) with validation gates at each transition. Saving another user's recipe creates an immutable snapshot (separate tables) preserving the original state.

See the [ER diagram](docs/diagrams.md#entity-relationship-diagram) and [Class diagram](docs/diagrams.md#class-diagram).

## API Overview

All endpoints are under `/api/`. The DRF browsable API is available at `/api/` when `DEBUG=True`.

| Prefix                                        | Purpose                          |
| --------------------------------------------- | -------------------------------- |
| `POST /api/token/`                            | Login (obtain JWT)               |
| `POST /api/token/refresh/`                    | Refresh access token             |
| `POST /api/token/logout/`                     | Clear auth cookies               |
| `GET /api/me/`                                | Current user info                |
| `/api/accounts/user_models/`                  | User CRUD                        |
| `/api/accounts/profile_models/`               | User profiles                    |
| `/api/recipes/recipe_models/`                 | Recipe CRUD, status changes      |
| `/api/recipes/{id}/steps/`                    | Recipe steps                     |
| `/api/recipes/{id}/photos/`                   | Recipe photos                    |
| `/api/recipes/recipe_models/{id}/save-copy/`  | Save recipe as immutable copy    |
| `/api/recipes/savedrecipe_models/`            | List saved recipes               |
| `/api/ingredients/ingredient_models/`         | Ingredients catalog              |
| `/api/ingredients/unit_models/`               | Measurement units                |
| `/api/ingredients/unitkind_models/`           | Unit categories (weight/volume/count) |

## User Flow & Auth Flow

See the [User Flow diagram](docs/diagrams.md#user-flow) and [Authentication Flow diagram](docs/diagrams.md#authentication-flow).

## Development Commands

### Frontend (`front-end/`)

```bash
npm run dev        # Start Vite dev server (localhost:5173)
npm run build      # TypeScript check + production build
npm run lint       # ESLint
npm run format     # Prettier (ts, tsx, css, json)
```

### Backend (`back-end/`)

```bash
uv run manage.py runserver          # Start Django dev server
uv run manage.py migrate            # Apply migrations
uv run manage.py makemigrations     # Create migrations
uv run manage.py createsuperuser    # Create admin user
uv add <package>                    # Add dependency
uv sync                             # Sync virtualenv from lockfile
```

Seed data commands:

```bash
uv run manage.py create_difficulties
uv run manage.py create_recipe_statuses
uv run manage.py create_unit_kinds
uv run manage.py create_units
```

## Environment Variables

- **Backend:** Uses `DJANGO_ENV` (default `dev`) to load `.env.<DJANGO_ENV>` via `python-dotenv`. See `.env.dev.example` and `.env.prod.example` for required variables.
- **Frontend:** Uses `.env.development` (loaded by `npm run dev`) with `VITE_` prefix. See `.env.dev.example` and `.env.prod.example`. The Docker production build gets `VITE_API_BASE_URL` from a build argument in `compose.prod.yml`.
- **Docker production:** All env vars injected via `compose.prod.yml` from `.env.prod`. Django does not load a `.env` file in production.

Full setup details in the [Installation Guide](INSTALLATION.md).

## Roadmap / Known Limitations

- No test suite or CI/CD pipeline yet
- Media served locally by Nginx (no S3/CDN)
- `animes` app is a stub (planned feature)
- Cookie-based JWT tokens are not yet `httpOnly` (migration planned)

## License

MIT — see [LICENSE](LICENSE)
