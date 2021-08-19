from django.urls import path
from . import views

urlpatterns = [
    path("<slug:slug>", views.ArticleDetail.as_view(), name="article_detail"),
]
