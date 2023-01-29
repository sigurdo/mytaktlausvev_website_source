from django.urls import path

from .views import (
    BalanceList,
    BrewCreate,
    BrewList,
    BrewPurchaseCreate,
    BrewUpdate,
    BrewView,
    DepositCreate,
)

app_name = "brewing"

urlpatterns = [
    path("", BrewView.as_view(), name="BrewView"),
    path("brygg/", BrewList.as_view(), name="BrewList"),
    path("brygg/ny/", BrewCreate.as_view(), name="BrewCreate"),
    path("brygg/<slug:slug>/rediger/", BrewUpdate.as_view(), name="BrewUpdate"),
    path(
        "brygg/<slug:slug>/kjop/",
        BrewPurchaseCreate.as_view(),
        name="BrewPurchaseCreate",
    ),
    path("saldoar/", BalanceList.as_view(), name="BalanceList"),
    path("innbetaling/", DepositCreate.as_view(), name="DepositCreate"),
    # TODO: This URL should be a child of `brygg/`
]
