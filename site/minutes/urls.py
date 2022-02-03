from django.urls import path

from . import views

app_name = "minutes"

urlpatterns = [
    path("", views.MinutesList.as_view(), name="MinutesList"),
]
