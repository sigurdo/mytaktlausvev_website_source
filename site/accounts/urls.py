from django.urls import path

from .views import (
    BirthdayList,
    ImageSharingConsentList,
    ImageSharingConsentUpdate,
    InstrumentGroupLeaderList,
    InstrumentGroupLeadersUpdate,
    MemberList,
    ProfileDetail,
    UserCustomCreate,
    UserCustomUpdate,
)

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
    path("bursdagar/", BirthdayList.as_view(), name="BirthdayList"),
    path(
        "biletedeling/",
        ImageSharingConsentList.as_view(),
        name="ImageSharingConsentList",
    ),
    path(
        "biletedeling/rediger/",
        ImageSharingConsentUpdate.as_view(),
        name="ImageSharingConsentUpdate",
    ),
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
