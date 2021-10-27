"""Views for the 'dashboard'-module"""
import random
from datetime import datetime, timedelta
from django.shortcuts import render
from quotes.models import Quote
from events.models import Event


def dashboard(request):
    """View for the main dashboard"""
    return render(
        request,
        "dashboard/dashboard.html",
        {
            "number": random.randint(0, 10),
            "quotes": Quote.objects.all()[:2],
            "events": Event.objects.filter(
                start_time__gte=(datetime.now() - timedelta(1))
            )[:10],
        },
    )
