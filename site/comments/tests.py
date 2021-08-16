from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse
from common.factories import UserFactory
from songs.factories import SongFactory
from .factories import CommentFactory
from .models import Comment


class CommentTestCase(TestCase):
    def setUp(self):
        self.song = SongFactory()
        self.comment = CommentFactory(content_object=self.song)

    def test_get_absolute_url(self):
        """Should link to the comment on the model's page."""
        self.assertEqual(
            self.comment.get_absolute_url(),
            f"{reverse('song_detail', args=[self.song.pk])}#comment-{self.comment.pk}",
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
        self.author = UserFactory()
        self.song = SongFactory()
        self.comment = CommentFactory(content_object=self.song, created_by=self.author)

    def test_should_redirect_to_content_object_on_success(self):
        """Should redirect to the model the comment is associated with on success."""
        self.client.force_login(self.author)
        response = self.client.post(reverse("comment_delete", args=[self.comment.pk]))
        self.assertEqual(response.url, reverse("song_detail", args=[self.song.pk]))

    def test_requires_login(self):
        """Should redirect to login page if user is not logged in."""
        response = self.client.post(reverse("comment_delete", args=[self.comment.pk]))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(response.url.startswith(reverse("login")))

    def test_fails_if_neither_author_nor_has_permission(self):
        """Should fail if the user is neither the author nor has permission."""
        self.client.force_login(UserFactory())
        response = self.client.post(reverse("comment_delete", args=[self.comment.pk]))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertTrue(Comment.objects.filter(pk=self.comment.pk).exists())

    def test_succeeds_if_author(self):
        """Should succeed if the user is the author."""
        self.client.force_login(self.author)
        self.client.post(reverse("comment_delete", args=[self.comment.pk]))
        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())

    def test_succeeds_if_has_permission(self):
        """Should succeed if the user has permission to delete comments."""
        self.client.force_login(UserFactory(permissions=("comments.delete_comment",)))
        self.client.post(reverse("comment_delete", args=[self.comment.pk]))
        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())
