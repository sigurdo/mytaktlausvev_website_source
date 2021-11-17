import multiprocessing

import PIL

from django.views.generic import FormView
from django.http import HttpResponse, HttpResponseBadRequest

from .forms import ButtonsForm
from .button_pdf_generator import button_pdf_generator

class Buttons(FormView):
    form_class = ButtonsForm
    template_name = "buttons/buttons.html"
    
    def form_valid(self, form):
        images = self.request.FILES.getlist("images")
        if len(images) > 64:
            return HttpResponseBadRequest("Kan ikkje bruke fleire enn 64 ulike motiv samtidig")
        images = [PIL.Image.open(image) for image in images]
        num_of_each = form.cleaned_data["num_of_each"]
        button_diameter_mm = form.cleaned_data["button_diameter_mm"]
        pdf = multiprocessing.Pool().apply(
            button_pdf_generator,
            [images],
            {
                "num_of_each": num_of_each,
                "button_width_mm": button_diameter_mm,
                "button_height_mm": button_diameter_mm,
            },
        )
        return HttpResponse(
            content=pdf.getvalue(),
            content_type="application/pdf"
        )
