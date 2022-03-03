from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView

from common.mixins import BreadcrumbsMixin, PermissionOrCreatedMixin
from common.views import DeleteViewCustom

from .forms import FileForm
from .models import File


def breadcrumbs():
    """Returns breadcrumbs for the user_files views."""
    return [{"url": reverse("user_files:FileList"), "name": "Brukarfiler"}]


class FileList(LoginRequiredMixin, ListView):
    model = File
    context_object_name = "user_files"


class FileCreate(LoginRequiredMixin, BreadcrumbsMixin, CreateView):
    model = File
    form_class = FileForm
    template_name = "common/form.html"

    # The `get_absolute_url` default doesn't work well
    # when the URL is the file itself
    success_url = reverse_lazy("user_files:FileList")

    def get_breadcrumbs(self):
        return breadcrumbs()

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        return super().form_valid(form)


class FileDelete(PermissionOrCreatedMixin, DeleteViewCustom):
    model = File
    permission_required = "user_files.delete_file"

    def get_success_url(self):
        return reverse("user_files:FileList")
