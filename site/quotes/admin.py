"""Admin settings for the 'quotes'-app"""

from django.contrib import admin
from .models import Quote

admin.site.register(Quote)
