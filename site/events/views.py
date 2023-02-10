from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import OuterRef
from django.db.models.functions import TruncMonth
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.timezone import localtime, now
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django_ical.views import ICalFeed

from accounts.models import UserCustom
from common.breadcrumbs.breadcrumbs import Breadcrumb, BreadcrumbsMixin
from common.forms.views import (
    DeleteViewCustom,
    InlineFormsetCreateView,
    InlineFormsetUpdateView,
)
from common.mixins import PermissionOrCreatedMixin

from .forms import EventAttendanceForm, EventForm, EventKeyinfoEntryFormset
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


class EventListYear(LoginRequiredMixin, BreadcrumbsMixin, ListView):
    model = Event
    context_object_name = "events"

    def get_base_queryset(self):
        return Event.objects.filter(start_time__year=self.kwargs["year"])

    def get_queryset(self):
        return (
            self.get_base_queryset()
            .annotate(
                start_month=TruncMonth("start_time"),
                user_attending_status=EventAttendance.objects.filter(
                    event=OuterRef("pk"), person=self.request.user
                ).values("status"),
            )
            .select_related("category")
            .prefetch_related("keyinfo_entries")
        )

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        for event in context_data["events"]:
            # Set attendance form on all events
            event.attendance_form = self.get_attendance_form(event)

        return context_data

    def get_attendance_form(self, event):
        form = EventAttendanceForm(initial={"status": Attendance.ATTENDING})
        form.helper.form_action = reverse(
            "events:EventAttendanceCreateFromList",
            args=[localtime(event.start_time).year, event.slug],
        )
        return form

    @classmethod
    def get_breadcrumb(cls, year, **kwargs):
        return Breadcrumb(
            url=reverse("events:EventListYear", args=[year]),
            label=f"Hendingar {year}",
        )


class EventList(EventListYear):
    breadcrumb_parent = EventListYear

    def get_base_queryset(self):
        return Event.objects.upcoming()

    def get_breadcrumbs_kwargs(self):
        return {"year": now().year}

    @classmethod
    def get_breadcrumb(cls, **kwargs):
        return Breadcrumb(
            url=reverse("events:EventList"),
            label="Alle framtidige",
        )


class EventListFilter(EventList):
    def get_base_queryset(self):
        match self.kwargs.filter_type:
            case "ikkje-svara-på":
                return Event.objects.upcoming().exclude(
                    attendances__person=self.request.user
                )
            case _:
                raise Http404(f"Ugyldig filtertype: {self.kwargs.filter_type}")


class EventDetail(LoginRequiredMixin, BreadcrumbsMixin, DetailView):
    """View for viewing an event."""

    model = Event

    def get_object(self, queryset=None):
        return get_event_or_404(self.kwargs.get("year"), self.kwargs.get("slug"))

    def get_form_attendance(self):
        attendance = self.object.get_attendance(self.request.user)
        form = EventAttendanceForm(
            instance=attendance,
            initial={"status": Attendance.ATTENDING} if not attendance else None,
        )
        if not attendance:
            form.helper.form_action = reverse(
                "events:EventAttendanceCreate",
                args=[localtime(self.object.start_time).year, self.object.slug],
            )
        else:
            form.helper.form_action = reverse(
                "events:EventAttendanceUpdate",
                args=[
                    localtime(self.object.start_time).year,
                    self.object.slug,
                    self.request.user.slug,
                ],
            )
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_attendance"] = self.get_form_attendance()
        return context

    @classmethod
    def get_breadcrumb_parent(cls, event, **kwargs):
        if event.is_upcoming():
            return EventList
        return EventListYear

    def get_breadcrumbs_kwargs(self):
        # In this case, we have to provide "event" even though it is not used by any parents
        # because it is used to choose the parent.
        return {"year": self.kwargs["year"], "event": self.object}

    @classmethod
    def get_breadcrumb(cls, event, **kwargs):
        return Breadcrumb(
            url=reverse("events:EventDetail", args=[event.start_time.year, event.slug]),
            label=str(event),
        )


class EventCreate(LoginRequiredMixin, BreadcrumbsMixin, InlineFormsetCreateView):
    """View for creating an event."""

    model = Event
    form_class = EventForm
    formset_class = EventKeyinfoEntryFormset
    template_name = "common/forms/form.html"
    breadcrumb_parent = EventList

    def get_breadcrumbs_kwargs(self):
        return {"year": now().year}

    def get_object(self, queryset=None):
        return get_event_or_404(self.kwargs.get("year"), self.kwargs.get("slug"))

    def get_context_data(self, **kwargs):
        # Formset is rendered inside the form
        kwargs["render_formset"] = False
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)

        sivert = UserCustom.objects.filter(username="Sivert").first()
        if sivert:
            EventAttendance.objects.create(
                event=self.object, person=sivert, status=Attendance.ATTENDING
            )
        marius = UserCustom.objects.filter(username="MariusV").first()
        if marius:
            EventAttendance.objects.create(
                event=self.object, person=marius, status=Attendance.ATTENDING
            )

        return response


class EventUpdate(PermissionOrCreatedMixin, BreadcrumbsMixin, InlineFormsetUpdateView):
    """View for updating an event."""

    model = Event
    form_class = EventForm
    formset_class = EventKeyinfoEntryFormset
    template_name = "common/forms/form.html"
    permission_required = "events.change_event"
    breadcrumb_parent = EventDetail

    def get_object(self, queryset=None):
        return get_event_or_404(self.kwargs.get("year"), self.kwargs.get("slug"))

    def get_context_data(self, **kwargs):
        # Tell `common/form.html` not to render the formset, since this is done by the form
        kwargs["render_formset"] = False
        return super().get_context_data(**kwargs)

    def get_breadcrumbs_kwargs(self) -> dict:
        return {"year": self.kwargs["year"], "event": self.object}


class EventDelete(PermissionOrCreatedMixin, BreadcrumbsMixin, DeleteViewCustom):
    model = Event
    success_url = reverse_lazy("events:EventList")
    permission_required = "events.delete_event"
    breadcrumb_parent = EventDetail

    def get_object(self, queryset=None):
        return get_event_or_404(self.kwargs.get("year"), self.kwargs.get("slug"))

    def get_breadcrumbs_kwargs(self) -> dict:
        return {"year": self.kwargs["year"], "event": self.object}


class EventAttendanceList(PermissionRequiredMixin, BreadcrumbsMixin, ListView):
    """View for viewing the attendances for an event."""

    model = EventAttendance
    context_object_name = "attendances"
    permission_required = "events.view_eventattendance"
    breadcrumb_parent = EventDetail

    event = None

    def get_event(self):
        if self.event is None:
            self.event = get_event_or_404(
                self.kwargs.get("year"), self.kwargs.get("slug")
            )
        return self.event

    def get_queryset(self):
        return (
            self.get_event()
            .attendances.select_related(
                "person__jacket", "person__instrument_type__group"
            )
            .order_by("-created")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["event"] = self.get_event()
        return context

    def get_breadcrumbs_kwargs(self) -> dict:
        return {"year": self.kwargs["year"], "event": self.get_event()}


class EventAttendanceCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """View for registering event attendance."""

    model = EventAttendance
    form_class = EventAttendanceForm
    template_name = "common/forms/form.html"
    http_method_names = ["post", "put"]

    def get_event(self):
        return get_event_or_404(self.kwargs.get("year"), self.kwargs.get("slug"))

    def form_valid(self, form):
        form.instance.person = self.request.user
        form.instance.event = self.get_event()
        return super().form_valid(form)

    def get_success_message(self, _) -> str:
        return f'"{self.object.get_status_display()}" registrert som svar på {self.object.event}.'

    def get_success_url(self):
        return self.object.event.get_absolute_url()


class EventAttendanceCreateFromList(EventAttendanceCreate):
    """View for registering event attendance from EventList."""

    def get_success_url(self):
        return reverse("events:EventList")


class EventAttendanceUpdate(
    PermissionOrCreatedMixin, SuccessMessageMixin, BreadcrumbsMixin, UpdateView
):
    """View for updating event attendance."""

    model = EventAttendance
    form_class = EventAttendanceForm
    template_name = "common/forms/form.html"
    permission_required = "events.change_eventattendance"
    field_created_by = "person"
    breadcrumb_parent = EventDetail

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

    def get_success_message(self, _) -> str:
        return f'"{self.object.get_status_display()}" registrert som svar på {self.object.event}.'

    def get_success_url(self):
        return self.get_object().event.get_absolute_url()

    def get_breadcrumbs_kwargs(self) -> dict:
        return {"year": self.kwargs["year"], "event": self.object.event}


class EventAttendanceDelete(
    PermissionOrCreatedMixin, BreadcrumbsMixin, DeleteViewCustom
):
    """View for deleting event attendance."""

    model = EventAttendance
    success_message = "Deltakinga vart fjerna."
    permission_required = "events.delete_eventattendance"
    field_created_by = "person"
    breadcrumb_parent = EventDetail

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

    def get_success_url(self):
        return self.get_object().event.get_absolute_url()

    def get_breadcrumbs_kwargs(self) -> dict:
        return {"year": self.kwargs["year"], "event": self.object.event}


class EventFeed(ICalFeed):
    product_id = "-//taktlaus.no//kalender//NO-NN"
    timezone = settings.TIME_ZONE
    title = "Taktlauskalender"
    description = "Kalender for taktlause hendingar"

    def __call__(self, request, *args, **kwargs):
        token = request.GET.get("token", None)
        if (
            token is not None
            and UserCustom.objects.filter(calendar_feed_token=token).exists()
        ):
            self.user = UserCustom.objects.only("calendar_feed_start_date").get(
                calendar_feed_token=token
            )
            return super().__call__(request, *args, *kwargs)
        return HttpResponseForbidden()

    def items(self):
        start_date = self.user.calendar_feed_start_date or self.user.date_joined
        return Event.objects.filter(start_time__gte=start_date)

    def item_guid(self, item):
        return f"@taktlaus.no{item.get_absolute_url()}"

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return f"""\
{self.item_link(item)}

{item.content}
"""

    def item_link(self, item):
        return f"https://taktlaus.no{item.get_absolute_url()}"

    def item_start_datetime(self, item):
        return localtime(item.start_time)

    def item_end_datetime(self, item):
        return localtime(item.end_time if item.end_time else item.start_time)

    def item_location(self, item):
        return item.location
