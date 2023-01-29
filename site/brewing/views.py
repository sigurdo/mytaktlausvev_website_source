from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Case, F, When
from django.db.models.aggregates import Sum
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView

from accounts.models import UserCustom
from common.breadcrumbs.breadcrumbs import Breadcrumb, BreadcrumbsMixin

from .forms import BrewPurchaseForm, DepositForm
from .models import Brew, Transaction, TransactionType


def breadcrumbs():
    """Returns breadcrumbs for the brewing views."""
    return [Breadcrumb(reverse("brewing:BrewView"), "Brygging")]


class BrewView(TemplateView):
    template_name = "brewing/brewing.html"

    def get_context_data(self, **kwargs):
        kwargs["brews"] = Brew.objects.all()
        kwargs["brew_sizes"] = Brew.Sizes
        return super().get_context_data(**kwargs)


class BalanceList(PermissionRequiredMixin, BreadcrumbsMixin, ListView):
    model = UserCustom
    template_name = "brewing/balance_list.html"
    context_object_name = "users"
    permission_required = "brewing.view_transaction"

    def get_breadcrumbs(self):
        return breadcrumbs()

    def sum_users_transactions_by_type(self, type):
        """Returns a `Sum` that sums a user's transactions by the `TransactionType` type."""
        price_if_matching_type = Case(
            When(
                brewing_transactions__type=type, then=F("brewing_transactions__price")
            ),
            default=0,
        )
        return Coalesce(Sum(price_if_matching_type), 0)

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .exclude(membership_status=UserCustom.MembershipStatus.INACTIVE)
            .annotate(
                balance=Coalesce(Sum("brewing_transactions__price"), 0),
                deposited=self.sum_users_transactions_by_type(TransactionType.DEPOSIT),
                purchased=self.sum_users_transactions_by_type(TransactionType.PURCHASE),
            )
        )


class DepositCreate(
    LoginRequiredMixin, SuccessMessageMixin, BreadcrumbsMixin, CreateView
):
    model = Transaction
    form_class = DepositForm
    template_name = "common/forms/form.html"
    success_url = reverse_lazy("brewing:BrewView")
    success_message = "Du har innbetalt %(price)s NOK til bryggjekassa."

    def get_breadcrumbs(self):
        return breadcrumbs()

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
    success_url = reverse_lazy("brewing:BrewView")

    brew = None

    def get_brew(self):
        return self.brew or get_object_or_404(Brew, pk=self.kwargs["slug"])

    def get_brew_size(self):
        return (
            Brew.Sizes.SIZE_0_5
            if self.request.GET.get("size") == Brew.Sizes.SIZE_0_5
            else Brew.Sizes.SIZE_0_33
        )

    def get_breadcrumbs(self):
        return breadcrumbs()

    def get_success_message(self, cleaned_data) -> str:
        return f"Du har kjøpt {self.get_brew_size().label} {self.get_brew()} for {abs(cleaned_data['price'])} NOK."

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
