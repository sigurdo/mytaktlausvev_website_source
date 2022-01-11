from django.urls import path
from django.views.generic import RedirectView

from .views import BrewView

app_name = "easter_eggs"

urlpatterns = [
    path(
        "dQw4w9WgXcQ/",
        RedirectView.as_view(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"),
    ),
    path("brygg/", BrewView.as_view(), name="BrewView"),
]
