from django.conf import settings
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from common.breadcrumbs import Breadcrumb, BreadcrumbsMixin
from common.templatetags.markdown import markdown

from .forms import UserCustomCreateForm, UserCustomUpdateForm
from .models import UserCustom


def breadcrumbs(user=None):
    """Returns breadcrumbs for the accounts views."""
    breadcrumbs = [Breadcrumb(reverse("accounts:MemberList"), "Alle medlemmar")]
    if user:
        breadcrumbs.append(Breadcrumb(user.get_absolute_url(), user))
    return breadcrumbs


class UserCustomCreate(PermissionRequiredMixin, BreadcrumbsMixin, CreateView):
    model = UserCustom
    form_class = UserCustomCreateForm
    template_name = "common/form.html"
    permission_required = "accounts.add_usercustom"

    def get_breadcrumbs(self) -> list:
        return breadcrumbs()

    def form_valid(self, form):
        response = super().form_valid(form)

        plain_text = render_to_string(
            "accounts/welcome_mail.md", {"username": self.object.username}
        )
        html = markdown(plain_text)
        send_mail(
            "Velkomen til Studentorchesteret Dei Taktlause!",
            plain_text,
            settings.EMAIL_HOST_USER,
            [self.object.email],
            html_message=html,
        )

        return response


class UserCustomUpdate(UserPassesTestMixin, BreadcrumbsMixin, UpdateView):
    model = UserCustom
    form_class = UserCustomUpdateForm
    template_name = "common/form.html"

    def get_breadcrumbs(self) -> list:
        return breadcrumbs(self.object)

    def test_func(self):
        user = self.request.user
        return self.get_object() == user or user.has_perm("accounts.change_usercustom")


class ProfileDetail(LoginRequiredMixin, BreadcrumbsMixin, DetailView):
    """View for user profiles."""

    model = UserCustom
    template_name = "accounts/profile_detail.html"
    context_object_name = "profile"

    def get_breadcrumbs(self) -> list:
        return breadcrumbs()


class MemberList(LoginRequiredMixin, ListView):

    model = UserCustom
    template_name = "accounts/member_list.html"
    context_object_name = "members"

    def get_context_data(self, **kwargs):
        kwargs["membership_status_enum"] = UserCustom.MembershipStatus
        return super().get_context_data(**kwargs)


class BirthdayList(LoginRequiredMixin, BreadcrumbsMixin, ListView):

    model = UserCustom
    template_name = "accounts/birthday_list.html"
    context_object_name = "users"

    def get_breadcrumbs(self) -> list:
        return breadcrumbs()

    def get_queryset(self):
        return UserCustom.objects.active().exclude(birthdate__isnull=True)
