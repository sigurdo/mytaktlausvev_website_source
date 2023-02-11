from datetime import datetime
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify
from django.utils.timezone import make_aware

from accounts.factories import SuperUserFactory, UserFactory
from common.comments.factories import CommentFactory
from common.mixins import TestMixin

from .factories import ForumFactory, TopicFactory
from .models import Topic
from .views import ForumList, TopicList


def create_post_override_created(created, topic=None, **kwargs):
    """
    Creates a post and overrides `created`.
    `created` must be set after creation to override `auto_now_add`.
    """
    post = CommentFactory(content_object=topic, **kwargs)
    post.created = created
    post.save()
    return post


class ForumTestSuite(TestCase):
    def setUp(self):
        self.forum = ForumFactory()

    def test_get_absolute_url(self):
        """Should link to the forum's topic list page."""
        self.assertEqual(
            self.forum.get_absolute_url(),
            reverse("forum:TopicList", args=[self.forum.slug]),
        )

    def test_creates_slug_from_title_automatically(self):
        """Should create a slug from the title automatically during creation."""
        self.assertEqual(self.forum.slug, slugify(self.forum.title))

    def test_does_not_update_slug_when_title_is_changed(self):
        """Should not change the slug when the title is changed."""
        slug_before = self.forum.slug
        self.forum.title = "Different title"
        self.forum.save()
        self.assertEqual(self.forum.slug, slug_before)

    def test_unique_slugs(self):
        """Should create unique slugs."""
        forum_same_title = ForumFactory(title=self.forum.title)
        self.assertNotEqual(self.forum.slug, forum_same_title.slug)

    def test_does_not_override_provided_slug(self):
        """Should not override the slug if provided during creation."""
        slug = "this-is-a-slug"
        forum = ForumFactory(
            title="Title that is very different from the slug", slug=slug
        )
        self.assertEqual(forum.slug, slug)

    def test_latest_post_returns_latest_in_forum_topics(self):
        """`latest_post()` should return the latest post in the forum's topics."""
        topic_in_forum = TopicFactory(forum=self.forum)
        topic_in_different_forum = TopicFactory()
        latest_in_forum = create_post_override_created(
            make_aware(datetime(2200, 1, 1)), topic=topic_in_forum
        )
        create_post_override_created(
            make_aware(datetime(2250, 1, 1)), topic=topic_in_different_forum
        )

        self.assertEqual(self.forum.latest_post(), latest_in_forum)


class TopicTestSuite(TestCase):
    def setUp(self):
        self.topic = TopicFactory()

    def test_get_absolute_url(self):
        """Should link to the topic's post list page."""
        self.assertEqual(
            self.topic.get_absolute_url(),
            reverse("forum:TopicDetail", args=[self.topic.forum.slug, self.topic.slug]),
        )

    def test_creates_slug_from_title_automatically(self):
        """Should create a slug from the title automatically during creation."""
        self.assertEqual(self.topic.slug, slugify(self.topic.title))

    def test_does_not_update_slug_when_title_is_changed(self):
        """Should not change the slug when the title is changed."""
        slug_before = self.topic.slug
        self.topic.title = "Different title"
        self.topic.save()
        self.assertEqual(self.topic.slug, slug_before)

    def test_creates_unique_slugs_for_topics_in_same_forum(self):
        """Should create unique slugs for topics in the same forum."""
        topic_same_forum = TopicFactory(title=self.topic.title, forum=self.topic.forum)
        self.assertNotEqual(self.topic.slug, topic_same_forum.slug)

    def test_topics_in_different_forums_can_have_equal_slugs(self):
        """Should allow topics in different forums to have equal slugs."""
        topic_different_forum = TopicFactory(
            title=self.topic.title, forum=ForumFactory()
        )
        self.assertEqual(self.topic.slug, topic_different_forum.slug)

    def test_does_not_override_provided_slug(self):
        """Should not override the slug if provided during creation."""
        slug = "this-is-a-slug"
        topic = TopicFactory(
            title="Title that is very different from the slug", slug=slug
        )
        self.assertEqual(topic.slug, slug)


class ForumListTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("forum:ForumList")

    def test_requires_login(self):
        self.assertLoginRequired(self.get_url())

    def test_breadcrumbs(self):
        """
        ForumList should have an empty list of breadcrumbs
        """
        self.client.force_login(SuperUserFactory())
        breadcrumbs = self.client.get(self.get_url()).context["breadcrumbs"]
        self.assertEqual(breadcrumbs, [])


class TopicListTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.forum = ForumFactory()

    def get_url(self):
        return reverse("forum:TopicList", args=[self.forum.slug])

    def test_requires_login(self):
        self.assertLoginRequired(self.get_url())

    def test_breadcrumbs(self):
        """
        TopicList should have breadcrumbs for the following views:
        ForumList
        """
        self.client.force_login(SuperUserFactory())
        breadcrumbs = self.client.get(self.get_url()).context["breadcrumbs"]
        self.assertEqual(
            breadcrumbs,
            [
                ForumList.get_breadcrumb(),
            ],
        )


class TopicCreateTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("forum:TopicCreate", args=[self.forum.slug])

    def setUp(self):
        self.forum = ForumFactory()

    def test_requires_login(self):
        self.assertLoginRequired(self.get_url())

    def test_create_topic(self):
        self.client.force_login(UserFactory())
        self.client.post(
            self.get_url(),
            {
                "title": "Kva er forskjellen på ein elefant?",
            },
        )
        topics = Topic.objects.all()
        self.assertEqual(len(topics), 1)
        topic = topics.last()
        self.assertEqual(topic.title, "Kva er forskjellen på ein elefant?")

    def test_breadcrumbs(self):
        """
        TopicCreate should have breadcrumbs for the following views:
        ForumList / TopicList
        """
        self.client.force_login(SuperUserFactory())
        breadcrumbs = self.client.get(self.get_url()).context["breadcrumbs"]
        self.assertEqual(
            breadcrumbs,
            [
                ForumList.get_breadcrumb(),
                TopicList.get_breadcrumb(self.forum),
            ],
        )


class PostListTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.topic = TopicFactory()

    def get_url(self, args=None):
        return reverse(
            "forum:TopicDetail", args=args or [self.topic.forum.slug, self.topic.slug]
        )

    def test_requires_login(self):
        self.assertLoginRequired(self.get_url())

    def test_returns_404_if_topic_not_exist(self):
        """Should return 404 if the topic doesn't exist."""
        self.client.force_login(SuperUserFactory())
        response = self.client.get(self.get_url(["forum-not-exist", "topic-not-exist"]))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_breadcrumbs(self):
        """
        PostList should have breadcrumbs for the following views:
        ForumList / TopicList
        """
        self.client.force_login(SuperUserFactory())
        breadcrumbs = self.client.get(self.get_url()).context["breadcrumbs"]
        self.assertEqual(
            breadcrumbs,
            [
                ForumList.get_breadcrumb(),
                TopicList.get_breadcrumb(self.topic.forum),
            ],
        )
