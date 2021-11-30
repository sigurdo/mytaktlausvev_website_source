"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("brukarar/", include("accounts.urls")),
    path("sitat/", include("quotes.urls")),
    path("hendingar/", include("events.urls")),
    path("", include("dashboard.urls")),
    path("notar/", include("sheetmusic.urls")),
    path("kommentarar/", include("comments.urls")),
    path("kontakt/", include("contact.urls")),
    path("repertoar/", include("repertoire.urls")),
    path("skiltmerke/", include("buttons.urls")),
    path("julekalender/", include("advent_calendar.urls")),
    path(
        "buttons/", RedirectView.as_view(pattern_name="buttons:buttons", permanent=True)
    ),
    path("", include("easter_eggs.urls")),
    path("", include("articles.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
