from django.urls import path

from .views import BrewView

app_name = "brewing"

urlpatterns = [
    path("", BrewView.as_view(), name="BrewView"),
]
