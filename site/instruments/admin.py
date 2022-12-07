from django.contrib.admin import ModelAdmin, site

from .models import Instrument, InstrumentGroup, InstrumentLocation, InstrumentType


class InstrumentGroupAdmin(ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class InstrumentTypeAdmin(ModelAdmin):
    list_display = ("name", "group")
    search_fields = ("name", "group__name")
    list_filter = ("group",)


class InstrumentLocationAdmin(ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class InstrumentAdmin(ModelAdmin):
    list_display = ("type", "identifier", "modified_by", "modified")
    search_fields = ("type__name", "identifier")
    list_filter = ("type__group",)
    readonly_fields = ("created", "created_by", "modified", "modified_by")


site.register(InstrumentGroup, InstrumentGroupAdmin)
site.register(InstrumentType, InstrumentTypeAdmin)
site.register(InstrumentLocation, InstrumentLocationAdmin)
site.register(Instrument, InstrumentAdmin)
