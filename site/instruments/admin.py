from django.contrib.admin import site

from .models import Instrument, InstrumentGroup, InstrumentLocation, InstrumentType

site.register(InstrumentGroup)
site.register(InstrumentType)
site.register(InstrumentLocation)
site.register(Instrument)
