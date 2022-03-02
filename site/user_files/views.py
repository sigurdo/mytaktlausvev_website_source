from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import File


class FileList(LoginRequiredMixin, ListView):
    model = File
    context_object_name = "user_files"
