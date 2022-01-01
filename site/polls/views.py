from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.core.exceptions import ViewDoesNotExist
from django.forms import Form
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.urls.base import reverse
from django.views.generic import CreateView, DetailView, FormView, ListView
from django.views.generic.base import RedirectView

from common.views import FormAndFormsetUpdateView

from .forms import (
    ChoiceFormset,
    ChoiceFormsetHelper,
    MultiVoteForm,
    PollForm,
    SingleVoteForm,
)
from .models import Poll, PollType, Vote


class PollList(ListView):
    model = Poll
    context_object_name = "polls"
    paginate_by = 25

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return super().get_queryset()
        return super().get_queryset().filter(public=True)


class PollRedirect(UserPassesTestMixin, RedirectView):
    poll = None

    def get_poll(self):
        if not self.poll:
            self.poll = get_object_or_404(Poll, slug=self.kwargs["slug"])
        return self.poll

    def test_func(self):
        return self.get_poll().public or self.request.user.is_authenticated

    def get_redirect_url(self, *args, **kwargs):
        poll = self.get_poll()
        if not self.request.user.is_authenticated or poll.has_voted(self.request.user):
            url_name = "polls:PollResults"
        else:
            url_name = "polls:VoteCreate"

        return reverse(url_name, args=[poll.slug])


class PollResults(DetailView):
    model = Poll


class PollVotes(LoginRequiredMixin, ListView):
    model = Vote
    template_name = "polls/poll_votes.html"
    context_object_name = "votes"

    poll = None

    def get_poll(self):
        if not self.poll:
            self.poll = get_object_or_404(Poll, slug=self.kwargs["slug_poll"])
        return self.poll

    def get_queryset(self):
        """Limit queryset to poll votes and sort by `created` descending."""
        return (
            super()
            .get_queryset()
            .filter(choice__poll=self.get_poll())
            .order_by("-created")
        )

    def get_context_data(self, **kwargs):
        kwargs["poll"] = self.get_poll()
        return super().get_context_data(**kwargs)


class PollUpdate(PermissionRequiredMixin, FormAndFormsetUpdateView):
    model = Poll
    form_class = PollForm
    formset_class = ChoiceFormset
    formset_helper = ChoiceFormsetHelper
    template_name = "common/form.html"
    permission_required = (
        "polls.change_poll",
        "polls.add_choice",
        "polls.change_choice",
        "polls.delete_choice",
    )

    def get_success_url(self) -> str:
        return self.get_object().get_absolute_url()


class VoteCreate(LoginRequiredMixin, FormView):
    template_name = "common/form.html"

    poll = None

    def get_poll(self):
        if not self.poll:
            self.poll = get_object_or_404(Poll, slug=self.kwargs["slug_poll"])
        return self.poll

    def get_form_class(self):
        return (
            SingleVoteForm
            if self.get_poll().type == PollType.SINGLE_CHOICE
            else MultiVoteForm
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"poll": self.get_poll(), "user": self.request.user})
        return kwargs

    def get_context_data(self, **kwargs):
        kwargs["form_title"] = self.get_poll().question
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse("polls:PollResults", args=[self.get_poll().slug])


class VoteDelete(LoginRequiredMixin, FormView):
    template_name = "polls/vote_delete.html"
    form_class = Form

    poll = None
    votes = None

    def get_poll(self):
        if not self.poll:
            self.poll = get_object_or_404(Poll, slug=self.kwargs["slug_poll"])
        return self.poll

    def get_votes(self):
        if not self.votes:
            self.votes = self.get_poll().votes.filter(user=self.request.user)
        if not self.votes.exists():
            raise Http404("Du har ikkje stemt på denne avstemminga.")
        return self.votes

    def get_context_data(self, **kwargs):
        kwargs["poll"] = self.get_poll()
        kwargs["votes"] = self.get_votes()
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        self.get_votes().delete()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return self.get_poll().get_absolute_url()
