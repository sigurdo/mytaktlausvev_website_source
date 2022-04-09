from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models.functions import Lower
from django.urls import reverse
from django.views.generic import FormView, TemplateView

from accounts.models import UserCustom
from storage.forms import StorageAccessUpdateFormset


class StorageAccess(PermissionRequiredMixin, TemplateView):
    template_name = "storage/storage.html"
    permission_required = "accounts.view_storage_access"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_users"] = UserCustom.objects.active()
        return context


class StorageAccessUpdate(PermissionRequiredMixin, FormView):
    form_class = StorageAccessUpdateFormset
    template_name = "common/form.html"
    permission_required = (
        "accounts.view_storage_access",
        "accounts.edit_storage_access",
    )

    def get_success_url(self):
        return reverse("storage:StorageAccess")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["queryset"] = UserCustom.objects.active().order_by(
            "has_storage_access", Lower("username")
        )
        return kwargs

    def get_context_data(self, **kwargs):
        kwargs["form_title"] = "Rediger lagertilgjenge"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
