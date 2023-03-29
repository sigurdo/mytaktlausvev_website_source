from django.contrib.admin import ModelAdmin, site

from .models import Constant


class ConstantAdmin(ModelAdmin):
    list_display = ("name", "value")
    search_fields = ("name", "value")


site.register(Constant, ConstantAdmin)
