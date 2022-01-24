from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import TemplateView

from accounts.models import UserCustom


class StorageAccessView(PermissionRequiredMixin, TemplateView):
    template_name = "storage/storage.html"
    permission_required = "common.storage_access"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users_with_storage_access"] = UserCustom.objects.filter(
            membership_status="ACTIVE"
        ).order_by("username")
        return context
