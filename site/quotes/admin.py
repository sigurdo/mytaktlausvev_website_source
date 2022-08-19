"""Admin settings for the 'quotes'-app"""

from django.contrib import admin

from .models import Quote


class QuoteAdmin(admin.ModelAdmin):
    list_display = ("quote", "context", "created")
    search_fields = ("quote", "context")


admin.site.register(Quote, QuoteAdmin)
