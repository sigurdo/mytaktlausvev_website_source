from django.contrib.admin import ModelAdmin, TabularInline, site

from .models import (
    Instrument,
    InstrumentGroup,
    InstrumentLocation,
    InstrumentType,
    InstrumentTypeDetectionException,
    InstrumentTypeDetectionKeyword,
)


class InstrumentGroupAdmin(ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class InstrumentTypeDetectionKeywordInline(TabularInline):
    model = InstrumentTypeDetectionKeyword


class InstrumentTypeDetectionExceptionInline(TabularInline):
    model = InstrumentTypeDetectionException


class InstrumentTypeAdmin(ModelAdmin):
    list_display = ("name", "group")
    search_fields = ("name", "group__name")
    list_filter = ("group",)
    inlines = [
        InstrumentTypeDetectionKeywordInline,
        InstrumentTypeDetectionExceptionInline,
    ]


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
