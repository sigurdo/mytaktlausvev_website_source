from django.db import IntegrityError
from django.test import TestCase
from django.utils.text import slugify

from accounts.factories import UserFactory

from .factories import ChoiceFactory, PollFactory, VoteFactory
from .models import PollType


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

    def test_type_single_choice_by_default(self):
        """Should set `type` to `SINGLE_CHOICE` by default."""
        self.assertEqual(self.poll.type, PollType.SINGLE_CHOICE)

    def test_num_votes(self):
        """Should return the total number of votes."""
        for _ in range(3):
            VoteFactory(choice__poll=self.poll)
        self.assertEqual(self.poll.num_votes, 3)

    def test_num_votes_excludes_votes_for_other_polls(self):
        """`num_votes` should exclude votes from other polls."""
        poll_different = PollFactory()
        for _ in range(3):
            VoteFactory(choice__poll=poll_different)

        VoteFactory(choice__poll=self.poll)
        self.assertEqual(self.poll.num_votes, 1)

    def test_num_votes_counts_multiple_votes_from_same_user(self):
        """`num_votes` should count multiple votes from the same user."""
        poll_multiple_choice = PollFactory(type=PollType.MULTIPLE_CHOICE)
        user = UserFactory()
        for _ in range(3):
            VoteFactory(choice__poll=poll_multiple_choice, user=user)
        self.assertEqual(poll_multiple_choice.num_votes, 3)

    def test_num_voting(self):
        """Should return the amount of people voting."""
        for _ in range(3):
            VoteFactory(choice__poll=self.poll)
        self.assertEqual(self.poll.num_voting, 3)

    def test_num_voting_excludes_votes_for_other_polls(self):
        """`num_voting` should exclude votes from other polls."""
        poll_different = PollFactory()
        for _ in range(3):
            VoteFactory(choice__poll=poll_different)

        VoteFactory(choice__poll=self.poll)
        self.assertEqual(self.poll.num_voting, 1)

    def test_num_voting_counts_only_single_vote_from_same_user(self):
        """`num_voting` should only count a single vote from the same user."""
        poll_multiple_choice = PollFactory(type=PollType.MULTIPLE_CHOICE)
        user = UserFactory()
        for _ in range(3):
            VoteFactory(choice__poll=poll_multiple_choice, user=user)
        self.assertEqual(poll_multiple_choice.num_voting, 1)


class ChoiceTestSuite(TestCase):
    def setUp(self):
        self.poll = PollFactory()
        self.choice = ChoiceFactory(poll=self.poll)

    def test_to_str(self):
        """`__str__` should be the text."""
        self.assertEqual(str(self.choice), self.choice.text)


class VoteTestSuite(TestCase):
    def setUp(self):
        self.poll = PollFactory()
        self.choice = ChoiceFactory(poll=self.poll)
        self.vote = VoteFactory(choice=self.choice)

    def test_to_str(self):
        """`__str__` should be ???."""
        pass

    def test_one_vote_per_user_per_choice(self):
        """Should only allow one vote per user per choice"""
        with self.assertRaises(IntegrityError):
            VoteFactory(choice=self.choice, user=self.vote.user)
