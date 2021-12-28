from django.urls import path

from .views import (
    AddJacketUser,
    JacketList,
    JacketsUpdate,
    JacketUserMakeOwner,
    JacketUsers,
    RemoveJacketUser,
)

app_name = "uniforms"

urlpatterns = [
    path("", JacketList.as_view(), name="JacketList"),
    path("rediger/", JacketsUpdate.as_view(), name="JacketsUpdate"),
    path(
        "jakkebrukarar/<int:jacket_number>/", JacketUsers.as_view(), name="JacketUsers"
    ),
    path(
        "jakkebrukarar/<int:jacket_number>/ny/",
        AddJacketUser.as_view(),
        name="AddJacketUser",
    ),
    path(
        "jakkebrukarar/<int:jacket_number>/fjern/<slug:user_slug>/",
        RemoveJacketUser.as_view(),
        name="RemoveJacketUser",
    ),
    path(
        "jakkebrukarar/<int:jacket_number>/gjer_eigar/<slug:user_slug>/",
        JacketUserMakeOwner.as_view(),
        name="JacketUserMakeOwner",
    ),
]
