from http import HTTPStatus

from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.urls import reverse

from accounts.factories import SuperUserFactory, UserFactory
from articles.factories import ArticleFactory
from common.mixins import TestMixin

from .factories import CommentFactory
from .models import Comment


class CommentTestCase(TestCase):
    def setUp(self):
        self.article = ArticleFactory()
        self.comment = CommentFactory(
            comment="Great article!", content_object=self.article
        )
        self.comment_long = CommentFactory(
            comment="I think this article was most exquisite, and I sincerely hope to see more in the future.",
            content_object=self.article,
        )
        self.comment_whitespace = CommentFactory(
            comment="Cool!                                                ",
            content_object=self.article,
        )

    def test_get_absolute_url(self):
        """Should link to the comment on the model's page."""
        self.assertEqual(
            self.comment.get_absolute_url(),
            f"{reverse('articles:ArticleDetail', args=[self.article.slug])}#comment-{self.comment.pk}",
        )

    def test_to_str_comment_shorter_than_20_characters(self):
        """`__str__` should be the entire comment when it's shorter than 20 characters."""
        self.assertEqual(str(self.comment), self.comment.comment)

    def test_to_str_comment_longer_than_20_characters(self):
        """
        `__str__` should truncate comment when it has more than 20 characters,
        and add an ellipsis.
        """
        self.assertEqual(str(self.comment_long), self.comment_long.comment[0:19] + "…")

    def test_to_str_strips_whitespace_before_checking(self):
        """`__str__` should strip whitespace before checking length."""
        self.assertEqual(
            str(self.comment_whitespace), self.comment_whitespace.comment.rstrip()
        )


class CommentCreateTestCase(TestMixin, TestCase):
    def setUp(self):
        article = ArticleFactory()
        self.comment_data = {
            "comment": "Here Hector entered,",
            "object_pk": article.pk,
            "content_type": ContentType.objects.get_for_model(article).id,
        }

    def get_url(self):
        return reverse("comments:CommentCreate")

    def test_get_not_allowed(self):
        """Should not allow GET requests."""
        self.client.force_login(UserFactory())
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url())

    def test_created_by_modified_by_set_to_current_user(self):
        """Should set `created_by` and `modified_by` to the current user on creation."""
        user = SuperUserFactory()
        self.client.force_login(user)
        self.client.post(self.get_url(), self.comment_data)

        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.last()
        self.assertEqual(comment.created_by, user)
        self.assertEqual(comment.modified_by, user)


class CommentUpdateTestCase(TestMixin, TestCase):
    def setUp(self):
        article = ArticleFactory()
        self.comment = CommentFactory(content_object=article, created_by=UserFactory())
        self.comment_data = {
            "comment": "Here Hector entered,",
            "object_pk": article.pk,
            "content_type": ContentType.objects.get_for_model(article).id,
        }

    def get_url(self):
        return reverse("comments:CommentUpdate", args=[self.comment.pk])

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url())

    def test_requires_permission(self):
        """Should require the `change_comment` permission."""
        self.assertPermissionRequired(self.get_url(), "comments.change_comment")

    def test_succeeds_if_not_permission_but_is_author(self):
        """
        Should succeed if the user is the author,
        even if the user doesn't have the `change_comment` permission.
        """
        self.client.force_login(self.comment.created_by)
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_created_by_not_changed(self):
        """Should not change `created_by` when updating comment."""
        self.client.force_login(SuperUserFactory())
        self.client.post(self.get_url(), self.comment_data)

        created_by_previous = self.comment.created_by
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.created_by, created_by_previous)

    def test_modified_by_set_to_current_user(self):
        """Should set `modified_by` to the current user on update."""
        user = SuperUserFactory()
        self.client.force_login(user)
        self.client.post(self.get_url(), self.comment_data)

        self.comment.refresh_from_db()
        self.assertEqual(self.comment.modified_by, user)


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
        response = self.client.post(
            reverse("comments:CommentDelete", args=[self.comment.pk])
        )
        self.assertRedirects(
            response, reverse("articles:ArticleDetail", args=[self.article.slug])
        )

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(
            reverse("comments:CommentDelete", args=[self.comment.pk])
        )

    def test_requires_permission(self):
        """Should require the `delete_comment` permission."""
        self.assertPermissionRequired(
            reverse("comments:CommentDelete", args=[self.comment.pk]),
            "comments.delete_comment",
        )

    def test_succeeds_if_not_permission_but_is_author(self):
        """
        Should succeed if the user is the author,
        even if the user doesn't have the `delete_comment` permission.
        """
        self.client.force_login(self.author)
        response = self.client.get(
            reverse("comments:CommentDelete", args=[self.comment.pk])
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
