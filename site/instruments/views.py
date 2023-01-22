from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.urls import reverse
from django.views.generic import FormView, ListView

from accounts.models import UserCustom
from common.breadcrumbs.breadcrumbs import Breadcrumb, BreadcrumbsMixin

from .forms import InstrumentFormset
from .models import Instrument


class InstrumentList(LoginRequiredMixin, ListView):
    model = Instrument
    context_object_name = "instruments"

    def get_queryset(self):
        return super().get_queryset().prefetch_related("type", "location", "user")


class InstrumentsUpdate(
    PermissionRequiredMixin,
    BreadcrumbsMixin,
    FormView,
):
    form_class = InstrumentFormset
    template_name = "common/forms/form.html"
    permission_required = (
        "instruments.add_instrument",
        "instruments.change_instrument",
        "instruments.delete_instrument",
    )

    def get_success_url(self) -> str:
        return reverse("instruments:InstrumentList")

    def get_breadcrumbs(self) -> list:
        return [Breadcrumb(reverse("instruments:InstrumentList"), "Instrumentoversikt")]

    def get_context_data(self, **kwargs):
        kwargs["form_title"] = "Rediger instrumentoversikt"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        # We must explicitly save the form because it is not done automatically by any ancestors
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class InstrumentGroupLeaderList(LoginRequiredMixin, ListView):
    model = UserCustom
    context_object_name = "instrument_group_leaders"
    template_name = "instruments/instrument_group_leader_list.html"

    def get_queryset(self):
        instrument_leaders_group, _ = Group.objects.get_or_create(
            name="instrumentgruppeleiar"
        )
        return instrument_leaders_group.user_set.all()
