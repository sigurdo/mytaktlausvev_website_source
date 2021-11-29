import random
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from .models import AdventCalendar, Window
from .forms import AdventCalendarForm, WindowCreateForm, WindowUpdateForm


class AdventCalendarList(LoginRequiredMixin, ListView):
    """View for viewing all advent calendars."""

    model = AdventCalendar
    template_name = "advent_calendar/advent_calendar_list.html"
    context_object_name = "advent_calendar_list"


class AdventCalendarCreate(PermissionRequiredMixin, CreateView):
    """View for creating advent calendars."""

    model = AdventCalendar
    form_class = AdventCalendarForm
    permission_required = "advent_calendar.add_adventcalendar"
    template_name = "advent_calendar/advent_calendar_form.html"
    context_object_name = "advent_calendar"


class AdventCalendarDetail(LoginRequiredMixin, DetailView):
    """View for viewing an advent calendar."""

    model = AdventCalendar
    template_name = "advent_calendar/advent_calendar_detail.html"
    context_object_name = "advent_calendar"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        advent_calendar = context["advent_calendar"]

        random.seed(advent_calendar.year)
        context["permutation"] = random.sample(range(1, 25), 24)
        context["form"] = WindowCreateForm(
            advent_calendar=advent_calendar,
            initial={"advent_calendar": advent_calendar},
        )

        return context


class WindowCreate(LoginRequiredMixin, CreateView):
    """
    View for creating an advent calendar window.
    Used with `WindowCreateForm`.
    """

    model = Window
    form_class = WindowCreateForm
    http_method_names = ["post", "put"]

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
            "advent_calendar.change_window"
        )

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        return super().form_valid(form)
