from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, DetailView

from .forms import UserCustomCreateForm
from .models import UserCustom


class UserCustomCreate(PermissionRequiredMixin, CreateView):
    model = UserCustom
    form_class = UserCustomCreateForm
    template_name = "common/form.html"
    permission_required = "accounts.add_usercustom"


class ProfileDetail(LoginRequiredMixin, DetailView):
    """View for user profiles."""

    model = UserCustom
    template_name = "accounts/profile_detail.html"
    context_object_name = "profile"
