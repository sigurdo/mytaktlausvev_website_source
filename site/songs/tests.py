from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Song


class SongTestCase(TestCase):
    def setUp(self):
        self.song = Song.objects.create(
            title="Song of Tests", lyrics="Test, test, test"
        )

    def test_sets_submitted_to_current_datetime_on_create(self):
        """`submitted` should be set to the current date and time on creation."""
        now = timezone.now()
        self.assertLess((now - self.song.submitted).total_seconds(), 5)

    def test_song_to_string_equals_title(self):
        """Song's to string method should return the song's title."""
        self.assertEqual(str(self.song), self.song.title)

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


class SongUpdateTestCase(TestCase):
    def test_requires_login(self):
        """Should redirect to login page if user is not logged in."""
        response = self.client.get(reverse("song_update", kwargs={"pk": 5}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(response.url.startswith(reverse("login")))
