from datetime import datetime
from http import HTTPStatus

from django.core.exceptions import NON_FIELD_ERRORS
from django.db import IntegrityError
from django.db.utils import InternalError
from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.text import slugify
from django.utils.timezone import make_aware

from accounts.factories import SuperUserFactory, UserFactory
from common.mixins import TestMixin
from common.test_utils import create_formset_post_data

from .factories import ChoiceFactory, PollFactory, VoteFactory
from .forms import ChoiceFormset, MultiVoteForm, SingleVoteForm
from .models import Choice, Poll, PollType, Vote


class PollTestSuite(TestCase):
    def setUp(self):
        self.poll = PollFactory()

    def test_get_absolute_url(self):
        """Absolute URL should be the poll redirect view."""
        self.assertEqual(
            self.poll.get_absolute_url(),
            reverse("polls:PollRedirect", args=[self.poll.slug]),
        )

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

    def test_changing_type_not_allowed(self):
        """Should not be able to change a poll's type."""
        with self.assertRaises(InternalError):
            self.poll.type = PollType.MULTIPLE_CHOICE
            self.poll.save()

    def test_votes(self):
        """Should return the poll's votes."""
        for _ in range(3):
            VoteFactory(choice__poll=self.poll)
            VoteFactory()
        self.assertEqual(self.poll.votes().count(), 3)
        for vote in self.poll.votes():
            self.assertEqual(vote.choice.poll, self.poll)

    def test_num_votes(self):
        """Should return the total number of votes."""
        for _ in range(3):
            VoteFactory(choice__poll=self.poll)
        self.assertEqual(self.poll.num_votes(), 3)

    def test_num_votes_excludes_votes_for_other_polls(self):
        """`num_votes` should exclude votes from other polls."""
        poll_different = PollFactory()
        for _ in range(3):
            VoteFactory(choice__poll=poll_different)

        VoteFactory(choice__poll=self.poll)
        self.assertEqual(self.poll.num_votes(), 1)

    def test_num_votes_counts_multiple_votes_from_same_user(self):
        """`num_votes` should count multiple votes from the same user."""
        poll_multiple_choice = PollFactory(type=PollType.MULTIPLE_CHOICE)
        user = UserFactory()
        for _ in range(3):
            VoteFactory(choice__poll=poll_multiple_choice, user=user)
        self.assertEqual(poll_multiple_choice.num_votes(), 3)

    def test_num_voting(self):
        """Should return the amount of people voting."""
        for _ in range(3):
            VoteFactory(choice__poll=self.poll)
        self.assertEqual(self.poll.num_voting(), 3)

    def test_num_voting_excludes_votes_for_other_polls(self):
        """`num_voting` should exclude votes from other polls."""
        poll_different = PollFactory()
        for _ in range(3):
            VoteFactory(choice__poll=poll_different)

        VoteFactory(choice__poll=self.poll)
        self.assertEqual(self.poll.num_voting(), 1)

    def test_num_voting_counts_only_single_vote_from_same_user(self):
        """`num_voting` should only count a single vote from the same user."""
        poll_multiple_choice = PollFactory(type=PollType.MULTIPLE_CHOICE)
        user = UserFactory()
        for _ in range(3):
            VoteFactory(choice__poll=poll_multiple_choice, user=user)
        self.assertEqual(poll_multiple_choice.num_voting(), 1)

    def test_latest_by_created(self):
        """Should get latest poll by `created`."""
        poll_early = PollFactory()
        poll_early.created = make_aware(datetime(1950, 5, 5))
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

    def test_winner(self):
        """Should return the winning choice of the poll."""
        winning_choice = ChoiceFactory(poll=self.poll)
        ChoiceFactory(poll=self.poll)
        VoteFactory(choice=winning_choice)

        self.assertEqual(self.poll.winner(), winning_choice)


class ChoiceTestSuite(TestCase):
    def setUp(self):
        self.poll = PollFactory()
        self.choice = ChoiceFactory(poll=self.poll)

    def test_to_str(self):
        """`__str__` should be the text."""
        self.assertEqual(str(self.choice), self.choice.text)

    def test_percentage(self):
        """
        `percentage` should return the choice's vote count
        as a percentage of the poll vote count,
        with 0 decimals.
        """
        self.assertEqual(self.choice.percentage(), "0%")

        VoteFactory(choice=self.choice)
        self.assertEqual(self.choice.percentage(), "100%")

        VoteFactory(choice__poll=self.poll)
        self.assertEqual(self.choice.percentage(), "50%")

    def test_percentage_excludes_other_polls(self):
        """
        `percentage` should not count votes
        for other polls.
        """
        VoteFactory(choice=self.choice)
        for _ in range(3):
            VoteFactory()
        self.assertEqual(self.choice.percentage(), "100%")


class VoteTestSuite(TestCase):
    def setUp(self):
        self.poll = PollFactory()
        self.choice = ChoiceFactory(poll=self.poll)
        self.vote = VoteFactory(choice=self.choice)

    def test_to_str(self):
        """
        `__str__` should include
        choice, poll, and username.
        """
        self.assertIn(str(self.vote.choice), str(self.vote))
        self.assertIn(str(self.vote.choice.poll), str(self.vote))
        self.assertIn(self.vote.user.username, str(self.vote))

    def test_one_vote_per_user_per_choice(self):
        """Should only allow one vote per user per choice"""
        with self.assertRaises(IntegrityError):
            VoteFactory(choice=self.choice, user=self.vote.user)


class SingleVoteFormTestSuite(TestCase):
    def setUp(self):
        self.poll = PollFactory()
        self.user = UserFactory()

    def test_limits_choice_queryset_to_poll(self):
        """Should only include choices related to the poll."""
        form = SingleVoteForm(poll=self.poll, user=self.user)
        self.assertQuerysetEqual(
            form.fields["choices"].queryset, Choice.objects.filter(poll=self.poll)
        )

    def test_can_only_vote_once_on_each_poll(self):
        """Should only be able to vote once on a poll."""
        VoteFactory(choice__poll=self.poll, user=self.user)

        form = SingleVoteForm(
            poll=self.poll,
            user=self.user,
            data={"choices": ChoiceFactory(poll=self.poll)},
        )
        self.assertFalse(form.is_valid())
        self.assertIn("Du har allereie stemt.", form.errors[NON_FIELD_ERRORS])

    def test_creates_vote_on_save(self):
        """Should create the vote for the user on `save()`."""
        choice = ChoiceFactory(poll=self.poll)
        form = SingleVoteForm(poll=self.poll, user=self.user, data={"choices": choice})

        self.assertTrue(form.is_valid())
        form.save()

        self.assertEqual(Vote.objects.count(), 1)
        vote = Vote.objects.last()
        self.assertEqual(vote.choice, choice)
        self.assertEqual(vote.user, self.user)

    def test_form_action_is_vote_view(self):
        """The form's `action` should be the vote view."""
        form = SingleVoteForm(poll=self.poll, user=self.user)
        self.assertEqual(
            form.helper.form_action, reverse("polls:VoteCreate", args=[self.poll.slug])
        )

    def test_includes_next_in_form_action(self):
        """Should include `next` in the form action, if it exists."""
        next = "/here-next/please/"
        form = SingleVoteForm(poll=self.poll, user=self.user, next=next)
        self.assertTrue(
            form.helper.form_action.endswith(f"?{urlencode({'next': next})}")
        )


class MultiVoteFormTestSuite(TestCase):
    def setUp(self):
        self.poll = PollFactory(type=PollType.SINGLE_CHOICE)
        self.user = UserFactory()

    def test_creates_votes_on_save(self):
        """Should create votes for the user on `save()`."""
        choices = [ChoiceFactory(poll=self.poll) for _ in range(3)]
        form = MultiVoteForm(poll=self.poll, user=self.user, data={"choices": choices})

        self.assertTrue(form.is_valid())
        form.save()

        self.assertEqual(Vote.objects.count(), 3)
        for vote, choice in zip(Vote.objects.all(), choices):
            self.assertEqual(vote.choice, choice)
            self.assertEqual(vote.user, self.user)


class PollListTestSuite(TestCase):
    def setUp(self):
        for _ in range(3):
            PollFactory()
            PollFactory(public=True)

    def get_url(self):
        return reverse("polls:PollList")

    def test_shows_all_polls_when_logged_in(self):
        """Should show all existing polls when logged in."""
        self.client.force_login(UserFactory())
        response = self.client.get(self.get_url())
        self.assertQuerysetEqual(response.context["polls"], Poll.objects.all())

    def test_show_only_public_polls_when_not_logged_in(self):
        """Should show only public polls when not logged in."""
        response = self.client.get(self.get_url())
        self.assertQuerysetEqual(
            response.context["polls"], Poll.objects.filter(public=True)
        )


class PollRedirectTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.poll = PollFactory()
        self.poll_public = PollFactory(public=True)

    def get_url(self, slug=None):
        return reverse("polls:PollRedirect", args=[slug or self.poll.slug])

    def test_404_if_poll_not_found(self):
        """Should return a 404 if the poll doesn't exist."""
        response = self.client.get(self.get_url(slug="poll-not-exist"))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_login_required_if_poll_not_public(self):
        """Should require login if the poll isn't public."""
        self.assertLoginRequired(self.get_url())

    def test_logged_in_not_voted(self):
        """
        Should redirect to vote view if
        user is logged in and hasn't voted.
        """
        self.client.force_login(UserFactory())
        response = self.client.get(self.get_url())
        self.assertRedirects(
            response, reverse("polls:VoteCreate", args=[self.poll.slug])
        )

    def test_logged_in_has_voted(self):
        """
        Should redirect to poll results view if
        user is logged in and has voted.
        """
        user = UserFactory()
        VoteFactory(choice__poll=self.poll, user=user)

        self.client.force_login(user)
        response = self.client.get(self.get_url())
        self.assertRedirects(
            response, reverse("polls:PollResults", args=[self.poll.slug])
        )

    def test_not_logged_in_public_poll(self):
        """
        Should redirect to the poll results view if
        user isn't logged in and the poll is public.
        """
        response = self.client.get(self.get_url(slug=self.poll_public.slug))
        self.assertRedirects(
            response, reverse("polls:PollResults", args=[self.poll_public.slug])
        )


class PollResultsTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.poll = PollFactory()

    def get_url(self, slug=None):
        return reverse("polls:PollResults", args=[slug or self.poll.slug])

    def test_login_required_if_poll_not_public(self):
        """Should require login if the poll isn't public."""
        self.assertLoginRequired(self.get_url())

    def test_login_not_required_if_poll_public(self):
        """Should not require login if the poll is public."""
        poll_public = PollFactory(public=True)
        response = self.client.get(self.get_url(poll_public.slug))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_adds_user_has_voted_to_context_data(self):
        """Should add whether the user has voted to context data."""
        user = UserFactory()
        self.client.force_login(user)

        response = self.client.get(self.get_url())
        self.assertFalse(response.context["user_has_voted"])

        VoteFactory(choice__poll=self.poll, user=user)
        response = self.client.get(self.get_url())
        self.assertTrue(response.context["user_has_voted"])


class PollVoteListTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.poll = PollFactory()
        for _ in range(3):
            VoteFactory(choice__poll=self.poll)

    def get_url(self, slug=None):
        return reverse("polls:PollVoteList", args=[slug or self.poll.slug])

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url())

    def test_404_if_poll_not_found(self):
        """Should return a 404 if the poll doesn't exist."""
        self.client.force_login(UserFactory())
        response = self.client.get(self.get_url(slug="poll-not-exist"))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_queryset_limited_to_poll_votes_sorted_by_created(self):
        """Should limit the queryset to votes for the poll and sort by `created`."""
        for _ in range(3):
            VoteFactory()

        self.client.force_login(UserFactory())
        response = self.client.get(self.get_url())
        self.assertQuerysetEqual(
            response.context["votes"],
            self.poll.votes().order_by("-created"),
        )

    def test_adds_poll_to_response_context(self):
        """Should add the poll to the response context."""
        self.client.force_login(UserFactory())
        response = self.client.get(self.get_url())
        self.assertEqual(response.context["poll"], self.poll)


class PollCreateTestSuite(TestMixin, TestCase):
    def get_url(self):
        return reverse("polls:PollCreate")

    def post(self):
        return self.client.post(
            self.get_url(),
            {
                "question": "Que?",
                "type": PollType.SINGLE_CHOICE,
                "public": False,
                **create_formset_post_data(
                    ChoiceFormset,
                    total_forms=0,
                    initial_forms=0,
                ),
            },
        )

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url())

    def test_requires_permission(self):
        """
        Should require permissions for adding polls and for adding choices.
        """
        self.assertPermissionRequired(
            self.get_url(),
            "polls.add_poll",
            "polls.add_choice",
        )

    def test_redirects_to_poll(self):
        """Should redirect to the created poll."""
        self.client.force_login(SuperUserFactory())
        response = self.post()
        self.assertEqual(Poll.objects.count(), 1)
        poll = Poll.objects.last()
        self.assertRedirects(
            response, poll.get_absolute_url(), fetch_redirect_response=False
        )

    def test_created_by_modified_by_set_to_current_user(self):
        """Should set `created_by` and `modified_by` to the current user on creation."""
        user = SuperUserFactory()
        self.client.force_login(user)
        self.post()

        self.assertEqual(Poll.objects.count(), 1)
        poll = Poll.objects.last()
        self.assertEqual(poll.created_by, user)
        self.assertEqual(poll.modified_by, user)


class PollUpdateTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.poll = PollFactory()

    def get_url(self):
        return reverse("polls:PollUpdate", args=[self.poll.slug])

    def post(self):
        return self.client.post(
            self.get_url(),
            {
                "question": self.poll.question,
                "type": self.poll.type,
                "public": self.poll.public,
                **create_formset_post_data(
                    ChoiceFormset,
                    total_forms=0,
                    initial_forms=0,
                ),
            },
        )

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url())

    def test_requires_permission(self):
        """
        Should require permissions for changing polls,
        for adding, changing, and deleting choices,
        and for deleting votes.
        """
        self.assertPermissionRequired(
            self.get_url(),
            "polls.change_poll",
            "polls.add_choice",
            "polls.change_choice",
            "polls.delete_choice",
            "polls.delete_vote",
        )

    def test_redirects_to_poll(self):
        """Should redirect to the updated poll."""
        self.client.force_login(SuperUserFactory())
        response = self.post()
        self.assertRedirects(
            response, self.poll.get_absolute_url(), fetch_redirect_response=False
        )

    def test_created_by_not_changed(self):
        """Should not change `created_by` when updating poll."""
        self.client.force_login(SuperUserFactory())
        self.post()

        created_by_previous = self.poll.created_by
        self.poll.refresh_from_db()
        self.assertEqual(self.poll.created_by, created_by_previous)

    def test_modified_by_set_to_current_user(self):
        """Should set `modified_by` to the current user on update."""
        user = SuperUserFactory()
        self.client.force_login(user)
        self.post()

        self.poll.refresh_from_db()
        self.assertEqual(self.poll.modified_by, user)


class PollDeleteTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.poll = PollFactory()

    def get_url(self):
        return reverse("polls:PollDelete", args=[self.poll.slug])

    def test_redirects_to_poll_list_on_success(self):
        """Should redirect to the poll list on success."""
        self.client.force_login(SuperUserFactory())
        response = self.client.post(self.get_url())
        self.assertRedirects(response, reverse("polls:PollList"))

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url())

    def test_requires_permission(self):
        """
        Should require permissions for deleting polls, choices, and votes.
        """
        self.assertPermissionRequired(
            self.get_url(),
            "polls.delete_poll",
            "polls.delete_choice",
            "polls.delete_vote",
        )


class VoteCreateTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.poll = PollFactory()

    def get_url(self, slug=None, next=None):
        url = reverse("polls:VoteCreate", args=[slug or self.poll.slug])
        if next:
            url += f"?{urlencode({'next': next})}"
        return url

    def vote(self, url=None):
        return self.client.post(
            url or self.get_url(), {"choices": ChoiceFactory(poll=self.poll).pk}
        )

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url())

    def test_404_if_poll_not_found(self):
        """Should return a 404 if the poll isn't found."""
        self.client.force_login(UserFactory())
        response = self.client.get(self.get_url("poll-not-exist"))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_adds_poll_to_context_data(self):
        """Should add the poll to the context data."""
        self.client.force_login(UserFactory())
        response = self.client.get(self.get_url())
        self.assertEqual(response.context["poll"], self.poll)

    def test_vote_registered_for_logged_in_user(self):
        """Should register the vote for the logged in user."""
        user = UserFactory()
        self.client.force_login(user)
        self.vote()

        self.assertEqual(Vote.objects.count(), 1)
        vote = Vote.objects.last()
        self.assertEqual(vote.user, user)

    def test_can_only_vote_once_on_each_poll(self):
        """Should only be able to vote once on a poll."""
        user = UserFactory()
        VoteFactory(choice__poll=self.poll, user=user)

        self.client.force_login(user)
        response = self.vote()
        self.assertEqual(Vote.objects.count(), 1)
        self.assertIn(
            "Du har allereie stemt.", response.context["form"].non_field_errors()
        )

    def test_vote_multiple_choice_poll(self):
        user = UserFactory()
        self.client.force_login(user)

        poll_multiple = PollFactory(type=PollType.MULTIPLE_CHOICE)
        self.client.post(
            self.get_url(poll_multiple.slug),
            {"choices": [ChoiceFactory(poll=poll_multiple).pk for _ in range(3)]},
        )
        self.assertEqual(Vote.objects.count(), 3)

    def test_success_redirect(self):
        """Should redirect to the poll results page."""
        self.client.force_login(UserFactory())
        response = self.vote()
        self.assertRedirects(
            response, reverse("polls:PollResults", args=[self.poll.slug])
        )

    def test_success_redirect_with_next(self):
        """Should return to the provided next URL if provided and safe."""
        next = reverse("polls:PollList")
        self.client.force_login(UserFactory())
        response = self.vote(url=self.get_url(next=next))
        self.assertRedirects(response, next)


class VoteDeleteTestSuite(TestMixin, TestCase):
    def setUp(self):
        self.poll = PollFactory()
        self.user = UserFactory()
        VoteFactory(choice__poll=self.poll, user=self.user)

    def get_url(self, slug=None):
        return reverse("polls:VoteDelete", args=[slug or self.poll.slug])

    def test_requires_login(self):
        """Should require login."""
        self.assertLoginRequired(self.get_url())

    def test_404_if_poll_not_found(self):
        """Should return a 404 if the poll isn't found."""
        self.client.force_login(self.user)
        response = self.client.get(self.get_url("poll-not-exist"))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_404_if_has_not_voted(self):
        """Should return a 404 if the user hasn't voted for the poll."""
        self.client.force_login(UserFactory())
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_adds_poll_to_context_data(self):
        """Should add the poll to the context data."""
        self.client.force_login(self.user)
        response = self.client.get(self.get_url())
        self.assertEqual(response.context["poll"], self.poll)

    def test_adds_user_votes_to_context_data(self):
        """Should add the user's votes to the context data."""
        self.client.force_login(self.user)
        response = self.client.get(self.get_url())
        self.assertQuerysetEqual(
            response.context["votes"], self.poll.votes().filter(user=self.user)
        )

    def test_deletes_user_vote(self):
        """Should delete the user's vote."""
        self.client.force_login(self.user)
        self.client.post(self.get_url())
        self.assertEqual(Vote.objects.count(), 0)
        self.assertFalse(self.poll.has_voted(self.user))

    def test_deletes_all_user_votes_if_multi_choice_poll(self):
        """
        Should delete all of a user's votes if
        the poll is multiple choice.
        """
        poll_multiple_choice = PollFactory(type=PollType.MULTIPLE_CHOICE)
        for _ in range(3):
            VoteFactory(choice__poll=poll_multiple_choice, user=self.user)
        self.client.force_login(self.user)
        self.client.post(self.get_url(poll_multiple_choice.slug))
        self.assertEqual(Vote.objects.count(), 1)
        self.assertFalse(poll_multiple_choice.has_voted(self.user))

    def test_does_not_delete_other_user_votes(self):
        """Should not delete the votes of other users."""
        for _ in range(3):
            VoteFactory(choice__poll=self.poll)
        self.client.force_login(self.user)
        self.client.post(self.get_url())
        self.assertEqual(Vote.objects.count(), 3)

    def test_redirects_to_poll_redirect(self):
        """Should redirect to the poll redirect page on success."""
        self.client.force_login(self.user)
        response = self.client.post(self.get_url())
        self.assertRedirects(
            response, self.poll.get_absolute_url(), fetch_redirect_response=False
        )
