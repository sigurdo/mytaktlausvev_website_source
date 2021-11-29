"""Admin settings for the 'sheetmusic'-app"""

from django.contrib import admin
from .models import Score, Pdf, Part

admin.site.register(Score)
admin.site.register(Pdf)
admin.site.register(Part)
