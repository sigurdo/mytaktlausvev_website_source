from django.contrib.admin import ModelAdmin, display, site

from .models import Brew, Transaction


class BrewAdmin(ModelAdmin):
    list_display = (
        "name",
        "price_per_liter",
        "available_for_purchase",
        "OG",
        "FG",
        "alcohol_by_volume",
    )
    search_fields = ("name", "price_per_liter", "OG", "FG")
    list_filter = ("available_for_purchase",)
    readonly_fields = ("created", "created_by", "modified", "modified_by")

    @display(description="alkoholprosent")
    def alcohol_by_volume(self, obj):
        if not obj.alcohol_by_volume():
            return None
        return f"{obj.alcohol_by_volume():.1f} %"


class TransactionAdmin(ModelAdmin):
    list_display = (
        "created",
        "user",
        "type",
        "amount",
        "brew",
        "comment",
    )
    search_fields = ("user__name", "user__username", "amount", "comment", "brew__name")
    list_filter = ("type", "brew")
    readonly_fields = ("created", "created_by", "modified", "modified_by")


site.register(Brew, BrewAdmin)
site.register(Transaction, TransactionAdmin)
