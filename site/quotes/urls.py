"""URLs for the 'quotes'-app"""
from django.urls import path

from quotes import views

app_name = "quotes"

urlpatterns = [
    path("", views.QuoteList.as_view(), name="QuoteList"),
    path("nytt/", views.QuoteCreate.as_view(), name="QuoteCreate"),
    path("<int:pk>/rediger/", views.QuoteUpdate.as_view(), name="QuoteUpdate"),
    path("<int:pk>/slett/", views.QuoteDelete.as_view(), name="QuoteDelete"),
]
