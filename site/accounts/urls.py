from django.urls import path

from .views import MemberList, ProfileDetail, UserCustomCreate

app_name = "accounts"

urlpatterns = [
    path("ny/", UserCustomCreate.as_view(), name="UserCustomCreate"),
    path("profil/<slug:slug>/", ProfileDetail.as_view(), name="ProfileDetail"),
    path("", MemberList.as_view(), name="MemberList"),
]
