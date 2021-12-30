from django.urls import path

from . import views

app_name = "polls"

urlpatterns = [
    path("<slug:slug_poll>/stem/", views.VoteCreate.as_view(), name="VoteCreate"),
    path("<slug:slug>/rediger/", views.PollUpdate.as_view(), name="PollUpdate"),
]
