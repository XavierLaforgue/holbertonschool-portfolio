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
