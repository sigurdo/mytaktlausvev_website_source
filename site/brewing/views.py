from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Case, F, When
from django.db.models.aggregates import Sum
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from accounts.models import UserCustom
from common.breadcrumbs.breadcrumbs import Breadcrumb, BreadcrumbsMixin

from .forms import BrewForm, BrewPurchaseForm, DepositForm
from .models import Brew, Transaction, TransactionType


class BrewOverview(LoginRequiredMixin, BreadcrumbsMixin, ListView):
    model = Brew
    context_object_name = "available_brews"
    template_name = "brewing/brew_overview.html"

    def get_queryset(self):
        return super().get_queryset().filter(available_for_purchase=True)

    def get_context_data(self, **kwargs):
        kwargs["brew_sizes"] = Brew.Sizes
        return super().get_context_data(**kwargs)

    @classmethod
    def get_breadcrumb(cls, **kwargs):
        return Breadcrumb(
            url=reverse("brewing:BrewOverview"),
            label="Brygging",
        )


class BrewList(LoginRequiredMixin, BreadcrumbsMixin, ListView):
    model = Brew
    context_object_name = "brews"
    breadcrumb_parent = BrewOverview

    def get_queryset(self):
        return super().get_queryset().order_by("-available_for_purchase", "name")

    @classmethod
    def get_breadcrumb(cls, **kwargs):
        return Breadcrumb(
            url=reverse("brewing:BrewList"),
            label="Alle brygg",
        )


class BrewCreate(
    PermissionRequiredMixin, SuccessMessageMixin, BreadcrumbsMixin, CreateView
):
    model = Brew
    form_class = BrewForm
    template_name = "common/forms/form.html"
    success_url = reverse_lazy("brewing:BrewList")
    success_message = 'Brygget "%(name)s" vart laga.'
    permission_required = "brewing.add_brew"
    breadcrumb_parent = BrewList


class BrewUpdate(
    PermissionRequiredMixin, SuccessMessageMixin, BreadcrumbsMixin, UpdateView
):
    model = Brew
    form_class = BrewForm
    template_name = "common/forms/form.html"
    success_url = reverse_lazy("brewing:BrewList")
    success_message = 'Brygget "%(name)s" vart oppdatert.'
    permission_required = "brewing.change_brew"
    breadcrumb_parent = BrewList


class BalanceList(PermissionRequiredMixin, BreadcrumbsMixin, ListView):
    model = UserCustom
    template_name = "brewing/balance_list.html"
    context_object_name = "users"
    permission_required = "brewing.view_transaction"
    breadcrumb_parent = BrewOverview

    def get_context_data(self, **kwargs):
        kwargs["membership_status_enum"] = UserCustom.MembershipStatus
        return super().get_context_data(**kwargs)

    def amount_if_matching_type(self, type):
        """Returns a `Case` that chooses the transaction `amount` if the type equals `type`, else 0."""
        return Case(
            When(
                brewing_transactions__type=type, then=F("brewing_transactions__amount")
            ),
            default=0,
        )

    def get_queryset(self):
        amount_sign_depending_on_type = Case(
            When(
                brewing_transactions__type=TransactionType.DEPOSIT,
                then=F("brewing_transactions__amount"),
            ),
            default=-F("brewing_transactions__amount"),
        )

        return (
            super()
            .get_queryset()
            .annotate(
                balance=Coalesce(Sum(amount_sign_depending_on_type), 0),
                deposited=Coalesce(
                    Sum(self.amount_if_matching_type(TransactionType.DEPOSIT)), 0
                ),
                purchased=Coalesce(
                    Sum(self.amount_if_matching_type(TransactionType.PURCHASE)), 0
                ),
            )
        )


class DepositCreate(
    LoginRequiredMixin, SuccessMessageMixin, BreadcrumbsMixin, CreateView
):
    model = Transaction
    form_class = DepositForm
    template_name = "common/forms/form.html"
    success_url = reverse_lazy("brewing:BrewOverview")
    success_message = "Du har innbetalt %(amount)s NOK til bryggjekassa."
    breadcrumb_parent = BrewOverview

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        kwargs["form_title"] = "Legg inn pengar i bryggjekassa"
        return super().get_context_data(**kwargs)


class BrewPurchaseCreate(
    LoginRequiredMixin, SuccessMessageMixin, BreadcrumbsMixin, CreateView
):
    model = Transaction
    form_class = BrewPurchaseForm
    template_name = "brewing/brew_purchase.html"
    success_url = reverse_lazy("brewing:BrewOverview")
    breadcrumb_parent = BrewOverview

    brew = None

    def get_brew(self):
        if not self.brew:
            self.brew = get_object_or_404(Brew, slug=self.kwargs["slug"])
        if not self.brew.available_for_purchase:
            raise PermissionDenied()
        return self.brew

    def get_brew_size(self):
        return (
            Brew.Sizes.SIZE_0_5
            if self.request.GET.get("size") == Brew.Sizes.SIZE_0_5
            else Brew.Sizes.SIZE_0_33
        )

    def get_success_message(self, cleaned_data) -> str:
        return f"Du har kjøpt {self.get_brew_size().label} {self.get_brew()} for {cleaned_data['amount']} NOK."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        kwargs["brew"] = self.get_brew()
        kwargs["size"] = self.get_brew_size()
        return kwargs

    def get_context_data(self, **kwargs):
        kwargs["form_title"] = f"Kjøp {self.get_brew()}"
        kwargs["brew"] = self.get_brew()
        kwargs["brew_size"] = self.get_brew_size().label
        return super().get_context_data(**kwargs)
