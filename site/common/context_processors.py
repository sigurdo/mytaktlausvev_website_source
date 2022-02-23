from django.conf import settings


def enable_pwa_manifest(request):
    return {
        "ENABLE_PWA_MANIFEST": settings.ENABLE_PWA_MANIFEST,
    }


def enable_serviceworker(request):
    return {
        "ENABLE_SERVICEWORKER": settings.ENABLE_SERVICEWORKER,
    }


def debug_flag(request):
    DEBUG = settings.DEBUG
    return {"DEBUG": DEBUG}
