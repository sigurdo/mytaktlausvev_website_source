from datetime import datetime
from http import HTTPStatus

from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.db import IntegrityError
from django.http.response import Http404
from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify
from django.utils.timezone import make_aware

from accounts.factories import UserFactory
from common.mixins import TestMixin

from .factories import ChoiceFactory, PollFactory, VoteFactory
from .forms import VoteCreateForm
from .models import Choice, Poll, PollType, Vote


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

    def test_latest_by_submitted(self):
        """Should get latest poll by `submitted`."""
        poll_early = PollFactory()
        poll_early.submitted = make_aware(datetime(1950, 5, 5))
        poll_early.save()
        self.assertEqual(Poll.objects.latest(), self.poll)

    def test_has_voted_returns_true_if_user_has_voted(self):
        """`has_voted` should return `True` if the user has voted for the poll."""
        user = UserFactory()
        VoteFactory(user=user, choice__poll=self.poll)
        self.assertTrue(self.poll.has_voted(user))

    def test_has_voted_returns_false_if_user_has_not_voted(self):
        """`has_voted` should return `False` if the user hasn't voted for the poll."""
        self.assertFalse(self.poll.has_voted(UserFactory()))


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


class VoteCreateFormTestSuite(TestCase):
    def setUp(self):
        self.poll = PollFactory()

    def test_limits_choice_queryset_to_poll(self):
        """Should only include choices related to the poll."""
        form = VoteCreateForm(poll=self.poll)
        self.assertQuerysetEqual(
            form.fields["choice"].queryset, Choice.objects.filter(poll=self.poll)
        )

    def test_can_only_vote_once_on_each_poll(self):
        """Should only be able to vote once on a poll."""
        user = UserFactory()
        VoteFactory(choice__poll=self.poll, user=user)

        form = VoteCreateForm(
            poll=self.poll, data={"choice": ChoiceFactory(poll=self.poll)}
        )
        form.instance.user = user
        self.assertFalse(form.is_valid())
        self.assertIn("Du har allereie stemt.", form.errors[NON_FIELD_ERRORS])


class PollUpdateTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.poll = PollFactory()

    def get_url(self):
        return reverse("polls:PollUpdate", args=[self.poll.slug])

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url())

    def test_requires_permission(self):
        """
        Should require permissions for changing polls,
        and for adding, changing, and deleting choices.
        """
        self.assertPermissionRequired(
            self.get_url(),
            "polls.change_poll",
            "polls.add_choice",
            "polls.change_choice",
            "polls.delete_choice",
        )

    def test_redirects_to_poll(self):
        """Should redirect to the updated poll."""
        pass


class VoteCreateTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.poll = PollFactory()

    def get_url(self):
        return reverse("polls:VoteCreate", args=[self.poll.slug])

    def vote(self, choice=None):
        return self.client.post(
            self.get_url(), {"choice": (choice or ChoiceFactory(poll=self.poll)).pk}
        )

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url())

    def test_404_if_poll_not_found(self):
        """Should return a 404 if the poll isn't found."""
        self.client.force_login(UserFactory())
        response = self.client.get(reverse("polls:VoteCreate", args=["poll-not-exist"]))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_vote_registered_for_logged_in_user(self):
        """Should register the vote for the logged in user."""
        user = UserFactory()
        self.client.force_login(user)
        response = self.vote()

        self.assertEqual(Vote.objects.count(), 1)
        vote = Vote.objects.last()
        self.assertEqual(vote.user, user)

    def test_can_only_vote_once_on_each_poll(self):
        """Should only be able to vote once on a poll."""
        user = UserFactory()
        VoteFactory(choice__poll=self.poll, user=user)

        self.client.force_login(user)
        response = self.vote()
        self.assertFormError(response, "form", None, "Du har allereie stemt.")
        self.assertEqual(Vote.objects.count(), 1)

    def test_success_redirect(self):
        """Should ..."""
        pass
