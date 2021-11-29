"""Admin settings for the 'repertoire'-app"""

from django.contrib import admin
from .models import Repertoire, RepertoireEntry

admin.site.register(Repertoire)
admin.site.register(RepertoireEntry)
