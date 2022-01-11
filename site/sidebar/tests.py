from django.contrib.auth.models import AnonymousUser
from django.test import TestCase

from accounts.factories import UserFactory
from authentication.forms import LoginForm
from polls.factories import PollFactory

from .templatetags.sidebar import sidebar


class SidebarTestSuite(TestCase):
    def test_user_in_context(self):
        """Should include user in context."""
        user = UserFactory()
        self.assertEqual(sidebar(user)["user"], user)

    def test_login_form_in_context(self):
        """Should include the login form in context."""
        self.assertEqual(sidebar(UserFactory())["form_login"], LoginForm)

    def test_latest_poll_logged_in(self):
        """Should include the latest poll when logged in."""
        poll = PollFactory()
        self.assertEqual(sidebar(UserFactory())["poll"], poll)

    def test_latest_public_poll_not_logged_in(self):
        """Should include the latest public poll when not logged in."""
        poll_public = PollFactory(public=True)
        [PollFactory() for _ in range(3)]

        self.assertEqual(sidebar(AnonymousUser())["poll"], poll_public)

    def test_poll_none_when_no_poll(self):
        """Should set `poll` to `None` when there are no polls."""
        self.assertIsNone(sidebar(UserFactory())["poll"])
