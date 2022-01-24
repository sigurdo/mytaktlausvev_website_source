from django.urls import include, path
from django.contrib.auth import views as auth_views

from .views import ProfileDetail, MemberList, UserCustomCreate

app_name = "accounts"

urlpatterns = [
    path("ny/", UserCustomCreate.as_view(), name="UserCustomCreate"),
    path("profil/<slug:slug>/", ProfileDetail.as_view(), name="ProfileDetail"),
    path("", MemberList.as_view(), name="medlemmer"),

]
