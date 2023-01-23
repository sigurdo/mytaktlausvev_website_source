from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView

from common.breadcrumbs.breadcrumbs import Breadcrumb, BreadcrumbsMixin

from .forms import BrewPurchaseForm, DepositForm
from .models import Brew, Transaction


class BrewView(TemplateView):
    template_name = "brewing/brewing.html"

    def get_context_data(self, **kwargs):
        kwargs["brews"] = Brew.objects.all()
        return super().get_context_data(**kwargs)


class DepositCreate(LoginRequiredMixin, BreadcrumbsMixin, CreateView):
    model = Transaction
    form_class = DepositForm
    template_name = "common/forms/form.html"
    success_url = reverse_lazy("brewing:BrewView")
    # TODO: Message saying that you've deposited?

    def get_breadcrumbs(self):
        return [Breadcrumb(reverse("brewing:BrewView"), "Brygging")]

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        kwargs["form_title"] = "Legg inn pengar i bryggjekassa"
        return super().get_context_data(**kwargs)


class BrewPurchaseCreate(LoginRequiredMixin, BreadcrumbsMixin, CreateView):
    model = Transaction
    form_class = BrewPurchaseForm
    template_name = "common/forms/form.html"
    success_url = reverse_lazy("brewing:BrewView")
    # TODO: Message saying that you've purchased?

    brew = None

    def get_brew(self):
        return self.brew or get_object_or_404(Brew, pk=self.kwargs["slug"])

    def get_breadcrumbs(self):
        return [Breadcrumb(reverse("brewing:BrewView"), "Brygging")]

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        kwargs["price"] = -self.get_brew().price_per_litre
        return kwargs

    def get_context_data(self, **kwargs):
        kwargs["form_title"] = f"Kjøp {self.get_brew()}"
        return super().get_context_data(**kwargs)
