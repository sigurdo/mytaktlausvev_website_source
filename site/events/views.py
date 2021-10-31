from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http.response import Http404, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView

# Create your views here.


from .models import Event, EventAttendance
from .forms import CreateEventForm, EventForm


class EventDetail(LoginRequiredMixin, DetailView):
    """View for viewing an event."""

    model = Event

    def get_queryset(self):
        year = self.kwargs.get("year")
        return super().get_queryset().filter(start_time__year=year)


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


@login_required
def new_event(request):
    if request.method == "POST":
        form = CreateEventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.owner = request.user
            event.save()
            return HttpResponseRedirect(reverse("event_details", args=(event.id,)))
    elif request.method == "GET":
        form = CreateEventForm()
        return render(request, "events/create_event.html", {"form": form})


@login_required
def update_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if event.owner != request.user:
        return HttpResponseForbidden()
    if request.method == "POST":
        form = CreateEventForm(request.POST)
        if form.is_valid():
            updated_event = form.instance
            event.title = updated_event.title
            event.description = updated_event.description
            event.start_time = updated_event.start_time
            event.end_time = updated_event.end_time
            event.save()
            return HttpResponseRedirect(reverse("event_details", args=(event.id,)))
    elif request.method == "GET":
        form = CreateEventForm(instance=event)
        return render(
            request, "events/update_event.html", {"event_id": event_id, "form": form}
        )


@login_required
def declare_attendance(request, event_id, attendance_status):
    EventAttendance.objects.filter(
        event__id=event_id, person__id=request.user.id
    ).delete()
    EventAttendance.objects.create(
        person=request.user,
        event=get_object_or_404(Event, id=event_id),
        status=attendance_status,
    )
    return HttpResponseRedirect(reverse("event_details", args=(event_id,)))
