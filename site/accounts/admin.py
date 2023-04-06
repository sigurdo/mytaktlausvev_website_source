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
            {
                "fields": (
                    "membership_status",
                    "membership_period",
                    "instrument_type",
                    "can_wear_hats",
                    "is_active_override",
                )
            },
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
    list_display = (
        "username",
        "email",
        "name",
        "membership_status",
        "date_joined",
        "can_wear_hats",
    )
    list_filter = (
        "is_staff",
        "is_superuser",
        "groups",
        "membership_status",
        "is_active_override",
    )
    list_editable = ("membership_status", "can_wear_hats")
    search_fields = ("username", "name", "email")


admin.site.register(UserCustom, UserAdminCustom)
