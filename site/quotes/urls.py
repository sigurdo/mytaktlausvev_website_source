from django.urls import path
from quotes import views

urlpatterns = [
    path("", views.all_quotes, name="all_quotes")
]