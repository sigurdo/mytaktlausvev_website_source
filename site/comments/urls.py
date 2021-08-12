from django.urls import path
from . import views

urlpatterns = [
    path("ny", views.CommentCreate.as_view(), name="comment_create"),
    path("<int:pk>/rediger", views.CommentUpdate.as_view(), name="comment_update"),
    path("<int:pk>/slett", views.CommentDelete.as_view(), name="comment_delete"),
]
