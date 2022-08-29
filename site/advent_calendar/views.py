import random

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from common.forms.views import DeleteViewCustom
from common.mixins import PermissionOrCreatedMixin

from .forms import AdventCalendarForm, WindowCreateForm, WindowUpdateForm
from .models import AdventCalendar, Window


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
        return super().form_valid(form)


class WindowUpdate(PermissionOrCreatedMixin, UpdateView):
    """View for updating an advent calendar window."""

    model = Window
    form_class = WindowUpdateForm
    permission_required = "advent_calendar.change_window"

    def get_object(self, queryset=None):
        return get_object_or_404(
            Window, advent_calendar=self.kwargs["year"], index=self.kwargs["index"]
        )


class WindowDelete(PermissionOrCreatedMixin, DeleteViewCustom):
    model = Window
    permission_required = "advent_calendar.delete_window"
    template_name = "advent_calendar/window_delete.html"

    def get_object(self, queryset=None):
        return get_object_or_404(
            Window, advent_calendar=self.kwargs["year"], index=self.kwargs["index"]
        )

    def get_success_message(self, cleaned_data):
        """Remove success message, since this is not shown by the advent calendar views."""
        return ""

    def get_success_url(self) -> str:
        return self.object.advent_calendar.get_absolute_url()
