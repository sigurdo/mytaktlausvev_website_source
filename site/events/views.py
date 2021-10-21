from django.http.response import Http404, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Create your views here.


from .models import Event, EventAttendance
from .forms import CreateEventForm


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
def event_details(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(
        request,
        "events/event_details.html",
        {"event": event, "is_owner": event.owner.id == request.user.id},
    )


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
