from django.conf import settings
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.core.mail import send_mail
from django.template import Context, Template
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic import CreateView, DetailView, FormView, ListView, UpdateView

from common.breadcrumbs import Breadcrumb, BreadcrumbsMixin
from common.templatetags.markdown import markdown
from embeddable_text.models import EmbeddableText

from .forms import ImageSharingConsentForm, UserCustomCreateForm, UserCustomUpdateForm
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

        embeddable_text, _ = EmbeddableText.objects.get_or_create(name="Velkomenepost")
        template = Template(embeddable_text.content).render(
            Context({"username": self.object.username})
        )
        html = markdown(template)
        send_mail(
            "Velkomen til Studentorchesteret Dei Taktlause!",
            embeddable_text.content,
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


class ImageSharingConsentList(PermissionRequiredMixin, BreadcrumbsMixin, ListView):

    model = UserCustom
    template_name = "accounts/image_sharing_consent_list.html"
    context_object_name = "users"
    permission_required = "accounts.view_image_sharing_consent"

    def get_breadcrumbs(self) -> list:
        return breadcrumbs()

    def get_queryset(self):
        return UserCustom.objects.active()


class ImageSharingConsentUpdate(LoginRequiredMixin, BreadcrumbsMixin, FormView):
    model = UserCustom
    form_class = ImageSharingConsentForm
    template_name = "common/form.html"
    http_method_names = ["post", "put"]

    def get_breadcrumbs(self) -> list:
        return breadcrumbs(self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        kwargs["form_title"] = "Samtykkje til deling av bilete"
        return super().get_context_data(**kwargs)

    def get_next_url(self):
        """Returns the next URL if it exists and is safe, else `None`."""
        next = self.request.GET.get(self.redirect_field_name, "")
        url_is_safe = url_has_allowed_host_and_scheme(
            url=next,
            allowed_hosts=self.request.get_host(),
            require_https=self.request.is_secure(),
        )
        return next if next and url_is_safe else None

    def get_success_url(self) -> str:
        next = self.get_next_url()
        if next:
            return next
        return self.request.user.get_absolute_url()
