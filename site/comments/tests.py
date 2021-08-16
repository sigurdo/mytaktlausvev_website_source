from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse
from common.factories import UserFactory
from songs.factories import SongFactory
from .factories import CommentFactory


class CommentTestCase(TestCase):
    def setUp(self):
        self.song = SongFactory()
        self.comment = CommentFactory(content_object=self.song)

    def test_get_absolute_url(self):
        """Should link to the comment on the model's page."""
        self.assertEqual(
            self.comment.get_absolute_url(),
            f"{reverse('song_detail', kwargs={'pk': self.song.pk})}#comment-{self.comment.pk}",
        )

    def test_to_str(self):
        """Should have the correct string representation."""
        self.assertEqual(str(self.comment), f"Kommentar #{self.comment.pk}")


class CommentCreateTestCase(TestCase):
    def setUp(self):
        self.client.force_login(UserFactory())

    def test_get_not_allowed(self):
        """Should not allow GET requests."""
        response = self.client.get(reverse("comment_create"))
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)


class CommentDeleteTestCase(TestCase):
    def setUp(self):
        self.client.force_login(UserFactory())
        self.song = SongFactory()
        self.comment = CommentFactory(content_object=self.song)

    def test_should_redirect_to_content_object_on_success(self):
        """Should redirect to the model the comment is associated with on success."""
        response = self.client.post(
            reverse("comment_delete", kwargs={"pk": self.comment.pk})
        )
        self.assertEqual(
            response.url, reverse("song_detail", kwargs={"pk": self.song.pk})
        )
