from django.urls import path
from .views import BrewView

app_name = "easter_eggs"

urlpatterns = [
    path("brygg", BrewView.as_view(), name="brew"),
]
