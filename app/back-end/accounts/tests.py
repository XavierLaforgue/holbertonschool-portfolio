"""API tests for accounts: sign-up, access rules and account deletion.

Run them with:  uv run manage.py test   (see recipes/tests.py)
"""
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import CustomUser, Profile

PASSWORD = "Itadakimasu-2026!"


class SignUpTests(APITestCase):

    def test_sign_up_with_a_good_password(self):
        response = self.client.post("/api/accounts/user_models/",
                                    {"email": "new@example.com",
                                     "password": PASSWORD})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # the password is stored hashed, never as typed
        user = CustomUser.objects.get(email="new@example.com")
        self.assertNotEqual(user.password, PASSWORD)
        self.assertTrue(user.check_password(PASSWORD))

    def test_weak_password_is_refused(self):
        response = self.client.post("/api/accounts/user_models/",
                                    {"email": "weak@example.com",
                                     "password": "123"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)
        self.assertFalse(
            CustomUser.objects.filter(email="weak@example.com").exists())


class AccountAccessTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.alice = CustomUser.objects.create_user(email="alice@example.com",
                                                   password=PASSWORD)
        cls.bob = CustomUser.objects.create_user(email="bob@example.com",
                                                 password=PASSWORD)

    def log_in(self, email):
        response = self.client.post("/api/token/",
                                    {"email": email, "password": PASSWORD})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_visitor_cannot_list_accounts(self):
        response = self.client.get("/api/accounts/user_models/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_cannot_list_accounts(self):
        self.log_in("alice@example.com")
        response = self.client.get("/api/accounts/user_models/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_change_someone_else_s_profile(self):
        self.log_in("alice@example.com")
        response = self.client.patch(
            f"/api/accounts/profile_models/{self.bob.profile.id}/",
            {"bio": "changed by Alice"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_delete_someone_else_s_account(self):
        self.log_in("alice@example.com")
        response = self.client.delete(
            f"/api/accounts/user_models/{self.bob.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(CustomUser.objects.filter(pk=self.bob.pk).exists())

    def test_user_deletes_their_own_account(self):
        self.log_in("alice@example.com")
        response = self.client.delete(
            f"/api/accounts/user_models/{self.alice.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # really deleted, with the profile (RGPD: right to erasure)
        self.assertFalse(
            CustomUser.objects.filter(pk=self.alice.pk).exists())
        self.assertFalse(Profile.objects.filter(user=self.alice.pk).exists())
        # the response deletes the cookies: the browser is logged out
        self.assertEqual(response.cookies["access_token"].value, "")
