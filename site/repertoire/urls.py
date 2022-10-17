from django.urls import path

from .views import (
    ActiveRepertoires,
    OldRepertoires,
    RepertoireCreate,
    RepertoireDelete,
    RepertoireDetail,
    RepertoirePdf,
    RepertoireUpdate,
)

app_name = "repertoire"

urlpatterns = [
    path("", ActiveRepertoires.as_view(), name="ActiveRepertoires"),
    path("dato/<str:date>/", ActiveRepertoires.as_view(), name="ActiveRepertoires"),
    path("gamle/", OldRepertoires.as_view(), name="OldRepertoires"),
    path("nytt/", RepertoireCreate.as_view(), name="RepertoireCreate"),
    path("<slug:slug>/", RepertoireDetail.as_view(), name="RepertoireDetail"),
    path("<slug:slug>/endre/", RepertoireUpdate.as_view(), name="RepertoireUpdate"),
    path("<slug:slug>/slett/", RepertoireDelete.as_view(), name="RepertoireDelete"),
    path("<slug:slug>/pdf/", RepertoirePdf.as_view(), name="RepertoirePdf"),
]
