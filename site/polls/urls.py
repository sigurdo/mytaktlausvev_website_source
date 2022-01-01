from django.urls import path

from . import views

app_name = "polls"

urlpatterns = [
    path("", views.PollList.as_view(), name="PollList"),
    path("ny/", views.PollCreate.as_view(), name="PollCreate"),
    path("<slug:slug>/", views.PollRedirect.as_view(), name="PollRedirect"),
    path("<slug:slug>/resultat/", views.PollResults.as_view(), name="PollResults"),
    path("<slug:slug>/stem/", views.VoteCreate.as_view(), name="VoteCreate"),
    path("<slug:slug>/stem/fjern/", views.VoteDelete.as_view(), name="VoteDelete"),
    path("<slug:slug>/stemmer/", views.PollVotes.as_view(), name="PollVotes"),
    path("<slug:slug>/rediger/", views.PollUpdate.as_view(), name="PollUpdate"),
    path("<slug:slug>/slett/", views.PollDelete.as_view(), name="PollDelete"),
]
