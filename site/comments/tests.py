from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from songs.models import Song
from .models import Comment


class CommentTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="bob", password="bob")

    def comment_create(self, model):
        return Comment.objects.create(
            content_type=ContentType.objects.get_for_model(model),
            object_pk=model.pk,
            comment="Test comment",
            created_by=self.user,
        )

    def test_get_absolute_url(self):
        """Should link to the comment on the model's page."""
        song = Song.objects.create(
            title="Test", description="Test", created_by=self.user
        )
        comment = self.comment_create(song)

        self.assertEqual(
            comment.get_absolute_url(),
            f"{reverse('song_detail', kwargs={'pk': song.pk})}#comment-{comment.pk}",
        )
