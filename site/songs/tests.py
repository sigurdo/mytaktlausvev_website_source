from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse
from accounts.factories import UserFactory, SuperUserFactory
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
    def test_author_set_to_current_user(self):
        """Should set the author to the current user on creation."""
        user = SuperUserFactory()
        self.client.force_login(user)
        self.client.post(
            reverse("song_create"), {"title": "A Title", "description": "Some lyrics"}
        )

        self.assertEqual(Song.objects.count(), 1)
        song = Song.objects.last()
        self.assertEqual(song.created_by, user)

    def test_requires_login(self):
        """Should redirect to login page if user is not logged in."""
        response = self.client.get(reverse("song_create"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(response.url.startswith(reverse("login")))

    def test_fails_if_missing_permission(self):
        """Should fail if missing add permission."""
        self.user = UserFactory()
        self.client.force_login(self.user)
        response = self.client.post(reverse("song_create"))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_succeeds_if_has_permission(self):
        """Should succeed if user has add permission."""
        self.user = UserFactory(permissions=("songs.add_song",))
        self.client.force_login(self.user)
        response = self.client.post(reverse("song_create"))
        self.assertEqual(response.status_code, HTTPStatus.OK)


class SongUpdateTestCase(TestCase):
    def setUp(self):
        self.song = SongFactory()

    def test_requires_login(self):
        """Should redirect to login page if user is not logged in."""
        response = self.client.get(reverse("song_update", kwargs={"pk": self.song.pk}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(response.url.startswith(reverse("login")))

    def test_fails_if_missing_permission(self):
        """Should fail if missing change permission."""
        self.user = UserFactory()
        self.client.force_login(self.user)
        response = self.client.post(reverse("song_update", kwargs={"pk": self.song.pk}))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_succeeds_if_has_permission(self):
        """Should succeed if user has change permission."""
        self.user = UserFactory(permissions=("songs.change_song",))
        self.client.force_login(self.user)
        response = self.client.post(reverse("song_update", kwargs={"pk": self.song.pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
