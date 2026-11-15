"""API tests for recipes: the jeu d'essai of the Dossier Projet, automated.

Run them with:  uv run manage.py test
Django creates an empty test database (test_<DB_NAME>), runs every
method whose name starts with `test`, then deletes the database: your
own data is never touched.

Each test logs in through the API, exactly like the front-end: the
login response sets the cookies, and the test client sends them back.
"""
from io import BytesIO, StringIO

from django.core.files.storage import default_storage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from PIL import Image
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import CustomUser
from ingredients.models import Ingredient, Unit, UnitKind
from recipes.models import Recipe, RecipePhoto

PASSWORD = "Itadakimasu-2026!"


def create_reference_data():
    """Difficulties, statuses and units, as entrypoint.sh creates them."""
    for command in ("create_difficulties", "create_recipe_statuses",
                    "create_unit_kinds", "create_units"):
        call_command(command, stdout=StringIO())  # StringIO: no output


def png_file(name="photo.png"):
    """A real, tiny PNG image, as an uploaded file."""
    content = BytesIO()
    Image.new("RGB", (2, 2), "red").save(content, format="PNG")
    return SimpleUploadedFile(name, content.getvalue(),
                              content_type="image/png")


class RecipeApiTestCase(APITestCase):
    """Shared set-up: reference data, an author and another user."""

    @classmethod
    def setUpTestData(cls):
        create_reference_data()
        CustomUser.objects.create_user(email="author@example.com",
                                       password=PASSWORD)
        CustomUser.objects.create_user(email="other@example.com",
                                       password=PASSWORD)
        cls.gram = Unit.objects.get(symbol="g")

    def log_in(self, email):
        response = self.client.post("/api/token/",
                                    {"email": email, "password": PASSWORD})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def create_recipe(self):
        """Log in as the author and create a blank draft recipe."""
        self.log_in("author@example.com")
        response = self.client.post("/api/recipes/recipe_models/")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response.data["id"]

    def fill_recipe(self, recipe_id, quantity=200, unit=None):
        """Same request as the editor's "Save" button."""
        return self.client.patch(
            f"/api/recipes/recipe_models/{recipe_id}/",
            {
                "title": "Onigiri de test",
                "anime_custom": "Test anime",
                "difficulty": self.client.get(
                    "/api/recipes/difficulty_models/").data[0]["id"],
                "ingredients": [{"ingredient_name": "riz",
                                 "quantity": quantity,
                                 "unit": (unit or self.gram).id}],
                "steps": [{"number": 1, "description": "Cuire le riz."}],
            },
            format="json",
        )

    def set_status(self, recipe_id, value):
        return self.client.patch(
            f"/api/recipes/recipe_models/{recipe_id}/status/",
            {"value": value}, format="json")


class JeuEssaiTests(RecipeApiTestCase):
    """The nine cases of the jeu d'essai (Dossier Projet, chapter 13)."""

    def test_visitor_cannot_create_a_recipe(self):  # case 1
        response = self.client.post("/api/recipes/recipe_models/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_new_recipe_is_a_draft(self):  # case 2
        recipe_id = self.create_recipe()
        response = self.client.get(f"/api/recipes/recipe_models/{recipe_id}/")
        self.assertEqual(response.data["status"]["value"], "Draft")

    def test_a_draft_cannot_be_published(self):  # case 3
        recipe_id = self.create_recipe()
        response = self.set_status(recipe_id, "Published")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_an_empty_ready_recipe_lists_four_missing_elements(self):
        # cases 4 and 5 (case 5 found the default title/anime problem)
        recipe_id = self.create_recipe()
        response = self.set_status(recipe_id, "Ready")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.set_status(recipe_id, "Published")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data["detail"]), 4)

    def test_publication_of_a_complete_recipe(self):  # cases 6 to 9
        recipe_id = self.create_recipe()
        self.assertEqual(self.fill_recipe(recipe_id).status_code,
                         status.HTTP_200_OK)
        self.set_status(recipe_id, "Ready")

        self.log_in("other@example.com")  # case 7: another user
        response = self.set_status(recipe_id, "Published")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.log_in("author@example.com")  # case 8: the author
        response = self.set_status(recipe_id, "Published")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data["published_at"])

        self.client.cookies.clear()  # case 9: a visitor reads the feed
        response = self.client.get("/api/recipes/recipe_models/")
        self.assertIn(recipe_id, [recipe["id"] for recipe in response.data])


class RecipeContentTests(RecipeApiTestCase):
    """Validation rules on a recipe's content."""

    def test_negative_quantity_is_refused(self):
        recipe_id = self.create_recipe()
        response = self.fill_recipe(recipe_id, quantity=-5)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unit_of_a_forbidden_kind_is_refused(self):
        # Here rice may only be weighed: a unit of another kind is refused.
        rice = Ingredient.objects.create(name="riz")
        rice.allowed_unit_kinds.add(self.gram.kind)
        other_unit = Unit.objects.exclude(kind=self.gram.kind).first()
        recipe_id = self.create_recipe()
        response = self.fill_recipe(recipe_id, unit=other_unit)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class StepAndPhotoAccessTests(RecipeApiTestCase):
    """Only the author changes a recipe's steps and photos."""

    def test_other_user_cannot_add_a_step(self):
        recipe_id = self.create_recipe()
        self.log_in("other@example.com")
        response = self.client.post(
            f"/api/recipes/{recipe_id}/steps/",
            {"recipe": recipe_id, "number": 9, "description": "intruder"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_author_uploads_and_deletes_a_photo(self):
        recipe_id = self.create_recipe()
        response = self.client.post(f"/api/recipes/{recipe_id}/photos/",
                                    {"image": png_file(), "position": 1},
                                    format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        photo_id = response.data["id"]
        response = self.client.delete(
            f"/api/recipes/{recipe_id}/photos/{photo_id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_reference_data_is_read_only(self):
        self.log_in("other@example.com")
        response = self.client.post("/api/ingredients/unitkind_models/",
                                    {"label": "x", "descriptive_name": "x"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(UnitKind.objects.exists())


class AccountDeletionTests(RecipeApiTestCase):
    """RGPD: deleting an account deletes its recipes and photo files."""

    def test_deleting_an_account_deletes_recipes_and_photo_files(self):
        recipe_id = self.create_recipe()
        self.client.post(f"/api/recipes/{recipe_id}/photos/",
                         {"image": png_file(), "position": 1},
                         format="multipart")
        file_name = RecipePhoto.objects.get(recipe=recipe_id).image.name
        self.assertTrue(default_storage.exists(file_name))

        author = CustomUser.objects.get(email="author@example.com")
        response = self.client.delete(
            f"/api/accounts/user_models/{author.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(pk=recipe_id).exists())
        self.assertFalse(default_storage.exists(file_name))
