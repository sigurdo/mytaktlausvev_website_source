import random

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from .models import Julekalender, Window
from .forms import NewJulekalenderForm, NewWindowForm, CalendarForm


class JulekalenderCreate(CreateView):
    """View for creating julekalenders."""

    model = Julekalender
    form_class = CalendarForm


@login_required
def julekalenders(request):
    """View function for displaying created julekalenders"""

    if request.method == "POST":
        form = NewJulekalenderForm(request.POST)
        if form.is_valid() and Julekalender.userCanCreate(request.user):
            julekalender = form.save(commit=False)
            julekalender.save()

    calendars = Julekalender.objects.all()
    return render(
        request,
        "julekalender/calendars.html",
        {
            "calendars": calendars,
            "userCanCreate": Julekalender.userCanCreate(request.user),
            "form": NewJulekalenderForm,
        },
    )


@login_required
def julekalender(request, year):
    """"View function for displaying the windows of a julekalender"""

    calendar = get_object_or_404(Julekalender, year=year)

    if request.method == "POST":
        form = NewWindowForm(request.POST)
        if form.is_valid() and (
            not Window.windowExists(year, form.cleaned_data["index"])
            or Window.objects.get(
                calendar=calendar, index=form.cleaned_data["index"]
            ).userCanEdit(request.user)
        ):
            Window.objects.update_or_create(
                calendar=calendar,
                index=form.cleaned_data["index"],
                author=request.user,
                defaults={
                    "title": form.cleaned_data["title"],
                    "content": form.cleaned_data["content"],
                },
            )

    random.seed(year)
    permutation = random.sample(range(1, 25), 24)

    windows = [
        {
            "title": window.title,
            "content": window.content,
            "index": window.index,
            "author": window.author.username,
            "canEdit": window.userCanEdit(request.user),
        }
        for window in Window.objects.filter(calendar=year)
    ]

    return render(
        request,
        "julekalender/calendar.html",
        {
            "calendar": calendar,
            "form": NewWindowForm,
            "permutation": permutation,
            "windows": windows,
        },
    )
