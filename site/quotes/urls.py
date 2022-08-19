"""URLs for the 'quotes'-app"""
from django.urls import path

from quotes import views

app_name = "quotes"

urlpatterns = [
    path("", views.QuoteList.as_view(), name="QuoteList"),
    path("nytt/", views.QuoteNew.as_view(), name="QuoteNew"),
    path("<int:pk>/rediger/", views.QuoteUpdate.as_view(), name="QuoteUpdate"),
]
