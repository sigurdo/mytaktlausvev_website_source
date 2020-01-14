from django.urls import path
from about import views

urlpatterns = [
    path("", views.home, name="home")
]