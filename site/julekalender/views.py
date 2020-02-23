from django.shortcuts import render
from django.http import HttpResponseRedirect

from julekalender.models import Julekalender
from julekalender.forms import NewJulekalenderForm

# Create your views here.
def julekalenders(request):
    """View function for displaying created julekalenders"""

    calendars = Julekalender.objects.all()
    return render(
        request,
        "julekalender/base.html",
        {"calendars": calendars, "form": NewJulekalenderForm},
    )


def newJulekalender(request):
    """View function for creating a new julekalender"""

    form = NewJulekalenderForm(request.POST)
    if form.is_valid():
        julekalender = form.save(commit=False)
        julekalender.save()
    return HttpResponseRedirect("/julekalender")

