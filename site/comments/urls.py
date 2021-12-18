from django.urls import path

from . import views

app_name = "comments"

urlpatterns = [
    path("ny", views.CommentCreate.as_view(), name="CommentCreate"),
    path("<int:pk>/rediger", views.CommentUpdate.as_view(), name="CommentUpdate"),
    path("<int:pk>/slett", views.CommentDelete.as_view(), name="CommentDelete"),
]
