from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required

from julekalender.models import Julekalender, Window
from julekalender.forms import NewJulekalenderForm, NewWindowForm


@login_required
def julekalenders(request):
    """View function for displaying created julekalenders"""

    if request.method == "POST":
        form = NewJulekalenderForm(request.POST)
        if form.is_valid():
            julekalender = form.save(commit=False)
            julekalender.save()

    calendars = Julekalender.objects.all()
    return render(
        request,
        "julekalender/calendars.html",
        {"calendars": calendars, "form": NewJulekalenderForm},
    )


@login_required
def julekalender(request, year):
    """"View function for displaying the windows of a julekalender"""

    calendar = get_object_or_404(Julekalender, year=year)

    if request.method == "POST":
        form = NewWindowForm(request.POST)
        if (
            form.is_valid()
            and not Window.windowExists(year, form.cleaned_data["index"])
            and 1 <= form.cleaned_data["index"] <= 24
        ):
            window = Window(
                title=form.cleaned_data["title"],
                post=form.cleaned_data["post"],
                author=request.user,
                calendar=calendar,
                index=form.cleaned_data["index"],
            )
            window.save()

    return render(
        request,
        "julekalender/calendar.html",
        {
            "calendar": calendar,
            "form": NewWindowForm,
            "calendarRange": range(1, 25),
            "windows": Window.objects.filter(calendar=year).order_by("index"),
        },
    )
