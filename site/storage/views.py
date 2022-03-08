from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models.functions import Lower
from django.views.generic import TemplateView

from accounts.models import UserCustom


class StorageAccessView(PermissionRequiredMixin, TemplateView):
    template_name = "storage/storage.html"
    permission_required = "common.view_storage_access"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users_with_storage_access"] = UserCustom.objects.filter(
            membership_status__in=[
                UserCustom.MembershipStatus.PAYING,
                UserCustom.MembershipStatus.ASPIRANT,
            ]
        ).order_by(Lower("username"))
        return context
