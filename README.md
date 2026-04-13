# End-of-the-year project - Holberton School: `animize_eat`

Final portfolio project for the Holberton School web developer program.
In the scope of this program, its students are required to carry out a project in its entirety: from ideation to delivery of the completed web-based software product.
As one of the students, I decided to develop an recipe-sharing platform where users create, publish, and save recipes inspired by anime.

## Author

Xavier Laforgue — [GitHub](https://github.com/XavierLaforgue)

## Project Stages

| Stage | Title                                  | Report                                             |
| ----- | -------------------------------------- | -------------------------------------------------- |
| 1     | Team formation, brainstorming, and MVP | [Stage 1 Report](project-reports/stage1_report.md) |
| 2     | Project planning                       | [Stage 2 Report](project-reports/stage2_report.md) |
| 3     | Technical documentation                | [Stage 3 Report](project-reports/stage3_report.md) |
| 4     | MVP development and execution          | [Stage 4 Report](project-reports/stage4_report.md) |
| 5     | Project closure and landing page       | [Stage 5 Report](project-reports/stage5_report.md) |

## MVP Scope

- User registration (signup) and login: email-based authentication, JWT in cookies for authorization
- Recipe CRUD with status-change workflow: **Draft** -> **Ready** -> **Published**
- Recipe with: steps, ingredients, and photo gallery (1 main + up to 4 extras)
- Save copy of other users' published recipes as immutable snapshots
- Public recipe feed
- Responsive UI

## Tech Stack

| Layer              | Technology                                                                    |
| ------------------ | ----------------------------------------------------------------------------- |
| Front-end          | React 19.2, Vite 7.3, TypeScript 5.9, Tailwind CSS 4.2, React Router DOM 7.13 |
| Back-end           | Python 3.13, Django 6.0, Django REST Framework 3.16, PostgreSQL 18.1          |
| Authorization      | JWT in cookies (drf-simpleJWT 5.5)                                            |
| Infrastructure     | Docker Compose, Nginx (reverse proxy + load balancer), Gunicorn               |
| Package management | npm (front-end), uv (back-end)                                                |

## Architecture

Nginx serves the React SPA and proxies `/api/` requests to scalable Django/Gunicorn replicas via round-robin load balancing.
Static and media files are served directly from Docker volumes.

See the [Production Architecture diagram](app/docs/diagrams.md#production-architecture).

## Key Technical Decisions

1. **Cookie-based JWT**: reduces XSS attack surface since tokens are not accessible via JavaScript (httpOnly migration in progress).
2. **Abstract base models for snapshots**: `RecipeBase`, `StepBase`, and `RecipeIngredientBase` are inherited by both mutable recipes and immutable saved copies, keeping the schema DRY while enforcing immutability.
3. **UUID primary keys**: prevents ID enumeration, makes records merge-safe across environments.
4. **Nginx as single entry point**: handles SPA routing (`try_files` fallback), round-robin load balancing across back-end replicas, and efficient static file delivery.

## Documentation

| Document | Description |
| -------- | ----------- |
| [Developer Guide](app/README.md) | Architecture, API overview, dev commands |
| [Installation Guide](app/INSTALLATION.md) | Docker setup, environment configuration |
| [Diagrams](app/docs/diagrams.md) | ER, class, architecture, auth flow, user flow |
| [Contributing](app/CONTRIBUTING.md) | Contribution guidelines |
| [Changelog](app/CHANGELOG.md) | Version history |
| [Contributors](app/CONTRIBUTORS.md) | Project contributors |
| [License](app/LICENSE) | MIT license |
