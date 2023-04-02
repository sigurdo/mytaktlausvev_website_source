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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path("brukarar/", include("accounts.urls")),
    path("", include("authentication.urls")),
    path("sitat/", include("quotes.urls")),
    path("lagertilgjenge/", include("storage.urls")),
    path("hendingar/", include("events.urls")),
    path("", include("dashboard.urls")),
    path("notar/", include("sheetmusic.urls")),
    path("kommentarar/", include("common.comments.urls")),
    path("kontakt/", include("contact.urls")),
    path("repertoar/", include("repertoire.urls")),
    path("buttons/", include("buttons.urls")),
    path("julekalender/", include("advent_calendar.urls")),
    path("instrument/", include("instruments.urls")),
    path("uniformer/", include("uniforms.urls")),
    path("forum/", include("forum.urls")),
    path("avstemmingar/", include("polls.urls")),
    path("fotoarkiv/", include("pictures.urls")),
    path("referat/", include("minutes.urls")),
    path("brygging/", include("brewing.urls")),
    path("brukarfiler/", include("user_files.urls")),
    path("pdfar/", include("common.pdfs.urls")),
    path("bergedagbok/", include("salvage_diary.urls")),
    path("", include("search.urls")),
    path("", include("easter_eggs.urls")),
    path("", include("articles.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


def handler500(request, template_name="500.html"):
    """Have to override this simple view to get context for the 500-template."""
    return render(request, template_name)
