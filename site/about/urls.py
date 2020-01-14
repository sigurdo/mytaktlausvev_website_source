from django.urls import path
from about import views

urlpatterns = [
    path("", views.about_us, name="about_us")
]