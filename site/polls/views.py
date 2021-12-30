from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView

from common.views import FormAndFormsetUpdateView

from .forms import ChoiceFormset, ChoiceFormsetHelper, PollForm, VoteCreateForm
from .models import Poll, Vote


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


class VoteCreate(LoginRequiredMixin, CreateView):
    model = Vote
    form_class = VoteCreateForm
    template_name = "common/form.html"
    success_url = reverse_lazy("repertoire:RepertoireList")

    poll = None

    def get_poll(self):
        if not self.poll:
            self.poll = get_object_or_404(Poll, slug=self.kwargs["slug_poll"])
        return self.poll

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.instance.user = self.request.user
        return form

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"poll": self.get_poll()})
        return kwargs

    def get_context_data(self, **kwargs):
        kwargs["form_title"] = self.get_poll().question
        return super().get_context_data(**kwargs)
