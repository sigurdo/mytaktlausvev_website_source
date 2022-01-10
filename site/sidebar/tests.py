from django.contrib.auth.models import AnonymousUser
from django.test import TestCase

from accounts.factories import UserFactory
from authentication.forms import LoginForm

from .templatetags.sidebar import sidebar


class SidebarTestSuite(TestCase):
    def setUp(self):
        self.context = {"user": UserFactory()}

    def test_authenticated_in_context(self):
        """Should include auth status in context."""
        self.assertTrue(sidebar(self.context)["authenticated"])

        self.context["user"] = AnonymousUser()
        self.assertFalse(sidebar(self.context)["authenticated"])

    def test_login_form_in_context(self):
        """Should include the login form in context."""
        self.assertEqual(sidebar(self.context)["form_login"], LoginForm)
