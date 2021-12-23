from django.urls import path

from . import views

app_name = "forum"

urlpatterns = [
    path("", views.ForumList.as_view(), name="ForumList"),
    path("<slug:slug>", views.ForumDetail.as_view(), name="ForumDetail"),
]
