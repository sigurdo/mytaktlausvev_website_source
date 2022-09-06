"""Views for quotes-app"""
import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView

from common.breadcrumbs.breadcrumbs import Breadcrumb, BreadcrumbsMixin
from common.forms.views import DeleteViewCustom
from common.mixins import PermissionOrCreatedMixin
from quotes.models import Quote

from .forms import QuoteForm


def breadcrumbs():
    """Returns breadcrumbs for the quotes views."""
    return [Breadcrumb(reverse("quotes:QuoteList"), "Sitat")]


class QuoteList(LoginRequiredMixin, ListView):
    model = Quote
    context_object_name = "quotes"
    paginate_by = 50

    def get_context_data(self, **kwargs):
        random_number = random.randint(50, 150)
        random_number2 = random.randint(1, random_number)
        random_number3 = random.randint(1, random_number)
        if random_number2 == random_number3:
            kwargs["title"] = "Skammens hjørne"
        else:
            kwargs["title"] = "Sitat"
        return super().get_context_data(**kwargs)


class QuoteCreate(LoginRequiredMixin, BreadcrumbsMixin, CreateView):
    model = Quote
    form_class = QuoteForm
    template_name = "common/forms/form.html"

    def get_breadcrumbs(self) -> list:
        return breadcrumbs()

    def get_success_url(self) -> str:
        return reverse("quotes:QuoteList")


class QuoteUpdate(PermissionOrCreatedMixin, BreadcrumbsMixin, UpdateView):
    model = Quote
    form_class = QuoteForm
    template_name = "common/forms/form.html"
    permission_required = "quotes.change_quote"

    def get_breadcrumbs(self) -> list:
        return breadcrumbs()

    def get_success_url(self) -> str:
        return reverse("quotes:QuoteList")


class QuoteDelete(PermissionOrCreatedMixin, BreadcrumbsMixin, DeleteViewCustom):
    model = Quote
    permission_required = "quotes.delete_quote"

    def get_breadcrumbs(self) -> list:
        return breadcrumbs()

    def get_success_url(self) -> str:
        return reverse("quotes:QuoteList")
