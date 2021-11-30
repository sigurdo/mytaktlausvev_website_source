from django.views.generic import FormView
from django.http import HttpResponse

from .forms import BrewForm


class BrewView(FormView):
    form_class = BrewForm
    template_name = "common/form.html"

    def form_valid(self, form):
        response = HttpResponse(content="Eg er ei tekanne!")
        response.status_code = 418
        return response
