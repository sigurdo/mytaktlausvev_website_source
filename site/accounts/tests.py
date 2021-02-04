from django.test import TestCase
from django.contrib.auth import authenticate
from accounts.models import UserCustom


class UserCustomTest(TestCase):
    def test_login_usernames_case_insensitive(self):
        """
        When logging in the username should be case insensitive.
        """
        password = "SuperSafePassword123"
        UserCustom.objects.create_user(username="Bob", password=password)
        self.assertIsNotNone(authenticate(username="Bob", password=password))
        self.assertIsNotNone(authenticate(username="BoB", password=password))
        self.assertIsNotNone(authenticate(username="bob", password=password))
        self.assertIsNotNone(authenticate(username="BOB", password=password))

    def test_creating_user_username_case_insensitive(self):
        """
        When creating a user the username should be case insensitive.
        """
        UserCustom.objects.create_user(username="BOB")
        with self.assertRaises(ValueError):
            UserCustom.objects.create_user(username="bob")
