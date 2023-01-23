from django.contrib.admin import ModelAdmin, site

from .models import Brew, Transaction

site.register(Brew, ModelAdmin)
site.register(Transaction, ModelAdmin)
