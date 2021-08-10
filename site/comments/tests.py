from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from songs.models import Song
from .models import Comment


class CommentTestCase(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(username="bob", password="bob")
        self.song = Song.objects.create(
            title="Test", description="Test", created_by=user
        )
        self.comment = Comment.objects.create(
            content_type=ContentType.objects.get_for_model(self.song),
            object_pk=self.song.pk,
            comment="Test comment",
            created_by=user,
        )

    def test_get_absolute_url(self):
        """Should link to the comment on the model's page."""
        self.assertEqual(
            self.comment.get_absolute_url(),
            f"{reverse('song_detail', kwargs={'pk': self.song.pk})}#comment-{self.comment.pk}",
        )

    def test_to_str(self):
        """Correct"""
        self.assertEqual(str(self.comment), f"Kommentar #{self.comment.pk}")


class CommentCreateTestCase(TestCase):
    def test_get_not_allowed(self):
        """Should not allow GET requests."""
        response = self.client.get(reverse("comment_create"))
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)
