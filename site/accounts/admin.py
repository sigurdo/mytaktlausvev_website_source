from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import UserCustom


class UserAdminCustom(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personleg",
            {
                "fields": (
                    "name",
                    "email",
                    "birthdate",
                    "phone_number",
                    "address",
                    "home_page",
                    "student_card_number",
                    "has_storage_access",
                    "avatar",
                    "light_mode",
                    "orchestras",
                )
            },
        ),
        (
            "Taktlaus-ting",
            {"fields": ("membership_status", "membership_period", "instrument_type")},
        ),
        (
            "Kalenderintegrasjon",
            {"fields": ("calendar_feed_start_date",)},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ("username", "email", "name", "membership_status", "date_joined")
    list_filter = ("is_staff", "is_superuser", "groups", "membership_status")
    list_editable = ("membership_status",)
    search_fields = ("username", "name", "email")


admin.site.register(UserCustom, UserAdminCustom)
