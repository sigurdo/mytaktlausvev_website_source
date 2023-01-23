from django.contrib.admin import ModelAdmin, site

from .models import Transaction

site.register(Transaction, ModelAdmin)
