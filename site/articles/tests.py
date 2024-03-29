from http import HTTPStatus

from django.http.response import Http404
from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify
from django.views.generic.detail import SingleObjectMixin

from accounts.factories import SuperUserFactory, UserFactory
from articles.views import SlugPathMixin
from common.breadcrumbs.breadcrumbs import Breadcrumb
from common.mixins import TestMixin

from .factories import ArticleFactory
from .models import Article


class ArticleTestCase(TestCase):
    def setUp(self):
        self.article = ArticleFactory()
        self.child = ArticleFactory(title="child", parent=self.article)
        self.grandchild = ArticleFactory(title="grandchild", parent=self.child)
        self.article_data = {
            "title": "Article",
            "content": "Article",
            "created_by": UserFactory(),
            "modified_by": UserFactory(),
        }

    def test_path(self):
        """Should return a /-separated list of ancestor slugs, including self."""
        self.assertEqual(self.article.path(), self.article.slug)
        self.assertEqual(self.child.path(), f"{self.article.slug}/{self.child.slug}")
        self.assertEqual(
            self.grandchild.path(),
            f"{self.article.slug}/{self.child.slug}/{self.grandchild.slug}",
        )

    def test_get_absolute_url(self):
        """Should link to the article's detail page."""
        self.assertEqual(
            self.article.get_absolute_url(),
            reverse("articles:ArticleDetail", args=[self.article.path()]),
        )

    def test_creates_slug_from_title_automatically(self):
        """Should create a slug from the title automatically during creation."""
        self.assertEqual(self.article.slug, slugify(self.article.title))

    def test_does_not_update_slug_when_title_is_changed(self):
        """Should not change the slug when the title is changed."""
        slug_before = self.article.slug
        self.article.title = "Different title"
        self.article.save()
        self.assertEqual(self.article.slug, slug_before)

    def test_creates_unique_slugs_for_articles_with_same_parent(self):
        """Should create unique slugs for articles with the same parent."""
        article_same_title_same_parent = ArticleFactory(
            title=self.child.title, parent=self.child.parent
        )
        self.assertNotEqual(self.child.slug, article_same_title_same_parent.slug)

    def test_articles_with_different_parents_can_have_equal_slugs(self):
        """Should allow articles with different parents to have equal slugs."""
        article_same_title_different_parent = ArticleFactory(
            title=self.child.title, parent=self.grandchild.parent
        )
        self.assertEqual(self.child.slug, article_same_title_different_parent.slug)

    def test_does_not_override_provided_slug(self):
        """Should not override the slug if provided during creation."""
        slug = "this-is-a-slug"
        article = ArticleFactory(
            title="Title that is very different from the slug", slug=slug
        )
        self.assertEqual(article.slug, slug)

    def test_public_false_by_default(self):
        """Should set `public` to false by default."""
        article = Article.objects.create(**self.article_data)
        self.assertFalse(article.public)

    def test_comments_allowed_by_default(self):
        """Should allow comments by default."""
        article = Article.objects.create(**self.article_data)
        self.assertTrue(article.comments_allowed)

    def test_breadcrumbs(self):
        """Should return a list of ancestor breadcrumbs."""
        self.assertEqual(
            self.grandchild.breadcrumbs(),
            [
                Breadcrumb(self.article.get_absolute_url(), self.article.title),
                Breadcrumb(self.child.get_absolute_url(), self.child.title),
            ],
        )

    def test_breadcrumbs_include_self(self):
        """
        Should return a list of ancestor breadcrumbs,
        including self, when `include_self=True`.
        """
        self.assertEqual(
            self.grandchild.breadcrumbs(include_self=True),
            [
                Breadcrumb(self.article.get_absolute_url(), self.article.title),
                Breadcrumb(self.child.get_absolute_url(), self.child.title),
                Breadcrumb(self.grandchild.get_absolute_url(), self.grandchild.title),
            ],
        )


class SlugPathMixinTest(TestCase):
    class DummyView(SlugPathMixin, SingleObjectMixin):
        model = Article

        def __init__(self, path):
            self.kwargs = {"path": path}

    def test_raises_404_when_article_not_found(self):
        """
        Raises a 404 error when an article
        matching the provided path couldn't be found.
        """
        view = self.DummyView("article-not-exist")
        with self.assertRaises(Http404):
            view.get_object()

        view = self.DummyView("another/article/not-exist/not")
        with self.assertRaises(Http404):
            view.get_object()

    def test_returns_article_when_matching_article_found(self):
        """
        Returns the article when an article
        matching the provided path is found.
        """
        article = ArticleFactory()
        view = self.DummyView(article.path())
        self.assertEqual(article, view.get_object())

        child = ArticleFactory(parent=article)
        grandchild = ArticleFactory(parent=child)
        view = self.DummyView(grandchild.path())
        self.assertEqual(grandchild, view.get_object())


class ArticleDetailTestCase(TestMixin, TestCase):
    def test_public_articles_do_not_require_login(self):
        """Should be able to view public articles without logging in."""
        article = ArticleFactory(public=True)
        response = self.client.get(
            reverse("articles:ArticleDetail", args=[article.path()])
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_not_public_articles_require_login(self):
        """Articles that aren't public should require logging in."""
        article = ArticleFactory(public=False)
        self.assertLoginRequired(
            reverse("articles:ArticleDetail", args=[article.path()])
        )

    def test_includes_only_public_subarticles_if_not_authenticated(self):
        """Should include only public subarticles if not authenticated."""
        article = ArticleFactory(public=True)
        subarticles_public = []
        for _ in range(3):
            subarticles_public.append(ArticleFactory(public=True, parent=article))
            ArticleFactory(public=False, parent=article)

        response = self.client.get(
            reverse("articles:ArticleDetail", args=[article.path()])
        )
        self.assertListEqual(
            list(response.context["subarticles"]),
            subarticles_public,
        )

    def test_includes_all_subarticles_if_authenticated(self):
        """Should include all subarticles if authenticated."""
        article = ArticleFactory(public=True)
        subarticles_public = [
            ArticleFactory(public=True, parent=article) for _ in range(3)
        ]
        subarticles_private = [
            ArticleFactory(public=False, parent=article) for _ in range(3)
        ]

        self.client.force_login(UserFactory())
        response = self.client.get(
            reverse("articles:ArticleDetail", args=[article.path()])
        )
        self.assertListEqual(
            list(response.context["subarticles"]),
            subarticles_public + subarticles_private,
        )


class ArticleCreateTestCase(TestMixin, TestCase):
    def get_url(self):
        return reverse("articles:ArticleCreate")

    def test_all_user_can_create_articles(self):
        """All users should be able to create an article."""
        self.client.force_login(UserFactory())
        self.client.post(
            self.get_url(),
            {"title": "A Title", "content": "Article text"},
        )

        self.assertEqual(Article.objects.count(), 1)

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url())


class SubarticleCreateTestCase(TestCase):
    def setUp(self):
        self.client.force_login(UserFactory())

    def test_form_initial_data_based_on_parent(self):
        """Should set the form's initial data based on the parent."""
        parent = ArticleFactory()
        response = self.client.get(
            reverse("articles:SubarticleCreate", args=[parent.path()])
        )
        self.assertDictEqual(
            response.context["form"].initial,
            {
                "parent": parent,
                "comments_allowed": parent.comments_allowed,
                "public": parent.public,
            },
        )


class ArticleUpdateTestCase(TestMixin, TestCase):
    def setUp(self):
        self.article = ArticleFactory()

    def get_url(self):
        return reverse("articles:ArticleUpdate", args=[self.article.path()])

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url())

    def test_requires_permission(self):
        """Should require the `change_article` permission."""
        self.assertPermissionRequired(self.get_url(), "articles.change_article")

    def test_succeeds_if_not_permission_but_is_author(self):
        """
        Should succeed if the user is the author,
        even if the user doesn't have the `change_event` permission.
        """
        self.client.force_login(self.article.created_by)
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, HTTPStatus.OK)


class ArticleDeleteTestCase(TestMixin, TestCase):
    def setUp(self):
        self.article = ArticleFactory()

    def get_url(self, path=None):
        return reverse("articles:ArticleDelete", args=[path or self.article.path()])

    def test_should_redirect_to_parent_on_success_if_exists(self):
        """Should redirect to the parent article on success, if it exists."""
        self.child = ArticleFactory(parent=self.article)
        self.client.force_login(SuperUserFactory())
        response = self.client.post(self.get_url(self.child.path()))
        self.assertRedirects(response, self.article.get_absolute_url())

    def test_should_redirect_to_dashboard_on_success_if_no_parent(self):
        """Should redirect to the dashboard on success, if the article doesn't have a parent."""
        self.client.force_login(SuperUserFactory())
        response = self.client.post(self.get_url())
        self.assertRedirects(response, reverse("dashboard:Dashboard"))

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url())

    def test_requires_permission(self):
        """Should require permission to delete articles."""
        self.assertPermissionRequired(
            self.get_url(),
            "articles.delete_article",
        )

    def test_succeeds_if_not_permission_but_is_author(self):
        """
        Should succeed if the user is the author,
        even if the user doesn't have permission to delete articles.
        """
        self.client.force_login(self.article.created_by)
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, HTTPStatus.OK)
