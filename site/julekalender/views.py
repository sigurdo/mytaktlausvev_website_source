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
        "julekalender/base.html",
        {"calendars": calendars, "form": NewJulekalenderForm},
    )


@login_required
def julekalender(request, year):
    """"View function for displaying the windows of a julekalender"""

    calendar = get_object_or_404(Julekalender, year=year)
    return render(
        request,
        "julekalender/julekalender.html",
        {"calendar": calendar, "form": NewWindowForm, "calendarRange": range(1, 25),},
    )


@login_required
def window(request, year, windowNumber):
    """View function for returning the content of and creating windows in a julekalender"""

    if request.method == "GET":
        window = get_object_or_404(Window, calendar=year, windowNumber=windowNumber)
        return JsonResponse(
            {
                "title": window.title,
                "post": window.post,
                "author": window.author.username,
            }
        )

    form = NewWindowForm(request.POST)
    if (
        form.is_valid()
        and not Window.windowExists(year, windowNumber)
        and 1 <= windowNumber <= 24
    ):
        calendar = get_object_or_404(Julekalender, year=year)
        window = Window(
            title=form.data["title"],
            post=form.data["post"],
            author=request.user,
            calendar=calendar,
            windowNumber=windowNumber,
        )
        window.save()
    return HttpResponseRedirect(f"/julekalender/{year}")

