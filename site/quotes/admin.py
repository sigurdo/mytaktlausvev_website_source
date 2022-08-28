"""Admin settings for the 'quotes'-app"""

from django.contrib import admin

from .models import Quote


class QuoteAdmin(admin.ModelAdmin):
    list_display = ("quote", "quoted_as_or_users_view", "created")
    search_fields = ("quote", "quoted_as")

    @admin.display(description="Sitert som")
    def quoted_as_or_users_view(self, obj):
        return obj.quoted_as_or_users()


admin.site.register(Quote, QuoteAdmin)
