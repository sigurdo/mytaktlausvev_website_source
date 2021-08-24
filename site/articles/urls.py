from django.urls import include, path, re_path
from . import views

app_name = "articles"

articles_patterns = [
    path("ny/", views.ArticleCreate.as_view(), name="create"),
    re_path(r"(?P<path>.*)/rediger/", views.ArticleUpdate.as_view(), name="update"),
]
urlpatterns = [
    path("artiklar/", include(articles_patterns)),
    re_path(r"(?P<path>.*)/", views.ArticleDetail.as_view(), name="detail"),
]
