import random
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from .models import Julekalender, Window
from .forms import AdventCalendarForm, WindowCreateForm, WindowUpdateForm


class AdventCalendarList(LoginRequiredMixin, ListView):
    """View for viewing all advent calendars."""

    model = Julekalender


class AdventCalendarCreate(PermissionRequiredMixin, CreateView):
    """View for creating advent calendars."""

    model = Julekalender
    form_class = AdventCalendarForm
    permission_required = "julekalender.add_julekalender"


class AdventCalendarDetail(LoginRequiredMixin, DetailView):
    """View for viewing an advent calendar."""

    model = Julekalender

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        random.seed(context["julekalender"].year)
        context["permutation"] = random.sample(range(1, 25), 24)
        context["form"] = WindowCreateForm(
            action=reverse(
                "advent_calendar:window_create",
                args=[context["julekalender"].year],
            ),
            initial={"advent_calendar": context["julekalender"]},
        )

        return context


class WindowCreate(LoginRequiredMixin, CreateView):
    """View for viewing an advent calendar window."""

    model = Window
    form_class = WindowCreateForm

    def form_valid(self, form):
        form.instance.advent_calendar_id = self.kwargs.get("year")
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        return super().form_valid(form)


class WindowUpdate(UserPassesTestMixin, UpdateView):
    """View for updating an advent calendar window."""

    model = Window
    form_class = WindowUpdateForm

    def get_object(self, queryset=None):
        return get_object_or_404(
            Window, advent_calendar=self.kwargs["year"], index=self.kwargs["index"]
        )

    def test_func(self):
        user = self.request.user
        return self.get_object().created_by == user or user.has_perm(
            "julekalender.change_window"
        )

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        return super().form_valid(form)
