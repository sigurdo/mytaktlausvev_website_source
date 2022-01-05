from django.contrib.admin import site, ModelAdmin, TabularInline, SimpleListFilter
from .models import NavbarItem, NavbarItemPermissionRequirement


class SubitemInline(TabularInline):
    model = NavbarItem
    verbose_name = "Underpunkt"
    verbose_name_plural = "Underpunkt"
    show_change_link = True
    extra = 3


class PermissionInline(TabularInline):
    model = NavbarItemPermissionRequirement
    verbose_name = "Løyvekrav"
    verbose_name_plural = "Løyvekrav"
    extra = 3


class NavbarItemListFilter(SimpleListFilter):
    """Makes the NavbarItemAdmin only display items that have no parent item by default."""
    title = "underpunkt"
    parameter_name = "underpunkt"

    def lookups(self, request, model_admin):
        return [
            ["vis", "Vis underpunkt"],
        ]
    
    def choices(self, request):
        """
        Discards the first element of super().choices, because that element is an automatically
        added "all" default value, but our default is not to show all.
        """
        choices = super().choices(request)
        for i, choice in enumerate(choices):
            if i == 0:
                continue
            yield choice
    
    def queryset(self, request, queryset):
        match self.value():
            case "vis":
                return queryset
            case _:
                return queryset.filter(parent=None)


class NavbarItemAdmin(ModelAdmin):
    list_display = ("text", "link", "order", "type", "parent")
    list_filter = [NavbarItemListFilter]
    ordering = ["order", "text"]
    inlines = [SubitemInline, PermissionInline]
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Makes only the NavbarItems of type DROPDOWN selectable for parent."""
        if db_field.name == "parent":
            kwargs["queryset"] = NavbarItem.objects.filter(type=NavbarItem.Type.DROPDOWN)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


site.register(NavbarItem, NavbarItemAdmin)
