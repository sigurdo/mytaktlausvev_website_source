"""URLs for the 'quotes'-app"""
from django.urls import path

from quotes import views

app_name = "quotes"

urlpatterns = [
    path("nytt/", views.new_quote, name="new_quote"),
    path("", views.quotes, name="quotes"),
]
