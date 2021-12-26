from django.urls import path

from . import views

app_name = "forum"

urlpatterns = [
    path("", views.ForumList.as_view(), name="ForumList"),
    path("<slug:slug_forum>/", views.TopicList.as_view(), name="TopicList"),
    path(
        "<slug:slug_forum>/<slug:slug_topic>/",
        views.PostList.as_view(),
        name="PostList",
    ),
]
