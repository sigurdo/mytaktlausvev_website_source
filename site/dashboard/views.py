"""Views for the 'dashboard'-module."""
from datetime import datetime, timedelta

from django.shortcuts import render
from django.utils.timezone import make_aware

from events.models import Event
from quotes.models import Quote


def dashboard(request):
    """View for the main dashboard."""
    return render(
        request,
        "dashboard/dashboard.html",
        {
            "quotes": Quote.objects.all()[:2],
            "events": Event.objects.filter(
                start_time__gte=make_aware(datetime.now() - timedelta(1))
            )[:10],
        },
    )
