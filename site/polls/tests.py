from django.test import TestCase
from django.utils.text import slugify

from .factories import ChoiceFactory, PollFactory


class ForumTestSuite(TestCase):
    def setUp(self):
        self.poll = PollFactory()

    def test_get_absolute_url(self):
        """..."""
        pass

    def test_to_str(self):
        """`__str__` should be the question."""
        self.assertEqual(str(self.poll), self.poll.question)

    def test_creates_slug_from_question_automatically(self):
        """Should create a slug from the question automatically during creation."""
        self.assertEqual(self.poll.slug, slugify(self.poll.question))

    def test_unique_slugs(self):
        """Should create unique slugs."""
        poll_same_question = PollFactory(question=self.poll.question)
        self.assertNotEqual(self.poll.slug, poll_same_question.slug)

    def test_public_false_by_default(self):
        """Should set `public` to `False` by default."""
        self.assertFalse(self.poll.public)


class ChoiceTestSuite(TestCase):
    def setUp(self):
        self.poll = PollFactory()
        self.choice = ChoiceFactory(poll=self.poll)

    def test_to_str(self):
        """`__str__` should be the text."""
        self.assertEqual(str(self.choice), self.choice.text)


class VoteTestSuite(TestCase):
    def test_to_str(self):
        """`__str__` should be ???."""
        pass
