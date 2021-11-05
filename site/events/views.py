from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from .models import Attendance, Event, EventAttendance
from .forms import EventAttendanceForm, EventForm


class EventDetail(LoginRequiredMixin, DetailView):
    """View for viewing an event."""

    model = Event

    def get_queryset(self):
        year = self.kwargs.get("year")
        return super().get_queryset().filter(start_time__year=year)

    def get_form_attendance(self):
        form = EventAttendanceForm(initial={"status": Attendance.ATTENDING})
        form.helper.form_action = reverse(
            "events:attendance", args=[self.object.start_time.year, self.object.slug]
        )
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_attendance"] = self.get_form_attendance()
        context["is_registered"] = EventAttendance.objects.filter(
            event=self.object, person=self.request.user
        ).exists()
        return context


class EventCreate(PermissionRequiredMixin, CreateView):
    """View for creating an event."""

    model = Event
    form_class = EventForm
    template_name = "common/form.html"
    permission_required = "events.add_event"

    def get_queryset(self):
        year = self.kwargs.get("year")
        return super().get_queryset().filter(start_time__year=year)

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        return super().form_valid(form)


class EventUpdate(PermissionRequiredMixin, UpdateView):
    """View for updating an event."""

    model = Event
    form_class = EventForm
    template_name = "common/form.html"
    permission_required = "events.change_event"

    def get_queryset(self):
        year = self.kwargs.get("year")
        return super().get_queryset().filter(start_time__year=year)

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        return super().form_valid(form)


class EventAttendanceList(PermissionRequiredMixin, ListView):
    """View for viewing the attendances for an event."""

    model = EventAttendance
    context_object_name = "attendances"
    permission_required = "events.view_eventattendance"

    object = None

    def get_event(self):
        year = self.kwargs.get("year")
        slug = self.kwargs.get("slug")
        return self.object or get_object_or_404(Event, start_time__year=year, slug=slug)

    def get_queryset(self):
        return self.get_event().attendances.order_by("-created")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["event"] = self.get_event()
        return context


class EventAttendanceCreate(LoginRequiredMixin, CreateView):
    """View for registering event attendance."""

    model = EventAttendance
    form_class = EventAttendanceForm
    template_name = "common/form.html"
    http_method_names = ["post", "put"]

    def form_valid(self, form):
        form.instance.person = self.request.user
        form.instance.event = Event.objects.get(
            start_time__year=self.kwargs.get("year"),
            slug=self.kwargs.get(self.slug_url_kwarg),
        )
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.event.get_absolute_url()
