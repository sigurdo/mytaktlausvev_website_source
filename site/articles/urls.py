from django.urls import path
from . import views

urlpatterns = [
    path("ny", views.ArticleCreate.as_view(), name="article_create"),
    path("<slug:slug>", views.ArticleDetail.as_view(), name="article_detail"),
    path("<slug:slug>/rediger", views.ArticleUpdate.as_view(), name="article_update"),
]
