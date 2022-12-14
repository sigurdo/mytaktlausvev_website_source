import os

import PIL
from django.http import FileResponse, HttpResponse
from django.template.loader import render_to_string
from django.views.generic import FormView, View

from buttons.button_pdf_generator import button_pdf_generator

from .forms import BrewForm


class BrewView(FormView):
    form_class = BrewForm
    template_name = "common/forms/form.html"

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data["form_title"] = "Brygg ein drikk"
        return context_data

    def form_valid(self, form):
        answer = form.cleaned_data["drink"]
        if answer == "coffee":
            response = HttpResponse(content="Eg er ei tekanne!")
            response.status_code = 418
        elif answer == "tea":
            content = render_to_string("easter_eggs/tea.html")
            return HttpResponse(content)
        else:
            response = HttpResponse(content="404 not found.")
        return response


class EasterEggButton(View):
    def get(self, request, *args, **kwargs):
        image_path = os.path.join(
            os.path.split(__file__)[0], "static", "easter_eggs", "easter_egg.png"
        )
        image = PIL.Image.open(image_path)
        pdf = button_pdf_generator([image], num_of_each=3)
        return FileResponse(
            pdf, content_type="application/pdf", filename="gratulerer.pdf"
        )
