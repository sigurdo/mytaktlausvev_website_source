from datetime import date, datetime

from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.db.models.fields import DateField
from django.db.models.functions import Trunc
from django.db.models.query_utils import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.timezone import localtime, make_aware
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django_ical.views import ICalFeed

from .forms import EventAttendanceForm, EventForm
from .models import Attendance, Event, EventAttendance


def get_event_or_404(year, slug):
    """Returns an Event if it exists, else raises a 404."""
    return get_object_or_404(Event, start_time__year=year, slug=slug)


def get_event_attendance_or_404(year, slug_event, slug_person):
    """Returns an EventAttendance if it exists, else raises a 404."""
    event = get_event_or_404(year, slug_event)
    return get_object_or_404(
        EventAttendance,
        event=event,
        person__slug=slug_person,
    )


class EventList(LoginRequiredMixin, ListView):
    model = Event
    context_object_name = "events"

    def get_queryset(self):
        match self.kwargs:
            case {"year": year}:
                filter = Q(start_time__year=year)
            case _:
                filter = Q(
                    start_time__gte=make_aware(
                        datetime.combine(date.today(), datetime.min.time())
                    )
                )

        return Event.objects.filter(filter).annotate(start_month=Trunc("start_time", "month", output_field=DateField()))


    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        for event in context_data["events"]:
            # Set attendance form on all events
            event.attendance_form = self.get_attendance_form(event)
        context_data["event_feed_absolute_url"] = self.request.build_absolute_uri(
            reverse("events:EventFeed")
        )
        if self.kwargs.get("year"):
            context_data["year"] = self.kwargs.get("year")
        return context_data

    def get_attendance_form(self, event):
        form = EventAttendanceForm(initial={"status": Attendance.ATTENDING})
        form.helper.form_action = reverse(
            "events:EventAttendanceCreateFromList",
            args=[localtime(event.start_time).year, event.slug],
        )
        return form


class EventDetail(LoginRequiredMixin, DetailView):
    """View for viewing an event."""

    model = Event

    def get_object(self, queryset=None):
        return get_event_or_404(self.kwargs.get("year"), self.kwargs.get("slug"))

    def get_form_attendance(self):
        form = EventAttendanceForm(initial={"status": Attendance.ATTENDING})
        form.helper.form_action = reverse(
            "events:EventAttendanceCreate",
            args=[localtime(self.object.start_time).year, self.object.slug],
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

    def get_object(self, queryset=None):
        return get_event_or_404(self.kwargs.get("year"), self.kwargs.get("slug"))

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

    def get_object(self, queryset=None):
        return get_event_or_404(self.kwargs.get("year"), self.kwargs.get("slug"))

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        return super().form_valid(form)


class EventAttendanceList(PermissionRequiredMixin, ListView):
    """View for viewing the attendances for an event."""

    model = EventAttendance
    context_object_name = "attendances"
    permission_required = "events.view_eventattendance"

    event = None

    def get_event(self):
        if self.event:
            return self.event
        self.event = get_event_or_404(self.kwargs.get("year"), self.kwargs.get("slug"))
        return self.event

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

    def get_event(self):
        return get_event_or_404(self.kwargs.get("year"), self.kwargs.get("slug"))

    def form_valid(self, form):
        form.instance.person = self.request.user
        form.instance.event = self.get_event()
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.event.get_absolute_url()


class EventAttendanceCreateFromList(EventAttendanceCreate):
    """View for registering event attendance from EventList."""

    def get_success_url(self):
        return reverse("events:EventList")

class EventAttendanceUpdate(UserPassesTestMixin, UpdateView):
    """View for updating event attendance."""

    model = EventAttendance
    form_class = EventAttendanceForm
    template_name = "common/form.html"

    object = None

    def get_object(self):
        if self.object:
            return self.object
        self.object = get_event_attendance_or_404(
            self.kwargs.get("year"),
            self.kwargs.get("slug_event"),
            self.kwargs.get("slug_person"),
        )
        return self.object

    def test_func(self):
        user = self.request.user
        return self.get_object().person == user or user.has_perm(
            "events.change_eventattendance"
        )

    def get_success_url(self):
        return self.get_object().event.get_absolute_url()


class EventAttendanceDelete(UserPassesTestMixin, DeleteView):
    """View for deleting event attendance."""

    model = EventAttendance
    template_name = "common/confirm_delete.html"

    object = None

    def get_object(self):
        if self.object:
            return self.object
        self.object = get_event_attendance_or_404(
            self.kwargs.get("year"),
            self.kwargs.get("slug_event"),
            self.kwargs.get("slug_person"),
        )
        return self.object

    def test_func(self):
        user = self.request.user
        return self.get_object().person == user or user.has_perm(
            "events.delete_eventattendance"
        )

    def get_success_url(self):
        return self.get_object().event.get_absolute_url()



class EventFeed(ICalFeed):
    product_id = "-//taktlaus.no//kalender//NO-NN"
    timezone = "UTC"
    title = "Taktlauskalender"
    description = "Kalender for taktlause hendingar"

    def items(self):
        return Event.objects.all()

    def item_guid(self, item):
        return f"@taktlaus.no{item.get_absolute_url()}"

    def item_title(self, item):
        return item.title

    def item_decription(self, item):
        return item.content

    def item_link(self, item):
        return f"https://taktlaus.no{item.get_absolute_url()}"

    def item_start_datetime(self, item):
        return item.start_time

    def item_end_datetime(self, item):
        return item.end_time

    def item_location(self, item):
        return "kommer snart"
