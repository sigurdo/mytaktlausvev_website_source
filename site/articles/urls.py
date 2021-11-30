from django.urls import include, path
from . import views

app_name = "articles"

articles_patterns = [
    path("ny/", views.ArticleCreate.as_view(), name="ArticleCreate"),
    path("<path:path>/ny/", views.SubarticleCreate.as_view(), name="SubarticleCreate"),
    path("<path:path>/rediger/", views.ArticleUpdate.as_view(), name="ArticleUpdate"),
]
urlpatterns = [
    path("artiklar/", include(articles_patterns)),
    path("<path:path>/", views.ArticleDetail.as_view(), name="ArticleDetail"),
]
