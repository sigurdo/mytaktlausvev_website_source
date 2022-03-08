import os

import PIL
from django.http import FileResponse, HttpResponse
from django.views.generic import FormView, View

from buttons.button_pdf_generator import button_pdf_generator

from .forms import BrewForm


class BrewView(FormView):
    form_class = BrewForm
    template_name = "common/form.html"

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data["form_title"] = "Brygg ein drikk"
        return context_data
    
    def form_valid(self, form):
        answer = form.cleaned_data["drink"]
        if (answer=="coffee"):
            response = HttpResponse(content="Eg er ei tekanne!")
        if (answer=="tea"):
            with open(os.path.join("site", "easter_eggs", "templates", "easter_eggs", "tea.html")) as file:
                content=file.read()
                print(content)
            response = HttpResponse(content)
        else:
            response = HttpResponse(content="404 not found.")
        response.status_code = 418
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
