from django.contrib.auth.models import AnonymousUser
from django.test import TestCase

from accounts.factories import UserFactory
from authentication.forms import LoginForm
from polls.factories import PollFactory

from .templatetags.sidebar import sidebar


class SidebarTestSuite(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.request_path = "/this-is/a-path/"

    def get_sidebar(self, user=None):
        return sidebar(user or self.user, self.request_path)

    def test_user_in_context(self):
        """Should include user in context."""
        self.assertEqual(self.get_sidebar()["user"], self.user)

    def test_request_path_in_context(self):
        """Should include request path in context."""
        self.assertEqual(self.get_sidebar()["request_path"], self.request_path)

    def test_login_form_in_context(self):
        """Should include the login form in context."""
        self.assertEqual(self.get_sidebar()["form_login"], LoginForm)

    def test_latest_poll_logged_in(self):
        """Should include the latest poll when logged in."""
        poll = PollFactory()
        self.assertEqual(self.get_sidebar()["poll"], poll)

    def test_latest_public_poll_not_logged_in(self):
        """Should include the latest public poll when not logged in."""
        poll_public = PollFactory(public=True)
        [PollFactory() for _ in range(3)]

        self.assertEqual(self.get_sidebar(AnonymousUser())["poll"], poll_public)

    def test_poll_none_when_no_poll(self):
        """Should set `poll` to `None` when there are no polls."""
        self.assertIsNone(self.get_sidebar()["poll"])
