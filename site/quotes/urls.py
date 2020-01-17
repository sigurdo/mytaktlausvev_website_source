from django.urls import path
from quotes import views

urlpatterns = [
    path("nytt/", views.new_quote, name="new_quote"),
    path("", views.quotes, name="quotes")
]