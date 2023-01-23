from django.urls import path

from .views import BrewPurchaseCreate, BrewView, DepositCreate

app_name = "brewing"

urlpatterns = [
    path("", BrewView.as_view(), name="BrewView"),
    path("innbetaling/", DepositCreate.as_view(), name="DepositCreate"),
    path("<slug:slug>/", BrewPurchaseCreate.as_view(), name="BrewPurchaseCreate"),
]
