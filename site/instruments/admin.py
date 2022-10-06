from django.contrib.admin import site
from django.contrib.admin import ModelAdmin

from .models import Instrument, InstrumentGroup, InstrumentLocation, InstrumentType

class InstrumentAdmin(ModelAdmin):
    list_display = ('type', 'identifier', 'last_modified')

    readonly_fields = ('last_modified',)

site.register(InstrumentGroup)
site.register(InstrumentType)
site.register(InstrumentLocation)
site.register(Instrument, InstrumentAdmin)
