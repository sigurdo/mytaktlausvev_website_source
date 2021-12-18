from django.urls import path

from .views import JacketList, JacketsUpdate

app_name = "uniforms"

urlpatterns = [
    path("", JacketList.as_view(), name="JacketList"),
    path("rediger/", JacketsUpdate.as_view(), name="JacketsUpdate"),
]
