from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserCustom

admin.site.register(UserCustom, UserAdmin)
