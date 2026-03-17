#!/usr/bin/env python3
"""
API-based database seeding script for animize_eat backend.

Creates a complete dataset using REST API endpoints:
- 5 users with personalized profiles
- 25 recipes (5 per user) with steps and ingredients
- 25 saved recipes (5 per user) copied from other users
- Foundational data: unit kinds, units, ingredients, difficulties

Usage:
    uv run python scripts/seed_data.py [--base-url URL] [--clean]
"""

import argparse
import random
import sys
from datetime import date, timedelta
from typing import Any, Dict, List, Optional

import requests
from faker import Faker

# Initialize Faker for generating realistic mock data
fake = Faker()

# Configuration
DEFAULT_BASE_URL = "http://localhost:8000"
API_TIMEOUT = 10  # seconds


# ============================================================================
# MOCK DATA CONSTANTS
# ============================================================================

# Anime titles for recipe inspiration
ANIME_TITLES = [
    "Food Wars! Shokugeki no Soma",
    "Restaurant to Another World",
    "Today's Menu for the Emiya Family",
    "Sweetness & Lightning",
    "Ms. Koizumi Loves Ramen Noodles",
    "Toriko",
    "Yakitate!! Japan",
    "Ben-To",
    "Isekai Izakaya: Japanese Food From Another World",
    "Campfire Cooking in Another World",
    "The Disastrous Life of Saiki K",
    "Silver Spoon",
    "Gourmet Girl Graffiti",
    "Cooking Papa",
    "Delicious in Dungeon",
    "Laid-Back Camp",
    "Flying Witch",
    "My Hero Academia",
    "One Piece",
    "Naruto",
]

# Recipe ideas with anime inspiration
RECIPE_IDEAS = [
    ("Gotcha Pork Roast", "Food Wars! Shokugeki no Soma", "Juicy roasted pork with a sweet glaze that melts in your mouth"),
    ("Chaliapin Steak Don", "Food Wars! Shokugeki no Soma", "Tender steak on rice with caramelized onions"),
    ("Rainbow Terrine", "Food Wars! Shokugeki no Soma", "Colorful layered vegetable terrine"),
    ("Soma's Transforming Furikake Gohan", "Food Wars! Shokugeki no Soma", "Rice with special seasoning that evolves with each bite"),
    ("Beef Stew from Another World", "Restaurant to Another World", "Rich, hearty beef stew that transcends dimensions"),
    ("Chicken Curry with Naan", "Restaurant to Another World", "Aromatic curry with fluffy homemade naan"),
    ("Hamburg Steak Deluxe", "Restaurant to Another World", "Classic Japanese-style hamburg with demi-glace sauce"),
    ("Nikujaga (Meat and Potatoes)", "Today's Menu for the Emiya Family", "Comforting Japanese home-style dish"),
    ("Tamagoyaki (Sweet Rolled Omelette)", "Today's Menu for the Emiya Family", "Perfectly layered sweet Japanese omelette"),
    ("Salmon Onigiri", "Today's Menu for the Emiya Family", "Hand-formed rice balls with grilled salmon"),
    ("Shoyu Ramen", "Ms. Koizumi Loves Ramen Noodles", "Classic soy sauce ramen with rich broth"),
    ("Tonkotsu Ramen", "Ms. Koizumi Loves Ramen Noodles", "Creamy pork bone broth with thin noodles"),
    ("Miso Ramen with Butter Corn", "Ms. Koizumi Loves Ramen Noodles", "Rich miso broth topped with butter and sweet corn"),
    ("Takoyaki (Octopus Balls)", "Delicious in Dungeon", "Crispy outside, creamy inside octopus fritters"),
    ("Okonomiyaki (Savory Pancake)", "Delicious in Dungeon", "Japanese savory pancake with various toppings"),
    ("Katsudon (Pork Cutlet Rice Bowl)", "Ben-To", "Crispy pork cutlet over rice with egg and sauce"),
    ("Tempura Assortment", "Flying Witch", "Light and crispy battered vegetables and seafood"),
    ("Matcha Ice Cream Parfait", "Sweetness & Lightning", "Layered dessert with matcha ice cream and sweet red beans"),
    ("Chicken Karaage", "My Hero Academia", "Japanese fried chicken, perfectly crispy"),
    ("Curry Rice (Japanese Style)", "One Piece", "Comforting Japanese curry with vegetables"),
    ("Onigiri Assortment", "Laid-Back Camp", "Various rice ball flavors perfect for camping"),
    ("Miso Soup with Tofu", "Silver Spoon", "Simple, warming soup with silky tofu"),
    ("Gyoza (Pot Stickers)", "Toriko", "Pan-fried dumplings with savory filling"),
    ("Yakitori Skewers", "Yakitate!! Japan", "Grilled chicken skewers with tare sauce"),
    ("Tonkatsu (Breaded Pork Cutlet)", "Gourmet Girl Graffiti", "Crispy breaded pork with tangy sauce"),
    ("Cream Stew", "Sweetness & Lightning", "White cream stew with chicken and vegetables"),
    ("Oyakodon (Chicken and Egg Bowl)", "Cooking Papa", "Tender chicken and egg over steaming rice"),
    ("Yakisoba Noodles", "Food Wars! Shokugeki no Soma", "Stir-fried noodles with vegetables and meat"),
    ("Sushi Roll Platter", "The Disastrous Life of Saiki K", "Assorted sushi rolls with fresh fish"),
    ("Pancakes with Maple Syrup", "Sweetness & Lightning", "Fluffy pancakes perfect for breakfast"),
    ("Green Tea Mochi", "Flying Witch", "Soft mochi filled with sweet green tea paste"),
    ("Beef Bowl (Gyudon)", "Restaurant to Another World", "Quick beef and onion over rice"),
    ("Dorayaki (Red Bean Pancakes)", "Campfire Cooking in Another World", "Sweet pancakes with red bean filling"),
    ("Udon Noodle Soup", "Ms. Koizumi Loves Ramen Noodles", "Thick wheat noodles in hot broth"),
    ("Fried Rice with Vegetables", "Isekai Izakaya", "Simple yet flavorful fried rice"),
    ("Steamed Pork Buns", "Toriko", "Soft steamed buns with savory pork filling"),
    ("Chawanmushi (Savory Egg Custard)", "Today's Menu for the Emiya Family", "Delicate steamed egg custard"),
    ("Mentaiko Pasta", "Food Wars! Shokugeki no Soma", "Creamy pasta with spicy cod roe"),
    ("Tsukemen (Dipping Ramen)", "Ms. Koizumi Loves Ramen Noodles", "Cold noodles with hot dipping broth"),
    ("Coffee Jelly", "The Disastrous Life of Saiki K", "Refreshing coffee-flavored jelly dessert"),
]

# Common ingredients for Japanese/anime-inspired recipes
INGREDIENT_LIST = [
    "all-purpose flour",
    "rice",
    "soy sauce",
    "miso paste",
    "sake",
    "mirin",
    "rice vinegar",
    "sesame oil",
    "vegetable oil",
    "sugar",
    "salt",
    "black pepper",
    "chicken breast",
    "pork belly",
    "beef chuck",
    "salmon fillet",
    "eggs",
    "butter",
    "milk",
    "heavy cream",
    "onion",
    "garlic",
    "ginger",
    "carrot",
    "potato",
    "scallions",
    "nori (seaweed)",
    "noodles",
    "panko breadcrumbs",
    "cornstarch",
    "dashi stock",
    "tofu",
    "shiitake mushrooms",
    "white mushrooms",
    "bell pepper",
    "cabbage",
    "bok choy",
    "spinach",
    "tomato",
    "cucumber",
    "daikon radish",
]

# Unit data: (name, symbol, kind_label)
UNIT_DATA = [
    # Weight units
    ("kilogram", "kg", "weight"),
    ("gram", "g", "weight"),
    ("pound", "lb", "weight"),
    ("ounce", "oz", "weight"),
    # Volume units
    ("liter", "L", "volume"),
    ("milliliter", "mL", "volume"),
    ("cup", "cup", "volume"),
    ("tablespoon", "tbsp", "volume"),
    ("teaspoon", "tsp", "volume"),
    # Count/piece units
    ("piece", "pc", "piece"),
    ("whole", "whole", "piece"),
    ("clove", "clove", "piece"),
    ("slice", "slice", "piece"),
    ("pinch", "pinch", "piece"),
    ("dash", "dash", "piece"),
]

# Difficulty levels
DIFFICULTY_DATA = [
    ("Easy", 1),
    ("Medium", 2),
    ("Hard", 3),
    ("Expert", 4),
]

# Recipe step templates
STEP_TEMPLATES = [
    "Prepare {ingredient} by {action}.",
    "{Action} the {ingredient} {method}.",
    "In a {container}, combine {ingredients}.",
    "Heat {ingredient} in a {container} over {heat} heat.",
    "{Action} for {time} minutes or until {done_state}.",
    "Season with {seasonings} to taste.",
    "Serve hot and garnish with {garnish}.",
    "Let rest for {time} minutes before serving.",
    "Mix thoroughly until {texture} forms.",
    "Bring to a boil, then reduce heat and simmer.",
]


# ============================================================================
# API HELPER FUNCTIONS
# ============================================================================

class APIClient:
    """Helper class for making API requests with consistent error handling."""
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.created_counts = {
            "users": 0,
            "profiles": 0,
            "recipes": 0,
            "saved_recipes": 0,
            "steps": 0,
            "ingredients": 0,
            "units": 0,
            "unit_kinds": 0,
            "recipe_ingredients": 0,
            "difficulties": 0,
        }
    
    def _log(self, message: str, level: str = "INFO"):
        """Simple logging helper."""
        print(f"[{level}] {message}")
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict[str, Any]]:
        """Make GET request to API."""
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.get(url, params=params, timeout=API_TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self._log(f"GET {endpoint} failed: {e}", "ERROR")
            return None
    
    def post(self, endpoint: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Make POST request to API."""
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.post(url, json=data, timeout=API_TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self._log(f"POST {endpoint} failed: {e}", "ERROR")
            if hasattr(e.response, 'text'):
                self._log(f"Response: {e.response.text}", "ERROR")
            return None
    
    def patch(self, endpoint: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Make PATCH request to API."""
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.patch(url, json=data, timeout=API_TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self._log(f"PATCH {endpoint} failed: {e}", "ERROR")
            return None
    
    def print_summary(self):
        """Print summary of created objects."""
        print("\n" + "=" * 60)
        print("SEEDING SUMMARY")
        print("=" * 60)
        for key, count in self.created_counts.items():
            print(f"  {key.replace('_', ' ').title()}: {count}")
        print("=" * 60)


# ============================================================================
# DATA CREATION FUNCTIONS
# ============================================================================

def create_unit_kinds(client: APIClient) -> Dict[str, str]:
    """Create unit kind categories and return mapping of label -> id."""
    client._log("Creating unit kinds...")
    unit_kinds = {}
    
    kinds = [
        ("weight", "Weight"),
        ("volume", "Volume"),
        ("piece", "Piece/Count"),
    ]
    
    for label, descriptive_name in kinds:
        data = {
            "label": label,
            "descriptive_name": descriptive_name,
        }
        result = client.post("/api/ingredients/unitkind_models/", data)
        if result and "id" in result:
            unit_kinds[label] = result["id"]
            client.created_counts["unit_kinds"] += 1
            client._log(f"  Created unit kind: {descriptive_name}")
        else:
            # Try to fetch existing unit kind
            existing = client.get("/api/ingredients/unitkind_models/", {"label": label})
            if existing and len(existing) > 0:
                unit_kinds[label] = existing[0]["id"]
                client._log(f"  Found existing unit kind: {descriptive_name}")
            else:
                client._log(f"  Failed to create or find unit kind: {label}", "WARN")
    
    return unit_kinds


def create_units(client: APIClient, unit_kinds: Dict[str, str]) -> List[Dict[str, Any]]:
    """Create measurement units and return list of created/existing units."""
    client._log("Creating units...")
    units = []
    
    for name, symbol, kind_label in UNIT_DATA:
        if kind_label not in unit_kinds:
            client._log(f"  Skipping unit {name}: kind {kind_label} not found", "WARN")
            continue
        
        data = {
            "name": name,
            "symbol": symbol,
            "kind": unit_kinds[kind_label],
        }
        result = client.post("/api/ingredients/unit_models/", data)
        if result and "id" in result:
            units.append(result)
            client.created_counts["units"] += 1
            client._log(f"  Created unit: {name} ({symbol})")
        else:
            # Try to fetch existing unit
            existing = client.get("/api/ingredients/unit_models/", {"name": name})
            if existing and len(existing) > 0:
                units.append(existing[0])
                client._log(f"  Found existing unit: {name}")
            else:
                client._log(f"  Failed to create or find unit: {name}", "WARN")
    
    return units


def create_ingredients(client: APIClient) -> List[Dict[str, Any]]:
    """Create ingredients and return list of created/existing ingredients."""
    client._log("Creating ingredients...")
    ingredients = []
    
    for name in INGREDIENT_LIST:
        data = {"name": name}
        result = client.post("/api/ingredients/ingredient_models/", data)
        if result and "id" in result:
            ingredients.append(result)
            client.created_counts["ingredients"] += 1
        else:
            # Try to fetch existing ingredient
            existing = client.get("/api/ingredients/ingredient_models/", {"name": name})
            if existing and len(existing) > 0:
                ingredients.append(existing[0])
            else:
                client._log(f"  Failed to create or find ingredient: {name}", "WARN")
    
    client._log(f"  Total ingredients available: {len(ingredients)}")
    return ingredients


def create_difficulties(client: APIClient) -> List[Dict[str, Any]]:
    """Create difficulty levels and return list of created difficulties."""
    client._log("Creating difficulty levels...")
    difficulties = []
    
    for label, value in DIFFICULTY_DATA:
        data = {
            "label": label,
            "value": value,
        }
        result = client.post("/api/recipes/difficulty_models/", data)
        if result and "id" in result:
            difficulties.append(result)
            client.created_counts["difficulties"] += 1
            client._log(f"  Created difficulty: {label} (value: {value})")
        else:
            # Try to fetch existing difficulty
            existing = client.get("/api/recipes/difficulty_models/", {"label": label})
            if existing and len(existing) > 0:
                difficulties.append(existing[0])
                client._log(f"  Found existing difficulty: {label}")
            else:
                client._log(f"  Failed to create or find difficulty: {label}", "WARN")
    
    return difficulties


def get_recipe_statuses(client: APIClient) -> Dict[str, str]:
    """Get existing recipe statuses and return mapping of value -> id."""
    client._log("Fetching recipe statuses...")
    result = client.get("/api/recipes/recipestatus_models/")
    
    if not result:
        client._log("  Failed to fetch recipe statuses", "ERROR")
        return {}
    
    statuses = {}
    for status in result:
        statuses[status["value"]] = status["id"]
        client._log(f"  Found status: {status['value']}")
    
    return statuses


def create_user_with_profile(client: APIClient, index: int) -> Optional[Dict[str, Any]]:
    """Create a user and update their profile with personalized data."""
    # Generate user data
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = f"{first_name.lower()}.{last_name.lower()}{index}@animize.example"
    password = "TestPassword123!"
    
    # Create user
    user_data = {
        "email": email,
        "password": password,
        "first_name": first_name,
        "last_name": last_name,
    }
    
    user = client.post("/api/accounts/user_models/", user_data)
    if not user or "id" not in user:
        client._log(f"  Failed to create user: {email}", "ERROR")
        return None
    
    client.created_counts["users"] += 1
    client._log(f"  Created user: {first_name} {last_name} ({email})")
    
    # Fetch user's profile (auto-created by signal)
    profiles = client.get("/api/accounts/profile_models/", {"user": user["id"]})
    if not profiles or len(profiles) == 0:
        client._log(f"  Profile not found for user {email}", "ERROR")
        return None
    
    profile = profiles[0]
    
    # Update profile with personalized data
    birth_year = random.randint(1985, 2005)
    birth_month = random.randint(1, 12)
    birth_day = random.randint(1, 28)
    birth_date = date(birth_year, birth_month, birth_day).isoformat()
    
    profile_data = {
        "display_name": f"{first_name} {last_name[0]}.",
        "birth_date": birth_date,
        "bio": fake.text(max_nb_chars=200),
        "favorite_anime_custom": random.choice(ANIME_TITLES),
        "favorite_meal": random.choice([recipe[0] for recipe in RECIPE_IDEAS[:20]]),
        "location": fake.city(),
        "dietary_preferences": random.choice([
            "No restrictions",
            "Vegetarian",
            "Pescatarian",
            "Gluten-free",
            "Dairy-free",
        ]),
    }
    
    updated_profile = client.patch(f"/api/accounts/profile_models/{profile['id']}/", profile_data)
    if updated_profile:
        client.created_counts["profiles"] += 1
        client._log(f"  Updated profile for {first_name} {last_name}")
    
    return {
        "user": user,
        "profile": updated_profile or profile,
        "email": email,
        "password": password,
    }


def generate_recipe_steps(recipe_title: str, num_steps: int) -> List[Dict[str, Any]]:
    """Generate mock recipe steps."""
    steps = []
    actions = ["chop", "dice", "mince", "slice", "grate", "mix", "stir", "whisk", "fold"]
    containers = ["pan", "pot", "bowl", "wok", "skillet"]
    heat_levels = ["low", "medium", "high", "medium-high"]
    
    for i in range(1, num_steps + 1):
        if i == 1:
            description = f"Prepare all ingredients and gather necessary equipment for making {recipe_title}."
        elif i == num_steps:
            description = "Serve hot and enjoy your delicious creation!"
        else:
            action = random.choice(actions).capitalize()
            container = random.choice(containers)
            description = f"{action} the ingredients in a {container} over {random.choice(heat_levels)} heat for {random.randint(3, 15)} minutes."
        
        duration_minutes = random.randint(2, 20) if i < num_steps else 0
        
        steps.append({
            "number": i,
            "description": description,
            "duration": f"00:{duration_minutes:02d}:00" if duration_minutes > 0 else None,
        })
    
    return steps


def create_recipe_with_details(
    client: APIClient,
    author_profile_id: str,
    difficulties: List[Dict[str, Any]],
    statuses: Dict[str, str],
    ingredients: List[Dict[str, Any]],
    units: List[Dict[str, Any]],
    recipe_index: int,
) -> Optional[Dict[str, Any]]:
    """Create a complete recipe with steps and ingredients."""
    # Select a recipe idea
    recipe_data = RECIPE_IDEAS[recipe_index % len(RECIPE_IDEAS)]
    title, anime, description = recipe_data
    
    # Add personalization to title
    variations = ["Homemade", "Classic", "Special", "Deluxe", "Ultimate"]
    title = f"{random.choice(variations)} {title}"
    
    # Create recipe
    recipe_payload = {
        "title": title,
        "anime_custom": anime,
        "description": description,
        "portions": random.randint(2, 6),
        "estimated_time_minutes": random.randint(15, 90),
        "author": author_profile_id,
        "difficulty": random.choice(difficulties)["id"] if difficulties else None,
        "status": statuses.get("Draft"),
    }
    
    recipe = client.post("/api/recipes/recipe_models/", recipe_payload)
    if not recipe or "id" not in recipe:
        client._log(f"  Failed to create recipe: {title}", "ERROR")
        return None
    
    client.created_counts["recipes"] += 1
    client._log(f"  Created recipe: {title}")
    
    # Create steps
    num_steps = random.randint(3, 6)
    steps = generate_recipe_steps(title, num_steps)
    
    for step_data in steps:
        step_payload = {
            "recipe": recipe["id"],
            **step_data,
        }
        step = client.post(f"/api/recipes/{recipe['id']}/steps/", step_payload)
        if step:
            client.created_counts["steps"] += 1
    
    client._log(f"    Added {num_steps} steps")
    
    # Create recipe ingredients
    num_ingredients = random.randint(5, 10)
    selected_ingredients = random.sample(ingredients, min(num_ingredients, len(ingredients)))
    
    for ingredient in selected_ingredients:
        # Select appropriate unit
        unit = random.choice(units)
        quantity = round(random.uniform(0.5, 5.0), 2)
        
        ingredient_payload = {
            "recipe": recipe["id"],
            "ingredient": ingredient["id"],
            "quantity": quantity,
            "unit": unit["id"],
        }
        
        result = client.post("/api/ingredients/recipeingredient_models/", ingredient_payload)
        if result:
            client.created_counts["recipe_ingredients"] += 1
    
    client._log(f"    Added {num_ingredients} ingredients")
    
    return recipe


def save_recipe(
    client: APIClient,
    original_recipe: Dict[str, Any],
    saver_profile_id: str,
    original_author_profile_id: str,
    statuses: Dict[str, str],
) -> Optional[Dict[str, Any]]:
    """Create a saved recipe (snapshot) from an original recipe."""
    # Get full recipe details
    recipe_details = client.get(f"/api/recipes/recipe_models/{original_recipe['id']}/")
    if not recipe_details:
        client._log(f"  Failed to fetch recipe details for {original_recipe['title']}", "ERROR")
        return None
    
    # Extract IDs from nested objects (API returns expanded objects in detail view)
    difficulty_id = None
    if recipe_details.get("difficulty"):
        if isinstance(recipe_details["difficulty"], dict):
            difficulty_id = recipe_details["difficulty"]["id"]
        else:
            difficulty_id = recipe_details["difficulty"]
    
    status_id = None
    if recipe_details.get("status"):
        if isinstance(recipe_details["status"], dict):
            status_id = recipe_details["status"]["id"]
        else:
            status_id = recipe_details["status"]
    
    # Create saved recipe
    saved_recipe_payload = {
        "title": recipe_details["title"],
        "anime_custom": recipe_details["anime_custom"],
        "description": recipe_details["description"],
        "portions": recipe_details["portions"],
        "estimated_time_minutes": recipe_details["estimated_time_minutes"],
        "difficulty": difficulty_id,
        "status": statuses.get("Saved") or statuses.get("Draft"),
        "saver": saver_profile_id,
        "original_recipe": original_recipe["id"],
        "original_author": original_author_profile_id,
    }
    
    saved_recipe = client.post("/api/recipes/savedrecipe_models/", saved_recipe_payload)
    if not saved_recipe or "id" not in saved_recipe:
        client._log(f"  Failed to save recipe: {recipe_details['title']}", "ERROR")
        return None
    
    client.created_counts["saved_recipes"] += 1
    client._log(f"  Saved recipe: {recipe_details['title']}")
    
    # Copy steps (using the steps from the GET response)
    if "steps" in recipe_details:
        for step in recipe_details["steps"]:
            step_payload = {
                "recipe": saved_recipe["id"],
                "number": step["number"],
                "description": step["description"],
                "duration": step.get("duration"),
            }
            # SavedStep uses the savedstep_models endpoint (not nested routing)
            client.post("/api/recipes/savedstep_models/", step_payload)
    
    # Copy ingredients
    if "ingredients" in recipe_details:
        for recipe_ingredient in recipe_details["ingredients"]:
            ingredient_payload = {
                "recipe": saved_recipe["id"],
                "ingredient": recipe_ingredient["ingredient"]["id"],
                "quantity": recipe_ingredient["quantity"],
                "unit": recipe_ingredient["unit"]["id"],
            }
            client.post("/api/ingredients/savedrecipeingredient_models/", ingredient_payload)
    
    return saved_recipe


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution flow for seeding script."""
    parser = argparse.ArgumentParser(description="Seed database via REST API")
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help=f"Base URL for API (default: {DEFAULT_BASE_URL})"
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Note: Manual database reset required. This flag is for documentation."
    )
    args = parser.parse_args()
    
    if args.clean:
        print("Note: To reset database, run: ./scripts/destroy_initialize_postgres.sh")
        print("Then run migrations before seeding.")
        return
    
    client = APIClient(args.base_url)
    
    print("=" * 60)
    print("STARTING DATABASE SEEDING")
    print("=" * 60)
    print(f"API Base URL: {args.base_url}")
    print()
    
    # Step 1: Create foundational data
    client._log("Step 1: Setting up foundational data")
    unit_kinds = create_unit_kinds(client)
    if not unit_kinds:
        client._log("Failed to create unit kinds. Aborting.", "ERROR")
        sys.exit(1)
    
    units = create_units(client, unit_kinds)
    if not units:
        client._log("Failed to create units. Aborting.", "ERROR")
        sys.exit(1)
    
    ingredients = create_ingredients(client)
    if not ingredients:
        client._log("Failed to create ingredients. Aborting.", "ERROR")
        sys.exit(1)
    
    difficulties = create_difficulties(client)
    statuses = get_recipe_statuses(client)
    
    if not statuses:
        client._log("No recipe statuses found. Aborting.", "ERROR")
        sys.exit(1)
    
    print()
    
    # Step 2: Create users with profiles
    client._log("Step 2: Creating users and profiles")
    users_data = []
    for i in range(1, 6):
        user_data = create_user_with_profile(client, i)
        if user_data:
            users_data.append(user_data)
    
    if len(users_data) != 5:
        client._log(f"Expected 5 users, created {len(users_data)}. Continuing...", "WARN")
    
    print()
    
    # Step 3: Each user creates 5 recipes
    client._log("Step 3: Creating recipes with steps and ingredients")
    all_recipes = []
    recipe_counter = 0
    
    for user_data in users_data:
        profile_id = user_data["profile"]["id"]
        user_name = user_data["profile"]["display_name"]
        client._log(f"Creating recipes for {user_name}...")
        
        user_recipes = []
        for i in range(5):
            recipe = create_recipe_with_details(
                client,
                profile_id,
                difficulties,
                statuses,
                ingredients,
                units,
                recipe_counter,
            )
            if recipe:
                recipe["author_profile_id"] = profile_id
                user_recipes.append(recipe)
            recipe_counter += 1
        
        all_recipes.extend(user_recipes)
        user_data["authored_recipes"] = user_recipes
    
    print()
    
    # Step 4: Each user saves 5 recipes from other users
    client._log("Step 4: Creating saved recipes")
    for user_data in users_data:
        profile_id = user_data["profile"]["id"]
        user_name = user_data["profile"]["display_name"]
        client._log(f"Saving recipes for {user_name}...")
        
        # Get recipes authored by other users
        other_recipes = [r for r in all_recipes if r.get("author_profile_id") != profile_id]
        
        if len(other_recipes) < 5:
            client._log(f"  Not enough recipes from other users (found {len(other_recipes)})", "WARN")
            recipes_to_save = other_recipes
        else:
            recipes_to_save = random.sample(other_recipes, 5)
        
        for recipe in recipes_to_save:
            save_recipe(
                client,
                recipe,
                profile_id,
                recipe["author_profile_id"],
                statuses,
            )
    
    print()
    
    # Print summary
    client.print_summary()
    print("\nSeeding completed successfully!")
    print(f"You can now test the API at: {args.base_url}/api/")


if __name__ == "__main__":
    main()
