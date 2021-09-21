from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserCustom


class ProfileDetail(LoginRequiredMixin, DetailView):
    """View for user profiles."""

    model = UserCustom
    template_name = "accounts/profile_detail.html"
    context_object_name = "profile"
