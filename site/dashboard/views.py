import random

from django.shortcuts import render
from quotes.models import Quote
# Create your views here.

def dashboard(request):
    return render(
        request,
        "dashboard/dashboard.html",
        {
            "number": random.randint(0, 10),
            "quotes": Quote.objects.all()[:2]
        }
    )