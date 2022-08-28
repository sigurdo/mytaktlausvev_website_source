"""Admin settings for the 'quotes'-app"""

from django.contrib import admin

from .models import Quote


class QuoteAdmin(admin.ModelAdmin):
    list_display = ("quote", "quoted_as", "created")
    search_fields = ("quote", "quoted_as")


admin.site.register(Quote, QuoteAdmin)
