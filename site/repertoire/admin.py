"""Admin settings for the 'repertoire'-app"""

from django.contrib.admin import site

from .models import Repertoire, RepertoireEntry

site.register(Repertoire)
site.register(RepertoireEntry)
