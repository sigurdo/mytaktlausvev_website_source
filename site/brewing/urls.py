from django.urls import path

from .views import (
    BalanceList,
    BrewCreate,
    BrewList,
    BrewPurchaseCreate,
    BrewView,
    DepositCreate,
)

app_name = "brewing"

urlpatterns = [
    path("", BrewView.as_view(), name="BrewView"),
    path("brygg/", BrewList.as_view(), name="BrewList"),
    path("brygg/ny/", BrewCreate.as_view(), name="BrewCreate"),
    path("saldoar/", BalanceList.as_view(), name="BalanceList"),
    path("innbetaling/", DepositCreate.as_view(), name="DepositCreate"),
    path("<slug:slug>/", BrewPurchaseCreate.as_view(), name="BrewPurchaseCreate"),
]
