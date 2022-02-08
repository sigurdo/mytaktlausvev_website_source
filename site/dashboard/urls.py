"""URLs for the 'dashboard'-module"""
from django.urls import path

from .views import Dashboard, DashboardRedirect

app_name = "dashboard"

urlpatterns = [
    path("", DashboardRedirect.as_view(), name="DashboardRedirect"),
    path("dashbord/", Dashboard.as_view(), name="Dashboard"),
]
