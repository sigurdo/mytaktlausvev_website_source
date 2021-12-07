from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import Instrument


class InstrumentList(LoginRequiredMixin, ListView):
    model = Instrument
    context_object_name = "instruments"
