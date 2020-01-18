"""Views for the 'about'-app"""
import random
from django.shortcuts import render


def about_us(request):
    """Main view for the "about-us"-page"""
    return render(
        request,
        "about/about_us.html",
        {
            "number": random.randint(0, 10)
        }
    )
