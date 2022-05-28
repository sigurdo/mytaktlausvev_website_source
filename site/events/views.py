from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models.functions.datetime import TruncMonth
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.timezone import localtime, now
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django_ical.views import ICalFeed

from accounts.models import UserCustom
from common.breadcrumbs import Breadcrumb, BreadcrumbsMixin
from common.mixins import PermissionOrCreatedMixin
from common.views import DeleteViewCustom

from .forms import EventAttendanceForm, EventForm
from .models import Attendance, Event, EventAttendance
from django.utils.timezone import localtime, make_aware, now
from datetime import datetime, timedelta


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


def event_breadcrumbs(event=None, include_event=True):
    """
    Generates breadcrumbs for events in the following fashion:
    - /hendingar/:                                     "Hendingar [current_year]"
    - /hendingar/ny:                                   "Hendingar [current_year] / Alle framtidige"
    - /hendingar/[year]/:                              ""
    - /hendingar/[year]/[slug]/ for future events:     "Hendingar [year] / Alle framtidige"
    - /hendingar/[year]/[slug]/ for past events:       "Hendingar [year]"
    - /hendingar/[year]/[slug]/.../ for future events: "Hendingar [year] / Alle framtidige / [event_title]"
    - /hendingar/[year]/[slug]/.../ for past events:   "Hendingar [year] / [event_title]"
    """
    breadcrumbs = []
    year = localtime(event.start_time).year if event else localtime(now()).year

    breadcrumbs.append(
        Breadcrumb(
            reverse("events:EventList", args=[year]),
            f"Hendingar {year}",
        )
    )
    if event is None:
        return breadcrumbs

    if event.is_in_future():
        breadcrumbs.append(
            Breadcrumb(
                reverse("events:EventList"),
                "Alle framtidige",
            )
        )

    if include_event:
        breadcrumbs.append(
            Breadcrumb(
                reverse("events:EventDetail", args=[year, event.slug]),
                str(event),
            )
        )

    return breadcrumbs


class EventList(LoginRequiredMixin, BreadcrumbsMixin, ListView):
    model = Event
    context_object_name = "events"

    def get_breadcrumbs(self):
        if "year" in self.kwargs:
            return []
        return event_breadcrumbs()

    def get_queryset(self):
        match self.kwargs:
            case {"year": year}:
                queryset = Event.objects.filter(start_time__year=year)
            case _:
                queryset = Event.objects.upcoming()

        return queryset.annotate(start_month=TruncMonth("start_time"))

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        for event in context_data["events"]:
            # Set attendance form on all events
            event.attendance_form = self.get_attendance_form(event)
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


class EventDetail(LoginRequiredMixin, BreadcrumbsMixin, DetailView):
    """View for viewing an event."""

    model = Event

    def get_breadcrumbs(self):
        return event_breadcrumbs(event=self.get_object(), include_event=False)

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


class EventCreate(LoginRequiredMixin, BreadcrumbsMixin, CreateView):
    """View for creating an event."""

    model = Event
    form_class = EventForm
    template_name = "common/form.html"

    def get_breadcrumbs(self):
        return event_breadcrumbs(
            event=Event(start_time=now() + timedelta(days=1)),
            include_event=False,
        )

    def get_object(self, queryset=None):
        return get_event_or_404(self.kwargs.get("year"), self.kwargs.get("slug"))

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        response = super().form_valid(form)

        sivert = UserCustom.objects.filter(username="Sivert").first()
        if sivert:
            EventAttendance.objects.create(
                event=self.object, person=sivert, status=Attendance.ATTENDING
            )
        sigurd = UserCustom.objects.filter(username="SigurdT").first()
        if sigurd:
            EventAttendance.objects.create(
                event=self.object, person=sigurd, status=Attendance.ATTENDING_MAYBE
            )

        return response


class EventUpdate(PermissionOrCreatedMixin, BreadcrumbsMixin, UpdateView):
    """View for updating an event."""

    model = Event
    form_class = EventForm
    template_name = "common/form.html"
    permission_required = "events.change_event"

    def get_breadcrumbs(self):
        return event_breadcrumbs(event=self.get_object())

    def get_object(self, queryset=None):
        return get_event_or_404(self.kwargs.get("year"), self.kwargs.get("slug"))

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        return super().form_valid(form)


class EventAttendanceList(PermissionRequiredMixin, BreadcrumbsMixin, ListView):
    """View for viewing the attendances for an event."""

    model = EventAttendance
    context_object_name = "attendances"
    permission_required = "events.view_eventattendance"

    event = None

    def get_breadcrumbs(self):
        return event_breadcrumbs(event=self.get_event())

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


class EventAttendanceUpdate(PermissionOrCreatedMixin, BreadcrumbsMixin, UpdateView):
    """View for updating event attendance."""

    model = EventAttendance
    form_class = EventAttendanceForm
    template_name = "common/form.html"

    permission_required = "events.change_eventattendance"
    field_created_by = "person"

    object = None

    def get_breadcrumbs(self):
        return event_breadcrumbs(event=self.get_object().event)

    def get_object(self):
        if self.object:
            return self.object
        self.object = get_event_attendance_or_404(
            self.kwargs.get("year"),
            self.kwargs.get("slug_event"),
            self.kwargs.get("slug_person"),
        )
        return self.object

    def get_success_url(self):
        return self.get_object().event.get_absolute_url()


class EventAttendanceDelete(
    PermissionOrCreatedMixin, BreadcrumbsMixin, DeleteViewCustom
):
    """View for deleting event attendance."""

    model = EventAttendance
    success_message = "Deltakinga vart fjerna."

    permission_required = "events.delete_eventattendance"
    field_created_by = "person"

    object = None

    def get_breadcrumbs(self):
        return event_breadcrumbs(event=self.get_object().event)

    def get_object(self):
        if self.object:
            return self.object
        self.object = get_event_attendance_or_404(
            self.kwargs.get("year"),
            self.kwargs.get("slug_event"),
            self.kwargs.get("slug_person"),
        )
        return self.object

    def get_success_url(self):
        return self.get_object().event.get_absolute_url()


class EventFeed(ICalFeed):
    product_id = "-//taktlaus.no//kalender//NO-NN"
    timezone = "UTC"
    title = "Taktlauskalender"
    description = "Kalender for taktlause hendingar"

    def __call__(self, request, *args, **kwargs):
        token = request.GET.get("token", None)
        if (
            token is not None
            and UserCustom.objects.filter(calendar_feed_token=token).exists()
        ):
            self.user = UserCustom.objects.only(
                "calendar_feed_only_upcoming", "calendar_feed_start_date"
            ).get(calendar_feed_token=token)
            return super().__call__(request, *args, *kwargs)
        return HttpResponseForbidden()

    def items(self):
        if self.user.calendar_feed_only_upcoming:
            return Event.objects.upcoming()
        if self.user.calendar_feed_start_date:
            return Event.objects.filter(
                start_time__gte=self.user.calendar_feed_start_date
            )
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
