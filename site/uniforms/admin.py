from django.contrib.admin import ModelAdmin, site

from .models import Jacket, JacketLocation

class JacketAdmin(ModelAdmin):

    list_display = ("number", "user", "modified_by", "modified")

    readonly_fields = ("created", "created_by", "modified", "modified_by")

site.register(Jacket, JacketAdmin)
site.register(JacketLocation)
