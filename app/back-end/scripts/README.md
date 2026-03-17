# Database Seeding Scripts

This directory contains scripts for initializing and populating the database with very bad AI-generated seed data.

## Scripts

### `seed_data.py`

API-based database seeding script that creates a complete dataset for testing and development.

**What it creates:**

- 5 users with personalized profiles (names, bios, favorite anime, dietary preferences, etc.)  
- 25+ recipes (5 per user) with:
  - Steps (3-6 per recipe)
  - Ingredients (5-10 per recipe)
  - Realistic anime-inspired titles and descriptions
- 25+ saved recipes (5 per user, copied from other users' recipes)
- Foundational data: unit kinds, units, ingredients, difficulty levels

**Usage:**

```bash
# Start the Django development server first
uv run manage.py runserver

# In another terminal, run the seeding script  
uv run python scripts/seed_data.py

# Custom base URL (if server is running on different port)
uv run python scripts/seed_data.py --base-url http://localhost:9000

# Show help
uv run python scripts/seed_data.py --help
```

**Features:**

- ✅ Idempotent - Can be run multiple times safely (skips existing data)
- ✅ Comprehensive logging - Shows progress and any errors
- ✅ Complete mock data - Uses Faker library for realistic user data
- ✅ Anime-themed - Recipes inspired by popular anime shows
- ✅ API-based - Tests your REST API endpoints

**Output example:**

```bash
============================================================
STARTING DATABASE SEEDING
============================================================
API Base URL: http://localhost:8000

[INFO] Step 1: Setting up foundational data
[INFO] Creating unit kinds...
[INFO]   Created unit kind: Weight
[INFO]   Created unit kind: Volume
[INFO]   Created unit kind: Piece/Count
[INFO] Creating units...
[INFO]   Created unit: kilogram (kg)
...
[INFO] Step 2: Creating users and profiles
[INFO]   Created user: Jonathan Moreno (jonathan.moreno1@animize.example)
[INFO]   Updated profile for Jonathan Moreno
...
[INFO] Step 3: Creating recipes with steps and ingredients
[INFO]   Created recipe: Homemade Gotcha Pork Roast
[INFO]     Added 5 steps
[INFO]     Added 8 ingredients
...
[INFO] Step 4: Creating saved recipes
[INFO]   Saved recipe: Tonkotsu Ramen
...
============================================================
SEEDING SUMMARY
============================================================
  Users: 5
  Profiles: 5
  Recipes: 25
  Saved Recipes: 25
  Steps: 110+
  Ingredients: 41
  Units: 15
  Unit Kinds: 3
  Recipe Ingredients: 200+
  Difficulties: 4
============================================================
```

**Requirements:**

- Django development server must be running
- Database must be migrated (`uv run manage.py migrate`)
- Python packages: `requests`, `faker` (automatically installed with `uv`)

**Notes:**

- All users have the password: `TestPassword123!`
- Email format: `firstname.lastname{N}@animize.example`
- The script creates data via API endpoints (no direct database access)
- Can be run multiple times - will reuse existing foundational data

---

### `destroy_initialize_postgres.sh`

**⚠️ DESTRUCTIVE** - Drops the database, removes migrations, and recreates from scratch.

**Usage:**

```bash
bash scripts/destroy_initialize_postgres.sh
```

**What it does:**

1. Drops the existing Postgres database
2. Removes all migration files (except `__init__.py`)
3. Creates a fresh database with proper ownership
4. Generates new migrations
5. Applies migrations
6. Creates a Django superuser

**Requirements:**

- Must be run from the `back-end/` directory
- Requires `.env.dev` file with database configuration
- Requires `sudo` access for Postgres operations

---

## Workflow

### Fresh Start with Seed Data

```bash
# 1. Reset database (optional, if starting fresh)
bash scripts/destroy_initialize_postgres.sh

# 2. Start development server  
uv run manage.py runserver &

# 3. Seed the database
uv run python scripts/seed_data.py

# 4. Access the application
# API Root: http://localhost:8000/api/
# Admin Panel: http://localhost:8000/admin/
```

### Adding More Seed Data

The seeding script is designed to be run multiple times. Each run will:

- Skip duplicate foundational data (units, ingredients, difficulties)
- Create 5 new users with unique emails
- Create 25 new recipes
- Create 25 new saved recipes

---

## Test Credentials

After running `seed_data.py`, you can log in with any created user:

**Format:** `firstname.lastname{1-5}@animize.example` / `TestPassword123!`

**Example users:**

- `jonathan.moreno1@animize.example`
- `cathy.gonzales2@animize.example`  
- `nicole.may3@animize.example`
- etc.

Check the script output or query the API to see actual created users:

```bash
curl http://localhost:8000/api/accounts/user_models/ | python -m json.tool
```

---

## Troubleshooting

### "Connection refused" errors

- Make sure Django development server is running: `uv run manage.py runserver`
- Check  the correct port in `--base-url` argument

### "Failed to create X" warnings

- Normal if running script multiple times (indicates data already exists)
- Script will fetch and reuse existing data automatically

### "500 Server Error" when saving recipes

- Check Django server logs for detailed error messages
- Ensure all migrations are applied: `uv run manage.py migrate`
- Verify database connection in `.env.dev`

### No data created

- Check script output for error messages
- Verify API endpoints are accessible: `curl http://localhost:8000/api/`
- Ensure proper permissions (authentication may be required if changed from default)

---

## Development

To modify the seed data:

1. **Add more recipes:** Edit `RECIPE_IDEAS` list in `seed_data.py`
2. **Add more ingredients:** Edit `INGREDIENT_LIST` in `seed_data.py`
3. **Change anime titles:** Edit `ANIME_TITLES` in `seed_data.py`
4. **Adjust user count:** Modify `range(1, 6)` in `main()` function
5. **Adjust recipes per user:** Modify `range(5)` in recipe creation loop

The script is well-commented and structured for easy modification.
