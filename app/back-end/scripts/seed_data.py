#!/usr/bin/env python3
"""Fill a running animize_eat instance with test users and recipes.

This script is for TESTING ONLY. It is never run automatically: a fresh
installation starts with an empty database (apart from the reference data
that `entrypoint.sh` / the management commands create: difficulties,
statuses, unit kinds and units).

It talks to the app exclusively through the public REST API, exactly like
the front-end does. This way every request goes through the same
validation (serializers, permission checks, status transitions) as a real
user's request, and the script also works against the Docker setup without
access to the database.

It only uses the Python standard library, so any Python >= 3.10 can run it
(no `uv sync` or `pip install` needed):

    python3 scripts/seed_data.py                                # Docker (Nginx on port 80)
    python3 scripts/seed_data.py --base-url http://localhost:8000  # local dev server

What it creates (skipping anything that already exists, so it is safe to
run several times):
    - 4 users (seed.user1@animize.example ... seed.user4@animize.example,
      all with the password in SEED_PASSWORD) with a filled-in profile
    - 2 published recipes per user (with ingredients and steps)
    - 1 draft recipe per user
    - 2 saved copies per user (of other users' published recipes)
"""

import argparse
import http.cookiejar
import json
import sys
import urllib.error
import urllib.request

# ---------------------------------------------------------------------------
# Seed data
# ---------------------------------------------------------------------------

# Shared password for every seed user. It is public (it is in this file), so
# never run this script against a real, publicly reachable deployment.
SEED_PASSWORD = "Itadakimasu-2026!"

# `.example` is a reserved top-level domain: these addresses can never
# belong to a real person.
EMAIL_TEMPLATE = "seed.user{n}@animize.example"

USERS = [
    {
        "display_name": "ramen_ronin",
        "bio": "Will cross any village for a good bowl of noodles.",
        "favorite_anime_custom": "Naruto",
        "favorite_meal": "Miso ramen",
        "location": "Lyon",
    },
    {
        "display_name": "bento_witch",
        "bio": "Delivering comfort food by broom since forever.",
        "favorite_anime_custom": "Kiki's Delivery Service",
        "favorite_meal": "Herring and pumpkin pie",
        "location": "Bordeaux",
    },
    {
        "display_name": "katsu_skater",
        "bio": "Eats katsudon only after winning. Wins a lot.",
        "favorite_anime_custom": "Yuri!!! on Ice",
        "favorite_meal": "Katsudon",
        "location": "Grenoble",
    },
    {
        "display_name": "moving_castle_cook",
        "bio": "Cooks breakfast on a fire demon. Bacon included.",
        "favorite_anime_custom": "Howl's Moving Castle",
        "favorite_meal": "Bacon and eggs",
        "location": "Nantes",
    },
]

# Each recipe belongs to the user at index `author` in USERS.
# Ingredients are (name, quantity, unit symbol); the unit symbols must exist
# in the database (they come from the `create_units` management command).
# Step durations use Django's DurationField format "HH:MM:SS" (or None).
RECIPES = [
    {
        "author": 0,
        "title": "Ninja Village Miso Ramen",
        "anime_custom": "Naruto",
        "description": "A rich miso broth with chashu, egg and naruto "
                       "fishcake, worthy of a future Hokage.",
        "difficulty": "Medium",
        "portions": 2,
        "estimated_time_minutes": 45,
        "ingredients": [
            ("Ramen noodles", 250, "g"),
            ("Chicken stock", 1, "l"),
            ("White miso paste", 3, "tbsp"),
            ("Pork belly", 300, "g"),
            ("Egg", 2, "pc"),
            ("Naruto fishcake", 4, "slice"),
            ("Spring onion", 1, "bunch"),
        ],
        "steps": [
            ("Sear the pork belly, then simmer it in the stock.", "00:30:00"),
            ("Soft-boil the eggs, peel them and cut them in half.",
             "00:06:30"),
            ("Whisk the miso into a ladle of hot stock, then pour it back.",
             None),
            ("Cook the noodles, drain them and assemble the bowls.",
             "00:03:00"),
        ],
    },
    {
        "author": 0,
        "title": "Hidden Leaf Onigiri",
        "anime_custom": "Naruto",
        "description": "Simple salted rice balls for long missions.",
        "difficulty": "Easy",
        "portions": 4,
        "estimated_time_minutes": 30,
        "ingredients": [
            ("Short-grain rice", 300, "g"),
            ("Nori sheet", 2, "pc"),
            ("Salt", 1, "pinch"),
            ("Umeboshi", 4, "pc"),
        ],
        "steps": [
            ("Rinse and cook the rice, then let it cool slightly.",
             "00:20:00"),
            ("Wet and salt your hands, shape the rice around an umeboshi.",
             None),
            ("Wrap each rice ball with a strip of nori.", None),
        ],
    },
    {
        "author": 1,
        "title": "Herring and Pumpkin Pot Pie",
        "anime_custom": "Kiki's Delivery Service",
        "description": "Grandma's famous pie, even if some people don't "
                       "like it.",
        "difficulty": "Hard",
        "portions": 6,
        "estimated_time_minutes": 90,
        "ingredients": [
            ("Pumpkin", 500, "g"),
            ("Smoked herring fillet", 300, "g"),
            ("Puff pastry", 2, "pc"),
            ("Heavy cream", 200, "ml"),
            ("Black olive", 12, "pc"),
        ],
        "steps": [
            ("Roast the pumpkin until soft, then mash it with the cream.",
             "00:35:00"),
            ("Layer the pumpkin mash and herring in a pie dish.", None),
            ("Cover with pastry, draw a fish with olives on top.", None),
            ("Bake until golden.", "00:40:00"),
        ],
    },
    {
        "author": 1,
        "title": "Bakery Chocolate Cake",
        "anime_custom": "Kiki's Delivery Service",
        "description": "The birthday cake that saved a rainy delivery day.",
        "difficulty": "Medium",
        "portions": 8,
        "estimated_time_minutes": 60,
        "ingredients": [
            ("Dark chocolate", 200, "g"),
            ("Butter", 150, "g"),
            ("Sugar", 150, "g"),
            ("Egg", 4, "pc"),
            ("Flour", 60, "g"),
        ],
        "steps": [
            ("Melt the chocolate and butter together.", "00:05:00"),
            ("Whisk the eggs and sugar, then fold in the chocolate.", None),
            ("Fold in the flour and bake.", "00:25:00"),
        ],
    },
    {
        "author": 2,
        "title": "Victory Katsudon",
        "anime_custom": "Yuri!!! on Ice",
        "description": "Crispy pork cutlet simmered with egg over rice. "
                       "Only after a gold medal.",
        "difficulty": "Medium",
        "portions": 2,
        "estimated_time_minutes": 40,
        "ingredients": [
            ("Pork loin", 2, "slice"),
            ("Panko", 100, "g"),
            ("Egg", 3, "pc"),
            ("Onion", 1, "whole"),
            ("Dashi", 200, "ml"),
            ("Soy sauce", 2, "tbsp"),
            ("Cooked rice", 400, "g"),
        ],
        "steps": [
            ("Bread the pork with flour, egg and panko, then deep-fry it.",
             "00:08:00"),
            ("Simmer the sliced onion in dashi and soy sauce.", "00:05:00"),
            ("Add the sliced cutlet, pour beaten egg over it and cover.",
             "00:01:30"),
            ("Slide everything over a bowl of rice.", None),
        ],
    },
    {
        "author": 2,
        "title": "Rink-side Pirozhki",
        "anime_custom": "Yuri!!! on Ice",
        "description": "Grandpa's pork and rice buns, a Russian skater's "
                       "favourite.",
        "difficulty": "Hard",
        "portions": 10,
        "estimated_time_minutes": 120,
        "ingredients": [
            ("Flour", 500, "g"),
            ("Milk", 250, "ml"),
            ("Dry yeast", 1, "tbsp"),
            ("Minced pork", 300, "g"),
            ("Cooked rice", 150, "g"),
        ],
        "steps": [
            ("Make a soft yeast dough and let it rise.", "01:00:00"),
            ("Cook the pork and mix it with the rice.", "00:10:00"),
            ("Fill and seal small dough rounds.", None),
            ("Fry until golden on both sides.", "00:06:00"),
        ],
    },
    {
        "author": 3,
        "title": "Fire Demon Bacon and Eggs",
        "anime_custom": "Howl's Moving Castle",
        "description": "Thick bacon and eggs cooked in one pan over a very "
                       "grumpy fire.",
        "difficulty": "Easy",
        "portions": 3,
        "estimated_time_minutes": 15,
        "ingredients": [
            ("Thick-cut bacon", 6, "slice"),
            ("Egg", 6, "pc"),
            ("Bread", 3, "slice"),
        ],
        "steps": [
            ("Lay the bacon in a cold pan and render it slowly.", "00:08:00"),
            ("Crack the eggs between the bacon slices.", "00:04:00"),
            ("Serve straight from the pan with bread.", None),
        ],
    },
    {
        "author": 3,
        "title": "Seaside Ham Ramen",
        "anime_custom": "Ponyo",
        "description": "Instant ramen upgraded with ham, egg and spring "
                       "onion. Do not peek before it is ready.",
        "difficulty": "Easy",
        "portions": 2,
        "estimated_time_minutes": 10,
        "ingredients": [
            ("Instant ramen", 2, "pc"),
            ("Ham", 2, "slice"),
            ("Egg", 2, "pc"),
            ("Spring onion", 1, "stick"),
        ],
        "steps": [
            ("Pour boiling water over the noodles and cover.", "00:03:00"),
            ("Top with ham, a soft-boiled egg and spring onion.", None),
        ],
    },
]

# One unfinished draft per user, so the "Drafts" group of My Recipes is not
# empty. Drafts only get a title.
DRAFT_TITLE = "Work in progress: secret family recipe"

# Each user saves the published recipes with these titles (from other
# users, since saving your own recipe makes little sense).
SAVES = {
    0: ["Victory Katsudon", "Fire Demon Bacon and Eggs"],
    1: ["Ninja Village Miso Ramen", "Seaside Ham Ramen"],
    2: ["Herring and Pumpkin Pot Pie", "Hidden Leaf Onigiri"],
    3: ["Bakery Chocolate Cake", "Rink-side Pirozhki"],
}

TIMEOUT_SECONDS = 15


# ---------------------------------------------------------------------------
# Minimal API client
# ---------------------------------------------------------------------------

class ApiError(Exception):
    """Raised when the API answers with an unexpected status code."""


class ApiClient:
    """One client = one browser-like session (its own cookie jar).

    The back-end authenticates with JWT tokens stored in cookies, so after
    `login()` the cookie jar sends the `access_token` cookie with every
    request, just like the browser does for the front-end.
    """

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar())
        )

    def request(self, method: str, path: str, data=None,
                expected=(200, 201)):
        """Send a JSON request and return (status code, decoded body).

        Raises ApiError if the status code is not in `expected`.
        """
        body = json.dumps(data).encode() if data is not None else None
        req = urllib.request.Request(
            self.base_url + path,
            data=body,
            method=method,
            headers={"Content-Type": "application/json",
                     "Accept": "application/json"},
        )
        try:
            with self.opener.open(req, timeout=TIMEOUT_SECONDS) as resp:
                code, raw = resp.status, resp.read()
        except urllib.error.HTTPError as err:
            # 4xx/5xx answers arrive as exceptions; read their body anyway
            # so we can show the API's error message.
            code, raw = err.code, err.read()
        try:
            payload = json.loads(raw) if raw else None
        except ValueError:
            # Not JSON (e.g. an HTML error page from Nginx or Django).
            payload = raw.decode(errors="replace")[:300]
        if code not in expected:
            raise ApiError(f"{method} {path} -> {code}: {payload}")
        return code, payload

    def login(self, email: str, password: str):
        self.request("POST", "/api/token/",
                     {"email": email, "password": password})


# ---------------------------------------------------------------------------
# Seeding steps
# ---------------------------------------------------------------------------

def log(message: str):
    print(message, flush=True)


def fetch_reference_ids(client: ApiClient):
    """Map difficulty labels and unit symbols to their database ids.

    These rows are created by the management commands (automatically in
    Docker), not by this script.
    """
    _, difficulties = client.request("GET", "/api/recipes/difficulty_models/")
    _, units = client.request("GET", "/api/ingredients/unit_models/")
    difficulty_ids = {d["label"]: d["id"] for d in difficulties}
    unit_ids = {u["symbol"]: u["id"] for u in units}
    if not difficulty_ids or not unit_ids:
        raise ApiError(
            "No difficulties or units found. Run the reference-data "
            "management commands first (see INSTALLATION.md)."
        )
    return difficulty_ids, unit_ids


def ensure_user(base_url: str, n: int, profile: dict) -> ApiClient:
    """Sign the user up (if needed), log in and fill in the profile.

    Returns a client logged in as that user.
    """
    email = EMAIL_TEMPLATE.format(n=n)
    client = ApiClient(base_url)
    # Same request as the front-end sign-up form. A 400 here means the
    # email is already taken, i.e. the user was seeded by a previous run.
    code, _ = client.request(
        "POST", "/api/accounts/user_models/",
        {"email": email, "password": SEED_PASSWORD},
        expected=(201, 400),
    )
    client.login(email, SEED_PASSWORD)
    if code == 201:
        _, me = client.request("GET", "/api/me/")
        client.request("PATCH",
                       f"/api/accounts/profile_models/{me['profile_id']}/",
                       profile)
        log(f"  created user {email} ({profile['display_name']})")
    else:
        log(f"  user {email} already exists, reusing it")
    return client


def create_recipe(client: ApiClient, recipe: dict, difficulty_ids: dict,
                  unit_ids: dict):
    """Create, fill in and publish one recipe, like the front-end editor.

    1. POST creates a blank draft owned by the logged-in user.
    2. PATCH fills in the fields, ingredients and steps.
    3. Status goes Draft -> Ready -> Published (the API only publishes
       Ready recipes that have a title, an anime, ingredients and steps).
    """
    _, draft = client.request("POST", "/api/recipes/recipe_models/", {})
    recipe_url = f"/api/recipes/recipe_models/{draft['id']}/"
    client.request("PATCH", recipe_url, {
        "title": recipe["title"],
        "anime_custom": recipe["anime_custom"],
        "description": recipe["description"],
        "difficulty": difficulty_ids[recipe["difficulty"]],
        "portions": recipe["portions"],
        "estimated_time_minutes": recipe["estimated_time_minutes"],
        "ingredients": [
            {"ingredient_name": name, "quantity": quantity,
             "unit": unit_ids[symbol]}
            for name, quantity, symbol in recipe["ingredients"]
        ],
        "steps": [
            {"number": number, "description": description,
             "duration": duration}
            for number, (description, duration)
            in enumerate(recipe["steps"], start=1)
        ],
    })
    client.request("PATCH", recipe_url + "status/", {"value": "Ready"})
    client.request("PATCH", recipe_url + "status/", {"value": "Published"})
    log(f"    published '{recipe['title']}'")


def create_draft(client: ApiClient):
    _, draft = client.request("POST", "/api/recipes/recipe_models/", {})
    client.request("PATCH", f"/api/recipes/recipe_models/{draft['id']}/",
                   {"title": DRAFT_TITLE})
    log(f"    created draft '{DRAFT_TITLE}'")


def seed_recipes(client: ApiClient, author: int, difficulty_ids: dict,
                 unit_ids: dict):
    """Create the user's recipes and draft, skipping existing titles."""
    _, mine = client.request("GET", "/api/me/recipes/")
    existing = {r["title"] for group in ("draft", "ready", "published")
                for r in mine[group]}
    for recipe in RECIPES:
        if recipe["author"] != author:
            continue
        if recipe["title"] in existing:
            log(f"    '{recipe['title']}' already exists, skipping")
            continue
        create_recipe(client, recipe, difficulty_ids, unit_ids)
    if DRAFT_TITLE in existing:
        log(f"    draft '{DRAFT_TITLE}' already exists, skipping")
    else:
        create_draft(client)


def seed_saves(client: ApiClient, titles: list, published: dict):
    """Save copies of other users' published recipes, skipping existing
    ones."""
    _, mine = client.request("GET", "/api/me/recipes/")
    already_saved = {r["title"] for r in mine["saved"]}
    for title in titles:
        if title in already_saved:
            log(f"    '{title}' already saved, skipping")
            continue
        recipe = published[title]
        # Same payload as the front-end "Save" button. The server sets the
        # saver, original recipe/author and the "Saved" status itself.
        client.request("POST", "/api/recipes/savedrecipe_models/", {
            "original_recipe": recipe["id"],
            "title": recipe["title"],
            "anime_custom": recipe["anime_custom"],
            "description": recipe["description"],
            "difficulty": recipe["difficulty"]["id"],
            "portions": recipe["portions"],
            "estimated_time_minutes": recipe["estimated_time_minutes"],
        })
        log(f"    saved '{title}'")


def main():
    parser = argparse.ArgumentParser(
        description="Fill a running animize_eat instance with test data "
                    "through its REST API.")
    parser.add_argument(
        "--base-url", default="http://localhost",
        help="URL of the running app: http://localhost for Docker "
             "(default), http://localhost:8000 for the Django dev server.")
    args = parser.parse_args()

    log(f"Seeding {args.base_url} ...")
    anonymous = ApiClient(args.base_url)
    try:
        difficulty_ids, unit_ids = fetch_reference_ids(anonymous)

        log("Users and recipes:")
        clients = []
        for index, profile in enumerate(USERS):
            client = ensure_user(args.base_url, index + 1, profile)
            seed_recipes(client, index, difficulty_ids, unit_ids)
            clients.append(client)

        # The public recipe list only contains published recipes. Use it
        # to find the ids (and current fields) of the recipes to save.
        _, public = anonymous.request("GET", "/api/recipes/recipe_models/")
        published = {r["title"]: r for r in public}

        log("Saved copies:")
        for index, client in enumerate(clients):
            # Access tokens only live 5 minutes: log in again so a slow run
            # does not fail half-way.
            client.login(EMAIL_TEMPLATE.format(n=index + 1), SEED_PASSWORD)
            log(f"  {USERS[index]['display_name']}:")
            seed_saves(client, SAVES[index], published)
    except urllib.error.URLError as err:
        sys.exit(f"Cannot reach {args.base_url} ({err.reason}). "
                 "Is the app running? Check --base-url.")
    except ApiError as err:
        sys.exit(f"API error: {err}")

    log("Done. Log in with any seed user, e.g. "
        f"{EMAIL_TEMPLATE.format(n=1)} / {SEED_PASSWORD}")


if __name__ == "__main__":
    main()
