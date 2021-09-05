from http import HTTPStatus
from django.http.response import Http404
from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify
from django.views.generic.detail import SingleObjectMixin
from accounts.factories import UserFactory, SuperUserFactory
from articles.views import SlugPathMixin
from .models import Article
from .factories import ArticleFactory


class ArticleTestCase(TestCase):
    def setUp(self):
        self.article = ArticleFactory()
        self.child = ArticleFactory(parent=self.article)
        self.grandchild = ArticleFactory(parent=self.child)
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
            reverse("articles:detail", args=[self.article.path()]),
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

    def test_creates_unique_slugs(self):
        """Should create unique slugs even if titles match."""
        article_same_title = ArticleFactory(title=self.article.title)
        self.assertNotEqual(self.article.slug, article_same_title.slug)

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


class ArticleDetailTestCase(TestCase):
    def test_public_articles_do_not_require_login(self):
        """Should be able to view public articles without logging in."""
        article = ArticleFactory(public=True)
        response = self.client.get(reverse("articles:detail", args=[article.slug]))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_not_public_articles_require_login(self):
        """Articles that aren't public should require logging in."""
        article = ArticleFactory(public=False)
        response = self.client.get(reverse("articles:detail", args=[article.slug]))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(response.url.startswith(reverse("login")))


class ArticleCreateTestCase(TestCase):
    def test_created_by_modified_by_set_to_current_user(self):
        """Should set `created_by` and `modified_by` to the current user on creation."""
        user = SuperUserFactory()
        self.client.force_login(user)
        self.client.post(
            reverse("articles:create_article"),
            {"title": "A Title", "content": "Article text"},
        )

        self.assertEqual(Article.objects.count(), 1)
        article = Article.objects.last()
        self.assertEqual(article.created_by, user)
        self.assertEqual(article.modified_by, user)

    def test_requires_login(self):
        """Should redirect to login page if user is not logged in."""
        response = self.client.get(reverse("articles:create_article"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(response.url.startswith(reverse("login")))

    def test_fails_if_missing_permission(self):
        """Should fail if missing add permission."""
        self.user = UserFactory()
        self.client.force_login(self.user)
        response = self.client.get(reverse("articles:create_article"))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_succeeds_if_has_permission(self):
        """Should succeed if user has add permission."""
        self.user = UserFactory(permissions=("articles.add_article",))
        self.client.force_login(self.user)
        response = self.client.get(reverse("articles:create_article"))
        self.assertEqual(response.status_code, HTTPStatus.OK)


class SubarticleCreateTestCase(TestCase):
    def setUp(self):
        user = SuperUserFactory()
        self.client.force_login(user)

    def test_form_initial_data_based_on_parent(self):
        """Should set the form's initial data based on the parent."""
        parent = ArticleFactory()
        response = self.client.get(
            reverse("articles:create_subarticle", args=[parent.path()])
        )
        self.assertDictEqual(
            response.context["form"].initial,
            {
                "parent": parent,
                "comments_allowed": parent.comments_allowed,
                "public": parent.public,
            },
        )


class ArticleUpdateTestCase(TestCase):
    def setUp(self):
        self.article = ArticleFactory()

    def test_requires_login(self):
        """Should redirect to login page if user is not logged in."""
        response = self.client.get(reverse("articles:update", args=[self.article.slug]))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(response.url.startswith(reverse("login")))

    def test_fails_if_missing_permission(self):
        """Should fail if missing change permission."""
        self.user = UserFactory()
        self.client.force_login(self.user)
        response = self.client.get(reverse("articles:update", args=[self.article.slug]))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_succeeds_if_has_permission(self):
        """Should succeed if user has change permission."""
        self.user = UserFactory(permissions=("articles.change_article",))
        self.client.force_login(self.user)
        response = self.client.get(reverse("articles:update", args=[self.article.slug]))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_created_by_not_changed(self):
        """Should not change `created_by` when updating article."""
        user = SuperUserFactory()
        self.client.force_login(user)
        self.client.post(
            reverse("articles:update", args=[self.article.slug]),
            {"title": "A Title", "content": "Article text"},
        )

        created_by_previous = self.article.created_by
        self.article.refresh_from_db()
        self.assertEqual(self.article.created_by, created_by_previous)

    def test_modified_by_set_to_current_user(self):
        """Should set `modified_by` to the current user on update."""
        user = SuperUserFactory()
        self.client.force_login(user)
        self.client.post(
            reverse("articles:update", args=[self.article.slug]),
            {"title": "A Title", "content": "Article text"},
        )

        self.article.refresh_from_db()
        self.assertEqual(self.article.modified_by, user)
