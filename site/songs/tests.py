from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Song


class SongTestCase(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(username="bob", password="bob")
        self.song = Song.objects.create(
            title="Song of Tests", description="Test, test, test", created_by=user
        )

    def test_get_absolute_url(self):
        """Should have the correct absolute URL."""
        self.assertEqual(
            self.song.get_absolute_url(),
            reverse("song_detail", kwargs={"pk": self.song.pk}),
        )


class SongCreateTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="bob", password="bob")
        self.client.login(username="bob", password="bob")

    def test_requires_login(self):
        """Should redirect to login page if user is not logged in."""
        self.client.logout()
        response = self.client.get(reverse("song_create"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(response.url.startswith(reverse("login")))

    def test_author_set_to_current_user(self):
        """Should set the author to the current user on creation."""
        response = self.client.post(
            reverse("song_create"), {"title": "A Title", "description": "Some lyrics"}
        )
        self.assertEqual(Song.objects.count(), 1)
        song = Song.objects.last()
        self.assertEqual(song.created_by, self.user)

    def test_redirects_to_created_song(self):
        """Should redirect to the created song."""
        response = self.client.post(
            reverse("song_create"), {"title": "A Title", "description": "Some lyrics"}
        )
        self.assertRedirects(
            response, reverse("song_detail", kwargs={"pk": Song.objects.last().pk})
        )


class SongUpdateTestCase(TestCase):
    def test_requires_login(self):
        """Should redirect to login page if user is not logged in."""
        response = self.client.get(reverse("song_update", kwargs={"pk": 5}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(response.url.startswith(reverse("login")))
