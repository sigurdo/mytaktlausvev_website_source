from django.contrib.admin import site
from .models import InstrumentGroup, Instrument

site.register(InstrumentGroup)
site.register(Instrument)
