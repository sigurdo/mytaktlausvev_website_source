from django.views.generic import FormView
from django.http import HttpResponse

from .forms import BrewForm


class BrewView(FormView):
    form_class = BrewForm
    template_name = "common/form.html"

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data["form_title"] = "Brygg ein drikk"
        return context_data

    def form_valid(self, form):
        response = HttpResponse(content="Eg er ei tekanne!")
        response.status_code = 418
        return response
