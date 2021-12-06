"""
Django settings for web project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESSDATA_DIR = os.path.join(BASE_DIR, "..", "tessdata", "tessdata_best-4.1.0")

# Simplifies management stuff like deleting output files from the code editor on the host system.
os.umask(0)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ")c9b-kx9169s*!v1i^era6)ez3^k*io3c9#d+(*gf52-i0wh_0"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [".localhost", "127.0.0.1", "[::1]", "0.0.0.0"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "crispy_forms",
    "crispy_bootstrap5",
    "sass_processor",
    "authentication",
    "accounts",
    "common",
    "articles",
    "comments",
    "contact",
    "quotes",
    "events",
    "dashboard",
    "buttons",
    "sheetmusic",
    "repertoire",
    "advent_calendar",
    "easter_eggs",
    "pwa",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

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
                "common.context_processors.pwa_app_enabled",
            ],
        },
    },
]

WSGI_APPLICATION = "web.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "taktlaus_db",
        "USER": "taktlaus",
        "PASSWORD": "taktlaus",
        "HOST": "db",
        "PORT": 5432,
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

# Email
# https://docs.djangoproject.com/en/3.2/topics/email/

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "nn-no"

TIME_ZONE = "Europe/Oslo"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    "/static/",
]

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "sass_processor.finders.CssFinder",
]

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "login"

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
CRISPY_FAIL_SILENTLY = not DEBUG

MEDIA_ROOT = os.path.join(BASE_DIR, "media/")
MEDIA_URL = "/media/"


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

# Settings for django-pwa
PWA_APP_NAME = "Taktlausveven"
PWA_APP_DESCRIPTION = "Heimvevstaden til Studentorchesteret Dei Taktlause"
PWA_APP_THEME_COLOR = "#a50104"
PWA_APP_BACKGROUND_COLOR = "#ffffff"
PWA_APP_DISPLAY = "standalone"
PWA_APP_ORIENTATION = "portrait"
PWA_APP_ICONS = [
    {
        "src": "/static/images/logo.svg",
        "type": "image/svg",
    },
    {
        "src": "/static/images/logo_256x256.png",
        "type": "image/png",
        "sizes": "256x256",
    },
    {
        "src": "/static/images/apple-touch-icon.png",
        "type": "image/png",
        "sizes": "180x180",
    },
]
# PWA_APP_ICONS_APPLE is currently not supported by django-pwa even though it's mentioned
# in their README. So it does nothing as it is now, but I feel like we should leave
# it in case they suddenly decide to fix their package.
PWA_APP_ICONS_APPLE = [
    {
        "src": "/static/images/apple-touch-icon.png",
        "sizes": "180x180",
        "type": "image/png",
    },
]
PWA_APP_DIR = "pwa"
PWA_APP_LANG = "nn-no"
PWA_APP_START_URL = "/"
PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, "static", "js", "serviceworker.js")
PWA_APP_DEBUG_MODE = DEBUG
PWA_APP_ENABLED = not DEBUG
