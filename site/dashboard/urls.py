"""URLs for the 'dashboard'-module"""
from django.urls import path
from dashboard import views

urlpatterns = [
    path("", views.dashboard, name="dashboard")
]
