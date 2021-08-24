from django.urls import include, path
from django.views.generic.base import RedirectView
from . import views

app_name = "articles"

articles_patterns = [
    path("ny/", views.ArticleCreate.as_view(), name="create"),
    path("<slug:slug>/rediger/", views.ArticleUpdate.as_view(), name="update"),
    path("<slug:slug>/", RedirectView.as_view(pattern_name="articles:detail")),
]
urlpatterns = [
    path("<slug:slug>/", views.ArticleDetail.as_view(), name="detail"),
    path("artiklar/", include(articles_patterns)),
]
