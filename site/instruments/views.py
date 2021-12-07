from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, FormView
from django.urls import reverse

from .models import Instrument
from .forms import InstrumentUpdateFormset


class InstrumentList(LoginRequiredMixin, ListView):
    model = Instrument
    context_object_name = "instruments"


class InstrumentsUpdate(
    PermissionRequiredMixin,
    FormView,
):
    form_class = InstrumentUpdateFormset
    template_name = "common/form.html"
    permission_required = (
        "instruments.add_instrument",
        "instruments.change_instrument",
        "instruments.delete_instrument",
    )

    def get_success_url(self) -> str:
        return reverse("instruments:InstrumentList")

    def form_valid(self, form):
        # We must explicitly save the form because it is not done automatically by any ancestors
        form.save()
        return super().form_valid(form)
