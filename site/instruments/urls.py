from django.urls import path

from .views import (
    InstrumentGroupLeaderList,
    InstrumentGroupLeadersUpdate,
    InstrumentList,
    InstrumentsUpdate,
)

app_name = "instruments"

urlpatterns = [
    path("", InstrumentList.as_view(), name="InstrumentList"),
    path("rediger/", InstrumentsUpdate.as_view(), name="InstrumentsUpdate"),
    path(
        "instrumentgruppeleiarar/",
        InstrumentGroupLeaderList.as_view(),
        name="InstrumentGroupLeaderList",
    ),
    path(
        "instrumentgruppeleiarar/rediger/",
        InstrumentGroupLeadersUpdate.as_view(),
        name="InstrumentGroupLeadersUpdate",
    ),
]
