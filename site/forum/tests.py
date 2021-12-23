from django.test import TestCase
from django.utils.text import slugify

from .factories import ForumFactory, PostFactory, TopicFactory


class ForumTestSuite(TestCase):
    def setUp(self):
        self.forum = ForumFactory()

    def test_get_absolute_url(self):
        """Should link to the forum's detail page."""
        pass

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


class TopicTestSuite(TestCase):
    def setUp(self):
        self.topic = TopicFactory()

    def test_get_absolute_url(self):
        """Should link to the topic's detail page."""
        pass

    def test_creates_slug_from_title_automatically(self):
        """Should create a slug from the title automatically during creation."""
        self.assertEqual(self.topic.slug, slugify(self.topic.title))

    def test_does_not_update_slug_when_title_is_changed(self):
        """Should not change the slug when the title is changed."""
        slug_before = self.topic.slug
        self.topic.title = "Different title"
        self.topic.save()
        self.assertEqual(self.topic.slug, slug_before)

    def test_unique_slugs(self):
        """Should create unique slugs."""
        topic_same_title = TopicFactory(title=self.topic.title)
        self.assertNotEqual(self.topic.slug, topic_same_title.slug)

    def test_does_not_override_provided_slug(self):
        """Should not override the slug if provided during creation."""
        slug = "this-is-a-slug"
        topic = TopicFactory(
            title="Title that is very different from the slug", slug=slug
        )
        self.assertEqual(topic.slug, slug)


class PostTestSuite(TestCase):
    def setUp(self):
        self.post = PostFactory()

    def test_get_absolute_url(self):
        """Should link to the post in the topic."""
        pass

    def test_content_short_truncated_when_long(self):
        """
        `content_short` should be truncated to 40 chars
        when `content` is long.
        """
        self.assertEqual(len(self.post.content_short()), 40)

    def test_content_short_ends_with_ellipsis_when_truncated(self):
        """`content_short` should end with an ellipsis when truncated."""
        self.assertEqual(self.post.content_short()[-1], "…")

    def test_content_short_unchanged_when_short_content(self):
        """`content_short` should be unchanged when `content` is less than 40 chars."""
        self.post.content = "I am short."
        self.assertEqual(self.post.content_short(), self.post.content)

    def test_to_str(self):
        """`__str__` should be equal to `content_short`."""
        self.assertEqual(str(self.post), self.post.content_short())
        self.post.content = "Ya ya ya"
        self.assertEqual(str(self.post), self.post.content_short())
