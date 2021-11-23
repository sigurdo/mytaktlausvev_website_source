from django.shortcuts import render
from django.views.generic import TemplateView
from accounts.models import UserCustom


class StorageAccessView(TemplateView):
    template_name = "storage/storage.html"

    def get_context_data(self, **kwargs):           
        context = super().get_context_data(**kwargs)
        context["users_with_storage_access"] = UserCustom.objects.filter(membership_status="ACTIVE")
        return context

