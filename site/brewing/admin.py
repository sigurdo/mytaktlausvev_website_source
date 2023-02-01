from django.contrib.admin import ModelAdmin, site

from .models import Brew, Transaction


class BrewAdmin(ModelAdmin):
    list_display = (
        "name",
        "price_per_liter",
        "available_for_purchase",
    )
    search_fields = (
        "name",
        "price_per_liter",
    )
    list_filter = ("available_for_purchase",)
    readonly_fields = ("created", "created_by", "modified", "modified_by")


class TransactionAdmin(ModelAdmin):
    list_display = (
        "created",
        "user",
        "type",
        "price",
        "brew",
        "comment",
    )
    search_fields = ("user__name", "price", "comment", "brew__name")
    list_filter = ("type",)
    readonly_fields = ("created", "created_by", "modified", "modified_by")


site.register(Brew, BrewAdmin)
site.register(Transaction, TransactionAdmin)
