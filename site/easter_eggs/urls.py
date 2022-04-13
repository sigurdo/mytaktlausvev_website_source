from django.urls import path
from django.views.generic import RedirectView

from .views import BrewView, EasterEggButton

app_name = "easter_eggs"

urlpatterns = [
    path(
        "dQw4w9WgXcQ/",
        RedirectView.as_view(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"),
        name="IceCream",
    ),
    path("brygg/", BrewView.as_view(), name="BrewView"),
    path("skiltmerke/", EasterEggButton.as_view(), name="EasterEggButton"),
]
