from django.contrib.admin import ModelAdmin, site

from .models import Instrument, InstrumentGroup, InstrumentLocation, InstrumentType


class InstrumentAdmin(ModelAdmin):
    
    list_display = ('type', 'identifier', 'modified_by', 'modified')

    readonly_fields = ('created', 'created_by', 'modified', 'modified_by')

site.register(InstrumentGroup)
site.register(InstrumentType)
site.register(InstrumentLocation)
site.register(Instrument, InstrumentAdmin)
