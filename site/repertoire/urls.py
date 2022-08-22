from django.urls import path

from .views import (
    ActiveRepertoires,
    RepertoireCreate,
    RepertoireDelete,
    RepertoireDetail,
    RepertoireList,
    RepertoirePdf,
    RepertoireUpdate,
)

app_name = "repertoire"

urlpatterns = [
    path("", ActiveRepertoires.as_view(), name="ActiveRepertoires"),
    path("alle/", RepertoireList.as_view(), name="RepertoireList"),
    path("nytt/", RepertoireCreate.as_view(), name="RepertoireCreate"),
    path("<slug:slug>/", RepertoireDetail.as_view(), name="RepertoireDetail"),
    path("<slug:slug>/endre/", RepertoireUpdate.as_view(), name="RepertoireUpdate"),
    path("<slug:slug>/slett/", RepertoireDelete.as_view(), name="RepertoireDelete"),
    path("<slug:slug>/pdf/", RepertoirePdf.as_view(), name="RepertoirePdf"),
]
