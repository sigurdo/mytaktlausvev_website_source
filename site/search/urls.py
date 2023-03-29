from django.urls import path
from django.views.generic import RedirectView

from .views import search_view

app_name = "search"

urlpatterns = [
    path("søk/", search_view, name="Search"),
    path(
        "search/",
        RedirectView.as_view(
            pattern_name="search:Search", query_string=True, permanent=True
        ),
    ),
]
