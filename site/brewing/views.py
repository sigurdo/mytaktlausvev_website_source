from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView

from brewing.forms import DepositForm
from brewing.models import Transaction
from common.breadcrumbs.breadcrumbs import Breadcrumb, BreadcrumbsMixin


class BrewView(TemplateView):
    template_name = "brewing/brewing.html"


class DepositCreate(LoginRequiredMixin, BreadcrumbsMixin, CreateView):
    model = Transaction
    form_class = DepositForm
    template_name = "common/forms/form.html"
    success_url = reverse_lazy("brewing:BrewView")

    def get_breadcrumbs(self):
        return [Breadcrumb(reverse("brewing:BrewView"), "Brygging")]

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        kwargs["form_title"] = "Legg inn pengar i bryggjekassa"
        return super().get_context_data(**kwargs)
