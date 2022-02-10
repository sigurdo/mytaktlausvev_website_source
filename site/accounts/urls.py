from django.urls import path

from .views import MemberList, ProfileDetail, UserCustomCreate, UserCustomUpdate

app_name = "accounts"

urlpatterns = [
    path("", MemberList.as_view(), name="MemberList"),
    path("ny/", UserCustomCreate.as_view(), name="UserCustomCreate"),
    path("profil/<slug:slug>/", ProfileDetail.as_view(), name="ProfileDetail"),
    path(
        "profil/<slug:slug>/rediger/",
        UserCustomUpdate.as_view(),
        name="UserCustomUpdate",
    ),
]
