from django.contrib.admin import site
from .models import InstrumentGroup, InstrumentLocation, Instrument

site.register(InstrumentGroup)
site.register(InstrumentLocation)
site.register(Instrument)
