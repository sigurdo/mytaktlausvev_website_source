from django.contrib.admin import site
from .models import InstrumentType, Instrument

site.register(InstrumentType)
site.register(Instrument)
