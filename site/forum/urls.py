from django.urls import path

from . import views

app_name = "forum"

urlpatterns = [
    path("", views.ForumList.as_view(), name="ForumList"),
    path("<slug:slug_forum>/", views.TopicList.as_view(), name="TopicList"),
    path(
        "<slug:slug_forum>/nytt_emne/", views.TopicCreate.as_view(), name="TopicCreate"
    ),
    path(
        "<slug:slug_forum>/<slug:slug>/",
        views.TopicDetail.as_view(),
        name="TopicDetail",
    ),
]
