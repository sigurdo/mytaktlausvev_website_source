from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
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

    windows = [
        Window.objects.filter(calendar=year, index=i).first() for i in range(1, 25)
    ]
    return render(
        request,
        "julekalender/calendar.html",
        {"calendar": calendar, "form": NewWindowForm, "windows": windows,},
    )


@login_required
def window(request, year, windowIndex):
    """View function for creating julekalender windows"""

    calendar = get_object_or_404(Julekalender, year=year)

    if request.method == "POST":
        form = NewWindowForm(request.POST)
        if (
            form.is_valid()
            and not Window.windowExists(year, windowIndex)
            and 1 <= windowIndex <= 24
        ):
            window = Window(
                title=form.cleaned_data["title"],
                content=form.cleaned_data["content"],
                author=request.user,
                calendar=calendar,
                index=windowIndex,
            )
            window.save()

    return HttpResponseRedirect(f"/julekalender/{year}")
