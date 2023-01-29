from django.contrib.admin import ModelAdmin, site

from .models import Brew, Transaction


class BrewAdmin(ModelAdmin):
    list_display = (
        "name",
        "price_per_litre",
        "available_for_purchase",
    )
    search_fields = (
        "name",
        "price_per_litre",
    )
    list_filter = ("available_for_purchase",)
    readonly_fields = ("created", "created_by", "modified", "modified_by")


class TransactionAdmin(ModelAdmin):
    list_display = (
        "created",
        "user",
        "type",
        "price",
        "comment",
    )
    search_fields = ("user__name", "comment", "price")
    list_filter = ("type",)
    readonly_fields = ("created", "created_by", "modified", "modified_by")


site.register(Brew, BrewAdmin)
site.register(Transaction, TransactionAdmin)
