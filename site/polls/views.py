from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import Form
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from django.urls.base import reverse, reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic import DetailView, FormView, ListView
from django.views.generic.base import RedirectView

from common.breadcrumbs.breadcrumbs import Breadcrumb, BreadcrumbsMixin
from common.forms.views import (
    DeleteViewCustom,
    InlineFormsetCreateView,
    InlineFormsetUpdateView,
)

from .forms import (
    ChoiceFormset,
    MultiVoteForm,
    PollCreateForm,
    PollUpdateForm,
    SingleVoteForm,
)
from .models import Poll, PollType, Vote


def breadcrumbs(poll=None):
    """Returns breadcrumbs for the poll views."""
    breadcrumbs = [Breadcrumb(reverse("polls:PollList"), "Alle avstemmingar")]
    if poll:
        breadcrumbs.append(Breadcrumb(poll.get_absolute_url(), poll))
    return breadcrumbs


class PollMixin:
    """
    Provides a function for getting a poll
    based on a slug URL kwarg.

    Adds the poll to context data.

    Returns 404 if the poll doesn't exist.
    """

    poll = None

    def get_poll(self):
        if not self.poll:
            self.poll = get_object_or_404(Poll, slug=self.kwargs["slug"])
        return self.poll

    def get_context_data(self, **kwargs):
        kwargs["poll"] = self.get_poll()
        return super().get_context_data(**kwargs)


class PollList(ListView):
    model = Poll
    context_object_name = "polls"
    paginate_by = 25

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return super().get_queryset()
        return super().get_queryset().filter(public=True)


class PollRedirect(UserPassesTestMixin, PollMixin, RedirectView):
    def test_func(self):
        return self.get_poll().public or self.request.user.is_authenticated

    def get_redirect_url(self, *args, **kwargs):
        poll = self.get_poll()
        if not self.request.user.is_authenticated or poll.has_voted(self.request.user):
            url_name = "polls:PollResults"
        else:
            url_name = "polls:VoteCreate"

        return reverse(url_name, args=[poll.slug])


class PollResults(UserPassesTestMixin, BreadcrumbsMixin, DetailView):
    model = Poll
    template_name_suffix = "_results"

    def test_func(self):
        return self.get_object().public or self.request.user.is_authenticated

    def get_breadcrumbs(self) -> list:
        return breadcrumbs()

    def get_context_data(self, **kwargs):
        kwargs[
            "user_has_voted"
        ] = self.request.user.is_authenticated and self.object.has_voted(
            self.request.user
        )
        return super().get_context_data(**kwargs)


class PollVoteList(LoginRequiredMixin, BreadcrumbsMixin, PollMixin, ListView):
    model = Vote
    template_name = "polls/poll_vote_list.html"
    context_object_name = "votes"

    def get_queryset(self):
        """Limit queryset to poll votes and sort by `created` descending."""
        return (
            super()
            .get_queryset()
            .filter(choice__poll=self.get_poll())
            .order_by("-created")
        )

    def get_breadcrumbs(self) -> list:
        return breadcrumbs(self.get_poll())


class PollCreate(PermissionRequiredMixin, BreadcrumbsMixin, InlineFormsetCreateView):
    model = Poll
    form_class = PollCreateForm
    formset_class = ChoiceFormset
    template_name = "common/forms/form.html"
    permission_required = ("polls.add_poll", "polls.add_choice")

    def get_breadcrumbs(self) -> list:
        return breadcrumbs()

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        super().form_valid(form)


class PollUpdate(PermissionRequiredMixin, BreadcrumbsMixin, InlineFormsetUpdateView):
    model = Poll
    form_class = PollUpdateForm
    formset_class = ChoiceFormset
    template_name = "common/forms/form.html"
    permission_required = (
        "polls.change_poll",
        "polls.add_choice",
        "polls.change_choice",
        "polls.delete_choice",
        "polls.delete_vote",
    )

    def get_breadcrumbs(self) -> list:
        return breadcrumbs(self.object)

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        super().form_valid(form)


class PollDelete(PermissionRequiredMixin, BreadcrumbsMixin, DeleteViewCustom):
    model = Poll
    success_url = reverse_lazy("polls:PollList")
    permission_required = (
        "polls.delete_poll",
        "polls.delete_choice",
        "polls.delete_vote",
    )

    def get_breadcrumbs(self) -> list:
        return breadcrumbs(self.object)


class VoteCreate(LoginRequiredMixin, BreadcrumbsMixin, PollMixin, FormView):
    template_name = "polls/vote_form.html"

    def get_form_class(self):
        return (
            SingleVoteForm
            if self.get_poll().type == PollType.SINGLE_CHOICE
            else MultiVoteForm
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["poll"] = self.get_poll()
        kwargs["user"] = self.request.user
        return kwargs

    def get_breadcrumbs(self) -> list:
        return breadcrumbs()

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_next_url(self):
        """Returns the next URL if it exists and is safe, else `None`."""
        next = self.request.GET.get(self.redirect_field_name, "")
        url_is_safe = url_has_allowed_host_and_scheme(
            url=next,
            allowed_hosts=self.request.get_host(),
            require_https=self.request.is_secure(),
        )
        return next if next and url_is_safe else None

    def get_success_url(self) -> str:
        next = self.get_next_url()
        if next:
            return next
        return reverse("polls:PollResults", args=[self.get_poll().slug])


class VoteDelete(
    LoginRequiredMixin, BreadcrumbsMixin, PollMixin, SuccessMessageMixin, FormView
):
    template_name = "polls/vote_delete.html"
    form_class = Form
    success_message = "Stemma di vart fjerna."

    votes = None

    def get_votes(self):
        if not self.votes:
            self.votes = self.get_poll().votes().filter(user=self.request.user)
        if not self.votes.exists():
            raise Http404("Du har ikkje stemt på denne avstemminga.")
        return self.votes

    def get_breadcrumbs(self) -> list:
        return breadcrumbs(self.get_poll())

    def get_context_data(self, **kwargs):
        kwargs["votes"] = self.get_votes()
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        self.get_votes().delete()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return self.get_poll().get_absolute_url()
