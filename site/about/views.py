import random
from django.shortcuts import render
from django.http import HttpResponse

def about_us(request):
    return render(
        request,
        "about/about_us.html",
        {
            "number": random.randint(0, 10)
        }
    )