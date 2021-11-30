from django.urls import path

from .views import (
    RepertoireList,
    RepertoireCreate,
    RepertoireUpdate,
    RepertoireDelete,
    RepertoirePdf,
)

app_name = "repertoire"

urlpatterns = [
    path("", RepertoireList.as_view(), name="RepertoireList"),
    path("nytt/", RepertoireCreate.as_view(), name="RepertoireCreate"),
    path("<slug:slug>/endre/", RepertoireUpdate.as_view(), name="RepertoireUpdate"),
    path("<slug:slug>/slett/", RepertoireDelete.as_view(), name="RepertoireDelete"),
    path("<slug:slug>/pdf/", RepertoirePdf.as_view(), name="RepertoirePdf"),
]
