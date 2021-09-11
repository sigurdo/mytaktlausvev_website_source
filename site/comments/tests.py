from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse
from accounts.factories import UserFactory
from articles.factories import ArticleFactory
from common.mixins import TestMixin
from .factories import CommentFactory


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


class CommentCreateTestCase(TestMixin, TestCase):
    def test_get_not_allowed(self):
        """Should not allow GET requests."""
        self.client.force_login(UserFactory())
        response = self.client.get(reverse("comment_create"))
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(reverse("comment_create"))


class CommentUpdateTestCase(TestMixin, TestCase):
    def setUp(self):
        self.author = UserFactory()
        self.article = ArticleFactory()
        self.comment = CommentFactory(
            content_object=self.article, created_by=self.author
        )

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(reverse("comment_update", args=[self.comment.pk]))

    def test_requires_permission(self):
        """Should require the `change_comment` permission."""
        self.assertPermissionRequired(
            reverse("comment_update", args=[self.comment.pk]), "comments.change_comment"
        )

    def test_succeeds_if_not_permission_but_is_author(self):
        """
        Should succeed if the user is the author,
        even if the user doesn't have the `change_comment` permission.
        """
        self.client.force_login(self.author)
        response = self.client.get(reverse("comment_update", args=[self.comment.pk]))
        self.assertEqual(response.status_code, HTTPStatus.OK)


class CommentDeleteTestCase(TestMixin, TestCase):
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
        """Should require login."""
        self.assertLoginRequired(reverse("comment_delete", args=[self.comment.pk]))

    def test_requires_permission(self):
        """Should require the `delete_comment` permission."""
        self.assertPermissionRequired(
            reverse("comment_delete", args=[self.comment.pk]), "comments.delete_comment"
        )

    def test_succeeds_if_not_permission_but_is_author(self):
        """
        Should succeed if the user is the author,
        even if the user doesn't have the `delete_comment` permission.
        """
        self.client.force_login(self.author)
        response = self.client.get(reverse("comment_delete", args=[self.comment.pk]))
        self.assertEqual(response.status_code, HTTPStatus.OK)
