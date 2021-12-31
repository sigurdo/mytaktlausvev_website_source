from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import ViewDoesNotExist
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, FormView, ListView

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


class PollUpdate(PermissionRequiredMixin, FormAndFormsetUpdateView):
    model = Poll
    form_class = PollForm
    formset_class = ChoiceFormset
    formset_helper = ChoiceFormsetHelper
    template_name = "common/form.html"
    success_url = reverse_lazy("repertoire:RepertoireList")
    permission_required = (
        "polls.change_poll",
        "polls.add_choice",
        "polls.change_choice",
        "polls.delete_choice",
    )


class VoteCreate(LoginRequiredMixin, FormView):
    template_name = "common/form.html"
    success_url = reverse_lazy("repertoire:RepertoireList")

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
