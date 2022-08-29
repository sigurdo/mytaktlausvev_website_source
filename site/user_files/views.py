from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from common.breadcrumbs.breadcrumbs import Breadcrumb, BreadcrumbsMixin
from common.forms.views import DeleteViewCustom
from common.mixins import PermissionOrCreatedMixin
from serve_media_files.views import ServeMediaFiles

from .forms import FileForm
from .models import File


def breadcrumbs():
    """Returns breadcrumbs for the user_files views."""
    return [Breadcrumb(reverse("user_files:FileList"), "Brukarfiler")]


class FileList(LoginRequiredMixin, ListView):
    model = File
    context_object_name = "user_files"


class FileServe(UserPassesTestMixin, ServeMediaFiles):
    def setup(self, request, *args, **kwargs):
        slug = kwargs["slug"]
        self.file = File.objects.only("file", "public").get(slug=slug)
        return super().setup(request, *args, **kwargs)

    def get_file_path(self):
        return self.file.file.name

    def test_func(self):
        if self.file.public:
            return True
        return self.request.user.is_authenticated


class FileCreate(LoginRequiredMixin, BreadcrumbsMixin, CreateView):
    model = File
    form_class = FileForm
    template_name = "common/forms/form.html"
    success_url = reverse_lazy("user_files:FileList")

    def get_breadcrumbs(self):
        return breadcrumbs()


class FileUpdate(PermissionOrCreatedMixin, BreadcrumbsMixin, UpdateView):
    model = File
    form_class = FileForm
    template_name = "common/forms/form.html"
    permission_required = "user_files.change_file"
    success_url = reverse_lazy("user_files:FileList")

    def get_breadcrumbs(self):
        return breadcrumbs()


class FileDelete(PermissionOrCreatedMixin, BreadcrumbsMixin, DeleteViewCustom):
    model = File
    permission_required = "user_files.delete_file"

    def get_breadcrumbs(self):
        return breadcrumbs()

    def get_success_url(self):
        return reverse("user_files:FileList")
