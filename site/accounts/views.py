from django.conf import settings
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.contrib.auth.models import Group
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.template import Context, Template
from django.urls import reverse, reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic import CreateView, DetailView, FormView, ListView, UpdateView

from common.breadcrumbs.breadcrumbs import Breadcrumb, BreadcrumbsMixin
from common.constants.models import Constant
from common.embeddable_text.models import EmbeddableText
from common.markdown.templatetags.markdown import markdown

from .forms import (
    ImageSharingConsentForm,
    InstrumentGroupLeadersForm,
    UserCustomCreateForm,
    UserCustomUpdateForm,
)
from .models import UserCustom


class MemberList(LoginRequiredMixin, BreadcrumbsMixin, ListView):
    model = UserCustom
    template_name = "accounts/member_list.html"
    context_object_name = "members"

    @classmethod
    def get_breadcrumb(cls, **kwargs) -> Breadcrumb:
        return Breadcrumb(
            url=reverse("accounts:MemberList"),
            label="Alle medlemmar",
        )

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related("groups")
            .select_related("instrument_type__group")
        )

    def get_context_data(self, **kwargs):
        kwargs["membership_status_enum"] = UserCustom.MembershipStatus
        return super().get_context_data(**kwargs)


class UserCustomCreate(PermissionRequiredMixin, BreadcrumbsMixin, CreateView):
    model = UserCustom
    form_class = UserCustomCreateForm
    template_name = "common/forms/form.html"
    permission_required = "accounts.add_usercustom"
    breadcrumb_parent = MemberList

    def form_valid(self, form):
        response = super().form_valid(form)

        embeddable_text, _ = EmbeddableText.objects.get_or_create(name="Velkomenepost")
        template = Template(embeddable_text.content).render(
            Context({"username": self.object.username})
        )
        html = markdown(template)
        send_mail(
            "Velkomen til (MYTAKTLAUSVEV_VARIABLE(appearance.orchestra_name))!",
            embeddable_text.content,
            settings.EMAIL_HOST_USER,
            [self.object.email],
            html_message=html,
        )

        return response


class ProfileDetail(LoginRequiredMixin, BreadcrumbsMixin, DetailView):
    """View for user profiles."""

    model = UserCustom
    template_name = "accounts/profile_detail.html"
    context_object_name = "profile"
    breadcrumb_parent = MemberList

    @classmethod
    def get_breadcrumb(cls, user, **kwargs) -> Breadcrumb:
        return Breadcrumb(
            url=user.get_absolute_url(),
            label=str(user),
        )


class UserCustomUpdate(UserPassesTestMixin, BreadcrumbsMixin, UpdateView):
    model = UserCustom
    form_class = UserCustomUpdateForm
    template_name = "common/forms/form.html"
    breadcrumb_parent = ProfileDetail

    def get_breadcrumbs_kwargs(self):
        return {"user": self.object}

    def test_func(self):
        user = self.request.user
        return self.get_object() == user or user.has_perm("accounts.change_usercustom")


class BirthdayList(LoginRequiredMixin, BreadcrumbsMixin, ListView):

    model = UserCustom
    template_name = "accounts/birthday_list.html"
    context_object_name = "users"
    breadcrumb_parent = MemberList

    def get_queryset(self):
        return UserCustom.objects.active().exclude(birthdate__isnull=True)


class ImageSharingConsentList(PermissionRequiredMixin, BreadcrumbsMixin, ListView):

    model = UserCustom
    template_name = "accounts/image_sharing_consent_list.html"
    context_object_name = "users"
    permission_required = "accounts.view_image_sharing_consent"
    breadcrumb_parent = MemberList

    def get_queryset(self):
        return UserCustom.objects.active()


class ImageSharingConsentUpdate(LoginRequiredMixin, BreadcrumbsMixin, FormView):
    model = UserCustom
    form_class = ImageSharingConsentForm
    template_name = "common/forms/form.html"
    http_method_names = ["post", "put"]
    breadcrumb_parent = MemberList

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


class InstrumentGroupLeaderList(LoginRequiredMixin, BreadcrumbsMixin, ListView):
    model = UserCustom
    context_object_name = "instrument_group_leaders"
    template_name = "accounts/instrument_group_leader_list.html"
    breadcrumb_parent = MemberList

    @classmethod
    def get_breadcrumb(cls, **kwargs) -> Breadcrumb:
        return Breadcrumb(
            url=reverse("accounts:InstrumentGroupLeaderList"),
            label="Instrumentgruppeleiarar",
        )

    def get_queryset(self):
        instrument_group_leader_group_name, _ = Constant.objects.get_or_create(
            name="Instrumentgruppeleiargruppenamn"
        )
        instrument_leaders_group, _ = Group.objects.get_or_create(
            name=instrument_group_leader_group_name.value
        )
        return instrument_leaders_group.user_set.all()


class InstrumentGroupLeadersUpdate(
    PermissionRequiredMixin, SuccessMessageMixin, BreadcrumbsMixin, FormView
):
    form_class = InstrumentGroupLeadersForm
    template_name = "common/forms/form.html"
    permission_required = ("accounts.edit_instrument_group_leaders",)
    success_message = "Instrumentgruppeleiarar redigert."
    success_url = reverse_lazy("accounts:InstrumentGroupLeaderList")
    breadcrumb_parent = InstrumentGroupLeaderList

    def get_context_data(self, **kwargs):
        kwargs["form_title"] = "Rediger instrumentgruppeleiarar"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
