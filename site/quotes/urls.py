"""URLs for the 'quotes'-app"""
from django.urls import path

from quotes import views

app_name = "quotes"

urlpatterns = [
    path("nytt/", views.QuoteNew.as_view(), name="new_quote"),
    path("", views.QuoteList.as_view(), name="quotes"),
    path("<int:pk>/rediger/", views.QuoteUpdate.as_view(), name="QuoteUpdate"),
]
