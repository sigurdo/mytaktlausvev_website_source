from django.urls import path

from . import views

app_name = "polls"

urlpatterns = [
    path("", views.PollList.as_view(), name="PollList"),
    path("<slug:slug>/", views.PollRedirect.as_view(), name="PollRedirect"),
    path("<slug:slug>/resultat/", views.PollResults.as_view(), name="PollResults"),
    path("<slug:slug_poll>/stem/", views.VoteCreate.as_view(), name="VoteCreate"),
    path("<slug:slug_poll>/stem/fjern/", views.VoteDelete.as_view(), name="VoteDelete"),
    path("<slug:slug_poll>/stemmer/", views.PollVotes.as_view(), name="PollVotes"),
    path("<slug:slug>/rediger/", views.PollUpdate.as_view(), name="PollUpdate"),
]
