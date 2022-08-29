from django.contrib import admin

from django.contrib.admin import site
from external_orchestras.models import Orchestra


site.register(Orchestra)

