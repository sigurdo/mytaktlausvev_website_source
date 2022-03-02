from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .forms import FileForm
from .models import File


class FileList(LoginRequiredMixin, ListView):
    model = File
    context_object_name = "user_files"


class FileCreate(LoginRequiredMixin, CreateView):
    model = File
    form_class = FileForm
    template_name = "common/form.html"

    # The `get_absolute_url` default doesn't work well
    # when the URL is the file itself
    success_url = reverse_lazy("user_files:FileList")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        return super().form_valid(form)
