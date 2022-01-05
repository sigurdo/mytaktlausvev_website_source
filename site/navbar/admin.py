from django.contrib.admin import site, ModelAdmin, TabularInline
from django.db.models import Q
from .models import NavbarItem


class SubitemInline(TabularInline):
    model = NavbarItem
    verbose_name = "Underpunkt"
    verbose_name_plural = "Underpunkt"
    extra = 3


class NavbarItemAdmin(ModelAdmin):
    list_display = ("text", "link", "order", "type", "parent")
    ordering = ["order", "text"]
    inlines = [SubitemInline]

    def get_queryset(self, request):
        return NavbarItem.objects.filter(Q(type=NavbarItem.Type.DROPDOWN) | Q(parent=None))
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent":
            kwargs["queryset"] = NavbarItem.objects.filter(type=NavbarItem.Type.DROPDOWN)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


site.register(NavbarItem, NavbarItemAdmin)
