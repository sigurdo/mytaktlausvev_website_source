from django.urls import path

from .views import InstrumentList

app_name = "instruments"

urlpatterns = [
    path("", InstrumentList.as_view(), name="InstrumentList"),
]
