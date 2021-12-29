from django.urls import path

from . import views

app_name = "polls"

urlpatterns = [
    path("<slug:slug>/rediger/", views.PollUpdate.as_view(), name="PollUpdate"),
]
