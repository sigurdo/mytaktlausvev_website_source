"""
Django settings for web project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import logging
import os
import sys

from django.contrib.messages import constants as messages

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESSDATA_DIR = os.path.join(BASE_DIR, "..", "tessdata", "tessdata_best-4.1.0")
INSTRUMENTS_YAML_PATH = os.path.abspath(
    os.path.join(
        BASE_DIR,
        "sheetmusic",
        "instruments.yaml",
    )
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    "SECRET_KEY", ")c9b-kx9169s*!v1i^era6)ez3^k*io3c9#d+(*gf52-i0wh_0"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.environ.get("DEBUG", "1"))
PRODUCTION = int(os.environ.get("PRODUCTION", "0"))

# ALLOWED_HOSTS should be a string of space-separated hosts
# e.g. ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "" if PRODUCTION else "*").split(" ")

# Simplifies management stuff like deleting output files from the code editor on the host system.
if DEBUG:
    os.umask(0)

# Debug toolbar should always display if debug is true.
# The default is to use `INTERNAL_IPS` to determine whether or not to display,
# which doesn't work with Docker.
# https://stackoverflow.com/a/50492036

DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda _: DEBUG}

DEBUG_TOOLBAR_PANELS = [
    "debug_toolbar.panels.history.HistoryPanel",
    "debug_toolbar.panels.versions.VersionsPanel",
    "debug_toolbar.panels.timer.TimerPanel",
    "debug_toolbar.panels.settings.SettingsPanel",
    "debug_toolbar.panels.headers.HeadersPanel",
    "debug_toolbar.panels.request.RequestPanel",
    "debug_toolbar.panels.sql.SQLPanel",
    "debug_toolbar.panels.staticfiles.StaticFilesPanel",
    "debug_toolbar.panels.templates.TemplatesPanel",
    "debug_toolbar.panels.cache.CachePanel",
    "debug_toolbar.panels.signals.SignalsPanel",
    "debug_toolbar.panels.logging.LoggingPanel",
    "debug_toolbar.panels.redirects.RedirectsPanel",
    "debug_toolbar.panels.profiling.ProfilingPanel",
    "template_profiler_panel.panels.template.TemplateProfilerPanel",
]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.sites",
    "django.contrib.redirects",
    "debug_toolbar",
    "template_profiler_panel",
    "crispy_forms",
    "crispy_bootstrap5",
    "sass_processor",
    "pgtrigger",
    "watson",
    "django_userforeignkey",
    "search",
    "authentication",
    "accounts",
    "common",
    "common.forms",
    "common.embeddable_text",
    "common.comments",
    "common.markdown",
    "common.breadcrumbs",
    "sidebar",
    "articles",
    "storage",
    "contact",
    "quotes",
    "events",
    "dashboard",
    "buttons",
    "sheetmusic",
    "repertoire",
    "instruments",
    "uniforms",
    "advent_calendar",
    "easter_eggs",
    "pwa",
    "forum",
    "polls",
    "navbar",
    "pictures",
    "minutes",
    "user_files",
    "external_orchestras",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "watson.middleware.SearchContextMiddleware",
    "django_userforeignkey.middleware.UserForeignKeyMiddleware",
    "common.middleware.RedirectFallbackMiddleware",
]


# CSRF_TRUSTED_ORIGINS should be a string of space-separated trusted origins
# e.g. CSRF_TRUSTED_ORIGINS=https://*.example.com
CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS", "http://localhost").split(
    " "
)

X_FRAME_OPTIONS = "SAMEORIGIN"

ROOT_URLCONF = "web.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            (os.path.join(BASE_DIR, "templates")),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "common.context_processors.enable_pwa_manifest",
                "common.context_processors.enable_serviceworker",
                "common.context_processors.debug_flag",
            ],
        },
    },
]

WSGI_APPLICATION = "web.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("DB_ENGINE", "django.db.backends.postgresql_psycopg2"),
        "NAME": os.environ.get("DB_NAME", "taktlaus_db"),
        "USER": os.environ.get("DB_USER", "taktlaus"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "taktlaus"),
        "HOST": os.environ.get("DB_HOST", "db"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}


AUTH_USER_MODEL = "accounts.UserCustom"

# Password hashers
# https://docs.djangoproject.com/en/3.0/ref/settings/#std:setting-PASSWORD_HASHERS

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "authentication.hashers.DrupalPasswordHasher",
]


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Sites framework
# https://docs.djangoproject.com/en/3.2/ref/contrib/sites/

SITE_ID = 1

# Messages framework
# https://docs.djangoproject.com/en/4.0/ref/contrib/messages/

MESSAGE_TAGS = {
    messages.DEBUG: "alert-secondary",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}

# Email
# https://docs.djangoproject.com/en/3.2/topics/email/

EMAIL_BACKEND = os.environ.get(
    "EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend"
)
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "mail@example.com")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "SoSecureSecure")
EMAIL_USE_TLS = int(os.environ.get("EMAIL_USE_TLS", "1"))

DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "mail@example.com")
SERVER_EMAIL = os.environ.get("SERVER_EMAIL", "mail@example.com")

# Logging
# https://docs.djangoproject.com/en/4.0/topics/logging/

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
}

# Disable excessive logging during tests
# https://stackoverflow.com/questions/5255657/how-can-i-disable-logging-while-running-unit-tests-in-python-django/7732916#7732916
if len(sys.argv) > 1 and sys.argv[1] == "test":
    logging.disable(logging.WARNING)

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "nn-no"

TIME_ZONE = "Europe/Oslo"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Search
# https://github.com/etianen/django-watson/wiki

WATSON_POSTGRES_SEARCH_CONFIG = "pg_catalog.norwegian"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "..", "staticfiles")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "sass_processor.finders.CssFinder",
]

MEDIA_URL = "/media/"
MEDIA_URL_NGINX = "/media_nginx/"
MEDIA_ROOT = (
    os.path.join(BASE_DIR, "media") if DEBUG else os.path.join(BASE_DIR, "..", "media")
)

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "login"

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
CRISPY_FAIL_SILENTLY = not DEBUG


# Sass config

# Default is 5, while 8 is required by bootsrap
SASS_PRECISION = 8

# Default for DEBUG is nested, while I think expanded is better
SASS_OUTPUT_STYLE = "expanded" if DEBUG else "compressed"

# Defines a root directory to output compiled scss files
SASS_PROCESSOR_ROOT = os.path.join(BASE_DIR, "compiled_scss")

# Directories that act as a base to include from
SASS_PROCESSOR_INCLUDE_DIRS = [
    os.path.join(BASE_DIR, "static/scss/"),
]

ENABLE_PWA_MANIFEST = True
ENABLE_SERVICEWORKER = not DEBUG

# Miscellangeous constants
BIRTHDAY_SONG_SLUG = "hurra-for-deg"
