"""Views for the 'dashboard'-module"""
import random

from django.shortcuts import render
from quotes.models import Quote


def dashboard(request):
    """View for the main dashboard"""
    return render(
        request,
        "dashboard/dashboard.html",
        {"number": random.randint(0, 10), "quotes": Quote.objects.all()[:2]},
    )
