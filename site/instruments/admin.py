from django.contrib.admin import site

from .models import Instrument, InstrumentGroup, InstrumentLocation

site.register(InstrumentGroup)
site.register(InstrumentLocation)
site.register(Instrument)
