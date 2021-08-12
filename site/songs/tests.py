from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse
from common.factories import UserFactory
from .models import Song
from .factories import SongFactory


class SongTestCase(TestCase):
    def setUp(self):
        self.song = SongFactory()

    def test_get_absolute_url(self):
        """Should have the correct absolute URL."""
        self.assertEqual(
            self.song.get_absolute_url(),
            reverse("song_detail", kwargs={"pk": self.song.pk}),
        )


class SongCreateTestCase(TestCase):
    def test_requires_login(self):
        """Should redirect to login page if user is not logged in."""
        response = self.client.get(reverse("song_create"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(response.url.startswith(reverse("login")))

    def test_author_set_to_current_user(self):
        """Should set the author to the current user on creation."""
        self.user = UserFactory()
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("song_create"), {"title": "A Title", "description": "Some lyrics"}
        )

        self.assertEqual(Song.objects.count(), 1)
        song = Song.objects.last()
        self.assertEqual(song.created_by, self.user)


class SongUpdateTestCase(TestCase):
    def test_requires_login(self):
        """Should redirect to login page if user is not logged in."""
        response = self.client.get(reverse("song_update", kwargs={"pk": 5}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(response.url.startswith(reverse("login")))
