from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse
from accounts.factories import UserFactory
from articles.factories import ArticleFactory
from .factories import CommentFactory
from .models import Comment


class CommentTestCase(TestCase):
    def setUp(self):
        self.article = ArticleFactory()
        self.comment = CommentFactory(content_object=self.article)

    def test_get_absolute_url(self):
        """Should link to the comment on the model's page."""
        self.assertEqual(
            self.comment.get_absolute_url(),
            f"{reverse('articles:detail', args=[self.article.slug])}#comment-{self.comment.pk}",
        )

    def test_to_str(self):
        """Should have the correct string representation."""
        self.assertEqual(str(self.comment), f"Kommentar #{self.comment.pk}")


class CommentCreateTestCase(TestCase):
    def test_get_not_allowed(self):
        """Should not allow GET requests."""
        self.client.force_login(UserFactory())
        response = self.client.get(reverse("comment_create"))
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_requires_login(self):
        """Should redirect to login page if user is not logged in."""
        response = self.client.post(reverse("comment_create"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(response.url.startswith(reverse("login")))


class CommentUpdateTestCase(TestCase):
    def setUp(self):
        self.author = UserFactory()
        self.article = ArticleFactory()
        self.comment = CommentFactory(
            content_object=self.article, created_by=self.author
        )

    def test_requires_login(self):
        """Should redirect to login page if user is not logged in."""
        response = self.client.post(reverse("comment_update", args=[self.comment.pk]))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(response.url.startswith(reverse("login")))

    def test_fails_if_neither_author_nor_has_permission(self):
        """Should fail if the user is neither the author nor has permission."""
        self.client.force_login(UserFactory())
        response = self.client.post(
            reverse("comment_update", args=[self.comment.pk]), {"comment": "Different"}
        )

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        comment_old = self.comment.comment
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.comment, comment_old)

    def test_succeeds_if_author(self):
        """Should succeed if the user is the author."""
        comment_new = "New Comment."
        self.client.force_login(self.author)
        self.client.post(
            reverse("comment_update", args=[self.comment.pk]), {"comment": comment_new}
        )

        self.comment.refresh_from_db()
        self.assertEqual(self.comment.comment, comment_new)

    def test_succeeds_if_has_permission(self):
        """Should succeed if the user has permission to change comments."""
        comment_new = "New Comment."
        self.client.force_login(UserFactory(permissions=("comments.change_comment",)))
        self.client.post(
            reverse("comment_update", args=[self.comment.pk]), {"comment": comment_new}
        )

        self.comment.refresh_from_db()
        self.assertEqual(self.comment.comment, comment_new)


class CommentDeleteTestCase(TestCase):
    def setUp(self):
        self.author = UserFactory()
        self.article = ArticleFactory()
        self.comment = CommentFactory(
            content_object=self.article, created_by=self.author
        )

    def test_should_redirect_to_content_object_on_success(self):
        """Should redirect to the model the comment is associated with on success."""
        self.client.force_login(self.author)
        response = self.client.post(reverse("comment_delete", args=[self.comment.pk]))
        self.assertRedirects(
            response, reverse("articles:detail", args=[self.article.slug])
        )

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
