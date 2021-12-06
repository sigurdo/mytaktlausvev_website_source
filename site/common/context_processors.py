from django.conf import settings


def pwa_app_enabled(request):
    return {"PWA_APP_ENABLED": settings.PWA_APP_ENABLED}
