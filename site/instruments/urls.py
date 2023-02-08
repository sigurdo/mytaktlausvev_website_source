from django.urls import path

from .views import InstrumentList, InstrumentsUpdate

app_name = "instruments"

urlpatterns = [
    path("", InstrumentList.as_view(), name="InstrumentList"),
    path("rediger/", InstrumentsUpdate.as_view(), name="InstrumentsUpdate"),
]
